import json

def readData():
    item_names = ['Level 0: Kanep + Hevea mahl',
                  'Level 13: Kanep + Maguni mahl',
                  'Level 25: GHB + Jamssi mahl',
                  'Level 36: GHB + Guaavi mahl',
                  'Level 46: Ecstasy + Bataadi mahl',
                  'Level 55: Ecstasy + Ebatsuuga mahl',
                  'Level 63: PCP + Manioki mahl',
                  'Level 70: PCP + Palmiira mahl',
                  'Level 76: LSD + Adzuki mahl',
                  'Level 81: LSD + Riitsinuse mahl',
                  'Level 85: Amfetamiin + Passioni mahl',
                  'Level 89: Amfetamiin + Dzuuti mahl',
                  'Level 92: Speed + Pappaia mahl',
                  'Level 95: Speed + Estragoni mahl',
                  'Level 97: Heroiin + Mangostani mahl',
                  'Level 99: Heroiin + Korianderi mahl',
                  'Level 101: Kokaiin + Lihdzchi mahl',
                  'Level 103: Kokaiin + Tamarillo mahl',
                  'Level 108: Kräkk + Senna mahl',
                  'Level 115: Kräkk + Annatto mahl'
                  ]

    item_to_narc_map = {
        'Level 0: Kanep + Hevea mahl': 'Kanep',
        'Level 13: Kanep + Maguni mahl': 'Kanep',
        'Level 25: GHB + Jamssi mahl': 'GHB',
        'Level 36: GHB + Guaavi mahl': 'GHB',
        'Level 46: Ecstasy + Bataadi mahl': 'Ecstasy',
        'Level 55: Ecstasy + Ebatsuuga mahl': 'Ecstasy',
        'Level 63: PCP + Manioki mahl': 'PCP',
        'Level 70: PCP + Palmiira mahl': 'PCP',
        'Level 76: LSD + Adzuki mahl': 'LSD',
        'Level 81: LSD + Riitsinuse mahl': 'LSD',
        'Level 85: Amfetamiin + Passioni mahl': 'Amfetamiin',
        'Level 89: Amfetamiin + Dzuuti mahl': 'Amfetamiin',
        'Level 92: Speed + Pappaia mahl': 'Speed',
        'Level 95: Speed + Estragoni mahl': 'Speed',
        'Level 97: Heroiin + Mangostani mahl': 'Heroiin',
        'Level 99: Heroiin + Korianderi mahl': 'Heroiin',
        'Level 101: Kokaiin + Lihdzchi mahl': 'Kokaiin',
        'Level 103: Kokaiin + Tamarillo mahl': 'Kokaiin',
        'Level 108: Kräkk + Senna mahl': 'Kräkk',
        'Level 115: Kräkk + Annatto mahl': 'Kräkk'
    }

    narc_to_value_map = {
        'Kanep': '1',
        'GHB': '2',
        'Ecstasy': '3',
        'PCP': '4',
        'LSD': '5',
        'Amfetamiin': '6',
        'Speed': '7',
        'Heroiin': '8',
        'Kräkk': '9',
        'Kokaiin': '10'
    }

    item_to_ready_narc_value_map = {
        'Level 0: Kanep + Hevea mahl': '11',
        'Level 13: Kanep + Maguni mahl': '12',
        'Level 25: GHB + Jamssi mahl': '13',
        'Level 36: GHB + Guaavi mahl': '14',
        'Level 46: Ecstasy + Bataadi mahl': '15',
        'Level 55: Ecstasy + Ebatsuuga mahl': '16',
        'Level 63: PCP + Manioki mahl': '17',
        'Level 70: PCP + Palmiira mahl': '18',
        'Level 76: LSD + Adzuki mahl': '19',
        'Level 81: LSD + Riitsinuse mahl': '20',
        'Level 85: Amfetamiin + Passioni mahl': '21',
        'Level 89: Amfetamiin + Dzuuti mahl': '22',
        'Level 92: Speed + Pappaia mahl': '23',
        'Level 95: Speed + Estragoni mahl': '24',
        'Level 97: Heroiin + Mangostani mahl': '25',
        'Level 99: Heroiin + Korianderi mahl': '26',
        'Level 101: Kokaiin + Lihdzchi mahl': '27',
        'Level 103: Kokaiin + Tamarillo mahl': '28',
        'Level 108: Kräkk + Senna mahl': '29',
        'Level 115: Kräkk + Annatto mahl': '30'
    }

    item_to_juice_map = {
        'Level 0: Kanep + Hevea mahl': 'Hevea mahl',
        'Level 13: Kanep + Maguni mahl': 'Maguni mahl',
        'Level 25: GHB + Jamssi mahl': 'Jamssi mahl',
        'Level 36: GHB + Guaavi mahl': 'Guaavi mahl',
        'Level 46: Ecstasy + Bataadi mahl': 'Bataadi mahl',
        'Level 55: Ecstasy + Ebatsuuga mahl': 'Ebatsuuga mahl',
        'Level 63: PCP + Manioki mahl': 'Manioki mahl',
        'Level 70: PCP + Palmiira mahl': 'Palmiira mahl',
        'Level 76: LSD + Adzuki mahl': 'Adzuki mahl',
        'Level 81: LSD + Riitsinuse mahl': 'Riitsinuse mahl',
        'Level 85: Amfetamiin + Passioni mahl': 'Passioni mahl',
        'Level 89: Amfetamiin + Dzuuti mahl': 'Dzuuti mahl',
        'Level 92: Speed + Pappaia mahl': 'Pappaia mahl',
        'Level 95: Speed + Estragoni mahl': 'Estragoni mahl',
        'Level 97: Heroiin + Mangostani mahl': 'Mangostani mahl',
        'Level 99: Heroiin + Korianderi mahl': 'Korianderi mahl',
        'Level 101: Kokaiin + Lihdzchi mahl': 'Lihdzchi mahl',
        'Level 103: Kokaiin + Tamarillo mahl': 'Tamarillo mahl',
        'Level 108: Kräkk + Senna mahl': 'Senna mahl',
        'Level 115: Kräkk + Annatto mahl': 'Annatto mahl'
    }

    juice_to_value_map = {
        'Hevea mahl': '1',
        'Maguni mahl': '2',
        'Jamssi mahl': '3',
        'Guaavi mahl': '4',
        'Bataadi mahl': '5',
        'Ebatsuuga mahl': '6',
        'Manioki mahl': '7',
        'Palmiira mahl': '8',
        'Adzuki mahl': '9',
        'Riitsinuse mahl': '10',
        'Passioni mahl': '11',
        'Dzuuti mahl': '12',
        'Pappaia mahl': '13',
        'Estragoni mahl': '14',
        'Mangostani mahl': '15',
        'Korianderi mahl': '16',
        'Lihdzchi mahl': '17',
        'Tamarillo mahl': '18',
        'Senna mahl': '19',
        'Annatto mahl': '20'
    }

    plant_to_value_map = {
        'Hevea taimed': '1',
        'Maguni taimed': '2',
        'Jamssi taimed': '3',
        'Guaavi taimed': '4',
        'Bataadi taimed': '5',
        'Ebatsuuga taimed': '6',
        'Manioki taimed': '7',
        'Palmiira taimed': '8',
        'Adzuki taimed': '9',
        'Riitsinuse taimed': '10',
        'Passioni taimed': '11',
        'Dzuuti taimed': '12',
        'Pappaia taimed': '13',
        'Estragoni taimed': '14',
        'Mangostani taimed': '15',
        'Korianderi taimed': '16',
        'Lihdzchi taimed': '17',
        'Tamarillo taimed': '18',
        'Senna taimed': '19',
        'Annatto taimed': '20'
    }

    level_to_item_map = {
        '0': 'Level 0: Kanep + Hevea mahl',
        '13': 'Level 13: Kanep + Maguni mahl',
        '25': 'Level 25: GHB + Jamssi mahl',
        '36': 'Level 36: GHB + Guaavi mahl',
        '46': 'Level 46: Ecstasy + Bataadi mahl',
        '55': 'Level 55: Ecstasy + Ebatsuuga mahl',
        '63': 'Level 63: PCP + Manioki mahl',
        '70': 'Level 70: PCP + Palmiira mahl',
        '76': 'Level 76: LSD + Adzuki mahl',
        '81': 'Level 81: LSD + Riitsinuse mahl',
        '85': 'Level 85: Amfetamiin + Passioni mahl',
        '89': 'Level 89: Amfetamiin + Dzuuti mahl',
        '92': 'Level 92: Speed + Pappaia mahl',
        '95': 'Level 95: Speed + Estragoni mahl',
        '97': 'Level 97: Heroiin + Mangostani mahl',
        '99': 'Level 99: Heroiin + Korianderi mahl',
        '101': 'Level 101: Kokaiin + Lihdzchi mahl',
        '103': 'Level 103: Kokaiin + Tamarillo mahl',
        '108': 'Level 108: Kräkk + Senna mahl',
        '115': 'Level 115: Kräkk + Annatto mahl'
    }

    data = {'plant_to_value_map': plant_to_value_map, 'juice_to_value_map': juice_to_value_map, 'item_names': item_names, 'narc_to_value_map': narc_to_value_map,
            'level_to_item_map': level_to_item_map, 'item_to_narc_map': item_to_narc_map, 'item_to_ready_narc_value_map': item_to_ready_narc_value_map, 'item_to_juice_map': item_to_juice_map}

    with open('data/chemistry.txt', 'w') as outfile:
        json.dump(data, outfile)