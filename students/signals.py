from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import CurrentStudent

# @receiver(post_save,sender=User)
# def create_CurrentStudent(sender,instance,created,**kwargs):
# 	if created:
# 		CurrentStudent.objects.create(user = instance)
#
# @receiver(post_save,sender=User)
# def save_CurrentStudent(sender,instance,created,**kwargs):
#     if created == False:
# 	    instance.currentstudent.save()