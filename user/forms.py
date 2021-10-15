from django import forms



class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password",widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    username = forms.CharField(max_length=50,min_length=4,label="Username")
    password = forms.CharField(max_length=20,min_length=8,label="Password",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,min_length=8,label="Password Again",widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and (password != confirm):
            raise forms.ValidationError("Your passwords does not match")

        values = {
            "username" : username,
            "password" : password,
            "email"    : email,

        }
        return values