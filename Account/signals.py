from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import UserProfile, EmployerProfile
from .utils import randon_slug

@receiver(post_save, sender=User)
def create_empty_profiles(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        EmployerProfile.objects.get_or_create(user=instance)

@receiver(m2m_changed, sender=User.groups.through)
def create_profile_based_on_group(sender, instance, action, **kwargs):
    if action == 'post_add':
        user = instance
        if user.groups.filter(name="jobSeeker").exists():
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created or not profile.slug:
                profile.slug = slugify(randon_slug() + '-' + str(user))
                profile.save()

        elif user.groups.filter(name="employer_company").exists():
            profile, created = EmployerProfile.objects.get_or_create(user=user)
            if created or not profile.slug:
                profile.slug = slugify(randon_slug() + '-' + profile.company_name)
                profile.save()
