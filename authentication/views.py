import re
from django.shortcuts import render , redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes , force_str , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.

class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error' :'Invalid Email'},status = 400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error' :'Sorry, email already in use, choose another one'},status = 409)
        return JsonResponse({'email_valid' : True})

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error' :'username should only contain alphanumeric characters'},status = 400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' :'Sorry, username already in use, choose another one'},status = 409)
        return JsonResponse({'username_valid' : True})

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')

    def post(self,request):
        #Get the user data
        # validate user data
        # create account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues' : request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if(len(password) < 6):
                    messages.error(request,'Password too short')
                    return render(request,'authentication/register.html',context)

                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active = False
                user.save()


                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
             
                domain = get_current_site(request).domain
                link = reverse('activate',kwargs={'uidb64':uidb64 ,'token':token_generator.make_token(user)})
                activate_url = 'http://'+domain+link
                email_subject = 'Activate your account'
                email_body = 'Hi ' + user.username + \
                'Please use this link to verigy your account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'sender.everyrupee@gmail.com',
                    [email],
                )

                email.send(fail_silently=False)
                messages.success(request,'Account successfully created')
        return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
        

            messages.success(request,'Account created Successfully')
            return redirect('login')

        except Exception as ex: 
            pass
        return redirect('login')


class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:

            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request,'Welcome '+user.username+ ', you are now logged in')
                    return redirect('expenses')
                else:        
                    messages.error(request,'Account is not active, please check your email')
                return render(request,'authentication/login.html')

            else:
                messages.error(request,'Invalid Crediatials,try again')
                return render(request,'authentication/login.html')
        else:
            messages.error(request,'Please fill all the fields')
            return render(request,'authentication/login.html')


class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You are successfully logged out')
        return redirect('login')



class RequestPasswordReset(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')

    def post(self,request):
        email = request.POST['email']
        context = {
            'values' : request.POST
        }
        if not validate_email(email):
            messages.error(request,'Please Supply a valid email')
            return render(request,'authentication/reset-password.html',context)
        
        current_site = get_current_site(request)
        user = request.objects.filter(email=email)


        if user.exists():
            email_contents = {
                'user' : user[0],
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token' : PasswordResetTokenGenerator().make_token(user[0]),
            }
            link = reverse('reset-user-password',kwargs={'uidb64':email_contents['uid'] ,'token':email_contents['token']})
            reset_url = 'http://'+current_site.domain+link
            email_subject = 'Password reset instruction'
            email_body = 'Hi there' +  \
            'Please use this link to reset your password\n' + reset_url
            email = EmailMessage(
                email_subject,
                email_body,
                'sender.everyrupee@gmail.com',
                [email],
            )

        email.send(fail_silently=False)
        # messages.success(request,'Account successfully created')
        
        messages.success(request, 'We have sent you an email to reset your password')
        


        return render(request,'authentication/reset-password.html')



class CompletePasswordReset(View):
    def get(self,request,uidb64,token):
        return render(request, 'authentication/set-newpassword.html')

    def post(self,request,uidb64,token):
        return render(request, 'authentication/set-newpassword.html')
