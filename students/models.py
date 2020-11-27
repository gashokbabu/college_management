from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from srkr.settings import EMAIL_HOST_USER
# class Section1(models.Model):
#     CHOICES = [('A', 'A'),
#                ('B', 'B'),
#                ('C', 'C'),
#                ('D', 'D')]
#     section = models.CharField(default='A', choices=CHOICES, max_length=100)
#     classTeacher = models.CharField(max_length=100)
# class Student1(models.Model):
#     section = models.ForeignKey
#     name = models.CharField(max_length=100)
#     regNo = models.CharField(max_length=100)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     attnd = models.FloatField()
#
#     def __str__(self):
#         return self.name


# class AcademicYear(models.Model):
#     academicYear = models.IntegerField()
#     def __str__(self):
#         return str(self.academicYear)
#
# class Year(models.Model):
#     CHOICES=[(1,'1'),
#              (2,'2'),
#              (3,'3'),
#              (4,'4')]
#     year = models.IntegerField(default=1,choices=CHOICES)
#     # acadamicyear = models.ForeignKey(AcademicYear,on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.year)
# class Sem(models.Model):
#     CHOICES=[(1,'1'),
#              (2,'2')
#              ]
#     year = models.ForeignKey(Year,on_delete=models.CASCADE)
#     subject1 = models.CharField(max_length=100, null=True)
#     subject2 = models.CharField(max_length=100, null=True)
#     subject3 = models.CharField(max_length=100, null=True)
#     sem = models.IntegerField(default=1,choices=CHOICES)
#     def __str__(self):
#         return str(str(self.year)+"-"+str(self.sem))
#
# class Section(models.Model):
#     CHOICES = [('A', 'A'),
#                ('B', 'B'),
#                ('C', 'C'),
#                ('D', 'D')]
#     sem = models.ForeignKey(Sem,on_delete=models.CASCADE)
#     section = models.CharField(default='A', choices=CHOICES,max_length=100)
#     classTeacher = models.CharField(max_length=100)
#     def __str__(self):
#         return self.section
class Teachers(models.Model):
    teacherUser = models.OneToOneField(User, on_delete=models.CASCADE)
    TeacherName = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        ordering = ["TeacherName"]
        verbose_name_plural = "Teachers"
    def __str__(self):
        return f'{self.TeacherName}'
class CurrentStudent(models.Model):
    YEAR_CHOICES = [(1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4')]
    SEM_CHOICES = [(1, '1'),
                   (2, '2')
                   ]
    SECTION_CHOICES = [('A', 'A'),
                       ('B', 'B'),
                       ('C', 'C'),
                       ('D', 'D')]
    AcadamicYear = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(
        default='default.jpg', upload_to='pictures')
    regNo = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    section = models.CharField(
        default='A', choices=SECTION_CHOICES, max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attnd = models.FloatField(default=100.00, null=True, blank=True)
    Year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    Sem = models.IntegerField(choices=SEM_CHOICES, blank=True, null=True)
    subject1 = models.CharField(max_length=100, null=True, blank=True)
    marks1 = models.IntegerField(default=0, blank=True, null=True)
    subject2 = models.CharField(max_length=100, null=True, blank=True)
    marks2 = models.IntegerField(default=0, blank=True, null=True)
    subject3 = models.CharField(max_length=100, null=True, blank=True)
    marks3 = models.IntegerField(default=0, blank=True, null=True)
    joinedYear = models.IntegerField(null=True, blank=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(Teachers,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_CurrentStudent(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            CurrentStudent.objects.create(user=instance)
            instance.currentstudent.save()
        print('created')


@receiver(post_save, sender=User)
def save_CurrentStudent(sender, instance, **kwargs):
    print('profile updated')


@receiver(post_save, sender=CurrentStudent)
def save_Email(sender, instance, **kwargs):
    if instance.attnd <= 75.00:
        send_mail('Attendence Shortage', f'you ward {instance.name} have attendence shortage.please contact the college for further process', EMAIL_HOST_USER, [
                  instance.user.email],fail_silently=True)


class Student(models.Model):
    YEAR_CHOICES = [(1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4')]
    SEM_CHOICES = [(1, '1'),
                   (2, '2')
                   ]
    SECTION_CHOICES = [('A', 'A'),
                       ('B', 'B'),
                       ('C', 'C'),
                       ('D', 'D')]
    AcadamicYear = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    regNo = models.CharField(max_length=100, null=True, blank=True)
    section = models.CharField(
        default='A', choices=SECTION_CHOICES, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attnd = models.FloatField(default=100.00, null=True, blank=True)
    Year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    Sem = models.IntegerField(choices=SEM_CHOICES, blank=True, null=True)
    subject1 = models.CharField(max_length=100, null=True, blank=True)
    marks1 = models.IntegerField(default=0, blank=True, null=True)
    subject2 = models.CharField(max_length=100, null=True, blank=True)
    marks2 = models.IntegerField(default=0, blank=True, null=True)
    subject3 = models.CharField(max_length=100, null=True, blank=True)
    marks3 = models.IntegerField(default=0, blank=True, null=True)
    joinedYear = models.IntegerField(null=True, blank=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'

# class Subjects(models.Model):
#     sem = models.ForeignKey(Sem,on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return str(self.sem) +" "+"subjects"
