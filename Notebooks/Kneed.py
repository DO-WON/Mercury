import pandas as pd
from kneed import KneeLocator
import matplotlib.pyplot as plt
import seaborn as sns
from bisect import bisect_left

# [1] Old X (Before rescaling)
aggregate_df2 = pd.read_csv('/Users/dowonkim/PycharmProjects/pythonProject2/Mercury/aggregate_df2.csv')
aggregate_df2.head()
agg_old_x = aggregate_df2["old_x"]
agg_old_y = aggregate_df2["y_old"]
agg_new_y = aggregate_df2["y_new"]


# Find knee
# 1) Old X, Old Y
kneedle_old_xy = KneeLocator(agg_old_x, agg_old_y,
                             S=1.0, curve="concave", direction="increasing",
                             interp_method="polynomial")   # default polynomial degree (=7) works the best

print(round(kneedle_old_xy.knee, 3))     # 11414 (Sensitivity doesn't change results)
print(round(kneedle_old_xy.knee_y, 3))   # 0.522

# Normalized data, normalized knee, and normalized distance curve.
kneedle_old_xy.plot_knee_normalized()

# Raw data and knee.
kneedle_old_xy.plot_knee()


# without polynomial interpolation (default)
kneedle_old_xy_def = KneeLocator(agg_old_x, agg_old_y,
                                 S=2500, curve="concave", direction="increasing")
# Sensitivity makes differences
print(round(kneedle_old_xy_def.knee, 3))   # (S=1) 345; (S=2500) 1485
print(round(kneedle_old_xy_def.knee_y, 3))   # (S=1) 0.375; (S=2500) 0.484

# Normalized data, normalized knee, and normalized distance curve.
kneedle_old_xy_def.plot_knee_normalized()

# Raw data and knee.
kneedle_old_xy_def.plot_knee()


# 2) Old X, New Y
kneedle_oldx_newy = KneeLocator(agg_old_x, agg_new_y,
                                S=1.0, curve="concave", direction="increasing",
                                interp_method="polynomial")

print(round(kneedle_oldx_newy.knee, 3))   # 24029 (Sensitivity doesn't change results)
print(round(kneedle_oldx_newy.knee_y, 3))   # 0.905

kneedle_oldx_newy.plot_knee_normalized()
kneedle_oldx_newy.plot_knee()


# what if I change polynomial degree (default=7)
kneedle_oldx_newy_deg = KneeLocator(agg_old_x, agg_new_y,
                                    S=1.0, curve="concave", direction="increasing",
                                    interp_method="polynomial", polynomial_degree=5)

print(round(kneedle_oldx_newy_deg.knee, 3))   # 23064
print(round(kneedle_oldx_newy_deg.knee_y, 3))    # 0.899

kneedle_oldx_newy_deg.plot_knee_normalized()
kneedle_oldx_newy_deg.plot_knee()

# without polynomial interpolation (default)
kneedle_oldx_newy_def = KneeLocator(agg_old_x, agg_new_y,
                                    S=1000, curve="concave", direction="increasing")

# Sensitivity makes differences
print(round(kneedle_oldx_newy_def.knee, 3))   # (S=1) 75; (S=1000) 800
print(round(kneedle_oldx_newy_def.knee_y, 3))    # (S=1) 0.348; (S=1000) 0.673

kneedle_oldx_newy_def.plot_knee_normalized()
kneedle_oldx_newy_def.plot_knee()


# Let's tune sensitivity parameter S:
sensitivity = [0.1, 1, 100, 1000, 2000]
knees = []
kl = []
norm_knees = []

for s in sensitivity:
    kl = KneeLocator(agg_old_x, agg_new_y,
                     curve="concave", direction="increasing",
                     S=s)
    knees.append(kl.knee)
    norm_knees.append(kl.norm_knee)

print(knees)
print([nk.round(3) for nk in norm_knees])

sns.set_style('ticks')
plt.figure(figsize=(10, 6))
plt.plot(kl.x_normalized, kl.y_normalized)
plt.plot(kl.x_difference, kl.y_difference)
colors = ["r", "g", "k", "m", "c", "orange"]
for k, c, s in zip(norm_knees, colors, sensitivity):
    plt.vlines(k, 0, 1, linestyles="--", colors=c, label=f"S = {s}")
plt.legend()
# Hence, S=1000 for kneedle_oldx_newy_def


# [2] Individual plots
df2 = pd.read_csv('/Users/dowonkim/PycharmProjects/pythonProject2/Mercury/df2.csv')

df2_by_user = df2.groupby('user_id')

listed_by_user = list(df2_by_user)

len(listed_by_user)
# 53 users left after removing whose max_friends_count =< 10

# just take each user and test:
knee_user0 = KneeLocator(listed_by_user[0][1]["old_x"], listed_by_user[0][1]["new_y"],
                         S=1.0, curve="concave", direction="increasing", interp_method="polynomial")
print(round(knee_user0.knee, 3))        # 470905.252
print(round(knee_user0.knee_y, 3))      # 0.90

# let's see another user
knee_user52 = KneeLocator(listed_by_user[52][1]["new_x"], listed_by_user[52][1]["new_y"],
                          S=100, curve="concave", direction="increasing", interp_method="polynomial")
print(round(knee_user52.knee, 3))       # 145705.698
print(round(knee_user52.knee_y, 3))     # 0.893
knee_user52.plot_knee()

# Thresholds: 70, 80, 90% of (low quality) friends seen seen...
# ...(1) among all friends (old_y);
# ...(2) among those are appeared in the timelines (new_y).
# Make a function where we change sensitivity and pick the one that maximizes the knee_y (or get closer to 0.9)
# Make the same function but the target knee_y = 0.8
# Make the same function but the target knee_y = 0.7

user_ids = []
sensitivity = [1, 100, 1000, 2000]
kns = []

for ls in range(len(listed_by_user)):
    user_id = listed_by_user[ls][0]
    user_ids.append(user_id)

    for s in sensitivity:
        knee_y = KneeLocator(listed_by_user[ls][1]["old_x"], listed_by_user[ls][1]["new_y"],
                             S=s, curve="concave", direction="increasing", interp_method="polynomial").knee_y
        knee = KneeLocator(listed_by_user[ls][1]["old_x"], listed_by_user[ls][1]["new_y"],
                           S=s, curve="concave", direction="increasing", interp_method="polynomial").knee
        kl = (knee, knee_y, ls, s)
        kns.append(kl)

df_kns = pd.DataFrame(list(kns))
df_kns = df_kns.rename(columns={0: "knee", 1: "knee_y", 2: "user_code", 3: "sensitivity"})

df_kns.to_csv('/Users/dowonkim/PycharmProjects/pythonProject2/Mercury/df_kns.csv')

# define a function that captures the closest element to value K in the list
def take_closest(mylist, mynumber):
    """
    Assumes mylist is sorted. Returns closest value to mynumber.
    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(mylist, mynumber)
    if pos == 0:
        return mylist[0]
    if pos == len(mylist):
        return mylist[-1]
    before = mylist[pos - 1]
    after = mylist[pos]
    if after - mynumber < mynumber - before:
        return after
    else:
        return before


take_closest(df_kns["knee_y"], 0.9)   # per user_code

###
# df_knee = pd.DataFrame({
#    "user_id": pd.Series(user_ids, name="user_id"),
#    "knee": pd.Series(knees, name="knee"),
#    "knee_y": pd.Series(knee_ys, name="knee_y")})

# print(df_knee)

# df_knee.to_csv('df_knee.csv')


########## IGNORE FROM HERE:

# [3] replicate with low-quality sources as y-axis
# lowq_df_only21.csv ; lowq_df2.csv
lowq_df_only21 = pd.read_csv('/Users/dowonkim/PycharmProjects/pythonProject2/Mercury/lowq_df_only21_agg.csv')

lowq_df_only21.head()
agg_old_x = lowq_df_only21["old_x"]
agg_old_y = lowq_df_only21["agg_y_old"]
agg_new_y = lowq_df_only21["agg_y_new"]


# test:
knee_test = KneeLocator(agg_old_x, agg_old_y,
                        S=1000, curve="concave", direction="increasing")
knee_test.plot_knee()
print(round(knee_test.knee, 3))        # 470905.252
print(round(knee_test.knee_y, 3))      # 0.90

# let's see another user
knee_user20 = KneeLocator(listed_by_21user[20][1]["new_x"], listed_by_21user[20][1]["new_y"],
                          S=100, curve="concave", direction="increasing", interp_method="polynomial")
print(round(knee_user20.knee, 3))       # 145705.698
print(round(knee_user20.knee_y, 3))     # 0.893
knee_user20.plot_knee()