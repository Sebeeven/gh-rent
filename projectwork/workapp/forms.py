from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from workapp.models import UserInfo


def username_word_validator(username):
    if len(username) > 14:
        raise forms.ValidationError("请输入14个字符以内的用户名!")

def password_validator(password):
    if len(password) < 6:
        raise forms.ValidationError("请输入6个字符以上的密码!")


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '邮箱'}), error_messages = {'required': u'邮箱不能为空!', 'invalid': u'请输入正确的邮箱!'})
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '用户名'}), error_messages = {'required': u'用户名不能为空!'}, validators=[username_word_validator])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '密码'}), error_messages = {'required': u'密码不能为空!'}, validators=[password_validator])

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email_data = self.cleaned_data.get('email')
        username_data = self.cleaned_data.get('username')
        if User.objects.filter(email=email_data).count() is not 0:
            msg = u'此邮箱已被注册过，请重新输入!'
            self._errors['email'] = self.error_class([msg])
            del cleaned_data['email']
        if User.objects.filter(username=username_data).count() is not 0:
            msg = u'此用户名已被注册过，请重新输入!'
            self._errors['username'] = self.error_class([msg])
            del cleaned_data['username']
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '邮箱'}), error_messages = {'required': u'邮箱不能为空!', 'invalid': u'请输入正确的邮箱!'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '密码'}), error_messages = {'required': u'密码不能为空!'})


class AlterUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '用户名'}), error_messages = {'required': u'用户名不能为空!'}, validators=[username_word_validator])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '密码'}), error_messages = {'required': u'密码不能为空!'}, validators=[password_validator])
    # avatar = forms.ImageField()

    class Meta:
        model = UserInfo
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super(AlterUserForm, self).clean()
        username_data = self.cleaned_data.get('username')
        if User.objects.filter(username=username_data).count() is not 0:
            msg = u'此用户名已被注册过，请重新输入!'
            self._errors['username'] = self.error_class([msg])
            del cleaned_data['username']
        return cleaned_data
