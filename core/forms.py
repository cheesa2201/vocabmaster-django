from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FileUpload, Word, LANGUAGE_CHOICES


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ExcelImportForm(forms.Form):
    # BUG FIX: Cập nhật accept + validate cho cả .docx
    file = forms.FileField(
        label="Chọn file Excel (.xlsx) hoặc Word (.docx)",
        widget=forms.FileInput(attrs={
            'accept': '.xlsx,.docx',
            'class': 'form-control',
        })
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.rsplit('.', 1)[-1].lower()
        if ext not in ['xlsx', 'docx']:
            raise forms.ValidationError("Chỉ chấp nhận file .xlsx hoặc .docx")
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File không được vượt quá 5MB.")
        return file


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['lang', 'word', 'reading', 'meaning', 'word_type', 'example']
        widgets = {
            'lang': forms.Select(attrs={'class': 'form-select'}),
            'word': forms.TextInput(attrs={'class': 'form-control'}),
            'reading': forms.TextInput(attrs={'class': 'form-control'}),
            'meaning': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'word_type': forms.TextInput(attrs={'class': 'form-control'}),
            'example': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class WordFilterForm(forms.Form):
    lang = forms.ChoiceField(
        choices=[('', 'Tất cả ngôn ngữ')] + list(LANGUAGE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    mastery = forms.ChoiceField(
        choices=[
            ('', 'Tất cả mức độ'),
            ('0', 'Chưa nhớ'),
            ('1', 'Đang học'),
            ('2', 'Thành thạo'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file', 'title']
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': '.pdf,.docx',
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.rsplit('.', 1)[-1].lower()
        if ext not in ['pdf', 'docx']:
            raise forms.ValidationError("Chỉ chấp nhận .pdf hoặc .docx")
        if file.size > 20 * 1024 * 1024:
            raise forms.ValidationError("File không được vượt quá 20MB.")
        return file