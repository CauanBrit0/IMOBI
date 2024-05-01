from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib import auth


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/plataforma/')
        return render(request,'login.html')
    
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('senha')

        if len(username.strip()) == 0 or len(password.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos em branco.')
            return redirect('/auth/login/')
        
        usuario = auth.authenticate(request,username=username, password=password)
        try:
            if usuario:
                auth.login(request,usuario)
                return redirect('/plataforma/')
            
            else:
                messages.add_message(request, constants.ERROR,'Credenciais inválidas.')
                return redirect('/auth/login/')
            
        except:
            messages.add_message(request, constants.ERROR,'Erro interno do sistema.')
            return redirect('/auth/login/')

def cadastro(request):
    if request.method =="GET":
        if request.user.is_authenticated:
            return redirect('/plataforma/')
        return render(request,'cadastro.html')
    
    if request.method=="POST":
        username=  request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')

        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
            return redirect('/auth/cadastro')
        
        if len(password.strip()) < 8 or len(password.strip()) > 10:
            messages.add_message(request,constants.ERROR,'Digite uma senha com no minímo 8 digitos e no máximo 10 digitos.')
            return redirect('/auth/cadastro')
        
    
        email = User.objects.filter(email = email)

        if User.objects.filter(username = username).exists():
            messages.add_message(request,constants.ERROR,'Nome de Usuário já cadastrado. Tente realizar o login.')
            return redirect('/auth/cadastro')
        
        if email.exists():
            messages.add_message(request,constants.ERROR,'Email já cadastrado. Tente realizar o login.')
            return redirect('/auth/cadastro')
        
        if len(username.strip()) < 4:
            messages.add_message(request,constants.ERROR,'Digite um nome de usuário maior que 4 digitos.')
            return redirect('/auth/cadastro')
        
        try:
            usuario = User.objects.create_user(username=username, email=email, password=password)
            usuario.save()
            messages.add_message(request,constants.SUCCESS,'Cadastro realizado com sucesso! Faça seu Login!')
            return redirect('/auth/login/')
        
        except:
            messages.add_message(request,constants.ERROR,'Erro interno do sistema.')
            return redirect('/auth/cadastro')




def sair(request):
    auth.logout(request)
    return redirect('/auth/login/')