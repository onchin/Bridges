import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
# import statsmodels.api as sm
import seaborn as sns
sns.set()


study_year_begin = 2013
indexes = [1, 2, 3, 4, 5]
show_index = ('year built is 28/26', 'year of improvement is 97/95', 'year reconstructed is 107/105')
ages = list(range(1, 101))
count_exits = [[]]
exposure_count = [[]]
count = 0
bridge_data = {}
hazard_age_list = [[]]


def import_data():
    """
    import bridge data and store as dataframe, then convert to list of lists
    :return: bridges_list List of Lists
    """
    bridges = pd.read_excel('bridges/2017HwyBridgesDelimitedAllStates.xlsx', dtype=str)
    bridges_list = bridges.values.tolist()
    bridges_list2 = [[]]
    for inside_list in bridges_list:
        inside_list = [item.strip(' ') for item in inside_list]
        bridges_list2.append(inside_list)
    del bridges_list2[0]
    bridge_data["data"] = bridges_list2
    # print(bridge_data["data"])
    return bridges_list2


def calc_age(current_study_yr, construction_year, reconstruct_yr):
    """
    by setting the age to 0 in the elif clause, the bridge has effectively been removed from the study
    the age can be reset by setting age to (current_study_yr - reconstruct_yr)
    :return: the age of the bridge
    """
    if reconstruct_yr >= current_study_yr:
        age = current_study_yr - construction_year
    elif reconstruct_yr > construction_year:
        age = 0
    else:
        age = current_study_yr - construction_year
    return age


def calc_ages():
    """
    this function creates the list of bridges and the ages of the bridge in each year of the study
    :return: a list of lists containing the raw exposure data
    """
    bridge_data = import_data()
    exposure_data = [[]]

    for bridge in bridge_data:
        inner_list = []
        inner_list.append(bridge[1])
        inner_list.append(bridge[105])
        for index in indexes:
            age = calc_age(int(study_year_begin) + index - 1, int(bridge[26]), int(bridge[105]))
            inner_list.append(age)
        exposure_data.append(inner_list)
    return exposure_data


output = calc_ages()
# for item in output:
#     print(item)

"""
calculate the total exposure for each age
"""
for age in ages:
    exposures = []
    count = 0
    exposures.append(age)
    for item in output:
        for index in item:
            if index == age:
                count += 1
    exposures.append(count)
    exposure_count.append(exposures)

# print(exposure_count)


def exits():
    for age in ages:
        exits = []
        count = 0
        exits.append(age)
        pos = [3, 4, 5, 6]
        for item in output:
            if item == []:
                continue
            else:
                for i in pos:
                    if item[i] == 0 and item[i - 1] > 0 and item[i - 1] == age - 1:
                        count += 1
        exits.append(count)
        count_exits.append(exits)
    # for item in count_exits:
    #     print(item)
    return count_exits


def compute_hx():
    """
    ratio of exits() to calc_ages()
    :return: the hazard rate for a bridge at each age
    """
    leave = exits()
    exposed = exposure_count
    for age in exposed:
        if age == []:
            continue
        temp = [age[0]]
        for item in leave:
            if item == []:
                continue
            elif age[0] == item[0]:
                if age[1] == 0:
                    num = 0
                else:
                    num = item[1]/age[1]
                temp.append(num)
        hazard_age_list.append(temp)
    return hazard_age_list


def compute_qx():
    hx = compute_hx()
    qx = [[]]
    for i in hx:
        temp = []
        if i == []:
            continue
        temp.append(i[0])
        sx = math.exp(-i[1])
        pdf = 1 - sx
        temp.append(pdf)
        qx.append(temp)
    return qx


def cum_qx():
    qx = compute_qx()
    cum = [[]]
    running = 0
    for item in qx:
        if item == []:
            continue
        temp = []
        temp.append(item[0])
        running += item[1]
        temp.append(running)
        cum.append(temp)
    return cum


see = cum_qx()
# for item in see:
#     print(item)


x = []
y = []
for item in see:
    if item == []:
        continue
    x.append(item[0])
    y.append(item[1])

plt.plot(x, y)
plt.xlabel('AGES')
plt.ylabel('PROB OF FAILURE')
plt.show()
