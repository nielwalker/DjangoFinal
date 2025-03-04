from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

class TrainerRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField()

    def __str__(self):
        return self.user.first_name
    
class CourseInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    course_category = (
        ('development', 'Development'),
        ('business', 'Business'),
        ('finance & accounting', 'Finance & Accounting'),
        ('it & software', 'IT & Software'),
        ('marketing', 'Marketing'),
    )
    category = models.CharField(max_length=1000, choices=course_category, default='development')

    def __str__(self):
        return self.course_name

def course_slug(instance):
    return instance.course_name.lower().replace(' ', '-')

def course_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = course_slug(instance)

pre_save.connect(course_slug_generator, sender=CourseInfo)

class CourseDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_info = models.ForeignKey(CourseInfo, on_delete=models.CASCADE)
    course_image = models.ImageField(blank=True, null=True)
    course_desc = models.TextField()