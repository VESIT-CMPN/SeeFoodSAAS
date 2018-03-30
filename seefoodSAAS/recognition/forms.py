from django import forms


class ImageUploadForm(forms.Form):
    # Ideally you should use ImageField but for that you will
    # have to install plugins for pillow to support different formats
    image_file = forms.FileField(label='Upload image')
