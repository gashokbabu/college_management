from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm, SetProfileForm, UserUpdateForm, ProfilePicForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import login, authenticate
from srkr.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
import time
# Create your views here.
# def LogInView(request):


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print(user.username)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username} you are now able to login')
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('students/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            sent = send_mail(mail_subject, message, EMAIL_HOST_USER, [to_email], fail_silently=False)
            print(sent)
            if sent==0:
                user.delete()
                return HttpResponse('please provide correct email address')

            print(message)
            return HttpResponse('Please confirm your email address to complete the registration')
            # return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'students/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        student = CurrentStudent.objects.get(user=user)

    context = {'student': student,
               }
    return render(request, 'students/profile.html', context)


def updateStudent(request):
    if request.user.is_superuser:
        currentStudent = CurrentStudent.objects.all()
        for student in currentStudent:
            if student.AcadamicYear == None or student.Sem == None or student.Year == None:
                continue
            student.attnd = 100.00
            if student.Year == 4:
                if student.Sem == 2:
                    student.delete()
                if student.Sem == 1:
                    student.Sem +=1
                    student.save()
            elif student.Sem == 1:
                student.Sem += 1
                student.save()
            elif student.Sem == 2:
                student.Year += 1
                student.Sem -= 1
                student.AcadamicYear += 1
                student.save()
        messages.success(request, f'All students are updated to next semister')
        return HttpResponse('<h4>All student data is updated to next semister</h4>')
    else:
        return HttpResponse('you are not allowed to change the subjects.please login as admin into admin pannelk')


def saveStudents(request):
    if request.user.is_superuser:
        currentStudent = CurrentStudent.objects.all()
        for student in currentStudent:
            # if student.name == None:
            #     continue
            acadamicyear = student.AcadamicYear
            name = student.name
            regno = student.regNo
            section = student.section
            user = student.user
            attnd = student.attnd
            year = student.Year
            sem = student.Sem
            subject1 = student.subject1
            subject2 = student.subject2
            subject3 = student.subject3
            marks1 = student.marks1
            marks2 = student.marks2
            marks3 = student.marks3
            joinedyear = student.joinedYear
            x = Student(AcadamicYear=acadamicyear,
                        name=name,
                        regNo=regno,
                        section=section,
                        user=user,
                        attnd=attnd,
                        Year=year,
                        Sem=sem,
                        subject1=subject1,
                        subject2=subject2,
                        subject3=subject3,
                        marks1=marks1,
                        marks2=marks2,
                        marks3=marks3,
                        joinedYear=joinedyear)
            x.save()
        return HttpResponse('<h4>All student data is saved to the database</h4>')
    else:
        return HttpResponse('you are not allowed to change the subjects.please login as admin into admin pannelk')


@login_required
def setprofile(request):
    u_form = UserUpdateForm()
    p_form = ProfilePicForm()
    s_form = None
    print(request.user.currentstudent.name)
    if request.user.currentstudent.name == None and request.user.currentstudent.regNo == None:
        s_form = SetProfileForm()
    if request.method == 'POST' and request.user.currentstudent.name == None and request.user.currentstudent.regNo == None:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilePicForm(
            request.POST, request.FILES, instance=request.user.currentstudent)
        s_form = SetProfileForm(
            request.POST, instance=request.user.currentstudent)
        if u_form.is_valid() and s_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            s_form.save()
            # username = u_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been updated')
            return redirect('profile')

    elif request.method == 'POST' and request.user.currentstudent.name != None and request.user.currentstudent.regNo != None:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilePicForm(
            request.POST, request.FILES, instance=request.user.currentstudent)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilePicForm(instance=request.user.currentstudent)
        if request.user.currentstudent.name == None:
            s_form = SetProfileForm(instance=request.user.currentstudent)
    context = {'u_form': u_form,
               's_form': s_form,
               'p_form': p_form}
    return render(request, 'students/set_profile.html', context)


def updateSubjects(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            year = request.POST.get('year')
            sem = request.POST.get('sem')
            subject1 = request.POST.get('subject1')
            subject2 = request.POST.get('subject2')
            subject3 = request.POST.get('subject3')
            students = CurrentStudent.objects.filter(Year=year, Sem=sem)
            for student in students:
                student.subject1 = subject1
                student.subject2 = subject2
                student.subject3 = subject3
                student.save()
            messages.success(
                request, f'All subjects of {year}-{sem} students are updated')

    else:
        return HttpResponse('you are not allowed to change the subjects.please login as admin into admin pannel')

    return render(request, 'students/update_subjects.html')


def saveandupdate(request):
    if request.user.is_superuser:
        return render(request, 'students/studentupdate.html')
    else:
        return HttpResponse('<h4>please lonin as administator by clicking on it <a href="{url "login"}">login</a></h4>')
