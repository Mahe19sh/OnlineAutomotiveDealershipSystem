from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import TestDrive, Car, Order


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("A user with that email already exists.", params={'value': value})


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        unique_together = [('email', 'username')]


class TestDriveForm(forms.ModelForm):

    class Meta:
        model = TestDrive
        fields = ['car', 'time']


class CompareForm(forms.Form):

    car1 = forms.ModelChoiceField(
        Car.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': "true"}
        )
    )
    car2 = forms.ModelChoiceField(
        Car.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': "true"}
        )
    )


class PostCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['picture', 'brand', 'name', 'car_make', 'price', 'fuel', 'dimensions', 'transmission', 'gears',
                  'seats', 'power', 'tank_capacity', 'engine_displacement', 'description', 'location', 'commision', 'added_by']


class TestDriveForm2(forms.ModelForm):
    class Meta:
        model = TestDrive
        fields = ['user', 'car', 'time', 'license', 'approved']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'car', 'amount', 'address', 'license', 'insurance', 'approved_by', 'is_delivered']
