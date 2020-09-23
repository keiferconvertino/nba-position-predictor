from bs4 import BeautifulSoup
import requests
import csv
import io




def get_players(years):
    player_list = []
    with io.open('player_list.csv', 'w', newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['name', 'pos'])
        for year in range(years[0], years[1]):
            source = requests.get(f'https://www.basketball-reference.com/leagues/NBA_{str(year)}_per_game.html').text
            soup = BeautifulSoup(source, features='html.parser')
            table = soup.find('tbody')
            rows = table.find_all('tr',class_='full_table')
            for row in rows:
                name = row.find(attrs={"data-stat": 'player'})['csk']
                pos = row.find(attrs= {"data-stat": 'pos'}).text[:2]
                name_list=name.split(',')
                name_list.reverse()

                name = " ".join(name_list)

                if name not in player_list:
                    player_list.append(name)
                    csv_writer.writerow([name,pos])

                else:
                    continue
        csv_file.close()


# years=[2005,2019]
#
# get_players(years)