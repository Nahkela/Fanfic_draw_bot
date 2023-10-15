user_db = {197232933: {'name': 'Алихан', 'age': '23', 'gender': 'Мужчина',
                        'photo_id': 'AgACAgIAAxkBAAIIUmUoTuH2o63qP4hf8WEW9RSb3gw9AALY6jEbFDYISc2WbnFOgFE7AQADAgADbQADMAQ',
                        'photo_unique_id': 'AQAD2OoxGxQ2CEly', 'modes': {}},
           1402475060: {'name': 'Бетховен', 'age': '80', 'gender': 'Мужчина', 'photo_id': 'AgACAgIAAxkBAAIJf2UpzsIWodAcVukOxyDF5dLVKqPNAAKXzjEbZmERSUNZov71Vh8_AQADAgADbQADMAQ', 'photo_unique_id': 'AQADl84xG2ZhEUly', 'modes': {}}
}
states: dict[str, [int, list]] = {'play_ids': set(),
                                  'step': 0,
                                  'names_count': 0,
                                  'get_name': 0,
                                  'genres_counts': 0,
                                  'conditions_counts': 0,
                                  'accepted_count_condition': 0}

drawing_options = {'is_drawing': True,
                   'is_initiator': False,
                   'time_id_key': False,
                   'prev_victim': None,
                   'prev_genders': list(),
                   'set_conditions': list(),
                   'needed_states': None
                   }
draw_rooms: dict[str, dict[str, [int, list]]] = {}
draw_rooms_story = {}


# 197232933: {'name': 'Алихан', 'age': '23', 'gender': 'Мужчина',
#                        'photo_id': 'AgACAgIAAxkBAAIIUmUoTuH2o63qP4hf8WEW9RSb3gw9AALY6jEbFDYISc2WbnFOgFE7AQADAgADbQADMAQ',
#                        'photo_unique_id': 'AQAD2OoxGxQ2CEly', 'modes': {}}

