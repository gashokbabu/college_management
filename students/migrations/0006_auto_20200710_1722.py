# Generated by Django 3.0.4 on 2020-07-10 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_currentstudent_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentstudent',
            name='profile_pic',
            field=models.FileField(default='default.jpg', upload_to='profilepics'),
        ),
    ]
