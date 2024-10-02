from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth import login, logout, authenticate
from .models import Lawyer_Profile,Reply
from user.models import Contact_lawyer,Complete_Profile
from Admin.models import Add_court,Add_law
from user.views import guest, Thread, ChatMessage
import random

# Create your views here.
def signup(request):
    if request.method == 'POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        username = request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'E-mail already exists!!!')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists!!!')
            else:
                user = User.objects.create_user(first_name=firstname,last_name=lastname, email=email, username=username, password=password1)
                user.save()
                user_login = authenticate(request, username=email, password=password1)
                if user_login is not None:
                    login(request, user_login)
                print('user saved')
                return redirect(lawyerprofile)
        else:
            messages.warning(request, 'password mismatch')
            print('password mismatch')
        
    return render(request, 'signup.html')

def lawyerprofile(request):
    if request.method=='POST':
        address=request.POST.get('address')
        license=request.POST.get('license')
        city = request.POST.get('city')
        aop = request.POST.get('aop')
        cop = request.POST.get('cop')
        description = request.POST.get('description')
        image=request.FILES['profile_img']
        print(request.user.id)
        user = User.objects.last()
        lawyer_profile = Lawyer_Profile.objects.create(user= user,license_no=license, image=image,address=address, city=city, aop=aop, description=description, cop=cop)
        lawyer_profile.save()
        print('user saved')
        return redirect(signin)
    return render(request,"lawyer_profile.html")


def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password1')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            messages.warning(request,'Account not found')
    return render(request,"signin.html")



def home(request):
    user = User.objects.get(id=request.user.id)
    lawyer = Lawyer_Profile.objects.get(user=user)
    if not lawyer.status:
        messages.error(request,"Your Application is Pending for Approval !")
    return render(request, 'home.html')


def view_clients(request):
    lawyer=User.objects.get(id=request.user.id)
    thread = Thread.objects.filter(second_person=lawyer)
    return render(request, 'view_customers.html',{'clients':thread})


def lawyer_view_court(request):
    view_court = Add_court.objects.all()
    return render(request, 'lawyer_view_court.html', {'view_court': view_court})


def view_lawyer_profile(request):
    user =  User.objects.get(id=request.user.id)
    viewlawyer = Lawyer_Profile.objects.get(user=user)
    print(viewlawyer.aop)
    return render(request, 'view_lawyer_profile.html', {'viewlawyer': viewlawyer})


def contact_clients(request):
    threads = None
    c_id = request.GET.get('id')
    print(c_id)
    l_id = request.user.id
    c = User.objects.get(id=c_id)
    l = User.objects.get(id=l_id)
    prof = Complete_Profile.objects.get(user=c)
    thread = Thread.objects.get(first_person=c,second_person=l)
    print(thread)
    unread_messages = ChatMessage.objects.filter(thread=thread, user=c_id, read=False)
    print(unread_messages)
    for msg in unread_messages:
        msg.read = True
        msg.save()
    if thread is not None:
        threads = Thread.objects.filter(pk=thread.pk).prefetch_related('chatmessage_thread').order_by('timestamp')
    return render(request, 'contact_clients.html', {'id': c_id,
                                                    'Threads': threads, 'to_user': c,'p':prof,
                                                    'logged_in_user_id': l_id})


def lawyer_view_laws(request):
    view_law = Add_law.objects.all()
    if request.method == "POST":
        search = request.POST.get('search')
        view_law = Add_law.objects.filter(law_section=search.upper())
        print(view_law)
    return render(request, 'lawyer_view_laws.html', {'view_law': view_law})


def forgotp(request):
    if request.method=='POST':
        email=request.POST.get('email')
        print(email)
        try:
            if User.objects.get(email = email):
                def generate_otp():
                    return random.randint(100000,999999)
                otp=generate_otp()
                print("generated otp:",otp)
                time=datetime.now()

                send_mail('forget password',f'One Time Password to verify your Email is :{otp}',settings.EMAIL_HOST_USER,[email])
                request.session['otp']=otp
                request.session['time']=str(time)
                request.session['email']=email
                return redirect(resetp)

        except:
            messages.warning(request,'E-mail does not exists')
    return render(request, 'forgot.html')


def resetp(request):
    otp = request.session.get("otp")
    email = request.session.get("email")
    time=request.session.get('time')
    send_time=datetime.strptime(time,"%Y-%m-%d %H:%M:%S.%f")
    current_time=datetime.now()
    time_difference=current_time-send_time
    print(type(otp))
    if request.method=='POST':
        confirm_otp=int(request.POST.get('otp'))
        new_password=request.POST.get('password1')
        confirm_password=request.POST.get('password2')
        if otp == confirm_otp and new_password == confirm_password and time_difference <= timedelta(minutes=5):
            user=User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            user_login=authenticate(request,username=user.username,password=new_password)
            if user_login is not None:
                login(request,user_login)
                return redirect(home)
            else:
                messages.error(request,'account not found')
        elif otp != confirm_otp:
            messages.error(request,'Invalid otp')
        elif new_password != confirm_password:
            messages.error(request,'password mismatch')
        elif otp==confirm_otp and time_difference >= timedelta(minutes=5):
            messages.error(request,'time exceeded')

    return render(request, 'resetp.html')

def user_requests(request,replied = None):
    id=request.GET.get('id')
    cid = User.objects.get(id=id)
    print(cid)
    lid= Lawyer_Profile.objects.get(user=request.user.id)
    lawyer= User.objects.get(id=lid.user.id)
    print(lawyer.id)
    contact=Contact_lawyer.objects.filter(user=cid,lawyer=lid)
    replied = Reply.objects.filter(user=cid)
    print(replied)
    if request.method=='POST':
        reply=request.POST.get('reply')
        print(reply)
        reply=Reply.objects.create(user=cid,lawyer=lid,reply=reply)
        reply.save()
        replied=Reply.objects.filter(user=cid)
        print(replied)
        return redirect(user_requests)
    return render(request, 'user_requests.html',{'contact':contact,'replied':replied})


def edit_lawyer_profile(request):
    user = User.objects.get(id=request.user.id)
    print(user.id)
    profile = Lawyer_Profile.objects.get(user=user.id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        city = request.POST.get('city')
        license = request.POST.get('license')
        aop = request.POST.get('aop')
        desc = request.POST.get('desc')
        cop = request.POST.get('cop')
        print(first_name, email,image,address,city,aop,desc,cop)
        user.first_name = first_name
        user.email = email
        profile.image = image
        profile.address = address
        profile.license_no = license
        profile.city = city
        profile.aop = aop
        profile.cop = cop
        profile.desc = desc
        profile.save()
        user.save()
        return redirect(view_lawyer_profile)
    return render(request,'edit_lawyer_profile.html',{'profile':profile})


def signout(request):
    return redirect(guest)