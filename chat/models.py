from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chat(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    data = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, **kwargs):
        self.slug = 'slugis'+str(self.student.pk)+'and'+str(self.teacher.pk)
        super(Chat, self).save()

    def __str__(self):
        return f'{self.student} & {self.teacher}'

    def getSlugURL(self):
        return f'{self.slug}'