from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from appMy.models import *
# Create your views here.

def indexPage(request):
    context = {}
    return render(request, 'index.html', context)

def registerPage(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        reply = request.POST.get("reply")
        
        if username and email and password1 and reply:
            if password1 == password2:
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(username=username, email=email, password=password1)
                        user.save()
                        user2 = User.objects.get(username=username)
                        reply = Reply(user=user2, reply=reply)
                        reply.save()
                        messages.success(request, "Kaydınız başarıyla oluşturulmuştur.")
                        return redirect("loginPage")
                    else:
                        messages.warning(request, "Bu mail zaten kullanılıyor!")
                else:
                    messages.warning(request, "Böyle bir kullanıcı adı zaten kullanılıyor!")
            else:
                messages.warning(request, "Şifreler uyuşmuyor!")
        else:
            messages.warning(request, "Bilgiler boş bırakılamaz!")
    context = {}
    return render(request, 'register.html', context)

def loginPage(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request,"Başarıyla giriş yaptınız!")
                return redirect("indexPage")
            else:
                messages.warning(request, "Kullanıcı adı veya parola hatalı!")
        else:
            messages.warning(request, "Hiçbir bilgi boş bırakılamaz!")           
    context = {}
    return render(request, 'login.html', context)

def passwordPage(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        reply = request.POST.get("reply")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if username and reply and password1 and password2:
            if password1 == password2:
                try:
                    user = User.objects.get(username=username)
                    if user.reply.reply == reply:
                        user.set_password(password1)
                        user.save()
                        messages.success(request,"Şifreniz başarıyla değiştirilmiştir.")
                        return redirect("loginPage")
                    else:
                        messages.warning(request, "Gizli yanıtınız yanlış!")
                except:
                    messages.warning(request, "Kullanıcı bulunamadı")
            else:
                messages.warning(request, "Şifreler uyuşmuyor!")
        else:
            messages.warning(request, "Hiçbir kutu boş bırakılamaz")
     
                        
        
    
    context = {}
    return render(request, 'password.html', context)

def logoutPage(request):
    logout(request)
    return redirect("loginPage")
