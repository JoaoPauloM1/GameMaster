from django.shortcuts import render
from games.jogos.jogo_da_memoria import jogo_da_memoria
from games.jogos.forca import forca
from games.jogos.batalha_naval import batalha_naval
from games.jogos.pedra_papel_tesoura import pedra_papel_tesoura
from games.jogos.blackjack import blackjack
from games.jogos.fazenda import fazenda

def jogo_da_memoria_view(request):
    context = jogo_da_memoria(request)
    if hasattr(context, 'status_code') and context.status_code == 302:
        return context 
    return render(request, 'jogo_da_memoria.html', context)

def batalha_naval_view(request):
    context = batalha_naval(request)
    if hasattr(context, 'status_code') and context.status_code == 302:
        return context 
    return render(request, 'batalha_naval.html', context)

def forca_view(request):
    context = forca(request)
    if hasattr(context, 'status_code') and context.status_code == 302:
        return context 
    return render(request, 'forca.html', context)

def pedra_papel_tesoura_view(request):
    context = pedra_papel_tesoura(request)
    if hasattr(context, 'status_code') and context.status_code == 302:
        return context 
    return render(request, 'pedra_papel_tesoura.html', context)

def blackjack_view(request):
    context = blackjack(request)
    if hasattr(context, 'status_code') and context.status_code == 302:
        return context
    return render(request, 'blackjack.html', context)

def fazenda_view(request):
    context = fazenda(request)
    if hasattr(context, 'status_code') and context.status_code == 302:
        return context 
    return render(request, 'fazenda.html', context)