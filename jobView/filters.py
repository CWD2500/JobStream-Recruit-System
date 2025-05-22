import django_filters
from Account.models import Jobs   , CAREER_TYPE_CHOICES , EDUCATION_CHOICES , CAREER_LEVEL_CHOICES , GENDER_CHOICES , CAREER_TYPE_CHOICES



class jobFilters(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label="عنوان الوظيفة")
    career_type = django_filters.ChoiceFilter(choices=CAREER_TYPE_CHOICES, label="نوع الوظيفة")
    education = django_filters.ChoiceFilter(choices=EDUCATION_CHOICES, label="المستوى التعليمي")
    career_level = django_filters.ChoiceFilter(choices=CAREER_LEVEL_CHOICES, label="المستوى الوظيفي")
    gender = django_filters.ChoiceFilter(choices=GENDER_CHOICES, label="الجنس")
    years_of_experience_from = django_filters.NumberFilter(field_name="years_of_experience_from", lookup_expr="gte", label="الخبرة من")
    years_of_experience_to = django_filters.NumberFilter(field_name="years_of_experience_to", lookup_expr="lte", label="الخبرة إلى")
    location = django_filters.CharFilter(lookup_expr="icontains", label="الموقع")

    class Meta:
        model = Jobs
        fields = ['title', 'career_type', 'education', 'career_level', 'gender', 'years_of_experience_from', 'years_of_experience_to', 'location']
        # exclude  = ["employer" , 'job_category'  , 'job_category' , 'salary', 'salary', 'email' , 'phone_number', 'publication_date', 'closing_date' ,'slug' , 'job_description']



class  CareerType  (django_filters.FilterSet):
    careettype = django_filters.ChoiceFilter(choices=CAREER_TYPE_CHOICES  , label="الوظائف")

    class Meta:
        model = Jobs
        fields = ['career_type']