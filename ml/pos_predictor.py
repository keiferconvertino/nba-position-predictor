import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from bs4 import BeautifulSoup
import requests
import re
from sklearn.model_selection import train_test_split


def init_data(filename):
    stats = pd.read_csv(filename, sep=',')
    stats = stats.dropna()
    X = stats.drop('POS',axis = 1)
    y = stats['POS']


    # Use internally to test models
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)

    sc = StandardScaler()
    # X_train = sc.fit_transform(X_train)
    # X_test = sc.fit_transform(X_test)
    X = sc.fit_transform(X_train)
    lc = LabelEncoder()
    y = lc.fit_transform(y_train)

    return X, y, sc, lc

class Model:

    def __init__(self, X, y, sc, lc):
        self.x = X
        self.y = y
        self.lc = lc
        self.sc = sc

        self.rfc = RandomForestClassifier(n_estimators=200)
        self.rfc.fit(X, y)

        self.clf = SVC()
        self.clf.fit(X, y)

        self.mlpc = MLPClassifier(hidden_layer_sizes=(12, 12, 12), max_iter=10000)
        self.mlpc.fit(X, y)

        # Chars to whitelist:
        self.whitelist_nums = '0123456789,'
        self.whitelist_chars = 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-'

        self.player = ''

    def name_format(self, name):
        player_str = name.replace('-', ' ')
        player_str = ''.join(filter(self.whitelist_chars.__contains__, player_str))
        player_str = player_str.replace(' ', '-').lower()
        self.player = player_str

    def get_stats(self, player):
        curr_player = 1
        # Stats to track:
        stats_to_track = ["fg2a_per_g", "fg2_pct", "fg3a_per_g", "fg3_pct", 'fta_per_g', 'ft_pct', 'trb_per_g',
                          'ast_per_g',
                          'stl_per_g', 'blk_per_g', 'tov_per_g']

        while True:
            # Go to college bball stat site

            source1 = requests.get(f'https://www.sports-reference.com/cbb/players/{player}-{curr_player}.html').text
            soup1 = BeautifulSoup(source1, features="html.parser")

            statline = soup1.find('tfoot')

            if statline is None:
                return None

            statline = statline.tr
            college = statline.find(attrs={"data-stat": 'school_name'}).text
            looking = input(f"Is {player} ({college}) who you are looking for (y/n)")
            if looking == 'n':
                curr_player += 1
                continue
            break
        stats = []

        # Grab each stat
        for stat in stats_to_track:
            try:
                if statline.find(attrs={"data-stat": f'{stat}'}).text == '':
                    stats.append('0')
                else:
                    stats.append(statline.find(attrs={"data-stat": f'{stat}'}).text)

            # If soup fails, exit
            except:
                return None
        # Grab height/weight measurements
        try:
            body_profile = soup1.find(id='meta').find('span', itemprop='height')

            body_text = body_profile.find_parent('p').text
        except:
            # If soup fails, exit

            return None

        # RegEx to grab height/weight in cm/kg
        body_text_list = re.search('\(([^)]+)', body_text).group(1)

        body_text_list = ''.join(filter(self.whitelist_nums.__contains__, body_text_list)).split(',')
        if len(body_text_list) != 2:
            stats.append(185)
            stats.append(92)
        else:
            for measurement in body_text_list:
                stats.append(measurement)

        return stats

    def predict(self, name):
        self.name_format(name)
        if self.player == '':
            print(f"Name ('{name}') invalid!")
            return
        stats = self.get_stats(self.player)
        if stats is None:
            print(f"Couldn't find ({self.player}'s) stats!")
            return
        stats = self.sc.transform([stats])
        # RFC
        pred_rfc = self.rfc.predict(stats)

        print(f'The Random Forest Classifier predicts that {self.player} will be a: {self.lc.inverse_transform(pred_rfc)[0]}')
        # SVC
        pred_clf = self.clf.predict(stats)
        print(f'The Support Vector Classifier predicts that {self.player} will be a: {self.lc.inverse_transform(pred_clf)[0]}')
        # NN
        # pred_nn = self.mlpc.predict(stats)
        # print(f'The Neural Network predicts that {self.player} will be a: {position[pred_nn]}')


# init_data('player_stats3.csv')
#
# rfc = RandomForestClassifier(n_estimators=200)
# rfc.fit(X_train, y_train)
# pred_rfc = rfc.predict(X_test)
#
# print(classification_report(y_test,pred_rfc))
#
# clf = SVC()
# clf.fit(X_train,y_train)
# pred_clf = clf.predict(X_test)
#
# print(classification_report(y_test,pred_clf))
#
# mlpc = MLPClassifier(hidden_layer_sizes=(12,12,12),max_iter=10000)
# mlpc.fit(X_train,y_train)
# pred_mlpc = mlpc.predict(X_test)
#
# print(classification_report(y_test,pred_mlpc))
