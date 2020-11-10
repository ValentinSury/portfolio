# -*- coding: utf-8 -*-
import copy
import csv
import datetime
import decimal
import json
import re

from termcolor import cprint


def dead_end(dict_0):
    for unit in dict_0.values():
        if unit[0] == 'L' or unit[0] == 'H':
            return 'Y'


class Game:
    """ Класс реализующий игру. Игра построенная на json-файле, в котором содержаться лакации и монстры с необходимым
        временем для прохождения и поучаемым опытом. Суть игры - найти выход в json-файлле (Hatch), для этого
        необходимо найти выход, накопить минимаьное количество опыта и оставить необходимое количество времени."""

    def __init__(self):
        self.location = r'Location_B{0,1}\d{1,2}_tm\d{1,5}[.]{0,1}\d{0,12}'
        self.loc_time = r'm\d{1,5}[.]{0,1}\d{0,12}'
        self.mob_ex = r'p[0-9]{1,3}'
        self.mob_time = r'm[0-9]{1,8}'
        self.game_result_data = []
        self.field_names = ['current_location', 'current_experience', 'current_date']
        self.remaining_time = decimal.Decimal('123456.0987654321')
        self.experience = 0
        self.start_time = datetime.datetime.now()
        self.n = 0
        self.act_dict = {}
        self.x = 0
        self.act = ''
        self.location_from_json = []
        self.loaded_file = {}
        self.start_loc = None
        self.game_result_data_0 = {}
        self.exit_game = 0

    def open_json_file(self, file_name):
        """ Открытие обьектом класса json-файла"""

        with open(file_name) as json_file:
            self.loaded_file = json.load(json_file)
        json_str = json.dumps(self.loaded_file)
        self.start_loc = re.search(self.location, json_str)

    def start_game(self):
        """ Начало игры обьектом класса """

        self.game_result_data_0 = {self.field_names[0]: self.start_loc.group()}
        print(f'Вы находитесь в {self.start_loc.group()}')
        print(f'У вас {self.experience} опыта и осталось {self.remaining_time} секунд до наводнения')
        print(f'Прошло времени: {self.start_time - self.start_time}')
        loaded_file_copy = copy.deepcopy(self.loaded_file)
        self.location_from_json = loaded_file_copy[self.start_loc.group()]

    def actions(self):
        """ Действия, которое может сдеать игрок, обьекта класса """

        while self.location_from_json:
            print('Внутри вы видите:')
            self.n = 0
            self.act_dict = {}
            self.abilities()
            if dead_end(self.act_dict) != 'Y':
                print('Вы зашли в тупик')
                break
            print('Выберите действие:')
            self.choose()
            self.x = int(input())
            if self.x > len(self.act_dict) + 1 or self.x < 1:
                print('Такого варианта нет! Попробуйте еще раз')
                continue
            if self.x == self.exit_game:
                print('Вы решили отступить...')
                break
            self.act = self.act_dict[self.x]
            if self.act[0] == 'M' or self.act[0] == 'B':
                if not self.fight_with_monster():
                    break
            elif self.act[0] == 'L':
                if not self.go_new_location():
                    break
            else:
                required_time = decimal.Decimal((re.search(self.loc_time, self.act)).group()[1:])
                if self.experience >= 280 and required_time <= self.remaining_time:
                    self.location_from_json = self.location_from_json[self.x - 1][self.act]
                    cprint(self.location_from_json, color='cyan')
                    break
                else:
                    print('Вы не успели...')
                    break
            self.date_on_console()

    def abilities(self):
        """ Вывод информации, что может сделать игрок, обьектом класса """

        for elem in self.location_from_json:
            if isinstance(elem, str):
                self.n += 1
                print(f'— Монстра : {elem}')
                self.act_dict[self.n] = elem
            else:
                for key in dict(elem).keys():
                    self.n += 1
                    print(f'— Вход в локацию: {key}')
                    self.act_dict[self.n] = key

    def choose(self):
        """ Осуществления выбора обьектом класса """

        for key, value in self.act_dict.items():
            if value[0] == 'M' or value[0] == 'B':
                print(key, '- Убить моба ', value)
            else:
                print(f'{key} - Войти в локацию {value}')
        else:
            self.exit_game = (key + 1)
            print(self.exit_game, '- Сдаться и начать сначала')

    def date_on_console(self):
        """ Вывод информации обьекта класса """

        current_time = datetime.datetime.now()
        spend_time = (current_time - self.start_time)
        cprint(f' Потрачено времени {spend_time.seconds}:{spend_time.microseconds}', color='red')
        cprint(f' У вас {self.experience} опыта, осталось {self.remaining_time} времени', color='red')
        print('#' * 73)
        self.game_result_data_0[self.field_names[1]] = str(self.experience)
        self.game_result_data_0[self.field_names[2]] = f'{spend_time.seconds}:{spend_time.microseconds}'
        self.game_result_data.append(copy.deepcopy(self.game_result_data_0))
        print(self.game_result_data)

    def write_csv_file(self):
        """ Запись результат игры в csv-файл"""

        with open('game_data.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.field_names)
            for actions in self.game_result_data:
                writer = csv.DictWriter(csv_file, fieldnames=self.field_names, delimiter=',')
                writer.writerow(actions)

    def go_new_location(self):
        """ Переход игрока в новую локацию"""

        required_time = re.search(self.loc_time, self.act)
        required_time_0 = decimal.Decimal(required_time.group()[1:])
        if required_time_0 <= self.remaining_time:
            self.remaining_time -= required_time_0
            self.location_from_json = self.location_from_json[self.x - 1][self.act]
            self.game_result_data_0[self.field_names[0]] = self.act
            cprint(f'Вы находитесь в  {self.act}', color='yellow')
            return True
        else:
            print('У вас недостаточно времени что войти в локацию... Подземелье затопило... Вы погибли...')
            return False

    def fight_with_monster(self):
        """ Сражение с монстром"""

        exp = re.search(self.mob_ex, self.act)
        required_time = re.search(self.mob_time, self.act)
        required_time_0 = decimal.Decimal(required_time.group()[1:])
        self.experience += int(exp.group()[1:])
        if required_time_0 <= self.remaining_time:
            self.remaining_time -= required_time_0
            self.location_from_json.remove(self.act)
            cprint('Вы выбрали сражаться с монстром', color='yellow')
            return True
        else:
            print('У вас недостаточно времени что бы победить этого монстра... Вы пали смертью храбрых...')
            return False


while True:
    game = Game()
    game.open_json_file('rpg.json')
    game.start_game()
    game.actions()
    game.write_csv_file()
    if game.location_from_json == 'You are winner':
        break
    cprint('Ангел-хранитель про вас не забыл, вы оживаете и снова оказываетесь в пещере...', color='green')
