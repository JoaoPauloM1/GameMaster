from django.shortcuts import render

def pedra_papel_tesoura_view(request):
    return render(request, 'pedra_papel_tesoura.html')