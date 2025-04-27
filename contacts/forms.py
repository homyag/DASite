from django import forms
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
from core.models import ContactRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone', 'company', 'budget', 'service', 'message']
        
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
                Column('message', css_class='mb-6'),
                css_class='mb-6'
            ),
            Div(
                Submit('submit', 'Отправить заявку',
                       css_class='w-full bg-indigo-600 text-white font-medium py-3 px-4 rounded-lg hover:bg-indigo-700 transition-all duration-300 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-75 disabled:cursor-not-allowed'),
                css_class='mb-6'
            )
        )

    def clean_phone(self):
        """Очищаем номер телефона от всех символов кроме цифр и плюса в начале."""
        phone = self.cleaned_data['phone']
        # Оставляем только цифры и плюс в начале
        digits = ''.join(c for c in phone if c.isdigit() or (c == '+' and phone.index(c) == 0))
        if not digits:
            raise forms.ValidationError('Введите корректный номер телефона')
        # Добавляем плюс в начало, если его нет
        if not digits.startswith('+'):
            digits = '+' + digits
        return digits