from django import forms


class UploadFileForm(forms.Form):
    filename = forms.CharField(max_length=100, required=True)
    file_type = forms.CharField(max_length=15, required=True)
    file_size = forms.CharField(required=False)
    parent_id = forms.IntegerField(required=False)
    storaged_file = forms.FileField(required=False)
