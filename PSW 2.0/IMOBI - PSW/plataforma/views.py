from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Imovei,Cidade,DiasVisita,Imagem, Horario, Visitas

@login_required(login_url='/auth/logar/')
def home(request):
    preco_minimo = request.GET.get('preco_minimo')
    preco_maximo = request.GET.get('preco_maximo')
    cidade = request.GET.get('cidade')
    tipo = request.GET.getlist('tipo')
    cidades = Cidade.objects.all()
    if preco_minimo or preco_maximo or cidade or tipo:
        
        if not preco_minimo:
            preco_minimo = 0
        if not preco_maximo:
            preco_maximo = 999999999
        if not tipo:
            tipo = ['A', 'C']
        
        
        imoveis = Imovei.objects.filter(valor__gte=preco_minimo)\
        .filter(valor__lte=preco_maximo)\
        .filter(tipo_imovel__in=tipo).filter(cidade=cidade)
    else:
        imoveis = Imovei.objects.all()
    
    return render(request, 'home.html', {'imoveis': imoveis, 'cidades': cidades})


def imovel(request, id):
    imovel = get_object_or_404(Imovei, id = id)
    sugestoes = Imovei.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]
    return render(request,'imovel.html',{'imovel':imovel,'sugestoes':sugestoes})


def agendar_visitas(request):
    usuario = request.user
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.get('id_imovel')
    visitas = Visitas(imovel_id = id_imovel, usuario = usuario, dia = dia, horario = horario)
    visitas.save()
    return redirect('/plataforma/agendamentos')



def agendamentos(request):
    visitas = Visitas.objects.filter(usuario = request.user)
    return render(request, 'agendamento.html',{'visitas':visitas})


def cancelar_agendamento(request,id):
    visita = get_object_or_404(Visitas, id=id)
    visita.status = 'C'
    visita.save()
    return redirect('/plataforma/agendamentos')