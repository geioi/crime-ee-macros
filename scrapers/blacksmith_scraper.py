import json


def readData():
    weapon_to_item_map = {'1': 'Level 48 - Terase sulam (Raud)',
                          '2': 'Level 60 - Titaani sulam (1) (Titaan)',
                          '3': 'Level 48 - Terase sulam (Raud)',
                          '4': 'Level 48 - Terase sulam (Raud)',
                          '5': 'Level 60 - Titaani sulam (1) (Titaan)',
                          '6': 'Level 60 - Titaani sulam (1) (Titaan)',
                          '7': 'Level 78 - Titaani sulam (2) (Vask + Titaan)',
                          '19': 'Level 48 - Terase sulam (Raud)',
                          '8': 'Level 78 - Titaani sulam (2) (Vask + Titaan)',
                          '9': 'Level 60 - Titaani sulam (1) (Titaan)',
                          '10': 'Level 60 - Titaani sulam (1) (Titaan)',
                          '11': 'Level 87 - Titaani sulam (3) (Raud + Titaan)',
                          '12': 'Level 78 - Titaani sulam (2) (Vask + Titaan)',
                          '13': 'Level 78 - Titaani sulam (2) (Vask + Titaan)',
                          '14': 'Level 87 - Titaani sulam (3) (Raud + Titaan)',
                          '15': 'Level 87 - Titaani sulam (3) (Raud + Titaan)',
                          '16': 'Level 87 - Titaani sulam (3) (Raud + Titaan)',
                          '17': 'Level 96 - Titaani sulam (4) (Raud + Vask + Titaan)',
                          '18': 'Level 96 - Titaani sulam (4) (Raud + Vask + Titaan)'
                          }

    item_names = ['Level 0: AK-47 (0.2 Terase sulamit)',
                  'Level 10: MG4 (0.2 Titaani sulamit (1))',
                  'Level 18: RPG-7 (0.4 Terase sulamit)',
                  'Level 24: Infrapuna binokkel (0.1 Terase sulamit)',
                  'Level 30: M1A1 (0.5 Titaani sulamit (1))',
                  'Level 38: M16 (0.2 Titaani sulamit (1))',
                  'Level 46: M24 SWS (0.3 Titaani sulamit (2))',
                  'Level 50: Terasplaat (1 Terase sulamit)',
                  'Level 53: M240B (0.2 Titaani sulamit (2))',
                  'Level 60: LightSpeed binokkel (0.1 Titaani sulamit(1))',
                  'Level 67: SPG-9 (0.4 Titaani sulamit (1))',
                  'Level 73: Pommivöö (0.3 Titaani sulamit (3))',
                  'Level 78: FmW 35 (0.5 Titaani sulamit (2))',
                  'Level 83: P90 (0.2 Titaani sulamit (2))',
                  'Level 87: M110 SASS (0.3 Titaani sulamit (3))',
                  'Level 91: M2HB (0.2 Titaani sulamit (3))',
                  'Level 95: M32 MGL (0.4 Titaani sulamit (3))',
                  'Level 98: M82A1 SASR (0.3 Titaani sulamit (4))',
                  'Level 101: M9A1-7 (0.5 Titaani sulamit (4))'
                  ]

    item_to_value_map = {
        'Level 0: AK-47 (0.2 Terase sulamit)': '1',
        'Level 10: MG4 (0.2 Titaani sulamit (1))': '2',
        'Level 18: RPG-7 (0.4 Terase sulamit)': '3',
        'Level 24: Infrapuna binokkel (0.1 Terase sulamit)': '4',
        'Level 30: M1A1 (0.5 Titaani sulamit (1))': '5',
        'Level 38: M16 (0.2 Titaani sulamit (1))': '6',
        'Level 46: M24 SWS (0.3 Titaani sulamit (2))': '7',
        'Level 50: Terasplaat (1 Terase sulamit)': '19',
        'Level 53: M240B (0.2 Titaani sulamit (2))': '8',
        'Level 60: LightSpeed binokkel (0.1 Titaani sulamit(1))': '9',
        'Level 67: SPG-9 (0.4 Titaani sulamit (1))': '10',
        'Level 73: Pommivöö (0.3 Titaani sulamit (3))': '11',
        'Level 78: FmW 35 (0.5 Titaani sulamit (2))': '12',
        'Level 83: P90 (0.2 Titaani sulamit (2))': '13',
        'Level 87: M110 SASS (0.3 Titaani sulamit (3))': '14',
        'Level 91: M2HB (0.2 Titaani sulamit (3))': '15',
        'Level 95: M32 MGL (0.4 Titaani sulamit (3))': '16',
        'Level 98: M82A1 SASR (0.3 Titaani sulamit (4))': '17',
        'Level 101: M9A1-7 (0.5 Titaani sulamit (4))': '18'
    }

    level_to_item_map = {
        '0': 'Level 0: AK-47 (0.2 Terase sulamit)',
        '10': 'Level 10: MG4 (0.2 Titaani sulamit (1))',
        '18': 'Level 18: RPG-7 (0.4 Terase sulamit)',
        '24': 'Level 24: Infrapuna binokkel (0.1 Terase sulamit)',
        '30': 'Level 30: M1A1 (0.5 Titaani sulamit (1))',
        '38': 'Level 38: M16 (0.2 Titaani sulamit (1))',
        '46': 'Level 46: M24 SWS (0.3 Titaani sulamit (2))',
        '50': 'Level 50: Terasplaat (1 Terase sulamit)',
        '53': 'Level 53: M240B (0.2 Titaani sulamit (2))',
        '60': 'Level 60: LightSpeed binokkel (0.1 Titaani sulamit(1))',
        '67': 'Level 67: SPG-9 (0.4 Titaani sulamit (1))',
        '73': 'Level 73: Pommivöö (0.3 Titaani sulamit (3))',
        '78': 'Level 78: FmW 35 (0.5 Titaani sulamit (2))',
        '83': 'Level 83: P90 (0.2 Titaani sulamit (2))',
        '87': 'Level 87: M110 SASS (0.3 Titaani sulamit (3))',
        '91': 'Level 91: M2HB (0.2 Titaani sulamit (3))',
        '95': 'Level 95: M32 MGL (0.4 Titaani sulamit (3))',
        '98': 'Level 98: M82A1 SASR (0.3 Titaani sulamit (4))',
        '101': 'Level 101: M9A1-7 (0.5 Titaani sulamit (4))'
    }

    data = {'weapon_to_item_map': weapon_to_item_map, 'item_names': item_names, 'item_to_value_map': item_to_value_map, 'level_to_item_map': level_to_item_map}

    with open('data/sepikoda.txt', 'w') as outfile:
        json.dump(data, outfile)
