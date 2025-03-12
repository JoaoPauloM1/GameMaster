from django.shortcuts import render, redirect
import random

def pedra_papel_tesoura_view(request):
    # Inicializa o placar e o último jogo na sessão, se não existirem
    if 'score' not in request.session:
        request.session['score'] = {'player': 0, 'machine': 0}
    if 'last_game' not in request.session:
        request.session['last_game'] = None

    # Verifica se o jogo terminou (melhor de 3)
    game_over = False
    winner = None
    if request.session['score']['player'] == 2:
        game_over = True
        winner = 'Você'
    elif request.session['score']['machine'] == 2:
        game_over = True
        winner = 'Máquina'

    # Processa a escolha do jogador ou o reinício do jogo
    if request.method == 'POST':
        if 'reset' in request.POST:  # Reiniciar o jogo
            request.session['score'] = {'player': 0, 'machine': 0}
            request.session['last_game'] = None
            return redirect('pedra_papel_tesoura')
        elif not game_over and 'choice' in request.POST:  # Jogada normal
            player_choice = request.POST.get('choice')
            machine_choice = random.choice(['pedra', 'papel', 'tesoura'])
            
            result = determine_winner(player_choice, machine_choice)
            
            if result == 'player':
                request.session['score']['player'] += 1
            elif result == 'machine':
                request.session['score']['machine'] += 1
            
            request.session['last_game'] = {
                'player_choice': player_choice,
                'machine_choice': machine_choice,
                'result': result
            }

            # Verifica novamente se o jogo terminou após atualizar o placar
            if request.session['score']['player'] == 2:
                game_over = True
                winner = 'Você'
            elif request.session['score']['machine'] == 2:
                game_over = True
                winner = 'Máquina'

    # Contexto para o template
    context = {
        'score': request.session['score'],
        'last_game': request.session['last_game'],
        'game_over': game_over,
        'winner': winner
    }
    return render(request, 'pedra_papel_tesoura.html', context)

def determine_winner(player_choice, machine_choice):
    if player_choice == machine_choice:
        return 'draw'
    elif (player_choice == 'pedra' and machine_choice == 'tesoura') or \
         (player_choice == 'papel' and machine_choice == 'pedra') or \
         (player_choice == 'tesoura' and machine_choice == 'papel'):
        return 'player'
    else:
        return 'machine'