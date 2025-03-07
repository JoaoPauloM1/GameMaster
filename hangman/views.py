from django.shortcuts import render

def hangman(request):
    return render(request, 'hangman.html')