from io import BytesIO
from tempfile import TemporaryDirectory
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create_user('autor', password='Test-only-5927!')
        cls.other = get_user_model().objects.create_user('otro', password='Test-only-5927!')
        cls.post = Post.objects.create(title='Primer artículo', content='Contenido de prueba', author=cls.author)

    def setUp(self):
        self.media = TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media.name)
        self.override.enable()
        self.addCleanup(self.media.cleanup)
        self.addCleanup(self.override.disable)

    def image(self):
        stream = BytesIO()
        Image.new('RGB', (20, 20), 'green').save(stream, 'PNG')
        return SimpleUploadedFile('foto.png', stream.getvalue(), content_type='image/png')

    def test_public_list_detail_without_image_and_escaping(self):
        self.assertContains(self.client.get('/'), self.post.title)
        self.assertContains(self.client.get(self.post.get_absolute_url()), self.post.content)
        self.post.content = '<script>alert(1)</script>'
        self.post.save()
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>')

    def test_anonymous_routes_require_login(self):
        routes = [reverse('post_create'), reverse('post_update', args=[self.post.pk]), reverse('post_delete', args=[self.post.pk]), reverse('profile')]
        for route in routes:
            for method in ('get', 'post'):
                with self.subTest(route=route, method=method):
                    self.assertRedirects(getattr(self.client, method)(route), reverse('login') + '?next=' + route)

    def test_other_user_cannot_edit_delete_or_forge_author(self):
        self.client.force_login(self.other)
        for name in ('post_update', 'post_delete'):
            route = reverse(name, args=[self.post.pk])
            self.assertEqual(self.client.get(route).status_code, 404)
            self.assertEqual(self.client.post(route, {'title': 'Ataque', 'content': 'No'}).status_code, 404)
        self.client.post(reverse('post_create'), {'title': 'Propio', 'content': 'Texto', 'author': self.author.pk})
        self.assertEqual(Post.objects.get(title='Propio').author, self.other)

    def test_full_crud_with_image_replacement_and_removal(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('post_create'), {'title': 'Foto', 'content': 'Mi texto', 'image': self.image()})
        post = Post.objects.get(title='Foto')
        self.assertRedirects(response, post.get_absolute_url())
        self.assertTrue(post.image.storage.exists(post.image.name))
        self.assertContains(self.client.get(post.get_absolute_url()), post.image.url)
        first_image = post.image.name
        self.client.post(reverse('post_update', args=[post.pk]), {'title': 'Editado', 'content': 'Otro texto', 'image': self.image()})
        post.refresh_from_db()
        self.assertEqual(post.title, 'Editado')
        self.assertNotEqual(post.image.name, first_image)
        self.client.post(reverse('post_update', args=[post.pk]), {'title': 'Sin foto', 'content': 'Texto', 'image-clear': 'on'})
        post.refresh_from_db()
        self.assertFalse(post.image)
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 200)
        route = reverse('post_delete', args=[post.pk])
        self.assertEqual(self.client.get(route).status_code, 200)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.assertRedirects(self.client.post(route), reverse('post_list'))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_invalid_image_and_required_fields(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('post_create'), {'title': 'No válida', 'content': 'Texto', 'image': SimpleUploadedFile('fake.png', b'not an image', content_type='image/png')})
        self.assertTrue(response.context['form'].errors.get('image'))
        response = self.client.post(reverse('post_create'), {'title': '', 'content': ''})
        self.assertIn('title', response.context['form'].errors)
        self.assertEqual(Post.objects.count(), 1)

    def test_image_limits(self):
        from .forms import PostForm
        upload = self.image()
        upload.size = 6 * 1024 * 1024
        form = PostForm({'title': 'Grande', 'content': 'Texto'}, {'image': upload})
        self.assertFalse(form.is_valid())
        self.assertIn('5 MB', str(form.errors))
        stream = BytesIO()
        Image.new('RGB', (10, 10)).save(stream, 'GIF')
        form = PostForm({'title': 'Gif', 'content': 'Texto'}, {'image': SimpleUploadedFile('a.gif', stream.getvalue())})
        self.assertFalse(form.is_valid())

    def test_register_login_logout_profile(self):
        credentials = {'username': 'nuevo', 'password1': 'Complex-test-7629!', 'password2': 'Complex-test-7629!'}
        self.assertRedirects(self.client.post(reverse('register'), credentials), '/')
        self.assertContains(self.client.get(reverse('profile')), 'nuevo')
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.assertRedirects(self.client.post(reverse('logout')), '/')
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(self.client.post(reverse('login'), {'username': 'nuevo', 'password': credentials['password1']}), '/')

    def test_weak_password_and_external_redirect_rejected(self):
        response = self.client.post(reverse('register'), {'username': 'weak', 'password1': '123', 'password2': '123'})
        self.assertTrue(response.context['form'].errors)
        response = self.client.post(reverse('login'), {'username': 'autor', 'password': 'Test-only-5927!', 'next': 'https://example.org'})
        self.assertRedirects(response, '/')

    def test_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.author)
        for route in (reverse('post_create'), reverse('post_update', args=[self.post.pk]), reverse('post_delete', args=[self.post.pk]), reverse('logout')):
            self.assertEqual(client.post(route, {'title': 'No', 'content': 'No'}).status_code, 403)

    def test_search_title_content_and_empty(self):
        for term in ('artículo', 'prueba'):
            self.assertContains(self.client.get('/', {'q': term}), self.post.title)
        self.assertContains(self.client.get('/', {'q': 'inexistente'}), 'No encontramos coincidencias')

    def test_missing_post(self):
        self.assertEqual(self.client.get(reverse('post_detail', args=[9999])).status_code, 404)
