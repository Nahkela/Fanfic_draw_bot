user_db = {197232933: {'name': 'Алихан', 'age': '23', 'gender': 'Мужчина',
                        'photo_id': 'AgACAgIAAxkBAAIIUmUoTuH2o63qP4hf8WEW9RSb3gw9AALY6jEbFDYISc2WbnFOgFE7AQADAgADbQADMAQ',
                        'photo_unique_id': 'AQAD2OoxGxQ2CEly', 'modes': {}},
           1402475060: {'name': 'Бетховен', 'age': '80', 'gender': 'Мужчина', 'photo_id': 'AgACAgIAAxkBAAIJf2UpzsIWodAcVukOxyDF5dLVKqPNAAKXzjEbZmERSUNZov71Vh8_AQADAgADbQADMAQ', 'photo_unique_id': 'AQADl84xG2ZhEUly', 'modes': {}}
}
states: dict[str, [int, list]] = {'play_ids': set(),
                                  'steps': 0,
                                  'room_id': None,
                                  'genres': list(),
                                  'all_conditions': list(),
                                  'names_count': 0,
                                  'get_name': 0,
                                  'genres_counts': 0,
                                  'conditions_counts': 0,
                                  'over': set(),
                                  'already_chosen': list(),
                                  'already_used_genres': list(),
                                  'already_used_conditions': list()}

drawing_options = {'is_initiator': False,
                   'time_id_key': False,
                   'owner': False,
                   'prev_victim': 0,
                   'prev_genders': list(),
                   'set_conditions': list(),
                   'needed_states': list(),
                   'step': 0,
                   'last_callback': None,
                   'state': None
                   }
draw_rooms: dict[str, dict[str, [int, list]]] = {}
draw_rooms_story = {}
all_genres = [
 'action and adventure',
 'detective',
 'dystopia',
 'historical fiction',
 'Romance novel',
 'Fantastic',
 'western',
 'horror',
 'fantasy',
 'musical',
 'furry',
 'hentai',
 'poetry',
 'action movie']


# 197232933: {'name': 'Алихан', 'age': '23', 'gender': 'Мужчина',
#                        'photo_id': 'AgACAgIAAxkBAAIIUmUoTuH2o63qP4hf8WEW9RSb3gw9AALY6jEbFDYISc2WbnFOgFE7AQADAgADbQADMAQ',
#                        'photo_unique_id': 'AQAD2OoxGxQ2CEly', 'modes': {}}

