import random
from django.shortcuts import render, redirect

PALAVRAS = [
    'algoritmo', 'aplicativo', 'backend', 'bigdata', 'bitcoin', 'blockchain', 
    'browser', 'bytecode', 'cache', 'cibernetica', 'cloud', 'compilador', 
    'computador', 'criptografia', 'dashboard', 'database', 'debug', 'desenvolvedor', 
    'devops', 'digital', 'disco', 'dispositivo', 'download', 'email', 'encryption', 
    'firewall', 'firmware', 'framework', 'frontend', 'github', 'hardware', 'html', 
    'internet', 'javascript', 'kernel', 'linux', 'machinelearning', 'mainframe', 
    'malware', 'microprocessador', 'mobile', 'nanotecnologia', 'network', 'openai', 
    'opensource', 'programacao', 'protocolo', 'python', 'quantum', 'realidadevirtual', 
    'robotica', 'script', 'seguranca', 'servidor', 'software', 'streaming', 
    'supercomputador', 'tecnologia', 'terminal', 'usabilidade', 'virtualizacao', 
    'web', 'webdesign', 'wi-fi', 'windows', 'wireless', 'xml', 'youtube', 'zip'
]

def hangman_view(request):
    if 'palavra_secreta' not in request.session:
        request.session['palavra_secreta'] = random.choice(PALAVRAS)
        request.session['letras_adivinhadas'] = []
        request.session['tentativas_erradas'] = 0
        request.session['palavra_visivel'] = ['_'] * len(request.session['palavra_secreta'])
    
    palavra_secreta = request.session['palavra_secreta']
    letras_adivinhadas = request.session['letras_adivinhadas']
    tentativas_erradas = request.session['tentativas_erradas']
    palavra_visivel = request.session['palavra_visivel']

    if request.method == "POST":
        if 'reiniciar' in request.POST:
            request.session['palavra_secreta'] = random.choice(PALAVRAS)
            request.session['letras_adivinhadas'] = []
            request.session['tentativas_erradas'] = 0
            request.session['palavra_visivel'] = ['_'] * len(request.session['palavra_secreta'])
            return redirect('hangman')

        letra = request.POST.get('letra').lower()
        if letra and letra not in letras_adivinhadas:
            letras_adivinhadas.append(letra)
            if letra in palavra_secreta:
                for i, char in enumerate(palavra_secreta):
                    if char == letra:
                        palavra_visivel[i] = letra
            else:
                tentativas_erradas += 1

            request.session['letras_adivinhadas'] = letras_adivinhadas
            request.session['tentativas_erradas'] = tentativas_erradas
            request.session['palavra_visivel'] = palavra_visivel

    ganhou = False
    perdeu = False
    if '_' not in palavra_visivel:
        ganhou = True
    if tentativas_erradas >= 6:
        perdeu = True

    return render(request, 'hangman.html', {
        'palavra_secreta': palavra_secreta,
        'palavra_visivel': ''.join(palavra_visivel),
        'tentativas_erradas': tentativas_erradas,
        'letras_adivinhadas': letras_adivinhadas,
        'ganhou': ganhou,
        'perdeu': perdeu
    })
