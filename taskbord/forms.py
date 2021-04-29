from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from django.forms.widgets import ChoiceWidget

from taskbord.models import CustomUser, Cards


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CardCreateForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['executor'].queryset = Cards.objects.filter(executor= self.user)

    class Meta:
        model = Cards
        exclude = ('creator', 'status')



