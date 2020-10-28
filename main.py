from ml import pos_predictor
from parse import parse_stats
from parse import parse_players
from time import sleep

filename_players = 'player_list.csv'
filename_stats = 'player_stats.csv'

print("Welcome to the NBA Position Predictor!")
sleep(1.5)
print("This program will allow you to predict the future NBA position of a college player!")
sleep(1.5)
print("You may train the model using data from all players who played between 1990 and 2020!\n")
sleep(1.5)
scraped = input("If you already have scraped the needed data, type 'yes', otherwise, type 'no':")

if scraped != 'yes':
    while True:

        print("\nSelect a range of historical data (between 1990 and 2020)")
        start_year = int(input("Start Year:"))
        if start_year > 2020 or start_year < 1990:
            print("Invalid start year")
            continue
        end_year = int(input("End Year:"))
        if end_year > 2020 or end_year < 1990:
            print("Invalid end year")
            continue
        break

    print("Scraping players...\n")
    parse_players.get_players([start_year, end_year])
    print("Done scraping players!\n")
    sleep(.2)
    print("Parsing stats...\n")
    parse_stats.get_stats(filename_players)
    print("Done parsing stats...\n")
    sleep(.2)

positionless = input("\nPredict PG/SG/SF/PF/C, or G/W/C? (Type 1 or 2):")
if positionless == '2':
    positionless = True
else:
    positionless = False

sleep(.2)
print("\nBuilding Models...\n")
X, y, sc, lc = pos_predictor.init_data(filename_stats, positionless)
m = pos_predictor.Model(X, y, sc, lc)
print("Models built!\n")
sleep(.2)
while True:
    player = input("Please select a player (enter 'q' to quit):")
    if player == 'q':
        break
    m.predict(player)
    sleep(1)


