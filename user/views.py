from .forms import *
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User, Group
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


# for email
from django.core.mail import send_mail
from django.template.loader import render_to_string

# for payment

import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    orgform = OrganizationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        orgform = OrganizationForm(request.POST)
        if form.is_valid() and orgform.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = Group.objects.get(name='organizations')
            user.groups.add(group)
            org = orgform.save(commit=False)
            org.user = user
            org.orgname = user.username
            org.orgemail = user.email
            org.save()
            return redirect('/thankyouuser')
    context = {'form': form, 'orgform': orgform}
    return render(request, 'user/registration.html', context)


@login_required(login_url='/login')
@unauthenticated_user
def thankyouuser(request):
    return render(request, 'user/thankyouuser.html')


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin', pk=user.id)
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'user/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/login')


def home(request):
    events = Event.objects.all().order_by('-date_created')

    context = {'events': events}
    return render(request, 'user/homepage.html', context)


def about(request):
    return render(request, 'user/about.html')


def gallary(request):
    images = Gallary.objects.all()
    context = {'images': images}
    return render(request, 'user/gallary.html', context)


@login_required(login_url='/login')
@admin_only
def upgallary(request):
    if request.method == 'POST':
        Gallary.objects.create(image=request.FILES.get('image'))
        return redirect('admin', pk=request.user.id)


def allevents(request):
    events = Event.objects.all().order_by('-date_created')
    p = Paginator(events, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'events': page}
    return render(request, 'user/viewevents.html', context)


def moneyevents(request):
    events = Event.objects.filter(event_type='MY')
    context = {'events': events}
    return render(request, 'user/viewevents.html', context)


def bevents(request):
    events = Event.objects.filter(event_type='BL')
    context = {'events': events}
    return render(request, 'user/viewevents.html', context)


def bothevents(request):
    events = Event.objects.filter(event_type='BH')
    context = {'events': events}
    return render(request, 'user/viewevents.html', context)


def donatemoney(request, pk):
    event = Event.objects.get(id=pk)
    form = MoneyDonatorForm(
        initial={'event': event.id, 'organization': event.organization_name.id})
    if request.method == 'POST':
        form = MoneyDonatorForm(request.POST)
        if form.is_valid():
            donator = form.save()
            return redirect('pay', pk=donator.pk)
    context = {'form': form}
    return render(request, 'user/donatemoney.html', context)


def payment(request, pk):
    info = MoneyDonatorInfo.objects.get(id=pk)
    store_id = 'spere5f3aeaafa6b1d'
    api_key = 'spere5f3aeaafa6b1d@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True,
                            sslc_store_id=store_id, sslc_store_pass=api_key)

    status_url = request.build_absolute_uri(
        reverse('status', kwargs={'pk': info.id}))

    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)

    donator = MoneyDonatorInfo.objects.get(id=pk)
    donate_amount = donator.amount
    mypayment.set_product_integration(total_amount=Decimal(donate_amount), currency='BDT', product_category='donation',
                                      product_name='Donate Money', num_of_item=1, shipping_method='None', product_profile='None')

    mypayment.set_customer_info(name=donator.name, email=donator.email, address1='demo address 1',
                                address2='demo address 2', city='Dhaka', postcode='1200', country='Bangladesh', phone=donator.contact)

    mypayment.set_shipping_info(shipping_to=donator.name, address='demo address',
                                city='Dhaka', postcode='1200', country='Bangladesh')

    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request, pk):
    info = MoneyDonatorInfo.objects.get(id=pk)
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        print(payment_data)
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            success_amount = payment_data['amount']
            info.val_id = val_id
            info.tran_id = tran_id
            info.status = status
            info.success_amount = success_amount
            info.save()
            event = info.event
            donators = event.moneydonatorinfo_set.all()
            get_total = donators.aggregate(Sum('success_amount'))
            raised = get_total['success_amount__sum']
            event.raised = raised
            event.save()
            messages.success(
                request, 'Your Donation has been Completed Successfully')
        elif status == 'FAILED':
            messages.warning(
                request, 'Your Donation has been Failed, Please try again')
    context = {'status': status}
    return render(request, 'user/thankyou.html', context)


def donatebelongings(request, pk):
    event = Event.objects.get(id=pk)
    form = BelongingsDonatorForm(
        initial={'event': event.id, 'organization': event.organization_name.id})
    if request.method == 'POST':
        form = BelongingsDonatorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'user/donatebelongings.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles='organizations')
def orghome(request, pk):
    organization = Organization.objects.get(id=pk)
    events = organization.event_set.all()
    mdonators = organization.moneydonatorinfo_set.all()
    bdonators = organization.belongingsdonatorinfo_set.all()
    context = {'events': events,
               'mdonators': mdonators, 'bdonators': bdonators}
    return render(request, 'user/organization.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles='organizations')
def adminpickup(request, pk):
    req = BelongingsDonatorInfo.objects.get(id=pk)
    req.is_submitted = True
    req.save()
    AdminPickup.objects.create(event=req.event, name=req.name, email=req.email, contact=req.contact,
                               opinion=req.opinion, address=req.address, organization=request.user.organization, image=req.image)
    return redirect('back', pk=request.user.organization.id)


@login_required(login_url='/login')
@admin_only
def adminhome(request, pk):
    user = User.objects.get(id=pk)
    events = Event.objects.all().order_by('-date_created')
    gallarys = Gallary.objects.all()
    donations = AdminPickup.objects.all()
    #inactive_users = User.objects.filter(is_active=False)
    inactive_users = Organization.objects.all().order_by('-orgdate')
    context = {'user': user, 'inactive_users': inactive_users,
               'events': events, 'donations': donations, 'gallarys': gallarys}
    return render(request, 'user/admin.html', context)


@login_required(login_url='/login')
@admin_only
def apporg(request, pk):
    org = User.objects.get(id=pk)
    if request.method == 'POST':
        org.is_active = True
        org.save()

        html_message = render_to_string('user/email.html', {'org': org})

        # send mail
        send_mail(
            'Verified',  # subject
            'Your Information is verified. You can Log in to Spread Smile Now',  # message
            'maiesha35-177@diu.edu.bd',  # from email
            ['syeda35-174@diu.edu.bd'],  # to email
            html_message=html_message,
            fail_silently=False,
        )
    return redirect('admin', pk=request.user.id)


@login_required(login_url='/login')
@admin_only
def deapporg(request, pk):
    org = User.objects.get(id=pk)
    if request.method == 'POST':
        org.is_active = False
        org.save()
    return redirect('admin', pk=request.user.id)


def singleevent(request, pk):
    event = Event.objects.get(id=pk)
    donators = event.moneydonatorinfo_set.filter(status='VALID')
    bdonator = event.belongingsdonatorinfo_set.all()

    donators_count = donators.count()
    if(donators_count == 0):
        raised = 0
        raised_p = 0
        context = {'event': event,
                   'donators_count': donators_count, 'raised': raised, 'raised_p': raised_p, 'bdonator': bdonator}
        return render(request, 'user/details.html', context)
    else:
        get_total = donators.aggregate(Sum('success_amount'))
        raised = get_total['success_amount__sum']
        raised_p = (get_total['success_amount__sum']/event.goal)*100
        context = {'event': event,
                   'donators_count': donators_count, 'raised': raised, 'raised_p': raised_p, 'bdonator': bdonator}
        return render(request, 'user/details.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles='organizations')
def create_event(request):
    form = EventForm(
        initial={'organization_name': request.user.organization.id})
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('back', pk=request.user.organization.id)

    context = {'form': form}
    return render(request, 'user/create_event.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles='organizations')
def update_event(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('back', pk=request.user.organization.id)
    context = {'form': form}
    return render(request, 'user/create_event.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles='organizations')
def delete_event(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        bar = event.organization_name.id
        return redirect('back', pk=bar)
    context = {'event': event}
    return render(request, 'user/delete_event.html', context)
