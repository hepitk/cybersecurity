from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Account, Message
from django.db.models import Q
import json

def transfer(sender, to, amount):
    if amount > 0:
        user1 = Account.objects.get(user=sender)
        user2 = Account.objects.get(user=to)
        if user1.balance >= amount:
            user1.balance -= amount
            user2.balance += amount
            user1.save()
            user2.save()

@login_required
@csrf_exempt
def transferView(request):
    if request.method == 'GET':        
        amount = int(request.GET.get('amount'))
        if amount > 0:
            to = User.objects.get(username=request.GET.get('to'))
            sender = User.objects.get(username=request.GET.get('user_id'))
            transfer (sender, to, amount)
            target = User.objects.get(username=request.GET.get('to'))
            Message.objects.create(source=sender, target=target, content=request.GET.get('content'), amount=amount)
    
    return redirect('/')

@login_required
def homePageView(request):
    accounts = Account.objects.exclude(user_id=request.user.id)
    messages = Message.objects.all()
    return render(request, 'pages/index.html', {'accounts': accounts, 'msgs': messages})
