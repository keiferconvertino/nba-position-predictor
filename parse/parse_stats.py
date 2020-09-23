from bs4 import BeautifulSoup
import requests
import csv
import time
import random
import re
import io


def get_stats(filename):

    # Grab player list
    with io.open(filename, 'r', encoding="utf-8") as players:
        reader = csv.reader(players)
        next(reader)
        player_list = list(reader)
    players.close()

    # Chars to whitelist:
    whitelist_nums = '0123456789,'
    whitelist_chars = 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-'

    # Stats to track:
    stats_to_track = ["fg2a_per_g", "fg2_pct", "fg3a_per_g", "fg3_pct", 'fta_per_g', 'ft_pct', 'trb_per_g', 'ast_per_g',
                      'stl_per_g', 'blk_per_g', 'tov_per_g']

    # Open file
    with io.open('player_stats.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(
            ['2PA', '2P%', '3PA', '3P%', 'FTA', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'HGT', "WGT", 'POS'])

        len_players = len(player_list)
        ten_percent = len_players / 10.0
        i = 0
        percent = 0
        # Grab each players stats
        for (player, pos) in player_list:
            i += 1
            if i > ten_percent:
                percent += 10
                i = 0
                print(f'{percent}% done parsing stats!')

            # Format name
            player_str = player.replace('-', ' ')
            player_str = ''.join(filter(whitelist_chars.__contains__, player_str))
            name1 = player_str.replace(' ', '-').lower()

            # Go to college bball stat site
            source1 = requests.get(f'https://www.sports-reference.com/cbb/players/{name1}-1.html').text
            soup1 = BeautifulSoup(source1, features="html.parser")

            statline = soup1.find('tfoot')

            if statline is None:
                continue

            statline = statline.tr

            stats = []

            # Grab each stat
            failed_bool = False
            for stat in stats_to_track:
                try:
                    if statline.find(attrs={"data-stat": f'{stat}'}).text == '':
                        stats.append('0')
                    else:
                        stats.append(statline.find(attrs={"data-stat": f'{stat}'}).text)

                # If soup fails, skip this player
                except:
                    failed_bool = True
            if failed_bool:
                continue
            # Grab height/weight measurements
            try:
                body_profile = soup1.find(class_='nothumb').find('span', itemprop='height')
                body_text = body_profile.find_parent('p').text
            except:
                # If soup fails, skip this player
                continue

            # RegEx to grab height/weight in cm/kg
            body_text_list = re.search('\(([^)]+)', body_text).group(1)

            body_text_list = ''.join(filter(whitelist_nums.__contains__, body_text_list)).split(',')
            for measurement in body_text_list:
                stats.append(measurement)

            stats.append(pos)
            csv_writer.writerow(stats)

        csv_file.close()
