from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Complete_Profile
from datetime import datetime, timedelta
from django.contrib.auth import login, logout, authenticate
import random
from lawyer.models import Lawyer_Profile
from .models import Contact_lawyer, Thread, ChatMessage
from Admin.models import Add_court, Add_law

from django.core.paginator import Paginator
import time


# Create your views here.

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'E-mail already exists!!!')
            else:
                user = User.objects.create_user(first_name=name, email=email, username=email, password=password1)

                user.save()
                user_login = authenticate(request, username=email, password=password1)
                if user_login is not None:
                    login(request, user_login)
                print('user saved')
                id = User.objects.last()
                request.session['id'] = id.id
                return redirect(completeprofile)
        else:
            messages.warning(request, 'password mismatch')
            print('password mismatch')

    return render(request, 'register.html')


def usersignin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        print(email, password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            messages.warning(request, 'Account not found')
    return render(request, "login.html")


def home(request):
    return render(request, 'login.html')


def completeprofile(request):
    id = request.session.get('id')
    print(id)
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip = request.POST.get('zip')
        mobile = request.POST.get('mobile')
        user = User.objects.get(id=id)
        image = request.FILES['profile_img']
        complete_profile = Complete_Profile.objects.create(user=user, image=image, address=address, city=city,
                                                           country=country, zip=zip, mobile=mobile)

        complete_profile.save()
        print('user saved')
        request.session['id'] = id
        return redirect(index)
    return render(request, "complete_profile.html")


def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        try:
            if User.objects.get(email=email):
                def generate_otp():
                    return random.randint(100000, 999999)

                otp = generate_otp()
                print("generated otp:", otp)
                time = datetime.now()

                send_mail('forget password', f'One Time Password to verify your Email is :{otp}',
                          settings.EMAIL_HOST_USER, [email])
                request.session['otp'] = otp
                request.session['time'] = str(time)
                request.session['email'] = email
                return redirect(reset)

        except:
            messages.warning(request, 'E-mail does not exists')
    return render(request, 'forgot.html')


def reset(request):
    otp = request.session.get("otp")
    email = request.session.get("email")
    time = request.session.get('time')
    send_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.now()
    time_difference = current_time - send_time
    print(type(otp))
    if request.method == 'POST':
        confirm_otp = int(request.POST.get('otp'))
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if otp == confirm_otp and new_password == confirm_password and time_difference <= timedelta(minutes=5):
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            user_login = authenticate(request, username=user.username, password=new_password)
            if user_login is not None:
                login(request, user_login)
                return redirect(index)
            else:
                messages.error(request, 'account not found')
        elif otp != confirm_otp:
            messages.error(request, 'Invalid otp')
        elif new_password != confirm_password:
            messages.error(request, 'password mismatch')
        elif otp == confirm_otp and time_difference >= timedelta(minutes=5):
            messages.error(request, 'time exceeded')

    return render(request, 'reset.html')


def Lawyers(request):
    request.session['id'] = request.session.get('id')
    print(request.session.get('id'))
    Lawyers = Lawyer_Profile.objects.all()
    return render(request, 'Lawyers.html', {'lawyers': Lawyers})


def contact_lawyer(request,id):
    logged_in_user_id = request.user.id
    print(request.user.id)
    user = User.objects.get(id=request.user.id)
    to_user = None
    threads = None
    prof = None

    if id is not None:
        to_user = User.objects.get(id=id)
        prof = Lawyer_Profile.objects.get(user=to_user)
        print(to_user)
        try:
            # Try to get existing thread between current user and the selected user
            thread = Thread.objects.get(first_person=user, second_person=to_user)
            print(1,thread)
        except Thread.DoesNotExist:
            try:
                # Try to get existing thread where the selected user is the first person
                thread = Thread.objects.get(first_person=to_user, second_person=user)
                print(2,thread)
            except Thread.DoesNotExist:
                # If no existing thread, create a new thread
                thread = Thread.objects.create(first_person=user, second_person=to_user)
                print(3,thread)
        finally:
            # Mark all unread messages as read
            unread_messages = ChatMessage.objects.filter(thread=thread, user=to_user, read=False)
            print(unread_messages)
            for msg in unread_messages:
                msg.read = True
                msg.save()
        # if not ChatMessage.objects.filter(thread=thread, user=user).exists() and not ChatMessage.objects.filter(
        #     thread=thread, user=to_user).exists():
        #         chat1 = ChatMessage.objects.create(thread=thread,user=user,message="Welcome to ChatNest")
        #         chat1.save()
        #         chat2 = ChatMessage.objects.create(thread=thread,user=to_user,message="Welcome to ChatNest")
        #         chat2.save()

    # Retrieve threads and messages
    if id is not None:
        if thread is not None:
            threads = Thread.objects.filter(pk=thread.pk).prefetch_related('chatmessage_thread').order_by('timestamp')
    return render(request, 'messages.html',
                  {'id': id, 'Threads': threads, 'to_user': to_user,'p':prof,'logged_in_user_id': logged_in_user_id})


# def contact_lawyer(request,id):
#     # lid = request.GET.get('id')
#     print(id)
#     if request.method == 'POST':
#         matter = request.POST.get('matter')
#         complaint = request.POST.get('complaint')
#         print(request.session.get('id'))
#         user = User.objects.get(id=request.user.id)
#         print(request.user.id)
#         lawyer = Lawyer_Profile.objects.get(id=id)
#         print(lawyer.user.id)
#         contact_lawyer = Contact_lawyer.objects.create(user=user, lawyer=lawyer, matter=matter, complaint=complaint)
#         contact_lawyer.save()
#         print('user saved')
#         return redirect(guest)
#     return render(request, 'messages.html',{ 'id':id})


def view_lawyer(request):
    lid = request.GET.get('id')
    view_lawyer = Lawyer_Profile.objects.get(user=lid)
    return render(request, 'view_lawyer.html', {'view_lawyer': view_lawyer})


def view_court(request):
    view_court = Add_court.objects.all()
    return render(request, 'view_court.html', {'view_court': view_court})


def view_law(request):
    view_law = Add_law.objects.all()
    if request.method == "POST":
        search = request.POST.get('search')
        view_law = Add_law.objects.filter(law_section=search.upper())
        print(view_law)
    return render(request, 'view_law.html', {'view_law': view_law})


def index(request):
    request.session['id'] = request.session.get('id')
    return render(request, 'index.html')


def guest(request):
    Lawyers = Lawyer_Profile.objects.all()
    return render(request, 'guest.html', {'lawyer': Lawyers})


def edit_user_profile(request):
    user = User.objects.get(id=request.user.id)
    print(user.id)
    profile = Complete_Profile.objects.get(user=user.id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip = request.POST.get('zip')
        mobile = request.POST.get('mobile')
        print(first_name, email,image,address,city,country,zip,mobile)
        user.first_name = first_name
        user.email = email
        user.username = email
        profile.image = image
        profile.address = address
        profile.city = city
        profile.country = country
        profile.zip = zip
        profile.mobile = mobile
        profile.save()
        user.save()
        return redirect(view_user_profile)
    return render(request, 'edit_user_profile.html', {'profile': profile, 'user': user})


def view_user_profile(request):
    user = User.objects.get(id=request.user.id)
    print(request.user.id)
    viewuser = Complete_Profile.objects.get(user=user)


    return render(request, 'view_user_profile.html', {'viewuser': viewuser})


# from django.shortcuts import redirect, render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from directs.models import Message
# from django.contrib.auth.models import User
# from authy.models import Profile
# from django.db.models import Q
# from django.core.paginator import Paginator


# def inbox(request):
#     user = request.user
#     messages = Contact_lawyer.get_message(user=request.user)
#     active_direct = None
#     directs = None
#     profile = get_object_or_404(User, user=user)
#
#     if messages:
#         message = messages[0]
#         active_direct = message['user'].username
#         directs = Contact_lawyer.objects.filter(user=request.user, reciepient=message['user'])
#         directs.update(is_read=True)
#
#         for message in messages:
#             if message['user'].username == active_direct:
#                 message['unread'] = 0
#     context = {
#         'directs':directs,
#         'messages': messages,
#         'active_direct': active_direct,
#         'profile': profile,
#     }
#     return render(request, 'directs/direct.html', context)


def Directs(request):
    lid = request.GET.get('id')
    print(lid)
    # print("lawyer=", lawyer)
    user = User.objects.get(id=lid)
    messages = Contact_lawyer.get_message(user=user)
    print(messages)
    active_direct = user.username
    directs = Contact_lawyer.objects.filter(user=user, reciepient=user)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == user.username:
            message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'contact_lawyer.html', context)


def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')
    print(body)

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Contact_lawyer.sender_message(from_user, to_user, body)
        return redirect('message')


# def NewConversation(request, username):
#     from_user = request.user
#     body = ''
#     try:
#         to_user = User.objects.get(username=username)
#     except Exception as e:
#         return redirect('search-users')
#     if from_user != to_user:
#         Contact_lawyer.sender_message(from_user, to_user, body)
#     return redirect('message')
def signout(request):
    return redirect(guest)
