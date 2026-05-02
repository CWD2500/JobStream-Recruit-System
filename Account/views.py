import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth  import login , authenticate , logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .forms import SeekerEditForm, UserRegisterjobSeeker,PasswordResetForm , UserProfileForm , UserEducation , UserExperience  , UserCertificate , UserProjects , UserLanguage , EmployerForm , JobForm , CategeryJob , LoginForm , EmployerFormEdit
from .models import UserProfile ,   Application  ,  NATIONALITY , ACADEMIC_DEGREE , Experience  , Education , Certificate , Language , LANGUAGE , LANGUAGE_LAVEL , Projects  , EmployerProfile , CAREER_TYPE_CHOICES , CAREER_LEVEL_CHOICES , EDUCATION_CHOICES  , GENDER_CHOICES , JobCategory , Jobs
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from .decorators  import redirect_if_logged_in
from django.contrib.auth import get_user_model

from django.contrib.auth import update_session_auth_hash



User = get_user_model()


@redirect_if_logged_in
def register_job_seeker(request):
    if request.method == "POST":
        form = UserRegisterjobSeeker(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'البريد الإلكتروني موجود بالفعل!')
                return redirect('register')

            user = form.save(commit=False)
            user.user_type = 'jobSeeker'  
            user.set_password(password)
            user.save()

            jobseeker_group, _ = Group.objects.get_or_create(name='jobSeeker')
            user.groups.add(jobseeker_group)

            user = authenticate(email=email, password=password)

            login(request, user)
            messages.success(request, f"{user.username}: تم إنشاء الحساب بنجاح!")
            return redirect('data-users')
    else:
        form = UserRegisterjobSeeker()

    return render(request, 'account/register.html', {'form': form})



# @redirect_if_logged_in
# def register_job_seeker(request):
#     if request.method == "POST":
#         form = UserRegisterjobSeeker(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password1']

#             if User.objects.filter(email=email).exists():
#                 messages.error(request, 'البريد الإلكتروني موجود بالفعل!')
#                 return redirect(reverse('register'))
#             else:
#                 user = form.save()
#                 user.set_password(password)  
#                 user.save()
#                 user = authenticate(username=username, password=password)
#                 login(request, user)
#                 group = Group.objects.get(name='jobSeeker')
#                 user.groups.add(group)
#                 user.save()
#                 messages.success(request, f"{user.username}: تم إنشاء الحساب بنجاح!")   
#                 return redirect(reverse('data-users'))
#     else:
#         form = UserRegisterjobSeeker()

#     context = {
#         'form': form
#     }
#     return render(request, 'account/register.html', context)

@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
        return JsonResponse({'exists': False})





@redirect_if_logged_in
def logins(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'تم تسجيل الدخول بنجاح')
                return redirect(reverse('home'))
            else:
                messages.error(request, 'البريد الإلكتروني أو كلمة المرور غير صحيحة.')
        else:
            messages.error(request, 'خطأ في البيانات المدخلة.')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'account/login.html', context)



def logouts(request):
    logout(request)
    return redirect(reverse('home'))



# # Registering basic user data in the profile...

@login_required
def datauser(request):
    if request.method == "POST":
        try:
            user_data_profile, created = UserProfile.objects.get_or_create(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, "حدث خطأ أثناء استرداد ملف البيانات.")
            return redirect('data-users')

   
        datausersform = UserProfileForm(request.POST, request.FILES, instance=user_data_profile)

        if datausersform.is_valid():
            datausersform.save()
            messages.success(request, "تم اضاقة البيانات الى الملف الشخصي بنجاح!")
            return redirect(reverse('home'))
        else:
            for field, errors in datausersform.errors.items():
                for error in errors:
                    messages.error(request, f"خطأ في {field}: {error}")
            return redirect(reverse('data-users'))

    else:
        try:
            user_data_profile, created = UserProfile.objects.get_or_create(user=request.user)
            datausersform = UserProfileForm(instance=user_data_profile)
        except UserProfile.DoesNotExist:
            datausersform = UserProfileForm()

    context = {
        'datauserform': datausersform,
        'nationalities': NATIONALITY,
    }
    return render(request, 'account/datausers.html', context)



# Show Profile User
@login_required
def profileUser(request, slug):
    userProfile = get_object_or_404(UserProfile, slug=slug)
    experience_filter = Experience.objects.filter(profile=userProfile)
    language_filter = Language.objects.filter(profile=userProfile)
    certificate_get = Certificate.objects.filter(profile=userProfile)
    project_get = Projects.objects.filter(profile=userProfile)
    education_get = Education.objects.filter(profile=userProfile)

    # experience_get = Experience.objects.filter(profile=userProfile)


    if request.method == "POST":
        form_type = request.POST.get("form_type")  
        item_id = request.POST.get("id")  

        if form_type == "experience":
            if item_id:  
                experience_instance = get_object_or_404(Experience, id=item_id, profile=userProfile)
                userExperience = UserExperience(request.POST, instance=experience_instance)
                if userExperience.is_valid():
                    experience = userExperience.save(commit=False)
                    experience.profile = userProfile  
                    experience.user = request.user 
                    experience.save()
                    messages.success(request, "تم تعديل الخبرة بنجاح.")
                else:
                    messages.error(request, f"حدث خطأ في تعديل الخبرة: {userExperience.errors}")
            else:  # إضافة خبرة جديدة
                userExperience = UserExperience(request.POST)
                if userExperience.is_valid():
                    experience = userExperience.save(commit=False)
                    experience.profile = userProfile  
                    experience.user = request.user  
                    experience.save()
                    messages.success(request, "تم إضافة الخبرة بنجاح.")
                else:
                    messages.error(request, f"حدث خطأ في إضافة الخبرة: {userExperience.errors}")

        elif form_type == "education":
            if item_id:
                education_instance = get_object_or_404(Education, id=item_id, profile=userProfile)
                education_form = UserEducation(request.POST, instance=education_instance)
                if education_form.is_valid():
                    education = education_form.save(commit=False)
                    education.profile = userProfile 
                    education.user = request.user  
                    education.user = request.user 
                    education.save()
                    messages.success(request, "تم تعديل التعليم بنجاح.")
                else:
                    messages.error(request, "حدث خطأ في تعديل التعليم.")
            else:
                education_form = UserEducation(request.POST)
                if education_form.is_valid():
                    education = education_form.save(commit=False)
                    education.profile = userProfile 
                    education.user = request.user 
                    education.save()
                    messages.success(request, "تم إضافة التعليم بنجاح.")
                else:
                    messages.error(request, "حدث خطأ في إضافة التعليم.")

        elif form_type == "certificate":
            if item_id:
                certificate_instance = get_object_or_404(Certificate, id=item_id, profile=userProfile)
                userCertificate = UserCertificate(request.POST, instance=certificate_instance)
                if userCertificate.is_valid():
                    certificate = userCertificate.save(commit=False)
                    certificate.profile = userProfile  
                    certificate.user = request.user  
                    certificate.save()
                    messages.success(request, "تم تعديل الشهادة بنجاح.")
                else:
                    messages.error(request, "حدث خطأ في تعديل الشهادة.")
            else:
                userCertificate = UserCertificate(request.POST)
                if userCertificate.is_valid():
                    certificate = userCertificate.save(commit=False)
                    certificate.profile = userProfile 
                    certificate.user = request.user  
                    certificate.save()
                    messages.success(request, "تم إضافة الشهادة بنجاح.")
                else:
                    messages.error(request, "حدث خطأ في إضافة الشهادة.")

        elif form_type == "language":
            if item_id:
                language_instance = get_object_or_404(Language, id=item_id, profile=userProfile)
                userLanguage = UserLanguage(request.POST, instance=language_instance)
                if userLanguage.is_valid():
                    language = userLanguage.save(commit=False)
                    language.profile = userProfile  
                    language.user = request.user  
                    language.save()
                    messages.success(request, "تم تعديل اللغة بنجاح.")
                else:
                    messages.error(request, "حدث خطأ في تعديل اللغة.")
            else:
                userLanguage = UserLanguage(request.POST)
                if userLanguage.is_valid():
                    language = userLanguage.save(commit=False)
                    language.profile = userProfile  
                    language.user = request.user  
                    language.save()
                    messages.success(request, "تم إضافة اللغة بنجاح.")
                else:
                    messages.error(request, "حدث خطأ في إضافة اللغة.")

        elif form_type == "project":
            if item_id:
                project_instance = get_object_or_404(Projects, id=item_id, profile=userProfile)
                userProjects = UserProjects(request.POST, instance=project_instance)
                if userProjects.is_valid():
                    project = userProjects.save(commit=False)
                    project.profile = userProfile  
                    project.user = request.user  
                    project.save()
                    messages.success(request, "تم تعديل المشروع بنجاح.")
                else:
                    messages.error(request, "حدث خطأ في تعديل المشروع.")
            else:
                userProjects = UserProjects(request.POST)
                if userProjects.is_valid():
                    project = userProjects.save(commit=False)
                    project.profile = userProfile  
                    project.user = request.user  
                    project.save()
                    messages.success(request, "تم إضافة المشروع بنجاح.")
                else:
                    messages.error(request, "حدث خطأ في إضافة المشروع.")
        
        elif form_type == "biography":
            userProfileForm = UserProfileForm(request.POST, request.FILES, instance=userProfile)
            if userProfileForm.is_valid():
         
                biography_file = request.FILES.get('the_biography')
                if biography_file and not biography_file.name.endswith('.pdf'):
                    messages.error(request, "الرجاء رفع ملف PDF فقط.")
                else:

                    userProfileForm.save()
                    messages.success(request, "تم رفع السيرة الذاتية بنجاح.")
            else:
                messages.error(request, "حدث خطأ في رفع السيرة الذاتية.")

     
        return redirect(reverse('profile-users', kwargs={'slug': userProfile.slug}))

    else:
        experiences = Experience.objects.filter(profile=userProfile)
        educations = Education.objects.filter(profile=userProfile)
        certificates = Certificate.objects.filter(profile=userProfile)
        languages = Language.objects.filter(profile=userProfile)
        projects = Projects.objects.filter(profile=userProfile)

        userExperience = UserExperience()
        education_form = UserEducation()
        userCertificate = UserCertificate()
        userLanguage = UserLanguage()
        userProjects = UserProjects()


        context = {
            'experiences': experiences,
            'educations': educations,
            'language_filter': language_filter,
            'certificate_get': certificate_get,
            'education_get': education_get,
            'project_get': project_get,
            'experience_filter': experience_filter,
            'certificates': certificates,
            'languages': languages,
            'projects': projects,
            'userExperience': userExperience,
            'education_form': education_form,
            'userCertificate': userCertificate,
            'userLanguage': userLanguage,
            'userProjects': userProjects,
            'profile': userProfile,
         
            'NATIONALITY': NATIONALITY,
            'academic_degree': ACADEMIC_DEGREE,
            'LANGUAGE': LANGUAGE,
            'LANGUAGE_LAVEL': LANGUAGE_LAVEL,
        }


        return render(request, 'account/profileuser.html', context)






# def edit_data_profile(request ,id):
#     experience = Experience.objects.get(id = id)
#     if request.method=="POST":
#         form_type = request.POST.get("form_type")  # تحديد النموذج المرسل
#         if form_type =="experience":
#             experience_edit = UserExperience(request.POST , instance=experience)
#             if experience_edit.is_valid():
#                 experience_edit.save()
#     else:
#         experience_edit = UserExperience(request.POST , instance=experience)

#     context = {
#         'experience':experience,
#     }

#     return render(request, 'account/profileuser.html', context)





@login_required
def delete_data_profile(request, id):
    deleted = False  

    models = [Experience, Education, Projects, Certificate, Language, Application]

    for model in models:
        try:
            instance = model.objects.get(id=id)
            instance.delete()
            deleted = True  
            break 
        except model.DoesNotExist:
            continue  

    if deleted:
        messages.success(request, "تم الحذف بنجاح.")
    else:
        messages.error(request, "العنصر غير موجود أو تم حذفه مسبقًا.")

    return redirect(request.META.get('HTTP_REFERER', '/'))







#  order my  

@login_required
def profile_order(request):
    user_profile = request.user.profile  
    if request.user.groups.filter(name='jobSeeker').exists(): 
        user_orders = Application.objects.filter(seeker=user_profile) 
    else:
        user_orders = []  
    
    context = {
        'user_orders': user_orders
    }

    return render(request, 'account/order.html', context)

@login_required
def order_delete(request  ,id):
    try:
        delete_application = get_object_or_404(Application , id=id)
        if request.method =="GET":
            delete_application.delete()
            messages.success(request  , 'تم حذف بنجاح ')
            return redirect(reverse('orders'))
    except:
        return redirect(reverse('orders'))



@redirect_if_logged_in
def register_employer(request):
    if request.method == "POST":
        form = EmployerForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name_of_responsible_person']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'البريد الإلكتروني موجود بالفعل!')
                return redirect('register-employer')

            username = name
            if User.objects.filter(username=username).exists():
                username = f"{username}{User.objects.filter(username__startswith=username).count() + 1}"

            user = User.objects.create_user(username=username, email=email, password=password)
            user.user_type = 'employer_company'  
            user.save() 

            
            employer_group, _ = Group.objects.get_or_create(name='employer_company')
            user.groups.add(employer_group)

            profile, _ = EmployerProfile.objects.get_or_create(user=user)
            profile.company_name = form.cleaned_data['company_name']
            profile.name_of_responsible_person = name
            profile.phone_number = form.cleaned_data['phone_number']
            profile.state = form.cleaned_data['state']
            profile.governorate = form.cleaned_data['governorate']
            profile.save()

            login(request, user)
            messages.success(request, "تم إنشاء الحساب بنجاح!")
            return redirect(reverse('employer-addJob', kwargs={'slug': profile.slug}))
    else:
        form = EmployerForm()

    return render(request, 'employer/register.html', {'form': form})


@login_required
def addJob(request, slug):
    employer_profile = get_object_or_404(EmployerProfile, slug=slug)
    now = timezone.now().date()

    Jobs.objects.filter(employer=employer_profile, closing_date__lt=now).delete()

    job_free = Jobs.objects.filter(employer=employer_profile)
    
    job_published = job_free.filter(publication_date__lte=now)  
    job_not_published = job_free.filter(publication_date__gt=now)

    cate_job = JobCategory.objects.all()
    get_application = Application.objects.filter(job__in=job_free).select_related('job', 'seeker')
    job_count_free = job_published.count()
    job_count_not_free = job_not_published.count()
    get_application_count = get_application.count()
    job_to_edit = None

    if request.method == 'POST':
        delete_job_id = request.POST.get('delete_job_id')
        if delete_job_id:
            job_to_delete = get_object_or_404(Jobs, id=delete_job_id, employer=employer_profile)
            job_to_delete.delete()
            messages.success(request, 'تم حذف الوظيفة بنجاح!')
            return redirect(reverse('employer-addJob', kwargs={'slug': employer_profile.slug}))

        formjob = JobForm(request.POST, request.FILES)
        if formjob.is_valid():
            myform = formjob.save(commit=False)
            myform.employer = employer_profile

            publication_date = myform.publication_date
            closing_date = myform.closing_date
            
            if closing_date <= publication_date:
                messages.error(request, ' يجب أن يكون تاريخ الإغلاق أكبر من تاريخ النشر!')
                return redirect(reverse('employer-addJob', kwargs={'slug': employer_profile.slug}))
            
            if publication_date and publication_date > timezone.now().date():
                myform.save()
                messages.success(request, 'تم إضافة وظيفة جديدة وسوف يتم نشرها في التاريخ المحدد!')
                return redirect(reverse('employer-addJob', kwargs={'slug': employer_profile.slug}))
            
            myform.save()  
            messages.success(request, 'تم إضافة وظيفة جديدة بنجاح!')
            return redirect(reverse('employer-addJob', kwargs={'slug': employer_profile.slug}))

    else:
        formjob = JobForm()

    context = {
        'form': formjob,
        'job_published': job_published,  
        'job_not_published': job_not_published,  
        'cate_job': cate_job,
        'job_to_edit': job_to_edit,
        'employer_profile': employer_profile,
        'job_count_free': job_count_free,
        'job_count_not_free': job_count_not_free,
        'get_application_count': get_application_count,
        'get_application': get_application,
        'now': now  
    }

    return render(request, 'employer/home.html', context)









def edit_job_employer(request, slug):
    job_editor = get_object_or_404(Jobs, slug=slug)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job_editor)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم التعديل بنجاح')
            return redirect(reverse('employer-addJob', kwargs={'slug': job_editor.employer.slug}))
    else:
        form = JobForm(instance=job_editor)

    return render(request, 'employer/edit_job.html', {'form': form, 'job_editor': job_editor})




def editUserProfile(request, slug):
    userProfile = get_object_or_404(UserProfile, slug=slug)
    if request.method == "POST":
        form = SeekerEditForm(request.POST, request.FILES, instance=userProfile)
        if form.is_valid():
            new_email = form.cleaned_data.get('email')   
            if User.objects.filter(email=new_email).exclude(id=userProfile.user.id).exists():
                messages.error(request, ' البريد الإلكتروني مستخدم بالفعل!')
            else:
                userProfile.user.email = new_email
                userProfile.user.save()
                form.save()
                messages.success(request, ' تم التعديل بنجاح!')
                return redirect(reverse('profile-users', kwargs={'slug': userProfile.slug}))
    
    else:
        form = SeekerEditForm(instance=userProfile)  

    context = {
        'form': form, 
        'profile': userProfile,
        'nationalities': NATIONALITY,
    }
    return render(request, 'account/editProfileInfo.html', context)

        



def edit_employer_data(request, slug):
    employer = get_object_or_404(EmployerProfile, slug=slug)

    if request.method == "POST":
        form = EmployerFormEdit(request.POST, request.FILES, instance=employer)

        if form.is_valid():
            new_email = form.cleaned_data.get('email')

           
            if User.objects.filter(email=new_email).exclude(id=employer.user.id).exists():
                messages.error(request, ' البريد الإلكتروني مستخدم بالفعل من قبل!')
            else:
                employer.user.email = new_email  
                employer.user.save()  
                form.save()  
                messages.success(request, ' تم التعديل بنجاح!')
                return redirect(reverse('employer-addJob', kwargs={'slug': employer.slug}))  
        else:
            messages.error(request, ' هناك خطأ في البيانات، تحقق من الحقول.')

    else:
        form = EmployerFormEdit(instance=employer)

    return render(request, 'employer/edit_employer.html', {'form': form})



def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            
            try:
                user = User.objects.get(email=email)
                
                if not user.check_password(old_password):
                    form.add_error('old_password', "كلمة المرور القديمة غير صحيحة.")
                elif new_password == old_password:
                    form.add_error('new_password', "كلمة المرور الجديدة يجب أن تكون مختلفة عن القديمة.")
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user) 
                    messages.success(request, "تم تغيير كلمة المرور بنجاح!")
                    return redirect('logins') 
                    
            except User.DoesNotExist:
                form.add_error('email', "البريد الإلكتروني غير مسجل لدينا.")
    else:
        form = PasswordResetForm()

    return render(request, "account/reset_password.html", {"form": form})