from ml import pos_predictor
from parse import parse_stats
from parse import parse_players

filename_players = 'player_list.csv'
filename_stats = 'player_stats.csv'


while True:
    print("Select a range of historical data (between 1990 and 2020)")
    start_year = int(input("Start Year:"))
    if start_year > 2020 or start_year < 1990:
        print("Invalid start year")
        continue
    end_year = int(input("End Year:"))
    if end_year > 2020 or end_year < 1990:
        print("Invalid end year")
        continue
    break

print("Parsing players...")
parse_players.get_players([start_year, end_year])
print("Done parsing players!")
print("Parsing stats...")
parse_stats.get_stats(filename_players)
print("Done parsing stats...")

print("Building Models...")
X, y, sc, lc = pos_predictor.init_data(filename_stats)
m = pos_predictor.Model(X, y, sc, lc)
print("Models built!")
while True:
    player = input("Please select a player (enter 'q' to quit):")
    if player == 'q':
        break
    m.predict(player)


