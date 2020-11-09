from django.contrib import admin

from .models import Student, Teacher, Chat

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Chat)