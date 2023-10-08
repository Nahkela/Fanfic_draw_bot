# Валидатор корректности имени
def is_name_correct(name: str):
    return name.isalpha() and name.istitle()


#
def is_age_correct(age: str):
    return age.isdigit() and 4 <= int(age) <= 120
