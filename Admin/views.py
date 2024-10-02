from django.shortcuts import render, redirect
from .models import Add_court, Add_law
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from lawyer.models import *
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect(admin_home)
        else:
            messages.warning(request, 'Account not found')
    return render(request,'admin_login.html')


def admin_home(request):
    return render(request,'admin_home.html')


def addcourt(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        cloc = request.POST.get('cloc')
        jurisdiction = request.POST.get('jurisdiction')
        year = request.POST.get('year')
        chiefjustice = request.POST.get('chiefjustice')
        noj = request.POST.get('noj')
        image = request.FILES['court_img']
        print(cname, cloc, year, image)
        addcourt = Add_court.objects.create(cname=cname, cloc=cloc, jurisdiction=jurisdiction, year=year,
                                            chiefjustice=chiefjustice, noj=noj, image=image)
        addcourt.save()
        print('court added')
        return redirect(view_all_court)
    return render(request, 'add_court.html')


def view_all_lawyers(request):
    lawyers = Lawyer_Profile.objects.all()
    return render(request, 'view_all_lawyers.html', {'lawyers': lawyers})


def approve_lawyer(request):
    lid = request.GET.get('id')
    action = Lawyer_Profile.objects.get(id=lid)
    action.status = True
    action.save()
    return redirect(view_all_lawyers)


def reject_lawyer(request):
    lid = request.GET.get('id')
    action = Lawyer_Profile.objects.get(id=lid)
    action1 = User.objects.get(id=action.user.id)
    action.delete()
    action1.delete()
    return redirect(view_all_lawyers)


def view_all_court(request):
    view_all_court = Add_court.objects.all()
    return render(request, 'view_all_court.html', {'view_all_court': view_all_court})


def edit_court(request):
    cid = request.GET.get('id')
    print(cid)
    edit_court = Add_court.objects.get(id=cid)
    print(edit_court)
    if request.method == 'POST':
        cname = request.POST.get('cname')
        cloc = request.POST.get('cloc')
        jurisdiction = request.POST.get('jurisdiction')
        year = request.POST.get('year')
        chiefjustice = request.POST.get('chiefjustice')
        noj = request.POST.get('noj')
        image = request.FILES.get('court_img')
        print(image)
        edit_court.cname = cname
        edit_court.cloc = cloc
        edit_court.jurisdiction = jurisdiction
        edit_court.year = year
        edit_court.chiefjustice = chiefjustice
        edit_court.noj = noj
        edit_court.image = image
        edit_court.save()
        return redirect(view_all_court)
    return render(request, 'edit_court.html', {'edit_court': edit_court})


def delete_court(request):
    cid = request.GET.get('id')
    delete_court = Add_court.objects.get(id=cid)
    delete_court.delete()
    return redirect(view_all_court)


def addlaw(request):
    if request.method == 'POST':
        law_section = request.POST.get('law_section')
        description = request.POST.get('description')
        category = request.POST.get('category')
        penalty = request.POST.get('penalty')
        amendment_details = request.POST.get('amendment_details')
        year_enacted = request.POST.get('year_enacted')
        provisions = request.POST.get('provisions')
        applicability = request.POST.get('applicability')
        addlaw = Add_law.objects.create(law_section=law_section, description=description, category=category,
                                        penalty=penalty, amendment_details=amendment_details, year_enacted=year_enacted,
                                        provisions=provisions, applicability=applicability)
        addlaw.save()
        print('law added')
        return redirect(view_all_law)
    return render(request, 'add_law.html')


def view_all_law(request):
    view_all_law = Add_law.objects.all()
    return render(request, 'view_all_law.html', {'view_all_law': view_all_law})


def edit_law(request):
    lid = request.GET.get('id')
    print(lid)
    edit_law = Add_law.objects.get(id=lid)
    print(edit_law)
    if request.method == 'POST':
        law_section = request.POST.get('law_section')
        description = request.POST.get('description')
        penalty = request.POST.get('penalty')
        category = request.POST.get('category')
        amendment_details = request.POST.get('amendment_details')
        provisions = request.POST.get('provisions')
        year_enacted = request.POST.get('year_enacted')
        applicability = request.POST.get('applicability')
        edit_law.law_section = law_section
        edit_law.description = description
        edit_law.penalty = penalty
        edit_law.year = category
        edit_law.amendment_details = amendment_details
        edit_law.provisions = provisions
        edit_law.year_enacted = year_enacted
        edit_law.applicability = applicability
        edit_law.save()
        return redirect(view_all_law)
    return render(request, 'edit_law.html', {'edit_law': edit_law})


def delete_law(request):
    lid = request.GET.get('id')
    delete_law = Add_law.objects.get(id=lid)
    delete_law.delete()
    return redirect(view_all_law)


def admin_logout(request):
    logout(request)
    return redirect(admin_login)