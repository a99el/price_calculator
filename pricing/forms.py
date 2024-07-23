# في ملف pricing/forms.py
from django import forms
from .models import OfferDetail, Service, Offer

class OfferDetailForm(forms.ModelForm):
    offer = forms.ModelChoiceField(queryset=Offer.objects.all(), label='Offer')
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Service')
    class Meta:
        model = OfferDetail
        fields = ['offer', 'service','quantity', 'total_price']
        #['offer', 'service',]
        widgets = {
            'total_price': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        #def __init__(self, *args, **kwargs):
            #super(OfferDetailForm, self).__init__(*args, **kwargs)
            #self.fields['offer'].queryset = Offer.objects.all()
            #self.fields['offer'].label_from_instance = lambda obj: str(obj.id)
            #self.fields['service'].queryset = Service.objects.all()
            #self.fields['service'].label_from_instance = lambda obj: str(obj.id)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['client_name', 'client_address']
        widgets = {
            'date' : forms.HiddenInput(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='اسم المستخدم', max_length=100)
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)
