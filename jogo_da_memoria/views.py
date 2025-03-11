from django.shortcuts import render, redirect
import random

def initialize_game():
    # Cria uma lista de pares de números (representando as cartas)
    cards = list(range(1, 9)) * 2  # 8 pares de cartas (16 cartas no total)
    random.shuffle(cards)  # Embaralha as cartas
    return cards

def memoria_view(request):
    if 'cards' not in request.session:
        # Inicializa o jogo se não houver cartas na sessão
        request.session['cards'] = initialize_game()
        request.session['flipped'] = []  # Cartas viradas
        request.session['matched'] = []  # Cartas combinadas
        request.session['attempts'] = 0  # Contador de tentativas

    cards = request.session['cards']
    flipped = request.session['flipped']
    matched = request.session['matched']
    attempts = request.session['attempts']

    if request.method == 'POST':
        if 'restart' in request.POST:
            # Reinicia o jogo
            request.session['cards'] = initialize_game()
            request.session['flipped'] = []
            request.session['matched'] = []
            request.session['attempts'] = 0
            return redirect('memoria')

        card_index = int(request.POST.get('card_index'))
        if card_index not in flipped and card_index not in matched:
            flipped.append(card_index)
            if len(flipped) == 2:
                # Verifica se as duas cartas viradas são iguais
                if cards[flipped[0]] == cards[flipped[1]]:
                    matched.extend(flipped)
                attempts += 1
                request.session['attempts'] = attempts
                request.session['matched'] = matched
                # Limpa as cartas viradas após a verificação
                flipped.clear()
            request.session['flipped'] = flipped

    return render(request, 'jogo_da_memoria.html', {
        'cards': cards,
        'flipped': flipped,
        'matched': matched,
        'attempts': attempts,
        'game_over': len(matched) == len(cards)  # Verifica se o jogo acabou
    })