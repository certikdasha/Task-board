
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.widgets import ChoiceWidget

from taskbord.models import CustomUser, Cards


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CardCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['executor'].queryset = CustomUser.objects.filter(username=user)
        else:
            self.fields['executor'].queryset = CustomUser.objects.exclude(is_staff=True)

    class Meta:
        model = Cards
        fields = ['executor', 'text']


class UpdateCardForm(ModelForm):

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['executor'].queryset = CustomUser.objects.exclude(is_staff=True)

    class Meta:
        model = Cards
        fields = ['executor', 'text']




