from django.shortcuts import redirect
import random

def initialize_game():
    board = [['' for _ in range(5)] for _ in range(5)]
    
    ships = 0
    while ships < 3:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if board[x][y] == '':
            board[x][y] = 'S'
            ships += 1
    
    return board

def batalha_naval(request):
    if 'board' not in request.session:
        request.session['board'] = initialize_game()
        request.session['hits'] = 0
        request.session['attempts'] = 0
        request.session['game_over'] = False
    
    board = request.session['board']
    hits = request.session['hits']
    attempts = request.session['attempts']
    game_over = request.session['game_over']
    
    if request.method == 'POST':
        if 'restart' in request.POST:
            request.session['board'] = initialize_game()
            request.session['hits'] = 0
            request.session['attempts'] = 0
            request.session['game_over'] = False
            return redirect('batalha_naval')
        
        if not game_over:
            x = int(request.POST.get('x'))
            y = int(request.POST.get('y'))
            
            if board[x][y] == 'S':
                board[x][y] = 'X'
                hits += 1
                message = "Você acertou um navio!"
            else:
                board[x][y] = 'O'
                message = "Você errou!"
            
            attempts += 1
            request.session['board'] = board
            request.session['hits'] = hits
            request.session['attempts'] = attempts
            
            if hits == 3:
                message = "Parabéns! Você afundou todos os navios!"
                request.session['game_over'] = True
            elif attempts >= 12:
                message = "Fim de jogo! Você esgotou suas tentativas."
                request.session['game_over'] = True
            
            return {
                'board': board,
                'message': message,
                'hits': hits,
                'attempts': attempts,
                'game_over': game_over
            }
    
    if game_over:
        for x in range(5):
            for y in range(5):
                if board[x][y] == 'S':
                    board[x][y] = '💥'
    
    return {
        'board': board,
        'hits': hits,
        'attempts': attempts,
        'game_over': game_over
    }