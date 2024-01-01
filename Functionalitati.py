import pandas as pd
import numpy as np
import re


def convert_money(value):
    value = value.replace(",", " ")
    money = int("".join(value.split(" ")[:-1]))
    if value.split(" ")[-1] == "RON":
        money = round(money / 5)
    return money


def convert_area(value):
    value = value.replace(",", ".")
    area = float("".join(value.split(" ")[0]))
    return area


def number_of_floors(value):
    new_value = None
    if value in [np.nan]:
        new_value = np.nan
    elif "/" in value:
        new_value = value.split("/")[1]
    else:
        new_value = np.nan
    return new_value


def apartment_floor(value):
    new_value = None
    if value in [np.nan]:
        new_value = value
    else:
        new_value = re.sub('[<>!,.?*]', "", value.split("/")[0])
        new_value = new_value.strip()
    return new_value


def get_year(value, text):
    new_value = value
    if value in [np.nan]:
        new_values = re.findall("[0-2][0-9][0-9][0-9]", text)
        if new_values == []:
            new_value = np.nan
        else:
            for val in new_values:
                if int(val) < 1900:
                    continue
                else:
                    new_value = val
                    break
    return new_value


def parcare_or_garaj(value, text):
    new_value = value
    if text not in [np.nan]:
        text = text.lower()
        words_list = ["garaj", "parcare"]
        if value in [np.nan]:
            for word in words_list:
                if word in text:
                    new_value = word
                    break
    return new_value


def building_floors(value, text):
    new_value = value
    flag = 0
    forms = ["\s[0-9][0-9]/[0-9][0-9]\s", "\s[0-9]/[0-9][0-9]\s", "\s[0-9]/[0-9]\s", "parter/[0-9][0-9]",
             "parter/[0-9]", "demisol/[0-9][0-9]",
             "demisol/[0-9]", "mansardă/[0-9][0-9]", "mansardă/[0-9]", "mansarda/[0-9][0-9]", "mansarda/[0-9]"]
    forms_2 = ['[0-9][0-9] etaje', '[0-9] etaje', '[0-9][0-9] nivele', '[0-9] nivele']
    forms_3 = ['etajul\s[0-9][0-9]/[0-9][0-9]', 'etajul\s[0-9]/[0-9][0-9]', "etajul\s[0-9]/[0-9]",
               'etajul\s[0-9][0-9]\sdin\s[0-9][0-9]',
               'etajul\s[0-9]\sdin\s[0-9][0-9]', "etajul\s[0-9]\sdin\s[0-9]", "etaj\s[0-9][0-9]/[0-9][0-9]",
               "etaj\s[0-9]/[0-9][0-9]",
               "etaj\s[0-9]/[0-9]", 'etaj\s[0-9][0-9]\sdin\s[0-9][0-9]', 'etaj\s[0-9]\sdin\s[0-9][0-9]',
               "etaj\s[0-9]\sdin\s[0-9]"]
    forms_4 = ['etajul\s[0-9][0-9]', 'etajul\s[0-9]']
    if text not in [np.nan]:
        text = text.lower()
    if (value in [np.nan]) or ("/" not in value):
        flag = 0
        for form in forms:
            new_values = re.findall(form, text)
            if len(new_values) > 0:
                new_value = new_values[0]
                flag = 1
                new_value = new_value.strip()
                break
        if flag == 0:
            for form in forms_3:
                new_values = re.findall(form, text)
                if len(new_values) > 0:
                    new_value = new_values[0].replace(' din ', '/')
                    new_value = new_value.split(" ")[1]
                    new_value = new_value.strip()
                    break
    if (new_value not in [np.nan]) and ("/" not in new_value):
        flag = 0
        for form in forms_2:
            new_values = re.findall(form, text)
            if len(new_values) > 0:
                flag = 1
                new_value = value + "/" + new_values[0].split(" ")[0]
                new_value = new_value.strip()
                break
    if (flag == 0) and (new_value in [np.nan]):
        for form in forms_4:
            new_values = re.findall(form, text)
            if len(new_values) > 0:
                new_value = new_values[0].split(" ")[1]
                new_value = new_value.strip()
                break

    return new_value


def set_max_floor(current_floor, max_floor, mode_mansarda):
    new_max = max_floor
    if (current_floor == 'mansardă') and (max_floor ==0):
        new_max = mode_mansarda
    elif (current_floor == "parter") or (current_floor == "demisol") or (current_floor == 'mansardă'):
        pass
    elif int(current_floor) > int(max_floor):
        new_max = current_floor
    return new_max


def dangerous_building(year, max_floor):
    status = None
    year = int(year)
    max_floor = int(max_floor)
    if (year <= 1977) and (max_floor > 5):
        status = "Cade"
    elif (year <= 1977) or (max_floor > 5):
        status = "Te simti norocos?"
    else:
        status = "Sigur"
    return status


def city_zone(zone_value):
    zone_value = zone_value.split(",")
    if "iasi" in zone_value[-2].lower():
        if len(zone_value) == 4:
            zone = zone_value[1]
        else:
            zone = zone_value[0]
    else:
        if len(zone_value) >= 3:
            zone = zone_value[1]
        else:
            zone = zone_value[0]
    return zone.strip()


def year_mode(zone_value, year_value, df):
    if year_value == 0:
        zone_mode = df[df['Zona Oras'] == zone_value]['Anul construcției'].mode().to_list()[0]
    else:
        zone_mode = year_value
    return zone_mode
