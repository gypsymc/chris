from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
    return render(request,'main/index.html')

def dashboard(request):

    context = {
    "user": User.objects.get(id=request.session["user_id"]),
    "quotes": Quote.objects.all(),
    "favorites":Favorite.objects.filter(user__id=request.session["user_id"])
    }
    return render(request,'main/dashboard.html',context)

def user_info(request, id):
    context = {
    "user":User.objects.get(id=id),
    "posts":Quote.objects.all().filter(user=id)
    }
    return render(request,'main/userinfo.html',context)

def register(request):
    if len(request.POST.get('name')) == 0:
        messages.warning(request, 'Enter Valid Information')
        return redirect('/')
    if len(request.POST.get('alias')) == 0:
        messages.warning(request, 'Enter Valid Information')
        return redirect('/')
    if len(request.POST.get('email')) == 0:
        messages.warning(request, 'Enter Valid Information')
        return redirect('/')
    if len(request.POST.get('password')) <8:
        messages.warning(request, 'Enter Valid Information')
        return redirect('/')
    if request.POST.get('password') != request.POST.get('password_confirmation'):
        messages.warning(request, 'Enter Valid Information')
        return redirect('/')
    else:
        user = User.objects.create(
        name = request.POST.get('name'),
        alias = request.POST.get('alias'),
        email = request.POST.get('email'),
        password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt()),
        date_of_birth = request.POST.get('date')
        )
        request.session['user_id']=user.id
        return redirect('/dashboard')

def login(request):
    if request.method == 'POST':
        login = User.objects.login_user(request.POST)
        if login:
            request.session["user_id"] = login[1].id
            return redirect ("/dashboard")
        else:
            messages.error(request,'Invalid')
    return redirect("/")

def add_quote(request):
        if len(request.POST.get("author"))<4:
            messages.warning(request, "Please enter valid Author")
            return redirect('/dashboard')
        elif len(request.POST.get("message"))<11:
            messages.warning(request, "Please enter Valid Message")
            return redirect('/dashboard')
        else:
            Quote.objects.create(
            author = request.POST.get('author'),
            message = request.POST.get('message'),
            user = User.objects.get(id=request.session['user_id']),
            )
            return redirect('/dashboard')

def favorites(request, id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Quote.objects.get(id=id)
    favorite = Favorite.objects.create(
    quote = quote,
    user = user
    )
    request.session["favs"]=favorite.quote.id
    return redirect ("/dashboard")

def remove(request, id):
    Favorite.objects.filter(quote__id=id).delete()
    print "deleting"
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")
