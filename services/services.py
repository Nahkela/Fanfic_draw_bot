from random import choice, randint, sample
from Base.Base import user_db, all_genres
from filters.filters import DickWriter


def choose_victim(victims: list, own_names: list, names: list) -> str:
    variants = [name for name in names if name not in victims and name not in own_names]
    goal = choice(variants)
    victims.append(goal)
    return goal


def key_generator():
    return f"{randint(1, 99):02}{randint(1, 99):02}{randint(1, 99):02}{randint(1, 99):02}"


@DickWriter
def generate(states, user_id, *args):

    dick = {}
    ids = list(states['play_ids'])
    ids.remove(user_id)
    wrong_variants = states['already_chosen'] + user_db[user_id]['modes']['drawing']['prev_victim']
    dick['victim'] = choice(list(filter(lambda x: x not in wrong_variants, ids)))
    user_db[user_id]['modes']['drawing']['new_victim'] = dick['victim']
    states['already_chosen'].append(dick['victim'])
    for mode in args:
        if mode == 'genres_counts':
            quantity = states['genres_counts']
            wrong_variants = states['already_used_genres'] + user_db[user_id]['modes']['drawing']['prev_genders']
            sequence = [genre for genre in states['genres'] if genre not in wrong_variants]
            if quantity > len(sequence):
                sequence = [genre for genre in all_genres if genre not in states['already_used_genres']]
            dick['genres'] = sample(sequence, quantity)
            states['already_used_genres'].extend(dick['genres'])
        if mode == 'conditions_counts':
            quantity = states['conditions_counts']
            ids.sort(key=lambda x: len(user_db[x]['modes']['drawing']['set_conditions']), reverse=True)
            counter = 0
            dick['conditions'] = []
            for user_cond in ids:
                n = user_db[user_cond]['modes']['drawing']['set_conditions'].pop(0)
                dick['conditions'].append(n)
    return dick

