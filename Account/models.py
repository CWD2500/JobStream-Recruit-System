import os
import string
import datetime
import random
from django.conf import settings
from django.db import models
from django.dispatch   import receiver
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save  ,pre_save
from django.contrib.auth.models import Group



class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('jobSeeker', 'Job Seeker'),
        ('employer_company', 'Employer Company'),
    )

    username = models.CharField(max_length=150 , unique=False)   
    email = models.EmailField(unique=True)     
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'             
    REQUIRED_FIELDS = ['username']       

    def __str__(self):
        return self.email


def uploade_image(request , filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" %(nowTime, original_filename)
    return os.path.join('uploade/product/' , filename)

def uploade_logo(request , filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" %(nowTime, original_filename)
    return os.path.join('uploade/product/logo' , filename)



def uploade_file(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  
    filename = "%s_%s" % (nowTime, original_filename) 
    return os.path.join('uploads/cvs/', filename)  


def validate_file_size(value):
    limit = 5 * 1024 * 1024  
    if value.size > limit:
        raise ValidationError("حجم الملف يجب أن لا يتجاوز 5 ميجابايت.")
    

def validate_image_size(value):
    if value:  
        if value.size > 5 * 1024 * 1024:  
            raise ValidationError('حجم الصورة كبير جدًا. الحد الأقصى 5 ميغابايت.')


def randon_slug():
    return "".join(random.choice(string.ascii_letters + string.ascii_uppercase )for _ in range(20))



GENDER = [
    ('male', 'ذكر'),
    ('female', 'أنثى'),
    ('unspecified', 'غير محدد'),
]


NATIONALITY = (
    ('سوريا', 'سوريا'),
    ('لبنان', 'لبنان'),
    ('الأردن', 'الأردن'),
    ('فلسطين', 'فلسطين'),
    ('العراق', 'العراق'),
    ('السعودية', 'السعودية'),
    ('الإمارات', 'الإمارات'),
    ('قطر', 'قطر'),
    ('الكويت', 'الكويت'),
    ('البحرين', 'البحرين'),
    ('عمان', 'عمان'),
    ('اليمن', 'اليمن'),
    ('مصر', 'مصر'),
    ('ليبيا', 'ليبيا'),
    ('السودان', 'السودان'),
    ('تونس', 'تونس'),
    ('الجزائر', 'الجزائر'),
    ('المغرب', 'المغرب'),
    ('موريتانيا', 'موريتانيا'),
    ('تركيا', 'تركيا'),
    ('إيران', 'إيران'),
    ('أفغانستان', 'أفغانستان'),
    ('باكستان', 'باكستان'),
    ('الهند', 'الهند'),
    ('الصين', 'الصين'),
    ('اليابان', 'اليابان'),
    ('كوريا الجنوبية', 'كوريا الجنوبية'),
    ('ماليزيا', 'ماليزيا'),
    ('إندونيسيا', 'إندونيسيا'),
    ('تايلاند', 'تايلاند'),
    ('فيتنام', 'فيتنام'),
    ('الفلبين', 'الفلبين'),
    ('فرنسا', 'فرنسا'),
    ('ألمانيا', 'ألمانيا'),
    ('إيطاليا', 'إيطاليا'),
    ('إسبانيا', 'إسبانيا'),
    ('بريطانيا', 'بريطانيا'),
    ('السويد', 'السويد'),
    ('النرويج', 'النرويج'),
    ('الدنمارك', 'الدنمارك'),
    ('سويسرا', 'سويسرا'),
    ('اليونان', 'اليونان'),
    ('هولندا', 'هولندا'),
    ('بلجيكا', 'بلجيكا'),
    ('النمسا', 'النمسا'),
    ('البرتغال', 'البرتغال'),
    ('بولندا', 'بولندا'),
    ('التشيك', 'التشيك'),
    ('روسيا', 'روسيا'),
    ('الولايات المتحدة', 'الولايات المتحدة'),
    ('كندا', 'كندا'),
    ('المكسيك', 'المكسيك'),
    ('البرازيل', 'البرازيل'),
    ('الأرجنتين', 'الأرجنتين'),
    ('كولومبيا', 'كولومبيا'),
    ('تشيلي', 'تشيلي'),
    ('بيرو', 'بيرو'),
    ('فنزويلا', 'فنزويلا'),
    ('جنوب أفريقيا', 'جنوب أفريقيا'),
    ('نيجيريا', 'نيجيريا'),
    ('كينيا', 'كينيا'),
    ('إثيوبيا', 'إثيوبيا'),
    ('غانا', 'غانا'),
    ('السنغال', 'السنغال'),

    ('أستراليا', 'أستراليا'),
    ('نيوزيلندا', 'نيوزيلندا')
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name="المستخدم")
    picture = models.ImageField(upload_to=uploade_image, null=True, blank=True, verbose_name="الصورة الشخصية")
    data_of_brith = models.DateField(auto_now_add=False, blank=True, null=True, verbose_name="تاريخ الميلاد")
    location = models.CharField(max_length=50, blank=True, null=True, verbose_name="الموقع")
    gender = models.CharField(max_length=50, choices=GENDER, blank=True, null=True, verbose_name="الجنس")
    nationality = models.CharField(max_length=50, choices=NATIONALITY, blank=True, null=True, verbose_name="الجنسية")
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name="الولاية")
    governorate = models.CharField(max_length=50, blank=True, null=True, verbose_name="المحافظة")
    # city = models.CharField(max_length=50, blank=True, null=True, verbose_name="المدينة")
    phone_Number = models.CharField(max_length=50, blank=True, null=True, verbose_name="رقم الهاتف")
    minimum_salary = models.CharField(max_length=50, blank=True, null=True, verbose_name="الراتب الأدنى")
    Number_of_years_of_experience = models.IntegerField(blank=True, null=True, verbose_name="عدد سنوات الخبرة")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    the_biography = models.FileField(
        upload_to='uploads/cvs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf']), validate_file_size],
        max_length=200,
        blank=True, null=True,
        verbose_name="السيرة الذاتية"
    )
    slug = models.SlugField(blank=True, null=True, verbose_name="الرابط الفريد")


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(randon_slug() + '-' +str(self.user) )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("قائمة الملف الشخصي للباحث ")
        verbose_name_plural = ("قائمة الملف الشخصي للباحث")
    
    def __str__(self):
        return  str(self.user) 

    





#  Create User (ProFile)
# @receiver(post_save, sender=User)
# def save_profile(sender,instance, created, **kwargs):
#     print('instance',instance)
#     user = instance
#     if created:
#         if user.groups.filter(name ="jobSeeker").exists():
#             profile = UserProfile(user = user)
#             profile.save()
     
ACADEMIC_DEGREE = (
    ('لم أكمل التعليم', 'لم أكمل التعليم'),
    ('التعليم الأساسي', 'التعليم الأساسي'),
    ('الثانوية العامة أو ما يعادلها', 'الثانوية العامة أو ما يعادلها'),
    ('دبلوم سنتين', 'دبلوم سنتين'),
    ('دبلوم 3 سنوات', 'دبلوم 3 سنوات'),
    ('دبلوم 5 سنوات', 'دبلوم 5 سنوات'),
    ('دبلوم عالي', 'دبلوم عالي'),
    ('جامعي (بكالوريوس / ليسانس)', 'جامعي (بكالوريوس / ليسانس)'),
    ('ماجستير', 'ماجستير'),
    ('دكتوراه', 'دكتوراه'),
    ('دكتوراه ما بعد التخصص', 'دكتوراه ما بعد التخصص'),
    ('بروفيسور', 'بروفيسور'),
    ('شهادة مهنية', 'شهادة مهنية'),
    ('دورة تدريبية متخصصة', 'دورة تدريبية متخصصة'),
    # ('شهادات معتمدة (مثل PMP, CFA, CCNA)', 'شهادات معتمدة (مثل PMP, CFA, CCNA)'),
)



class Education(models.Model):  
    profile = models.ForeignKey(UserProfile, verbose_name="اسم الملف الشخصي", on_delete=models.CASCADE)
    academic_degree = models.CharField(max_length=50, verbose_name="الدرجة الأكاديمية", choices=ACADEMIC_DEGREE, blank=True, null=True)
    institute_university = models.CharField(max_length=50, verbose_name="المعهد / الجامعة", blank=True, null=True)
    Domain = models.CharField(max_length=50, verbose_name="التخصص", blank=True, null=True)
    Appreciation = models.CharField(max_length=50, verbose_name="التقدير", blank=True, null=True)
    Year_of_completion_or_graduation = models.DateField(auto_now_add=False, verbose_name="سنة التخرج أو الإكمال", blank=True, null=True)

    def __str__(self):
        return str(self.profile.user)

    class Meta:
        verbose_name = 'قائمة التعليم  '
        verbose_name_plural = 'قائمة  التعليم ' 


class Experience(models.Model):
    profile = models.ForeignKey(UserProfile, verbose_name="اسم الملف الشخصي", related_name='experiences', on_delete=models.CASCADE)
    jobTitle = models.CharField(max_length=70, verbose_name="المسمى الوظيفي", blank=True, null=True)
    Company_Name = models.CharField(max_length=70, verbose_name="اسم الشركة", blank=True, null=True)
    Company_location = models.CharField(max_length=70, verbose_name="موقع الشركة", blank=True, null=True)
    From_history = models.DateField(auto_now_add=False, verbose_name="تاريخ البداية", blank=True, null=True)
    To_date = models.DateField(auto_now_add=False, verbose_name="تاريخ النهاية", blank=True, null=True)
    Description = models.TextField(verbose_name="الوصف", blank=True, null=True)
   
    def __str__(self):
        return str(self.profile.user)
    class Meta:
        verbose_name = 'قائمة الخبرات '
        verbose_name_plural = 'قائمة  الخبرات' 



class Certificate(models.Model):
    profile = models.ForeignKey(UserProfile, verbose_name="اسم الملف الشخصي", on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=70, verbose_name="اسم الشهادة", blank=True, null=True)
    Donor = models.CharField(max_length=70, verbose_name="الجهة المانحة", blank=True, null=True)
    Date = models.DateField(auto_now_add=False, verbose_name="تاريخ المنح", blank=True, null=True)
    Certificate_description = models.TextField(verbose_name="وصف الشهادة", blank=True, null=True)

    def __str__(self):
        return str(self.profile.user)

    class Meta:
        verbose_name = 'قائمة الشهادات '
        verbose_name_plural = 'قائمة  الشهادات' 

class Projects(models.Model):
    profile = models.ForeignKey(UserProfile, verbose_name="اسم الملف الشخصي", on_delete=models.CASCADE)
    project_Name_Link = models.CharField(max_length=70, verbose_name="رابط أو اسم المشروع", blank=True, null=True)
    end_date = models.DateField(auto_now_add=False, verbose_name="تاريخ الانتهاء", blank=True, null=True)
    project_description = models.TextField(verbose_name="وصف المشروع", blank=True, null=True)

    def __str__(self):
        return str(self.profile.user)
    class Meta:
        verbose_name = 'قائمة المشاريع '
        verbose_name_plural = 'قائمة  المشاريع' 
LANGUAGE = (
   
    ('العربية', 'العربية'),
    ('الإنجليزية', 'الإنجليزية'),
    ('الفرنسية', 'الفرنسية'),
    ('التركية', 'التركية'),
    ('الإسبانية', 'الإسبانية'),
    ('الألمانية', 'الألمانية'),
    ('الإيطالية', 'الإيطالية'),
    ('البرتغالية', 'البرتغالية'),
    ('الروسية', 'الروسية'),
    ('الصينية', 'الصينية'),
    ('اليابانية', 'اليابانية'),
    ('الكورية', 'الكورية'),
    ('الهندية', 'الهندية'),
    ('الأوردو', 'الأوردو'),
    ('الفارسية', 'الفارسية'),
    ('العبرية', 'العبرية'),
    ('البنغالية', 'البنغالية'),
    ('التايلاندية', 'التايلاندية'),
    ('الهولندية', 'الهولندية'),
    ('اليونانية', 'اليونانية'),
    ('السويدية', 'السويدية'),
    ('الدنماركية', 'الدنماركية'),
    ('النرويجية', 'النرويجية'),
    ('الفنلندية', 'الفنلندية'),
    ('البولندية', 'البولندية'),
    ('التشيكية', 'التشيكية'),
    ('الرومانية', 'الرومانية'),
    ('المجرية', 'المجرية'),
    ('التاميلية', 'التاميلية'),
    ('التيلوجو', 'التيلوجو'),
    ('الماليزية', 'الماليزية'),
    ('الإندونيسية', 'الإندونيسية'),
    ('الفلبينية', 'الفلبينية'),
    ('الفيتنامية', 'الفيتنامية'),
    ('السواحلية', 'السواحلية'),
)


LANGUAGE_LAVEL = (
    ('لغة الأم', 'لغة الأم'),
    ('ضعيف', 'ضعيف'),
    ('مبتدئ', 'مبتدئ'),
    ('متوسط', 'متوسط'),
    ('جيد جداً', 'جيد جداً'),  
    ('ممتاز', 'ممتاز'),
    ('متقدم', 'متقدم'),
    ('خبير', 'خبير'),
  
)

class Language(models.Model):
    profile = models.ForeignKey(UserProfile, verbose_name="اسم الملف الشخصي", on_delete=models.CASCADE)
    language_name = models.CharField(max_length=50, verbose_name="اللغة", choices=LANGUAGE, blank=True, null=True)
    language_lavel = models.CharField(max_length=50, verbose_name="مستوى اللغة", choices=LANGUAGE_LAVEL, blank=True, null=True)

   
    def __str__(self):
        return str(self.profile.user)
    class Meta:
        verbose_name = 'قائمة اللغات '
        verbose_name_plural = 'قائمة  اللغات' 




# Employer / Company 
class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='userEmployer', verbose_name="اسم المستخدم", on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, verbose_name="اسم الشركة")
    name_of_responsible_person = models.CharField(max_length=50, verbose_name="اسم الشخص المسؤول")
    phone_number = models.CharField(max_length=50, verbose_name="رقم الهاتف")
    state = models.CharField(max_length=50, verbose_name="الولاية")
    governorate = models.CharField(max_length=50, verbose_name="المحافظة")
    logo = models.ImageField(upload_to=uploade_logo, null=True, blank=True, verbose_name="شعار الشركة")
    slug = models.SlugField(blank=True, null=True, verbose_name="الرابط الفريد")


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(randon_slug() +'-' +  self.company_name )
        super().save(*args, **kwargs)


    def __str__(self):
        return "employer : {}".format(str(self.user))

        
    class Meta:
        verbose_name = 'قائمة الملف الشخصي للشركة'
        verbose_name_plural = 'قائمة الملف الشخصي للشركة'


#  Create User (ProFile employer )
# @receiver(post_save, sender=User)
# def save_profile_employer(sender, instance, created, **kwargs):
#     if not isinstance(instance, User):
#         return

#     user = instance
#     if created:
#         if user.groups.filter(name="employer_company").exists():
#             profile, created = EmployerProfile.objects.get_or_create(user=user)
#             if created:
#                 profile.save()




# categories job 
class JobCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="اسم الفئة الوظيفية" ,  unique=True ,  error_messages ={'unique': "فئة وظيفية بهذا الاسم موجودة بالفعل."})
    icon_class = models.CharField(max_length=100, help_text="أدخل اسم أيقونة FontAwesome أو Bootstrap Icons", blank=True, null=True, verbose_name="اسم الأيقونة")
    slug = models.SlugField(blank=True, null=True, verbose_name="الرابط الفريد")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(randon_slug() + '-' + str(self.name))
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "فئات الوظيفية"
        verbose_name_plural = " فئات الوظيفية"

    def __str__(self):
        return "{}".format(self.name)

# add Jobs 

CAREER_TYPE_CHOICES = (
        ('full_time', 'دوام كامل'),
        ('part_time', 'دوام جزئي'),
        ('contract', 'عقد'),
        ('temporary', 'وظيفة مؤقتة'),
        ('freelance', 'عمل حر'),
        ('internship', 'تدريب'),
        ('remote', 'عمل عن بُعد'),
        ('on_site', 'عمل مكتبي'),
    )
EDUCATION_CHOICES = (
    ('high_school', 'الثانوية العامة أو ما يعدلها (High School)'),
    ('bachelor', 'جامعي (بكالوريوس / ليسانس) (Bachelor\'s Degree)'),
    ('master', 'ماجستير (Master\'s Degree)'),
    ('phd', 'دكتوراه (PhD)'),
    ('diploma_3_years', 'دبلوم 3 سنوات (3-Year Diploma)'),
    ('diploma_5_years', 'دبلوم 5 سنوات (5-Year Diploma)'),
    ('higher_diploma', 'دبلوم عالي (Higher Diploma)'),
    ('associate_degree', 'دبلوم مساعد (Associate Degree)'),
    ('postgraduate', 'دراسات ما بعد التخرج (Postgraduate Studies)'),
    ('professional_certificate', 'شهادة مهنية (Professional Certificate)'),
    ('vocational_training', 'تدريب مهني (Vocational Training)'),
    ('other', 'آخر (Other)'),
)

CAREER_LEVEL_CHOICES = (
    ('intern', 'متدرب'),
    ('entry', 'مبتدئ'),
    ('mid', 'متوسط الخبرة'),
    ('senior', 'متقدم الخبرة'),
    ('manager', 'مدير'),
    ('director', 'مدير تنفيذي'),
    ('vp', 'نائب الرئيس'),
    ('freelance', 'عمل حر'),
    ('consultant', 'مستشار'),
    ('executive', 'تنفيذي'),
    ('ceo', 'المدير التنفيذي (CEO)'),
    ('coo', 'المدير العملياتي (COO)'),
    ('cto', 'المدير التقني (CTO)'),
    ('founder', 'مؤسس'),
)


GENDER_CHOICES = (
        ('male', 'ذكر'),
        ('female', 'أنثى'),
        ('unspecified', 'غير محدد'),
    )

class Jobs(models.Model):
    # العلاقات
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs', verbose_name="صاحب العمل")
    job_category = models.ForeignKey('JobCategory', on_delete=models.CASCADE, verbose_name="الفئة الوظيفية")
    title = models.CharField(max_length=255, verbose_name="اسم الوظيفة")

    # الحقول الأساسية
    job_description = models.TextField(verbose_name="وصف الوظيفة")
    career_type = models.CharField(
        max_length=255,
        choices=CAREER_TYPE_CHOICES,
        verbose_name="نوع الوظيفة"
    )
    education = models.CharField(
        max_length=255,
        choices=EDUCATION_CHOICES,
        verbose_name="المستوى التعليمي"
    )
    career_level = models.CharField(
        max_length=255,
        choices=CAREER_LEVEL_CHOICES,
        verbose_name="المستوى الوظيفي"
    )
    gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        verbose_name="الجنس"
    )
    years_of_experience_from = models.IntegerField(verbose_name="سنوات الخبرة (من)")
    years_of_experience_to = models.IntegerField(verbose_name="سنوات الخبرة (إلى)")
    salary = models.CharField(max_length=255,  verbose_name="الراتب")
    email = models.EmailField( verbose_name="البريد الإلكتروني")
    phone_number = models.CharField(max_length=255, verbose_name="رقم الهاتف")
    publication_date = models.DateField(verbose_name="تاريخ النشر")
    closing_date = models.DateField(verbose_name="تاريخ الإغلاق")
    location = models.CharField(max_length=255, verbose_name="الموقع")

    slug = models.SlugField(blank=True, null=True, verbose_name="الرابط الفريد")



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(randon_slug() + '-' + str(self.job_category))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job_category} - {self.employer}"

    class Meta:
        verbose_name = "وظيفة"
        verbose_name_plural = "الوظائف"






STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]


class Application(models.Model):
    # العلاقة بالباحث عن العمل (Seeker) وعلاقته بالوظيفة (Job)
    seeker = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications', verbose_name="الباحث عن العمل")
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='applications', verbose_name="الوظيفة")
 
    full_name = models.CharField(max_length=100, verbose_name="اسم المتقدم")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone_number = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    application_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التقديم")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الطلب")
    cv_link = models.URLField(blank=True, null=True, verbose_name="رابط السيرة الذاتية") 
    cover_letter = models.TextField(verbose_name="خطاب التقديم", blank=True, null=True)
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    create_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="تاريخ الإنشاء")



    def __str__(self):
        return f"طلب {self.seeker.user} لوظيفة {self.job.title}"

    class Meta:
        verbose_name = "طلب توظيف"
        verbose_name_plural = "طلبات التوظيف"
        ordering = ['-application_date']  # ترتيب الطلبات حسب تاريخ التقديم




class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_notifications", verbose_name="المرسل")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_notifications", verbose_name="المستلم")
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True, verbose_name="الطلب")
    message = models.TextField(verbose_name="الرسالة")
    is_read = models.BooleanField(default=False, verbose_name="تم قراءته؟") 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return f"إشعار من {self.sender} إلى {self.receiver}"
    
    class Meta:
        verbose_name = 'الاشعارات'
        verbose_name_plural = 'الاشعارات'