from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import (
    CustomUser, UserProfile, Education, Experience, Language,
    Projects, Certificate, EmployerProfile, JobCategory,
    Jobs, Application, Notification
)
from django import forms


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


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm       
    add_form = CustomUserCreationForm 

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('معلومات إضافية', {'fields': ('email', 'user_type')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

    list_display = ('username', 'email', 'get_user_type')
    search_fields = ('email', 'username')
    ordering = ('email',)

    def get_user_type(self, obj):
        if obj.groups.filter(name="jobSeeker").exists():
            return "باحث عن عمل"
        elif obj.groups.filter(name="employer_company").exists():
            return "شركة / صاحب عمل"
        return "غير محدد"

    get_user_type.short_description = 'نوع المستخدم'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.user_type == 'jobSeeker':
            job_seeker_group, _ = Group.objects.get_or_create(name='jobSeeker')
            obj.groups.set([job_seeker_group])
        elif obj.user_type == 'employer_company':
            employer_group, _ = Group.objects.get_or_create(name='employer_company')
            obj.groups.set([employer_group])


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Language)
admin.site.register(Projects)
admin.site.register(Certificate)
admin.site.register(EmployerProfile)
admin.site.register(JobCategory)
admin.site.register(Jobs)
admin.site.register(Application)
admin.site.register(Notification)
