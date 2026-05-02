from django  import  forms
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models  import User  

from django.core.exceptions import ValidationError

from .models import UserProfile , Education , Experience , Certificate , Projects , Language , EmployerProfile , Jobs  , JobCategory , Application , CustomUser

from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()



class UserRegisterjobSeeker(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isdigit():
            raise forms.ValidationError("Server: الاسم لا يمكن أن يحتوي على أرقام فقط.")
        return username 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("البريد الإلكتروني مستخدم مسبقًا!")
        return email

    def save(self, commit=True):
        """ تجاوز التحقق من تكرار اسم المستخدم """
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user




#  User Profile 
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'picture', 'data_of_brith', 'location', 'gender', 
            'nationality', 'state', 'governorate',  'phone_Number', 
            'minimum_salary', 'Number_of_years_of_experience',    #currency
            'description', 'the_biography',
        ]
        widgets = {
            'picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',  # فقط صور
            }),
            'jobTitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: مطور ويب',
            }),
            'data_of_brith': forms.DateInput(attrs={    'type': 'date'  }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: دمشق، سوريا',
            }),
            'phone_Number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: +963-912345678',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'اكتب وصفًا مختصرًا عنك...',
            }),
            'the_biography': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf',  # فقط PDF\
                'required':False,
            }),
        }
        widgets = {
            'job_description': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_the_biography(self):
        file = self.cleaned_data.get('the_biography', None)
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("يرجى رفع ملف PDF فقط.")
            if file.size > 5 * 1024 * 1024:  # تحديد حجم الملف بـ 5 ميجابايت كحد أقصى
                raise forms.ValidationError("حجم الملف يجب ألا يتجاوز 5 ميجابايت.")
        return file
    # جعل كل الحقول اختيارية
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


# Edit UserName Seeker 

class SeekerEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="البريد الإلكتروني")  # ✅ إضافة البريد الإلكتروني
    username = forms.CharField(required=True , label="اسم المستخدم ")
    class Meta:
        model = UserProfile
        fields = [
            'picture',
            'data_of_brith',
            'location',
            'gender',
            'nationality',
            'state',
            'governorate',
            'phone_Number',
            'minimum_salary',
            'Number_of_years_of_experience',
            'description'
        ]
        exclude = ['user', 'the_biography', 'slug']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',  # فقط صور
            }),
            
            'data_of_brith': forms.DateInput(attrs={'type': 'date' }),
            'location': forms.TextInput(attrs={
           
                'placeholder': 'مثال: دمشق، سوريا',
            }),
            'phone_Number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: +963-912345678',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'اكتب وصفًا مختصرًا عنك...',
            }),
            'the_biography': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf',  # فقط PDF\
                'required':False,
            }),
        }
        widgets = {
            'data_of_brith': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:  
            self.fields['username'].initial = self.instance.user.username  
            self.fields['email'].initial = self.instance.user.email  

    def save(self, commit=True):
        userProfile = super().save(commit=False)
        userProfile.user.username = self.cleaned_data['username'] 
        userProfile.user.email = self.cleaned_data['email']  

        if commit:
            userProfile.user.save()
            userProfile.save()
        return userProfile



class UserEducation(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
        # 'profile',
        'academic_degree',
        'institute_university',
        'Domain',
        'Appreciation',
        'Year_of_completion_or_graduation',
        ] 



class UserExperience(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['jobTitle', 'Company_Name', 'Company_location', 'From_history', 'To_date' , 'Description']  # تأكد من مطابقة الحقول
        widgets = {
            'from_history': forms.DateInput(attrs={'type': 'date'}),
            'To_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserCertificate(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = [
        # 'profile',
        'certificate_name',
        'Donor',    
        'Date',
        'Certificate_description',
        ] 
        

class UserProjects(forms.ModelForm):
    class Meta:
        model = Projects
        fields = [
        # 'profile',
        'project_Name_Link',
        'end_date',
        'project_description',
    ] 
        

class UserLanguage(forms.ModelForm):
    class Meta:
        model = Language
        fields = [
        # 'profile',
        'language_name',
        'language_lavel',
    ] 
        



class EmployerForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        label="البريد الإلكتروني", 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        label="كلمة المرور"
    )

    logo = forms.ImageField(
        required=False,
        label="شعار الشركة",
        widget=ClearableFileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'name_of_responsible_person', 'phone_number', 'state', 'governorate', 'logo']




class EmployerFormEdit(forms.ModelForm):
    email = forms.EmailField(required=True, label="البريد الإلكتروني")
    logo = forms.ImageField(
        required=False,
        label="شعار الشركة",
        widget=ClearableFileInput(attrs={'accept': 'image/*'})
    )
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'name_of_responsible_person', 'phone_number', 'state', 'governorate', 'logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['email'].initial = self.instance.user.email 

    def save(self, commit=True):
        employer = super().save(commit=False)
        employer.user.email = self.cleaned_data['email']
        if commit:
            employer.user.save()  
            employer.save() 
        return employer





#  job 
class CategeryJob(forms.ModelForm):
    class Meta:
        model =JobCategory
        fields = [
            'name'
        ] 

class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = [
            # 'employer',
            'title' , 
            'job_category',
            'job_description',
            'career_type',

            'education',
            'career_level',
            'gender',
            'years_of_experience_from',
            'years_of_experience_to',
            'salary',
            'email',
            'phone_number',
            'publication_date',
            'closing_date',
            'location',

        ]
        widgets = {
            'job_description': forms.Textarea(attrs={'rows': 5}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'closing_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'job_category': 'الفئة الوظيفية',
            'job_description': 'وصف الوظيفة',
            'career_type': 'نوع الوظيفة',
            'education': 'المستوى التعليمي',
            'career_level': 'المستوى الوظيفي',
            'gender': 'الجنس',
            'years_of_experience_from': 'سنوات الخبرة (من)',
            'years_of_experience_to': 'سنوات الخبرة (إلى)',
            'salary': 'الراتب',
            'email': 'البريد الإلكتروني',
            'phone_number': 'رقم الهاتف',
            'publication_date': 'تاريخ النشر',
            'closing_date': 'تاريخ الإغلاق',
            'location': 'الموقع',
        }

    # تنظيف الحقول (Validation)
    def clean_years_of_experience_to(self):
        years_from = self.cleaned_data.get('years_of_experience_from')
        years_to = self.cleaned_data.get('years_of_experience_to')
        if years_to < years_from:
            raise forms.ValidationError("سنوات الخبرة (إلى) يجب أن تكون أكبر من أو تساوي سنوات الخبرة (من).")
        return years_to








class ApplicationApply(forms.ModelForm):
    class Meta:
        model = Application
        fields = [ 
            'full_name',
            'email',
            'phone_number',
            # 'application_date',
            # 'status',
            # 'cv_link',
            'cover_letter',
            'notes',
        ]






class LoginForm(forms.Form):
    email = forms.EmailField(
        label="البريد الإلكتروني", 
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control input-custom',
            'placeholder': 'أدخل البريد الإلكتروني',
            'style': 'direction: rtl;',
            'id': 'email'
        })
    )
    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-custom',
            'placeholder': 'أدخل كلمة المرور',
            'id': 'password'
        })
    )

    class Meta:
        model  = User
        fields = ['email' , 'password']







class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="البريد الإلكتروني", required=True)
    old_password = forms.CharField(label="كلمة المرور الحالية", widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(label="كلمة المرور الجديدة", widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label="تأكيد كلمة المرور", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.add_error('email', "البريد الإلكتروني غير مسجل لدينا!")
            return

        if not user.check_password(old_password):
            self.add_error('old_password', "كلمة المرور الحالية غير صحيحة!")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "كلمتا المرور غير متطابقتين")












# job_category
# job_description
# career_type
# education
# career_level
# gender
# years_of_experience_from
# years_of_experience_to
# salary
# email
# phone_number
# publication_date
# closing_date
# location










# class UserRegistrationForm(forms.ModelForm):
#     confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password']

#     # التحقق من تطابق كلمة المرور
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password != confirm_password:
#             raise forms.ValidationError("كلمة المرور غير متطابقة")
        
#         return cleaned_data











        # def __init__(self , *args , **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['username'].validators = []
        
        # # def clean_username(self):
        # # # تجاوز التحقق الافتراضي للسماح بتكرار الاسم
        # #     return self.cleaned_data["username"]
        
        # def clean_email(self):
        #     email = self.cleaned_data["email"]
        #     if User.objects.filter(email=email).exists():
        #         raise forms.ValidationError("البريد الإلكتروني موجود مسبقًا.")
        #     return email
                
  
            


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

    def clean_username(self):
        return self.cleaned_data.get('username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_username(self):
        return self.cleaned_data.get('username')
