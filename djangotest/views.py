from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from djangotest.models import Profile,Comment,Room,RoomType,Image
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return render(request, 'homepage.html')
# Create your views here.

def signin(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        userName=request.POST.get('username')
        userPassword=request.POST.get('password')
        user=authenticate(username=userName,password=userPassword)
        if user == None:
            return render(request,'login.html',{'message':'Invalid Username or Password'})
        else:
            login(request,user)
            return HttpResponseRedirect('/profile')
    else:
        return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        try:
            checkUser = User.objects.get(username=username)
        except User.DoesNotExist:
            checkUser=None
        if not checkUser is None:
            return render(request,'signup.html',{'message':'Username Already taken'})

        try:
            checkUser = User.objects.get(email=email)
        except User.DoesNotExist:
            checkUser=None
        if not checkUser is None:
            return render(request,'signup.html',{'message':'An account with this Email already exists'})

        user=User.objects.create_user(first_name=name,username=username,email=email,password=password)
        if image is not None:
            user.profile.profilePicture=image
        user.save()
        login(request,user)
        return redirect('profile')
        #return HttpResponseRedirect('/profile')
    else:
        return render(request, 'signup.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method=="POST":
        newName=request.POST.get('name')
        newEmail=request.POST.get('email')
        newImage=request.FILES.get('image')
        user = request.user
        user.email=newEmail
        user.first_name=newName
        if newImage is not None:
            user.profile.profilePicture = newImage
        user.save()
        return HttpResponseRedirect('/profile')
    else:
        return render(request, 'profile.html')

def feedback(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        customerComment=request.POST.get('comment')
        user=request.user
        comment=Comment(comment=customerComment,user=user)
        comment.save()
        allComments=getComments()
        context={'comments':allComments}
        return render(request, 'feedback.html', context)
    allComments=getComments
    user=request.user
    context = {'comments': allComments}
    return render(request, 'feedback.html', context)

def getComments():
    comments=Comment.objects.all()
    return comments

def rating(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        customerRating=request.POST.get('rating')
        user=request.user
        user.profile.rating=customerRating
        user.save()
        return HttpResponseRedirect('/profile')

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        user=request.user
        newPassword=request.POST.get('password')
        user.set_password(newPassword)
        user.save()
        update_session_auth_hash(request, user)
        return redirect('profile')


def test(request):
    if request.method=="POST":
        to=request.POST.get('to')
        fro = request.POST.get('from')
        print('')

    return render(request,'test.html')

def rooms(request):
    allRooms=RoomType.objects.all()
    allImages=Image.objects.all()
    context={'rooms':allRooms,'images':allImages}
    return render(request,'rooms.html',context)




