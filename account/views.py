from django.shortcuts import render,redirect
from django.contrib import auth,messages
from .forms import RegisterForm
from .models import Account
# foor email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Login Successfull ')
            return redirect('store')
        else:
            messages.error(request,'Please check your Credentials ')
            return redirect('login')

    return render(request,'account/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are succcessfully logged out")
    return redirect('login')

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.save()
            user.phone_number=phone_number
            user.save()
            messages.success(request,"Registration Successfull .. We have send you an Email kindly check your Email ")

            current_site=get_current_site(request)
            mail_subject='Please Activate your account'
            message=render_to_string('account/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()

            return redirect('login')
    form=RegisterForm()
    context={
        "form":form,
    }
    return render(request, 'account/register.html',context)

def activate(request,uidb64,token):
    uid=urlsafe_base64_decode(uidb64).decode()
    user=Account._default_manager.get(pk=uid)
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations ur acc is activated ')
        return redirect('login')
    else:
        messages.error('Invalid Link')
        return redirect('home')
def forgotPassword(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="Reset your password"
            message=render_to_string('account/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
            messages.success(request,'Password reset email has been sent to ur email address')
            return redirect('forgotpassword')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotpassword')

    return render(request,'account/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    uid=urlsafe_base64_decode(uidb64).decode()#uid=1
    user=Account._default_manager.get(pk=uid)
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,"please reset your password")
        return redirect('resetpassword')
    else:
        messages.error(request,'this link has been expired')
        return redirect('login')

def resetPassword(request):
    if request.method=="POST":
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password has been reset')
            return redirect('login')
        else:
            messages.error(request,'password do not match')
            return redirect('resetPassword')
    return render(request,'account/reset_password.html')