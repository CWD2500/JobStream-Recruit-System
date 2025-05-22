from django.contrib.auth.models import Group
from Account.models import Notification
from django.urls import reverse
def user_groups(request):
    if request.user.is_authenticated:
        return {
            'is_job_seeker': request.user.groups.filter(name='jobSeeker').exists(),
            'is_employer': request.user.groups.filter(name='employer_company').exists(),
            'is_admin': request.user.is_staff,
        }
    return {}




def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver=request.user, is_read=False).order_by('-created_at')
        for notification in notifications:
            notification.message_lines = notification.message.split("\n")
        # نضيف الـ URL الذي سيتعامل مع طلب تحديث الإشعارات
        notifications_url = reverse('mark_all_notifications_read')
    else:
        notifications = []
        notifications_url = None  # إذا كان المستخدم غير مسجل الدخول

    return {'notifications': notifications, 'notifications_url': notifications_url}