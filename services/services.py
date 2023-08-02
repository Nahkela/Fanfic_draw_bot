from random import choice


def choose_victim(victims: list, own_names: list, names: list) -> str:
    variants = [name for name in names if name not in victims and name not in own_names]
    goal = choice(variants)
    victims.append(goal)
    return goal
