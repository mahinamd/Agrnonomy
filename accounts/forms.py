from django import forms
from django.contrib.auth.forms import UsernameField
from .models import Account
from django.contrib.auth import password_validation, authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class AccountForm(forms.ModelForm):
    error_messages = {'password_mismatch': _('The two password fields didn’t match.'), }
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    fname = forms.CharField(max_length=32)
    lname = forms.CharField(max_length=32)
    mpass = forms.CharField(label=_("Password"), strip=False,
                            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
                            help_text=password_validation.password_validators_help_text_html(), )
    cpass = forms.CharField(label=_("Password confirmation"), strip=False,
                            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
                            help_text=_("Enter the same password as before, for verification."), )

    class Meta:
        model = Account
        fields = ('phone', 'fname', 'lname', 'email', 'mpass', 'cpass')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_cpass(self):
        mpass = self.cleaned_data.get("mpass")
        cpass = self.cleaned_data.get("cpass")
        if mpass and cpass and mpass != cpass:
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch', )
        return cpass

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(phone=phone)
        except Account.DoesNotExist:
            return phone
        raise forms.ValidationError('Phone number "%s" is already in use.' % account)

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('cpass')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('cpass', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["mpass"])
        if commit:
            user.save()
        return user


class AccountUpdateForm(forms.ModelForm):
    initial = {}

    class Meta:
        model = Account
        fields = ('pimg', 'fname', 'lname', 'gender', 'dob', 'house_no', 'address_line', 'city', 'zip_code', 'country', 'social_li', 'social_fb', 'social_tw')

    def set_initial(self, initial):
        self.initial = initial

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)

        fname = self.cleaned_data['fname']
        lname = self.cleaned_data['lname']
        gender = self.cleaned_data['gender']
        dob = self.cleaned_data['dob']
        mobile = self.cleaned_data['mobile']
        house_no = self.cleaned_data['house_no']
        address_line = self.cleaned_data['address_line']
        city = self.cleaned_data['city']
        zip_code = self.cleaned_data['zip_code']
        country = self.cleaned_data['country']
        social_li = self.cleaned_data['social_li']
        social_fb = self.cleaned_data['social_fb']
        social_tw = self.cleaned_data['social_tw']

        if fname and fname != '':
            account.fname = fname
        else:
            account.fname = self.initial['fname']

        if lname and lname != '':
            account.lname = lname
        else:
            account.lname = self.initial['lname']

        if gender and gender != '':
            account.gender = gender
        else:
            account.gender = self.initial['gender']

        if dob and dob != '':
            account.dob = dob
        else:
            account.dob = self.initial['dob']

        if house_no and house_no != '':
            account.house_no = house_no
        else:
            account.house_no = self.initial['house_no']

        if address_line and address_line != '':
            account.address_line = address_line
        else:
            account.address_line = self.initial['address_line']

        if city and city != '':
            account.city = city
        else:
            account.city = self.initial['city']

        if zip_code and zip_code != '':
            account.zip_code = zip_code
        else:
            account.zip_code = self.initial['zip_code']

        if country and country != '':
            account.country = country
        else:
            account.country = self.initial['country']

        if social_li and social_li != '':
            account.social_li = social_li
        else:
            account.social_li = self.initial['social_li']

        if social_fb and social_fb != '':
            account.social_fb = social_fb
        else:
            account.social_fb = self.initial['social_fb']

        if social_tw and social_tw != '':
            account.social_tw = social_tw
        else:
            account.social_tw = self.initial['social_tw']

        if commit:
            account.save()
        return account


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password', 'rme')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Credentials")
