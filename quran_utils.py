import json

import requests


# generate data

def gen_ayat_count(surah_num):
    response = requests.get(f"https://api.quran.com/api/v4/chapters/{surah_num}?language=en").json()
    count = response["chapter"]["verses_count"]
    return count


def gen_ayat_word_counts(surah, ayah):
    response = requests.get(f"https://api.quran.com/api/v4/verses/by_key/{surah}:{ayah}?language=en&words=true").json()
    count = len(response["verse"]["words"]) - 1
    print(surah, ayah)
    return count


def gen_surah_name(surah_num):
    response = requests.get(
        f"https://api.quran.com/api/v4/chapters/{surah_num}?language=en"
    ).json()
    name = response["chapter"]["name_simple"]
    return name


def gen_data():
    data = {"surahs": []}
    for i in range(1, 115):
        data["surahs"].append({
            "num": i,
            "name": gen_surah_name(i),
            "ayat_count": gen_ayat_count(i),
            "ayat_word_counts": []
        })
        for j in range(1, data["surahs"][i - 1]["ayat_count"] + 1):
            data["surahs"][i - 1]["ayat_word_counts"].append(gen_ayat_word_counts(i, j))
    return data


# manipulate files

def write_to_file(data, filename, to_indent=False):
    with open(filename, "w") as outfile:
        if to_indent:
            json.dump(data, outfile, indent=4)
        else:
            json.dump(data, outfile)


def load_json(filename):
    with open(filename) as json_file:
        return json.load(json_file)


# track memorisation

def surah_num_to_name(num, surahs_data):
    return surahs_data[num - 1]["name"]


def calc_end(logbook, surahs_data):
    words_left = logbook["target_words"]
    surah_index = logbook["surah"] - 1
    ayah_index = logbook["ayah"]
    while words_left > 0:
        ayah_index += 1
        if ayah_index >= surahs_data[surah_index]["ayat_count"]:
            surah_index += 1
            ayah_index = 0
        words_left -= surahs_data[surah_index]["ayat_word_counts"][ayah_index]
    return [surahs_data[surah_index]["num"], ayah_index + 1]


def calc_start(logbook, surahs_data):
    start = [logbook["surah"], logbook["ayah"] + 1]
    if start[1] > surahs_data[logbook["surah"] - 1]["ayat_count"]:
        start[0] += 1
        start[1] = 1
    return start


def print_target(logbook, surahs_data):
    start = calc_start(logbook, surahs_data)
    end = calc_end(logbook, surahs_data)
    print(
        f'From {surah_num_to_name(start[0], surahs_data)}:{start[1]} to {surah_num_to_name(end[0], surahs_data)}:{end[1]}')


def update_logbook(section, logbook, surahs_data, filename):
    updated = calc_end(logbook[section], surahs_data)
    logbook[section]["surah"] = updated[0]
    logbook[section]["ayah"] = updated[1]
    write_to_file(logbook, filename, True)


# console user interface

def print_ayah_range(section, logbook, surahs_data):
    print('--------')
    print(section.upper())
    print('--------')
    print_target(logbook[section], surahs_data)
    print()
