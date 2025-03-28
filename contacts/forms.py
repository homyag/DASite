from django import forms
from django.core.validators import RegexValidator
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
from core.models import ContactRequest


class ContactForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Формат телефона: '+999999999'. До 15 цифр разрешено."
    )
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border-gray-300 border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Введите ваш email'}),
            'phone': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Введите ваш телефон'}),
            'service': forms.Select(attrs={
                'class': 'w-full border-gray-300 border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent'}),
            'message': forms.Textarea(attrs={
                'class': 'w-full border-gray-300 border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Расскажите о вашем проекте', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='mb-6'),
                css_class='mb-6'
            ),
            Row(
                Column('email', css_class='mb-6'),
                css_class='mb-6'
            ),
            Row(
                Column('phone', css_class='mb-6'),
                css_class='mb-6'
            ),
            Row(
                Column('service', css_class='mb-6'),
                css_class='mb-6'
            ),
            Row(
                Column('message', css_class='mb-6'),
                css_class='mb-6'
            ),
            Row(
                Column('captcha', css_class='mb-6'),
                css_class='mb-6'
            ),
            Div(
                Submit('submit', 'Отправить заявку',
                       css_class='w-full bg-indigo-600 text-white font-medium py-3 px-4 rounded-lg hover:bg-indigo-700 transition-colors duration-300'),
                css_class='mb-6'
            )
        )