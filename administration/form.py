from accounts.models import Doctor
from doctors.models import Bill
from django import forms
from administration.models import DentalPost

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['qualification','specialization','contact', 'profile_img','available_days','facebook','twitter','instagram']
        widgets = {
            'qualification': forms.Select(attrs={'class': 'form-control', }),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teeth Whitening, Tooth Extraction'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '9800012321'}),
            'profile_img': forms.FileInput(attrs={'class':'form-control'}),
            'available_days': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class':'form-control','placeholder':'https://facebook.com/user_1'}),
            'twitter': forms.URLInput(attrs={'class':'form-control','placeholder':'https://x.com/user_1'}),
            'instagram': forms.URLInput(attrs={'class':'form-control','placeholder':'https://instagram.com/user_1'}),
        }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['appointment','amount','payment_status','invoice_num']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_status': forms.CheckboxInput(attrs={'class': 'form-check-input','checked':''}),
            'invoice_num': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class PostForm(forms.ModelForm):
    class Meta:
        model = DentalPost
        fields = ['title','slug','keywords','meta_description','content','feature_img']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'}),
            'keywords':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'meta_description':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'content':forms.Textarea(attrs={'class':'form-control','rows':5}),
            'feature_img': forms.FileInput(attrs={'class':'form-control'})
        }