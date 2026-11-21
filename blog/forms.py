from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {'content': forms.Textarea(attrs={'rows': 12})}

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'content_type'):
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La imagen no debe superar los 5 MB.')
            if image.image.format not in ('JPEG', 'PNG', 'WEBP'):
                raise forms.ValidationError('Usá una imagen JPG, PNG o WEBP.')
        return image
