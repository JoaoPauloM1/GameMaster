from django.shortcuts import redirect
import random

def initialize_game():
    cards = list(range(1, 9)) * 2 
    random.shuffle(cards)
    return cards

def jogo_da_memoria(request):
    if request.method == 'POST' and 'restart' in request.POST:
        request.session.flush()
        return redirect('jogo_da_memoria')

    if 'cards' not in request.session:
        request.session['cards'] = initialize_game()
        request.session['flipped'] = [] 
        request.session['matched'] = []  
        request.session['attempts'] = 0
        request.session.modified = True

    cards = request.session['cards']
    flipped = request.session['flipped']
    matched = request.session['matched']
    attempts = request.session['attempts']

    if request.method == 'POST' and 'card_index' in request.POST:
        card_index = int(request.POST.get('card_index'))
        if card_index not in flipped and card_index not in matched:
            flipped.append(card_index)

            if len(flipped) == 2:
                if cards[flipped[0]] == cards[flipped[1]]:
                    matched.extend(flipped)
                
                attempts += 1
                request.session['attempts'] = attempts
                request.session['matched'] = matched

                request.session['flipped'] = flipped.copy()  
            else:
                request.session['flipped'] = flipped

            request.session.modified = True

    return {
        'cards': cards,
        'flipped': flipped,
        'matched': matched,
        'attempts': attempts,
        'game_over': len(matched) == len(cards)
    }