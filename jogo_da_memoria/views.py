from django.shortcuts import render

def memoria_view(request):
    return render (request, 'jogo_da_memoria.html')