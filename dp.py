# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
weather = [
    'HT', 'HT', 'Sunny', 'Storm', 'Sunny', 'HT', 
    'Storm', 'Sunny', 'HT', 'HT', 'Storm', 'HT', 
    'Sunny', 'HT', 'HT', 'HT', 'Storm', 'Storm', 
    'HT', 'HT', 'Sunny', 'Sunny', 'HT', 'Sunny', 
    'Storm', 'HT', 'Sunny', 'Sunny', 'HT', 'HT'
]
E = {
    1: [2, 25],
    2: [3],
    3: [2, 4, 25],
    4: [3, 5, 24, 25],
    5: [4, 6, 24],
    6: [5, 7, 23 ,24],
    7: [6, 8, 22],
    8: [7, 9, 22],
    9: [8, 10 ,15, 16, 17, 21, 22],
    10: [9, 11, 13, 15],
    11: [10, 12, 13],
    12: [11, 13, 14],
    13: [10, 11, 12, 14, 15],
    14: [12, 13, 15, 16],
    15: [9, 10, 13, 14, 16],
    16: [9, 14, 15, 17, 18],
    17: [9, 16, 18, 21],
    18: [16, 17, 19, 20],
    19: [18, 20],
    20: [18, 19, 21],
    21: [17, 20, 22, 23, 27],
    22: [7, 8, 9, 21, 23],
    23: [6, 21, 22, 24, 26],
    24: [4, 5, 6, 23, 25, 26],
    25: [3, 4, 24, 26],
    26: [23, 24, 25, 27],
    27: [21, 26]
}
V = 15
M = 12
N = len(E)
T = 30
# load_limit = 1200
load_limit = 200
# initial_money = 10000
initial_money = 2000
# bonus_income = 1000
bonus_income = 10000
quality = [3, 2]
price = [5, 10]
consumption = {
    'Sunny': [1, 2],
    'HT': [3 ,2],
    'Storm': [6, 6]
    # 'Sunny': [5, 7],
    # 'HT': [8 ,6],
    # 'Storm': [10, 10]
}
DP = {}

water_range = range(load_limit // quality[0] + 1)
food_range = lambda w: range((load_limit - w * quality[0]) // quality[1] + 1)

for d in range(T+1):
    for p in range(1, N+1):
        for w in water_range:
            for f in food_range(w):
                DP[(d,p,w,f)] = (float('-inf'), (), '', '', 0)
                


# %%
for w in water_range:
    for f in food_range(w):
        DP[(0,1,w,f)] = (initial_money - w * price[0] - f * price[1], (), '', '', w * quality[0] + f * quality[1])


# %%
for d in range(T):
    for p in range(1, N+1):
        if p == V:
            for w in water_range:
                for f in food_range(w):
                    capacity = load_limit - w * quality[0] - f * quality[1]
                    wb_range = range(capacity // quality[0] + 1)
                    fb_range = lambda w: range((capacity - w * quality[0]) // quality[1] + 1)
                    for wb in wb_range:
                        for fb in fb_range(wb):
                            key = (d, V, w + wb, f + fb)
                            if DP[(d,p,w,f)][0] - 2 * wb * price[0] - 2 * fb * price[1] >= 0                                 and DP[key][0] < DP[(d,p,w,f)][0] - 2 * wb * price[0] - 2 * fb * price[1]:
                                DP[key] = (
                                    DP[(d,p,w,f)][0] - 2 * wb * price[0] - 2 * fb * price[1], 
                                    (d,p,w,f), 
                                    'purchase', 
                                    'Village',
                                    w * quality[0] + f * quality[1]
                                )
        for w in water_range:
            for f in food_range(w):
                key = (d + 1, p, w - consumption[weather[d]][0], f - consumption[weather[d]][1])
                if w - consumption[weather[d]][0] >= 0 and f - consumption[weather[d]][1] >= 0:
                    if DP[key][0] < DP[(d,p,w,f)][0]:
                        DP[key] = (
                            DP[(d,p,w,f)][0], 
                            (d,p,w,f), 
                            'stay', 
                            weather[d],
                            w * quality[0] + f * quality[1]
                        )
        for w in water_range:
            for f in food_range(w):
                for p_prime in E[p]:
                    key = (d + 1, p_prime, w - 2 * consumption[weather[d]][0], f - 2 * consumption[weather[d]][1])
                    if w - 2 * consumption[weather[d]][0] >= 0 and f - 2 * consumption[weather[d]][1] >= 0: 
                        if DP[key][0] < DP[(d,p,w,f)][0]:
                            DP[key] = (
                                DP[(d,p,w,f)][0], 
                                (d,p,w,f), 
                                'go', 
                                weather[d],
                                w * quality[0] + f * quality[1]
                            )
        if p == M:
            for w in water_range:
                for f in food_range(w):
                    key = (d + 1, M, w - 3 * consumption[weather[d]][0], f - 3 * consumption[weather[d]][1])
                    if w - 3 * consumption[weather[d]][0] >= 0 and f - 3 * consumption[weather[d]][1] >= 0: 
                        if DP[key][0] < DP[(d,p,w,f)][0] + bonus_income:
                            DP[key] = (
                                DP[(d,p,w,f)][0] + bonus_income, 
                                (d,p,w,f), 
                                'mine', 
                                weather[d],
                                w * quality[0] + f * quality[1]
                            )


# %%
DP_end = {key: DP[key] for key in DP if key[1] == N}
maxIdx = max(DP_end, key=DP_end.get)
print(f'{maxIdx}: {DP_end[maxIdx]}')
prevKey = DP_end[maxIdx][1]
while len(prevKey) != 0:
    print(f'{prevKey}: {DP[prevKey]}')
    prevKey = DP[prevKey][1]


