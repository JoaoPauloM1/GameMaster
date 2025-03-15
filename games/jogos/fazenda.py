import random
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def initialize_farm():
    return {
        'plantations': [],
        'animals': [],
        'coins': 15,
        'events': [],
        'day': 1,
        'pest_chance': 10,
        'plant_cost': 4,
        'animal_cost': {'cow': 20, 'chicken': 5, 'pig': 15},
        'animal_maintenance': {'cow': 2, 'chicken': 1, 'pig': 3},
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

def buy_animal(farm, animal_type):
    animal_names = {'cow': 'vaca', 'chicken': 'galinha', 'pig': 'porco'}
    if farm['coins'] >= farm['animal_cost'][animal_type]:
        if len([animal for animal in farm['animals'] if animal['type'] == animal_type]) >= 2:
            return f"Você já tem 2 {animal_names[animal_type]}s. Limite atingido!"
        farm['coins'] -= farm['animal_cost'][animal_type]
        farm['animals'].append({'type': animal_type, 'days_until_production': random.randint(3, 7)})
        return f"Você comprou um(a) {animal_names[animal_type]}!"
    else:
        return f"Moedas insuficientes para comprar um(a) {animal_names[animal_type]}."

def update_animals(farm):
    animal_messages = []
    animal_names = {'cow': 'vaca', 'chicken': 'galinha', 'pig': 'porco'}
    for animal in farm['animals'][:]: 
        animal['days_until_production'] -= 1
        if animal['days_until_production'] <= 0:
            if animal['type'] == 'cow':
                farm['coins'] += 10  
                animal_messages.append(f"🐄 Sua vaca produziu leite e rendeu 10 moedas!")
            elif animal['type'] == 'chicken':
                farm['coins'] += 3 
                animal_messages.append(f"🐔 Sua galinha botou ovos e rendeu 3 moedas!")
            elif animal['type'] == 'pig':
                farm['coins'] += 7  
                animal_messages.append(f"🐖 Seu porco produziu carne e rendeu 7 moedas!")
            animal['days_until_production'] = random.randint(3, 7)

        if random.randint(1, 100) <= 5:
            farm['animals'].remove(animal)
            animal_messages.append(f"💀 Seu(a) {animal_names[animal['type']]} morreu!")

    return animal_messages

def fazenda(request):
    if request.method == 'POST' and 'restart' in request.POST:
        request.session['farm'] = initialize_farm()
        request.session.modified = True
        return HttpResponseRedirect(reverse('fazenda'))

    if 'farm' not in request.session:
        request.session['farm'] = initialize_farm()
    else:
        farm = request.session['farm']
        if 'day' not in farm:
            farm['day'] = 1
        if 'pest_chance' not in farm:
            farm['pest_chance'] = 10
        if 'plant_cost' not in farm:
            farm['plant_cost'] = 4
        if 'animal_cost' not in farm:
            farm['animal_cost'] = {'cow': 20, 'chicken': 5, 'pig': 15}
        if 'animal_maintenance' not in farm:
            farm['animal_maintenance'] = {'cow': 2, 'chicken': 1, 'pig': 3}
        if 'game_over' not in farm:
            farm['game_over'] = False
        request.session['farm'] = farm

    request.session.modified = True
    farm = request.session['farm']
    message = ""
    event_message = ""
    animal_messages = []

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
                    event_message = apply_random_events(farm)
                    grow_plants(farm)
                elif len(farm['plantations']) >= 5:
                    message = "Limite máximo de plantações atingido!"
                else:
                    message = f"Moedas insuficientes para comprar sementes (custo: {farm['plant_cost']} moedas)."

            elif 'water' in request.POST:
                plants_not_ready = [plant for plant in farm['plantations'] if plant['growth'] < 100]
                if plants_not_ready:
                    cost_to_water = 2 * len(plants_not_ready)
                    if farm['coins'] >= cost_to_water:
                        farm['coins'] -= cost_to_water
                        for plant in plants_not_ready:
                            plant['growth'] += 15
                            if plant['growth'] > 100:
                                plant['growth'] = 100
                        message = f"Você regou {len(plants_not_ready)} plantações por {cost_to_water} moedas!"
                        
                        farm['day'] += 1
                        animal_messages = update_animals(farm)
                        event_message = apply_random_events(farm)
                        grow_plants(farm)
                    else:
                        message = f"Moedas insuficientes para regar. Custo: {cost_to_water} moedas."
                else:
                    message = "Todas as plantações já estão prontas para colheita!"

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
                            farm['coins'] += 10
                        for plant in harvested:
                            farm['plantations'].remove(plant)
                        if harvested:
                            message = f"Você colheu {len(harvested)} vegetais e ganhou {len(harvested) * 10} moedas!"
                else:
                    message = "Nenhuma plantação pronta para colheita."

                if ready_to_harvest:
                    event_message = apply_random_events(farm)
                    grow_plants(farm)

            elif 'buy_animal' in request.POST:
                animal_type = request.POST['buy_animal']
                message = buy_animal(farm, animal_type)

            elif 'next_day' in request.POST:
                farm['day'] += 1
                animal_messages = update_animals(farm)
                event_message = apply_random_events(farm)
                message = "Você passou o dia!"

            plants_not_ready = [plant for plant in farm['plantations'] if plant['growth'] < 100]
            cost_to_water = 2 * len(plants_not_ready)
            min_animal_cost = min(farm['animal_cost'].values())

            if (not farm['animals'] and
                not farm['plantations'] and
                farm['coins'] < farm['plant_cost'] and
                farm['coins'] < min_animal_cost):
                farm['game_over'] = True
                message = "<span style='color: red;'>Game Over! Você não tem mais opções. Reinicie o jogo para continuar.</span>"
            elif (plants_not_ready and
                  farm['coins'] < cost_to_water and
                  farm['coins'] < farm['plant_cost'] and
                  farm['coins'] < min_animal_cost):
                farm['game_over'] = True
                message = "<span style='color: red;'>Game Over! Você não tem mais opções. Reinicie o jogo para continuar.</span>"

        request.session['farm'] = farm
        request.session.modified = True

    return {
        'farm': farm,
        'message': message,
        'event_message': event_message,
        'animal_messages': animal_messages,
    }