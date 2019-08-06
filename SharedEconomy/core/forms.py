from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from datetime import datetime
from django_countries.widgets import CountrySelectWidget

class UserRegisterForm(forms.ModelForm):
    # email = forms.EmailField()
    password= forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class TravellerForm(forms.ModelForm):

	day = forms.DateField(
		initial=datetime.today().strftime('%Y-%m-%d'), label='What is departure date?',widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))


	class Meta:
		model = Traveller
		fields = ['origin','destination','day']
		widgets = {'origin': CountrySelectWidget(), 'destination': CountrySelectWidget()}

class BuyerForm(forms.ModelForm):
	class Meta:
		model = Buyer
		fields = ['location']
		widgets = {'location': CountrySelectWidget()}