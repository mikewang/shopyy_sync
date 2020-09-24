import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from sklearn.linear_model import LinearRegression


def get_all_coefficient():
    begTime = time.time()
    csvfile = pd.read_csv('play_data32_200labelled.csv')
    df = pd.DataFrame(csvfile, columns=["player_id", "time_end", "mean", "solo"])
    df["time"] = pd.to_datetime(df["time_end"], format='%Y-%m-%d %H:%M:%S').astype(np.int64)
    df = df[["player_id", "time", "mean", "solo"]]
    df = df.sort_values(by=['player_id'])
    print("read csv time：", time.time() - begTime)
    player_list = []
    df_player_id = df["player_id"].unique()
    begTime = time.time()
    index = 1
    for player_id in df_player_id:
        begTime2 = time.time()
        df_player = df[(df["player_id"] == player_id)]
        X = df_player.iloc[:, 1:2].values
        # print(X)
        y = df_player.iloc[:, 2].values
        # print(y)
        # Visualising the Linear Regression results
        lin = LinearRegression()
        lin.fit(X, y)
        co = lin.intercept_
        solo_list = df_player.iloc[:, 3].values
        nums = len(solo_list)
        nums_solo = 0
        for solo in solo_list:
            if solo:
                nums_solo = nums_solo + 1
        pct = round(nums_solo*100/nums, 2)
        player_list.append([player_id, co, pct])
        if index%1000 == 0:
            print(index, "time：", time.time() - begTime2, player_id, co, pct)
        index = index + 1
    # print(player_list)
    print(index-1, "get all time：", time.time() - begTime)
    begTime = time.time()
    player_list_csv = pd.DataFrame(player_list, columns=['Player_id', 'Coefficient', 'Pct'])
    player_list_csv.to_csv('player_list.csv')
    print("write csv time：", time.time() - begTime)


def get_coefficient(player_id):
    begTime = time.time()
    csvfile = pd.read_csv('play_data32_200labelled.csv')
    df = pd.DataFrame(csvfile)
    df = df[(df["player_id"] == player_id)]
    df = df[["time_end", "mean"]]
    df["time"] = pd.to_datetime(df["time_end"], format='%Y-%m-%d %H:%M:%S').astype(np.int64)
    df = df[["time", "mean"]]
    df = df.sort_values(by=['time'])
    endTime = time.time()
    print("time：", endTime - begTime)
    X = df.iloc[:, 0:1].values
    # print(X)
    y = df.iloc[:, 1].values
    # print(y)
    # Visualising the Linear Regression results
    lin = LinearRegression()
    lin.fit(X, y)
    # print('intercept:', lin.intercept_)
    # Visualising the Linear Regression results
    plt.scatter(X, y, color='blue')
    plt.plot(X, lin.predict(X), color='red')
    plt.title('Linear Regression')
    plt.xlabel('Timing')
    plt.ylabel('Skill Level')
    plt.show()
    return lin.intercept_


def get_solo_percent(player_id):
    begTime = time.time()
    csvfile = pd.read_csv('play_data32_200labelled.csv')
    df = pd.DataFrame(csvfile, columns=["player_id", "solo"])
    df = df[(df["player_id"] == player_id)]
    # df = df.sort_values(by=['player_id'])
    player_list = []

    for i in range(0, len(df)):
        # print(df.iloc[i]['player_id'], df.iloc[i]['solo'])
        player_id = df.iloc[i]['player_id']
        solo = df.iloc[i]['solo']
        e_player = {}
        for player in player_list:
            if player["player_id"] == player_id:
                e_player = player
                break
        if "player_id" not in e_player:
            e_player["player_id"] = player_id
            e_player["nums"] = 1
            if solo:
                e_player["nums_solo"] = 1
            else:
                e_player["nums_solo"] = 0
            player_list.append(e_player)
        else:
            e_player["nums"] = e_player["nums"] + 1
            if solo:
                e_player["nums_solo"] = e_player["nums_solo"] + 1
        # print(e_player)
    endTime = time.time()
    print("time：", endTime - begTime)
    pct = round(player_list[0]["nums_solo"]*100/player_list[0]["nums"], 2)
    return pct


if __name__ == "__main__":
    get_all_coefficient()
    exit()
    coefficient = get_coefficient(75)
    print("coefficient", coefficient)
    pct = get_solo_percent(75)
    print("pct", pct)






