from django.shortcuts import redirect
import random

def initialize_deck():
    naipes = ['ouros', 'copas', 'espadas', 'paus']
    valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [{'valor': valor, 'naipe': naipe} for valor in valores for naipe in naipes]
    random.shuffle(deck)
    return deck

def card_value(card):
    if card['valor'] in ['J', 'Q', 'K']:
        return 10
    elif card['valor'] == 'A':
        return 11
    else:
        return int(card['valor'])

def calculate_hand(hand):
    total = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if card['valor'] == 'A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def blackjack(request):
    if 'deck' not in request.session:
        request.session['deck'] = initialize_deck()
        request.session['player_hand'] = []
        request.session['dealer_hand'] = []
        request.session['game_over'] = False
        request.session['message'] = ''
        request.session.modified = True

    deck = request.session['deck']
    player_hand = request.session['player_hand']
    dealer_hand = request.session['dealer_hand']
    game_over = request.session['game_over']
    message = request.session['message']

    if request.method == 'POST':
        if 'restart' in request.POST:
            request.session.flush()
            return redirect('blackjack')

        if not game_over:
            if 'hit' in request.POST:
                player_hand.append(deck.pop())
                if calculate_hand(player_hand) > 21:
                    game_over = True
                    message = "Você estourou! A casa venceu."
            elif 'stand' in request.POST:
                while calculate_hand(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                game_over = True
                player_total = calculate_hand(player_hand)
                dealer_total = calculate_hand(dealer_hand)
                if dealer_total > 21 or player_total > dealer_total:
                    message = "Você venceu!"
                elif player_total == dealer_total:
                    message = "Empate!"
                else:
                    message = "A casa venceu."

            request.session['deck'] = deck
            request.session['player_hand'] = player_hand
            request.session['dealer_hand'] = dealer_hand
            request.session['game_over'] = game_over
            request.session['message'] = message
            request.session.modified = True

    player_total = calculate_hand(player_hand)
    dealer_total = calculate_hand(dealer_hand)

    return {
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'game_over': game_over,
        'message': message,
        'player_total': player_total,
        'dealer_total': dealer_total,
    }