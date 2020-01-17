from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Job
import bcrypt

def index(request):
    print('*'*70)
    print("index route reached.")
    print('*'*70)
    return render(request, 'main/index.html')

def validate(request):
    print('*'*70)
    print("validaiton route reached.")
    print(request.POST)
    print('*'*70)
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/handy')
    else:
        pwh = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        User.objects.create(first=request.POST['first'], last=request.POST['last'], email=request.POST['email'], password=pwh)
    return redirect('/handy')


def login(request):
    print("*"*70)
    print("login method reached. Info recieved is below:")
    print(request.POST)
    print("*"*70)
    errors=User.objects.loginVal(request.POST)
    print("*"*70)
    print("Made it to apps/login views.login.")
    print("*"*70)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        logged_user=user[0]
        request.session['id']= logged_user.id
        return redirect('/handy/success')
    print("*"*70)
    print("recieved this info from HTML form")
    print(request.POST)
    print("*"*70)
    return redirect ("/")

def success(request):
    context ={
        "user":User.objects.get(id=request.session['id'])
    }
    print('*'*70)
    print("sucess route reached.")
    print('*'*70)
    if 'id' not in request.session:
        messages.error(request, "You are not currently logged in. Please sign in.")
        return redirect('/handy')
    else: 
        return render(request, 'main/dashboard.html', context)

def logout(request):
    print("*"*70)
    print("logout request reached")
    print("*"*70)
    request.session.clear()
    print(request.session)
    return redirect ('/')

def dashboard(request):
    print("*"*70)
    print("dashboard method reached")
    print("*"*70)
    context = {
        "user":User.objects.get(id=request.session['id']),
        "all_users":User.objects.all(),
        "jobs":Job.objects.filter(user=User.objects.get(id=request.session['id'])),
        "others_jobs":Job.objects.exclude(user=User.objects.get(id=request.session['id'])),
        "all_jobs":Job.objects.all()
        
        }
    return render(request, "main/dashboard.html", context)

def job_page(request):
    context = {
        "specific_user":User.objects.get(id=request.session['id'])
    }
    print("*"*70)
    print("job_page method reached")
    print("*"*70)
    return render(request, "main/jobNew.html", context)

def newJob(request):
    print("*"*70)
    print(request.POST)
    print("newJob method reached")
    print("*"*70)

    if request.method =="GET":
        return render(request, "main/jobNew.html")

    elif request.method =="POST":
        errors = Job.objects.job_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect(f'/handy/newJob')

    else:
        Job.objects.create(title=request.POST['title'], description=request.POST['desc'], location=request.POST['loc'], user=User.objects.get(id=request.session['id']))
        return redirect("/handy/dashboard")

def detail(request, id):
    context ={
        "user":User.objects.last(),
        "job":Job.objects.get(id=id)
    }
    print('*'*70)
    print("reached detail method")
    print(request.POST)
    print('*'*70)
    return render(request, "main/jobDetail.html", context)


def destroy(request, id):
    Job.objects.get(id=id).delete()
    return redirect ("/handy/dashboard")

def jobEdit(request, id):
    context ={
        "job":Job.objects.get(id=id),
        "jobss":Job.objects.all()
        }
    if request.method =="GET":
        return render(request, "main/jobEdit.html", context)

    elif request.method =="POST":
        errors = Job.objects.job_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect(f'/handy/{id}/edit')

    else:
        j=Job.objects.get(id=id)
        j.title=request.POST["title"]
        j.description=request.POST["desc"]
        j.location=request.POST["loc"]
        j.save()
        return redirect(f'/handy/dashboard')
