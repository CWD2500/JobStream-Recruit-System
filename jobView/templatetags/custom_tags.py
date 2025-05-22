from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='is_job_seeker')
def is_job_seeker(user):
    return user.groups.filter(name='jobSeeker').exists()

@register.filter(name='is_employer')
def is_employer(user):
    return user.groups.filter(name='employer_company').exists()

@register.filter(name='is_admin')
def is_admin(user):
    return user.is_staff
