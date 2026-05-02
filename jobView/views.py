from django.shortcuts import redirect, render , get_object_or_404
from Account.models import JobCategory , Jobs , EmployerProfile   , UserProfile , Notification  , Application
from Account.forms  import ApplicationApply
from .filters import jobFilters  , CareerType
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.timezone import now
from django.db.models  import Q
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Count




def home(request):
    now = timezone.now().date()
    category = JobCategory.objects.all()

    jobs_get = Jobs.objects.filter(
        publication_date__lte=now,
        closing_date__gte=now
    ).order_by('-publication_date')[:6]

    categories_with_job_count = JobCategory.objects.annotate(
        job_count=Count(
            'jobs',
            filter=Q(jobs__publication_date__lte=now, jobs__closing_date__gte=now)
        )
    ).all()

    careey_type = request.GET.get('careey_types', None)
    allowed_types = ['full_time', 'part_time', 'on_site']

    if careey_type in allowed_types:
        jobs = Jobs.objects.filter(
            career_type=careey_type,
            publication_date__lte=now,
            closing_date__gte=now
        )
    else:
        jobs = Jobs.objects.filter(
            publication_date__lte=now,
            closing_date__gte=now
        )

    unread_notifications = Notification.objects.all() if request.user.groups.filter(name='employer_company').exists() else Notification.objects.none()

    context = {
        'categories': category,
        'categories_with_job_count': categories_with_job_count,
        'jobs_get': jobs,
        'careey_type': careey_type,
        'unread_notifications': unread_notifications,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'index.html', context)

    return render(request, 'index.html', context)


    
def job_list(request, slug):
    now = timezone.now().date()
    category_job = None
    job_list = Jobs.objects.none()

    if JobCategory.objects.filter(slug=slug).exists():
        category_job = JobCategory.objects.get(slug=slug)
        job_list = Jobs.objects.filter(
            job_category=category_job,
            publication_date__lte=now,    
            closing_date__gte=now       
        )

    myfilter = jobFilters(request.GET, queryset=job_list)
    job_list = myfilter.qs
    pagnator = Paginator(job_list, 6)
    page_number = request.GET.get('page')
    page_obj = pagnator.get_page(page_number)

    context = {
        'job_list': page_obj,
        'myfilter': myfilter,
        'category_job': category_job,
        'filters_params': request.GET.urlencode(),
        'now': now
    }

    return render(request, 'job_list.html', context)




def apply_for_job_details(request, slug):
    job = get_object_or_404(Jobs, slug=slug)


    is_employer = request.user.is_authenticated and request.user.groups.filter(name="employer_company").exists()

    if not job.employer:
        messages.error(request, "لا يمكن العثور على صاحب العمل لهذه الوظيفة.")
        return redirect('home')

    employer_slug = getattr(job.employer, 'slug', None)
    if not employer_slug:
        messages.error(request, "لا يوجد معرف صالح لصاحب العمل.")
        return redirect('home')

    employer_profile = None
    if UserProfile.objects.filter(slug=employer_slug).exists():
        employer_profile = get_object_or_404(UserProfile, slug=employer_slug)
    elif EmployerProfile.objects.filter(slug=employer_slug).exists():
        employer_profile = get_object_or_404(EmployerProfile, slug=employer_slug)
    else:
        messages.error(request, "لم يتم العثور على ملف صاحب العمل.")
        return redirect('home')

    if not request.user.is_authenticated or is_employer:
        can_apply = False
        form = None  
    else:
        if hasattr(request.user, 'profile'):
            previous_application = Application.objects.filter(seeker=request.user.profile, job=job).last()
            if previous_application:
                time_difference = timezone.now() - previous_application.application_date
                can_apply = time_difference >= timedelta(days=90)
            else:
                can_apply = True

            form = ApplicationApply() if can_apply else None
        else:
            can_apply = False
            form = None 

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "يجب عليك تسجيل الدخول لتتمكن من التقديم على الوظيفة.")
            return redirect('login')

        if is_employer:
            messages.error(request, "لا يمكنك التقديم على وظيفة لأنك صاحب عمل.")
            return redirect('home')

        form = ApplicationApply(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.seeker = request.user.profile
            application.job = job
            application.status = 'pending'
            application.cv_link = request.user.profile.slug
            application.save()

            notification_message = (
                f" طلب وظيفة جديد!\n"
                f" المتقدم:  {request.user.first_name} ({request.user.email})\n"
                f" وقت التقديم: {timezone.now().strftime('%Y-%m-%d %H:%M')}\n"
                f" الوظيفة: {job.title}\n"
                f" مراجعة الطلبات من لوحة التحكم."
            )
            Notification.objects.create(
                sender=request.user,
                receiver=job.employer.user,
                application=application,
                message=notification_message
            )
            messages.success(request, 'تم التقديم بنجاح، من فضلك تحقق من حالة طلبك.')
            return redirect('home')
        else:
            messages.error(request, 'هناك خطأ في البيانات المدخلة')

    context = {
        'job': job,
        'form': form,
        'can_apply': can_apply,
        'is_employer': is_employer, 
    }
    return render(request, 'details.html', context)




def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)

    if request.user != application.job.employer.user:
        return JsonResponse({'error': 'غير مصرح لك بتنفيذ هذا الإجراء'}, status=403)


    if status not in ['accepted', 'rejected']:
        return JsonResponse({'error': 'حالة غير صالحة'}, status=400)

    application.status = status
    application.save()

    if status == 'accepted':
        sender = request.user  
        receiver = application.seeker.user
        message = f"تم قبول طلبك للوظيفة: {application.job.title}"
    else:
        sender = application.seeker.user  
        receiver = request.user  
        message = f" تم رفض طلبك للوظيفة: {application.job.title}"

    Notification.objects.create(
        sender=sender,
        receiver=receiver,
        application=application,
        message=message
    )

    return JsonResponse({'success': 'تم تحديث الطلب بنجاح!', 'status': status})




def about (request):
    return render(request , 'about.html')

def mark_all_notifications_read(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver=request.user, is_read=False)
        notifications.update(is_read=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'User not authenticated'})

def user_groups(request):
    return {
        'is_employer': request.user.groups.filter(name='employer_company').exists(),
        'is_jobSeeker': request.user.groups.filter(name='jobSeeker').exists(),
        'is_admin': request.user.is_staff
    }



# Searching 

def job_search(request):
    query = request.GET.get('query', '').strip()  
    if query:
        jobs = Jobs.objects.filter(
            Q(title__icontains=query) |
            Q(job_description__icontains=query) |
            Q(job_category__name__icontains=query) |
            Q(career_type__icontains=query) |
            Q(education__icontains=query) |
            Q(career_level__icontains=query) |
            Q(gender__icontains=query) |
            Q(salary__icontains=query) |
            Q(location__icontains=query)
        ).distinct().order_by('-publication_date')  
        print(f"عدد النتائج: {jobs.count()}")  
    else:
        jobs = Jobs.objects.all().order_by('-publication_date')
    
    context = {
        'jobs': jobs, 
        'query': query
    }
    return render(request, 'searchJobs.html', context)