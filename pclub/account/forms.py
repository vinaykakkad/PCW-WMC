from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'fields form-control', 'autocomplete': 'off',
               'placeholder': 'Username'}
    ))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'fields form-control',
               'autocomplete': 'off', 'placeholder': 'Email'}
    ))
    fullname = forms.CharField(label='Full name', widget=forms.TextInput(
        attrs={'class': 'fields form-control', 'autocomplete': 'off',
               'placeholder': 'Fullname'}
    ))
    cf_username = forms.CharField(label='Codeforces id', required=False, 
        widget=forms.TextInput(attrs={'class': 'fields form-control',
        'autocomplete': 'off', 'placeholder': 'Codeforces id'}
    ))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'fields form-control', 'autocomplete': 'off',
               'placeholder': 'Password'}
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'fields form-control', 'autocomplete': 'off',
               'placeholder': 'Confirm Password'}
    ))

    class meta:
        fields = ['username', 'email', 'fullname',
                  'cf_username' 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'fields form-control', 'autocomplete': 'off',
               'placeholder': 'Username'}
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'fields form-control', 'autocomplete': 'off',
               'placeholder': 'Password'}
    ))

    class meta:
        fields = ['username', 'email']
