from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300', 'placeholder': 'Last Name'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text form-text-alter text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text form-text-alter text-muted small"><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text form-text-alter text-muted"><small>Enter the same password as before, for verification.</small></span>'



    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with this username already exists.')

        existing_user = User.objects.filter(email__iexact=email).first()
        if existing_user:
            if existing_user.is_active:
                self.add_error('email', 'A user with this email address already exists.')
            else:
                # Delete the inactive user with the same email address
                existing_user.delete()

        return cleaned_data
