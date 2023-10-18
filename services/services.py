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
    dick['victim'] = choice(list(filter(lambda x: x not in states['already_chosen'], ids)))
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
            wrong_variants = user_db[user_id]['modes']['drawing']['set_conditions'] + states['already_used_conditions']
            sequence = [cond for cond in states['all_conditions'] if cond not in wrong_variants]
            dick['conditions'] = sample(sequence, quantity)
            states['already_used_conditions'].extend(dick['conditions'])
    return dick

