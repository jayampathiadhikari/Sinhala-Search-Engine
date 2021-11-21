# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from urllib import parse
import pandas as pd
import json
import codecs
from mtranslate import translate

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

page = requests.get("https://en.wikipedia.org/wiki/List_of_Sri_Lankan_actors")
soup = BeautifulSoup(page.content, 'html.parser')
urls = soup.find_all("a")

actors = []
for url in urls:
    if (url.get_text() == url.get('title')):
        actors.append(url.attrs)


def remove_cite(string):
    stripped = re.sub('\[\d+\]', '', string)
    return stripped


def get_active_years_vital_status(soup):
    vital_status = "ජීවතුන් අතර"
    years_active = ""
    active_tag = soup.find("table", {"class": "infobox biography vcard"})
    try:
        next_td_tag = active_tag.findNext()
        children = active_tag.findChildren("th", recursive=True)
        for child in children:
            if ("Years" in child.text and "active" in child.text):
                next_td_tag = child.findNext()
                if re.search('[a-zA-Z]', next_td_tag.text.strip()):
                    years_active = translate(next_td_tag.text.strip(), 'si')
                else:
                    years_active = next_td_tag.text.strip()
            if "Died" in child.text:
                vital_status = "මියගිය"
        return years_active, vital_status
    except Exception as e:
        print('ERROR get active years', e)
        return years_active, ""


def get_career(soup):
    career = ''
    try:
        career_tag = soup.find("span", {"id": "Career"}) or soup.find("span", {"id": "Drama_career"}) or soup.find(
            "span", {"id": "Theater_career"}) or soup.find("span", {"id": "Acting_career"}) or soup.find("span", {
            "id": "Cinema_career"}) or soup.find("span", {"id": "Theatre_career"}) or soup.find("span", {
            "id": "Theater_work"}) or soup.find("span", {"id": "Film_career"}) or soup.find("span",
                                                                                            {"id": "Golden_career"})
        if (career_tag):
            h2_1 = career_tag.parent
            next_td_tag = h2_1.findNext()
            while (True):
                next_td_tag = next_td_tag.findNext()
                if (next_td_tag.name == "p"):
                    stripped = re.sub('\[\d+\]', '', next_td_tag.text.strip())
                    translated = translate(stripped, 'si')
                    career += translated + '\n'
                if (next_td_tag.name == "h2"):
                    break
            return career
        else:
            return career
            print('NO CAREER TAG')
    except Exception as e:
        print('ERROR get career', e)
        return career


def get_bio(soup):
    bio = ''
    try:
        bio_tag = soup.find("span", {"id": "Biography"}) or soup.find("span", {"id": "Family"}) or soup.find("span", {
            "id": "Background"}) or soup.find("span", {"id": "Personal_life"}) or soup.find("span", {
            "id": "Family_background"}) or soup.find("span", {"id": "Early_life"}) or soup.find("span", {
            "id": "Personal_life_and_early_life"})
        if (bio_tag):
            h2_1 = bio_tag.parent
            next_td_tag = h2_1.findNext()
            while (True):
                next_td_tag = next_td_tag.findNext()
                if (next_td_tag.name == "p"):
                    stripped = re.sub('\[\d+\]', '', next_td_tag.text.strip())
                    translated = translate(stripped, 'si')
                    bio += translated
                if (next_td_tag.name == "h2"):
                    break
            return bio
        else:
            print('NO BIO TAG')
            return bio
    except Exception as e:
        print('ERROR get bio', e)
        return bio


def get_films(soup):
    films = []
    try:
        films_tag = soup.find("span", {"id": "Filmography"}) or soup.find("span",
                                                                          {"id": "Filmography_and_stunt_coordination"})
        if (films_tag):
            h2_1 = films_tag.parent
            next_td_tag = h2_1.findNext()
            # table = soup.find("table",{"class": "wikitable"})
            year_index = 0
            name_index = 1

            while (True):
                next_td_tag = next_td_tag.findNext()
                if (next_td_tag.name == "tr"):
                    listf = next_td_tag.text.strip().split('\n')

                    if ("Year" in listf):
                        if ("No." in listf):
                            year_index = 0
                            name_index = 4
                        else:
                            year_index = 0
                            name_index = 1
                        pass

                    year = listf[year_index]
                    if (year.isnumeric()):
                        name = listf[name_index]
                        film = {}
                        si_name = translate(name, 'si')
                        film["year"] = year
                        film["name"] = si_name
                        films.append(film)
                    else:
                        pass
                if (next_td_tag.name == "h2"):
                    break
            return films
        else:
            print('NO FILMOGRAPHY TAG')
            return films
    except Exception as e:
        print('ERROR get films', e)
        return films


def get_awards(soup):
    awards = []
    try:
        if (len(soup.findAll("span", {"id": "Awards_and_accolades"})) > 0 or len(
                soup.findAll("span", {"id": "Awards"})) > 0):
            tables = soup.findAll("table", {"class": "wikitable plainrowheaders"})
            for table in tables:
                trs = table.findAll("tr")
                for tr in trs:
                    # if year get indexes

                    splitted = tr.text.strip().split("\n")

                    film_index = 1
                    award_index = 2

                    if ("Year" in splitted):
                        if ("No." in splitted):
                            film_index = 2
                            award_index = 3
                        else:
                            film_index = 1
                            award_index = 2
                        pass

                    year = splitted[0]
                    if (year.isnumeric()):
                        award = {}
                        film = splitted[film_index]
                        si_name = translate(film, 'si')
                        award_name = remove_cite(splitted[award_index])
                        si_award = translate(award_name, 'si')
                        if (year == "" or si_name == "" or si_award == ""):
                            pass
                        else:
                            award["year"] = year
                            award["film"] = si_name
                            award["name"] = si_award
                            awards.append(award)
                    else:
                        pass

            return awards
        else:
            return awards
    except Exception as e:
        print('ERROR', e)
        return awards


def get_gender(bio, career):
    fm = bio.count('ඇය') + career.count('ඇය')
    m = bio.count('ඔහු') + career.count('ඔහු')
    if (fm > m):
        return "ගැහැණු ස්ත්‍රී කාන්තා නිලිය නිළිය"
    else:
        return "පිරිමි පුරුෂ නලුව නළුව"


def fetch_data(actor_array, name):
    try:
        new_actors = []
        for actor in actor_array:
            page = requests.get("https://en.wikipedia.org" + actor.get('href'))
            soup = BeautifulSoup(page.content, 'html.parser')
            career = get_career(soup)
            bio = get_bio(soup)
            films = get_films(soup)
            awards = get_awards(soup)
            active_years, vital_status = get_active_years_vital_status(soup)
            if (bio == '' or career == '' or len(films) == 0):
                print('PASSED', actor['title'])
                pass
            else:
                actor['career'] = career
                actor['bio'] = bio
                actor['films'] = films
                actor['awards'] = awards
                actor['gender'] = get_gender(bio, career)
                actor['active_years'], actor['vital_status'] = active_years, vital_status
                # si_name = translate(actor['title'], 'si')
                # actor['name'] = si_name
                new_actors.append(actor)

        print('CORPUS SIZE', len(new_actors))
        json.dump(new_actors, open("/content/drive/MyDrive/IR Project/" + name + ".json", "w", encoding='utf8'),
                  ensure_ascii=False, indent=4)

    except Exception as e:
        print('FETCH DATA ERROR', e)
