from django.contrib import admin

# Register your models here.
from review_service.models import Question, Person, ReviewCycle

admin.site.register(Person)
admin.site.register(Question)
admin.site.register(ReviewCycle)
