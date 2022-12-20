from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User, Transactions
from django.contrib import messages


def isfloat(num):
    try:
        float(num)
        return True
    except:
        return False 

def index(request):
    if request.method == 'POST':
        form = request.POST
        print(form)
        name = form['name']
        password = form['password']
        users = User.objects.filter(name=name).values()
        print(users)
        if users[0]['password'] == password:
            return redirect('/'+str(users[0]['id']))
    return render(request,'index.html')

def create(request):
    if request.method == 'POST':
        form = request.POST
        user = User()
        user.name = form['name']
        user.password = form['password']
        user.balance = float(form['balance'])
        user.pin = int(form['pin'])
        users = User.objects.filter(name=user.name).values()
        all_users = User.objects.all()
        last_user = all_users[len(all_users)-1]
        print(last_user.id)
        if not users and user.name != 'admin' and user.password != '' and user.balance!=0 and user.pin!=0:
            user.save()
            u = User.objects.get(name=user.name)
            # id= user1[0]['id']
            # u=User.objects.get(id=id)
            print(u)
            tran = Transactions()
            # user = User.objects.get(id=id)
            tran.user_id = u
            tran.transaction_type = 'credit'
            tran.amount = float(user.balance)
            tran.balance = float(user.balance)
            tran.save()
            messages.add_message(request, messages.INFO, 'User added successfully')
            # return redirect('/tran/'+str(u['id']))
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Incorrect Input')

    return render(request,'create.html')

# def tran(request,id):


def dashboard(request,id):
    users = User.objects.filter(id=id).values()
    trans = Transactions.objects.filter(user_id=id).values()
    context = {'users': users, 'trans':trans}
    return render(request,'indi_usr.html',context)

def credit(request,id):
    cred = request.POST
    amount = cred['credit']
    pin = cred['pin']
    user = User.objects.get(id=id)
    if isfloat(amount) and pin.isdigit():
        if user.pin == int(pin):
            user.balance =  float(user.balance) + float(amount)
            user.save()
            tran = Transactions()
            tran.user_id = user
            tran.transaction_type = 'credit'
            tran.amount = float(amount)
            tran.balance = float(user.balance)
            print(tran)
            tran.save()
            messages.add_message(request, messages.INFO, 'Amount Credited Successfully')
        else:
            messages.add_message(request, messages.INFO, 'Incorrect PIN')

    else:
        messages.add_message(request, messages.INFO, 'Incorrect Input')
    return redirect('/'+id)

    # users[0]['balance'] = float(users[0]['balance']) + float(amount)
    
def debit(request,id):
    deb = request.POST
    amount = deb['debit']
    pin = deb['pin']

    user = User.objects.get(id=id)
    if isfloat(amount) and pin.isdigit():
        user.balance =  float(user.balance) - float(amount)
        if user.balance >=0:
            if user.pin == int(pin):
                user.save()
                tran = Transactions()
                tran.user_id = user
                tran.transaction_type = 'debit'
                tran.amount = float(amount)
                tran.balance = float(user.balance)
                tran.save()
                messages.add_message(request, messages.INFO, 'Amount Debited Successfully')
            else:
                messages.add_message(request, messages.INFO, 'Incorrect PIN')
        else:
            messages.add_message(request, messages.INFO, 'Insufficient Balance')

    else:
        messages.add_message(request, messages.INFO, 'Incorrect Input')
    return redirect('/'+id)

def logout(request):
    return redirect('/')
