import random
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def initialize_farm():
    return {
        'plantations': [],
        'coins': 20,  
        'events': [],  
        'level': 1,
        'experience': 0, 
        'day': 1, 
        'pest_chance': 10,  
        'plant_cost': 4, 
        'game_over': False,
    }

def grow_plants(farm):
    for plant in farm['plantations']:
        if plant['growth'] < 100:  
            growth_increment = random.randint(10, 20)  
            if 'rain' in farm['events']:
                growth_increment += 10  
            plant['growth'] += growth_increment
            if plant['growth'] > 100:
                plant['growth'] = 100  

def apply_random_events(farm):
    if farm['events']:
        if random.randint(1, 100) <= 50:
            if farm['events'][0] == 'rain':
                return "🌧️ A chuva continua ajudando suas plantações!"
            else:
                return "🐛 A praga continua na plantação!"
        else:
            event = farm['events'][0]
            farm['events'] = []
            if event == 'rain':
                return "🌧️ A chuva passou!"
            else:
                return "🐛 As pragas sumiram!"
    else:
        if random.randint(1, 100) <= 5: 
            farm['events'] = ['rain']
            return "🌧️ Chuva! Suas plantações estão crescendo mais rápido."
        elif random.randint(1, 100) <= farm['pest_chance']:  
            farm['events'] = ['pest']
            if farm['plantations']:
                plant = random.choice(farm['plantations'])
                farm['plantations'].remove(plant)  
                return f"🐛 Praga! Uma plantação de {plant['type']} foi destruída."
    return ""

def update_difficulty(farm):
    farm['day'] += 1
    if farm['day'] % 5 == 0:  
        farm['pest_chance'] += 3  
    if farm['day'] % 10 == 0:  
        farm['plant_cost'] += 1  
        return f"O custo das sementes aumentou para {farm['plant_cost']} moedas."
    return ""

def fazenda(request):
    if request.method == 'POST' and 'restart' in request.POST:
        request.session['farm'] = initialize_farm()
        request.session.modified = True
        return HttpResponseRedirect(reverse('fazenda')) 

    if 'farm' not in request.session:
        request.session['farm'] = initialize_farm()
    else:
        farm = request.session['farm']
        if 'experience' not in farm:
            farm['experience'] = 0
        if 'level' not in farm:
            farm['level'] = 1
        if 'day' not in farm:
            farm['day'] = 1
        if 'pest_chance' not in farm:
            farm['pest_chance'] = 10
        if 'plant_cost' not in farm:
            farm['plant_cost'] = 4
        if 'game_over' not in farm:
            farm['game_over'] = False
        request.session['farm'] = farm

    request.session.modified = True
    farm = request.session['farm']
    message = ""
    level_up_message = ""
    difficulty_message = ""
    event_message = ""

    if farm['game_over']:
        message = "<span style='color: red;'>Game Over! Você não tem mais opções. Reinicie o jogo para continuar.</span>"
    else:
        if request.method == 'POST':
            if 'plant' in request.POST:
                if farm['coins'] >= farm['plant_cost'] and len(farm['plantations']) < 5:  
                    farm['coins'] -= farm['plant_cost']
                    farm['plantations'].append({
                        'type': random.choice(['Cenoura', 'Batata', 'Tomate', 'Milho', 'Abóbora']),
                        'growth': 0,  
                    })
                    message = f"Você plantou uma semente por {farm['plant_cost']} moedas!"
                    difficulty_message = update_difficulty(farm) 
                    event_message = apply_random_events(farm)
                    grow_plants(farm)
                elif len(farm['plantations']) >= 5:
                    message = "Limite máximo de plantações atingido!"
                else:
                    message = f"Moedas insuficientes para comprar sementes (custo: {farm['plant_cost']} moedas)."

            elif 'water' in request.POST:
                cost_to_water = 2 * len(farm['plantations'])  
                if farm['coins'] >= cost_to_water:  
                    if farm['plantations']:
                        farm['coins'] -= cost_to_water
                        for plant in farm['plantations']:
                            plant['growth'] += 15 
                            if plant['growth'] > 100:
                                plant['growth'] = 100  
                        message = f"Você regou {len(farm['plantations'])} plantações por {cost_to_water} moedas!"
                        difficulty_message = update_difficulty(farm)  
                        event_message = apply_random_events(farm)  
                        grow_plants(farm)
                    else:
                        message = "Não há plantações para regar."
                else:
                    message = f"Moedas insuficientes para regar. Custo: {cost_to_water} moedas."

            elif 'harvest' in request.POST:
                harvested = []
                ready_to_harvest = [plant for plant in farm['plantations'] if plant['growth'] >= 100]
                
                if ready_to_harvest:
                    lose_chance = 10
                    if 'rain' in farm['events']:
                        lose_chance += 5  
                    if 'pest' in farm['events']:
                        lose_chance += 10  

                    if random.randint(1, 100) <= lose_chance:  
                        for plant in ready_to_harvest:
                            farm['plantations'].remove(plant)
                        message = "<span style='color: red;'>Oh não! Você perdeu a colheita devido a um evento inesperado.</span>"
                    else:
                        for plant in ready_to_harvest:
                            harvested.append(plant)
                            farm['coins'] += 15  
                            farm['experience'] += 5  
                            if farm['experience'] >= 100:  
                                farm['level'] += 1
                                farm['experience'] = 0
                                level_up_message = f"Parabéns! Você subiu para o nível {farm['level']}!"
                        for plant in harvested:
                            farm['plantations'].remove(plant)
                        if harvested:
                            message = f"Você colheu {len(harvested)} vegetais e ganhou {len(harvested) * 15} moedas!"
                else:
                    message = "Nenhuma plantação pronta para colheita."

                if ready_to_harvest:
                    difficulty_message = update_difficulty(farm) 
                    event_message = apply_random_events(farm) 
                    grow_plants(farm)

            if (farm['coins'] < farm['plant_cost'] and  
                farm['coins'] < 2 * len(farm['plantations']) and  
                not any(plant['growth'] >= 100 for plant in farm['plantations'])):  
                farm['game_over'] = True
                message = "<span style='color: red;'>Game Over! Você não tem mais opções. Reinicie o jogo para continuar.</span>"

        request.session['farm'] = farm
        request.session.modified = True

    return {
        'farm': farm,
        'message': message,
        'level_up_message': level_up_message,
        'difficulty_message': difficulty_message,
        'event_message': event_message,  
    }