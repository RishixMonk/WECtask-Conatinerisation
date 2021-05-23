from django.shortcuts import render, redirect
from django.urls import reverse
from base.models import Club, Request, Item
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import *

from math import ceil
# Create your views here.


def index(request):

    clubs = Club.objects.all()
    context = {'clubs': clubs}
    return render(request, 'index.html', context)


def club_add(request):

    #Adding a new club
    form = ClubForm()
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'club_add.html', context)


def item_add(request, pk):

    club = Club.objects.get(id=pk)
    initial = {'club':club}
    #Adding a new item
    form = ItemForm(initial=initial)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('items_view', args = [pk]))
    context = {'club':club, 'form':form}
    return render(request, 'item_add.html', context)


def club_view(request, pk):
    # Display all users belonging to that club
    club = Club.objects.get(id=pk)
    members = club.users.all()
    context = {'club': club, 'members': members}

    return render(request, 'club_view.html', context)

def items_view(request, pk):

    #Display all items belonging to that club as a carousel of cards
    club = Club.objects.get(id=pk)
    items = club.item_set.all()
    all_items = []
    n = len(items)
    nSlides = n//4 + ceil(n/4-n//4) #logic for displaying slides
    all_items.append([items, range(1, nSlides), nSlides])

    #Display all requests pertaining to that club
    reqs = club.request_set.all()

    context = {'club':club, 'all_items':all_items, 'reqs':reqs}
    return render(request, 'items_view.html', context)

def request_approve(request, request_id):
    #Approve the request if there is sufficient quantity available
    req = Request.objects.get(id = request_id)
    club_id = req.item.club.id 
    if req.item.qty - req.qty >= 0:
        req.item.qty -= req.qty
        req.status = 'Approved'
        req.item.save()
        req.save()
        messages.success(request, 'Request approved successfully!')
        return redirect(reverse('items_view', args = [club_id]))
    else:
        messages.info(request, 'Request cannot be approved - Insufficient Quantity')
        return redirect(reverse('items_view', args = [club_id]))

def request_reject(request, request_id):
    req = Request.objects.get(id = request_id)
    club_id = req.item.club.id 
    req.status = 'Rejected'
    req.save()
    messages.info(request, 'Request rejected successfully!')
    return redirect(reverse('items_view', args = [club_id]))