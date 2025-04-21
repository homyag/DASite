from django import forms
from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    """Форма для подписки на рассылку."""

    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'bg-gray-800 text-gray-200 rounded-l-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Ваш email',
                'aria-label': 'Адрес электронной почты для подписки'
            }),
        }
        error_messages = {
            'email': {
                'unique': "Вы уже подписаны на нашу рассылку.",
                'invalid': "Пожалуйста, введите корректный email адрес.",
                'required': "Email обязателен для заполнения."
            }
        }

    def clean_email(self):
        """Дополнительная валидация и нормализация email."""
        email = self.cleaned_data.get('email', '').strip().lower()

        # Проверка существующего подписчика
        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError("Вы уже подписаны на нашу рассылку.")

        return email