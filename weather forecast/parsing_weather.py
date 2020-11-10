import requests
from bs4 import BeautifulSoup
import re
import copy

temperature_re = r'[+][0-9]{1,3}'

weather_list = []
weather_dict = {}
weather_list_last_week = []


def parsing_weather(param=None):
    """ Парсинг значений погоды с сайта yandex.ru """

    if param == 'last':
        list_0 = weather_list_last_week
        a = 0
        b = 4
    else:
        list_0 = weather_list
        a = 4
        b = 12
    response = requests.get('https://yandex.ru/pogoda/moscow')
    html_doc = BeautifulSoup(response.text, features='html.parser')
    list_of_day_temperature = html_doc.find_all(class_='temp forecast-briefly__temp forecast-briefly__temp_day')
    list_of_week_day = html_doc.find_all(class_='forecast-briefly__name')
    list_of_condition = html_doc.find_all(class_='forecast-briefly__condition')
    list_of_dates = html_doc.find_all(class_="time forecast-briefly__date")
    for week_day, temp, condition, date in zip(list_of_week_day[a:b], list_of_day_temperature[a:b],
                                               list_of_condition[a:b], list_of_dates[a:b]):
        day_temperature = re.search(temperature_re, temp.text)
        weather_dict['день недели'] = week_day.text
        weather_dict['температура'] = day_temperature.group()
        weather_dict['погода'] = condition.text
        weather_dict['дата'] = date.text
        list_0.append(copy.deepcopy(weather_dict))
    return list_0
