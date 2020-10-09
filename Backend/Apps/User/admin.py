from django.contrib import admin
from .models import Student, Teacher, UserReport, UserProfilePhoto, UserOnline

admin.site.register(UserOnline)
admin.site.register(UserProfilePhoto)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(UserReport)
