# -*- coding: utf-8 -*-
from database_update import put_weather_in_db, take_weather_from_db
from parsing_weather import parsing_weather
from weather_image import image_maker


def parsing_weather_from_internet_current():
    weather_list = parsing_weather()
    for day in weather_list:
        print(day)


class WeatherPredictions:
    """ Класс создания прогноза погоды """

    def __init__(self):
        self.actions = {'1': 'добавить прогноз погоды за прошлую неделю в БД',
                        '2': 'получить прогноз погоды за прошлую неделю имеющиеся в БД',
                        '3': 'узнать прогноз на следующую неделю',
                        '4': 'создать открытку на выбранный день недели'}
        self.x = None
        self.weather_list_last_week = []
        self.act_functions = {'1': self.put_date,
                              '2': take_weather_from_db,
                              '3': parsing_weather_from_internet_current,
                              '4': self.create_image}

    def parsing_weather_from_internet_last_week(self):
        """ Парсинг погоды объектом класса """

        self.weather_list_last_week = parsing_weather('last')
        print('Прогноз погоды за прошлую неделю:')
        for day in self.weather_list_last_week:
            print(day)

    def choose_actions(self):
        """ Выбор дейтсвия объекта класса """

        print('Выберите действие:')
        for key, value in self.actions.items():
            print(f'{key} : {value}')
        self.x = input()

    def act(self):
        """ Действие объекта класса """

        if self.x in self.act_functions.keys():
            self.act_functions[self.x]()
        else:
            print('Такого варианта нет...')

    def put_date(self):
        """ Сохранение значений объектом класса в БД """

        put_weather_in_db(self.weather_list_last_week)
        print('прогноз погоды за прошлую неделю добавлен в БД')

    def create_image(self):
        """ Создание изображения объектом класса """

        print('Выбирите день недели:')
        weather_list = parsing_weather()
        weather_list_full = self.weather_list_last_week + weather_list
        for w, z in enumerate(weather_list_full):
            print(f'{w + 1} - {z["день недели"]} : {z["дата"]}')
        x = input()
        choose_day = weather_list_full[int(x) - 1]
        image_maker(choose_day)


def weather_predictions():
    """ Функция прогноза погоды """

    prediction = WeatherPredictions()
    prediction.parsing_weather_from_internet_last_week()
    prediction.choose_actions()
    prediction.act()


if __name__ == '__main__':
    weather_predictions()