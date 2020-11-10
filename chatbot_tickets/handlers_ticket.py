import re
from copy import deepcopy
from operator import itemgetter

import settings_ticket

re_city = r'[Мм]оскв\w{,1}|[Лл]ондон\w{,1}'
re_date = r'\d{2}-\d{2}-\d{4}'
re_phone_number = r'[0-9]{10}'


def handler_city_start(text, context):
    """ Функция-обработчик введенного пользователем города отправления """

    match = re.match(re_city, text)
    context['cities'] = deepcopy(settings_ticket.CITIES)
    if match:
        context['city_start'] = text.lower()
        elem = [city for city in settings_ticket.CITIES if city[:4].lower() == context['city_start'][:4]]
        if elem[0] in context['cities']:
            pass
            context['cities'].remove(elem[0])
        return True
    else:
        return False


def handler_city_finish(text, context):
    """ Функция-обработчик введенного пользователем города прибытия """

    match = re.match(re_city, text)
    if match:
        if text[:4].lower() == context['city_start'][:4]:
            return False
        else:
            context['city_finish'] = text.lower()
            return True
    else:
        return False


def handler_date(text, context):
    """ Функция-обработчик введенной пользователем даты отправления """

    match = re.match(re_date, text)
    if match:
        context['date'] = text
        return True
    else:
        return False


def handler_fly(text, context):
    """ Функция-обработчик выбраного пользователем рейса """

    if text.isdigit():
        if 0 < int(text) <= len(context['fly_list']):
            context['number_fly'] = '{}-{}-{}'.format(*context['fly_list'][int(text) - 1])
            return True
        else:
            return False
    else:
        return False


def handler_sits(text, context):
    """ Функция-обработчик введенного пользователем количества мест """

    if 1 <= int(text) <= 5:
        context['sits'] = text
        return True
    else:
        return False


def handler_comment(text, context):
    """ Функция-обработчик введенного пользователем коментария """

    context['comment'] = text
    return True


def handler_correct_data(text, context):
    """ Функция-обработчик введенной пользователем коректности даты  """

    if text == 'да':
        return True
    elif text == 'нет':
        return 'No'
    else:
        return False


def handler_phone_number(text, context):
    """ Функция-обработчик введенного пользователем номера телефона """

    match = re.match(re_phone_number, text)
    if match:
        context['number'] = text
        return True
    else:
        return False


def dispatcher(city_start, city_finish, date, context):
    """ Функция подбирающая пользователю подходящий рейс по его введенным данным """

    choose_fly = ''
    fly_list = []
    city_path = city_start[:4] + '-' + city_finish[:4]
    schedule = context['fly_list'][city_path]
    for fly in schedule:
        if fly[0:2] >= date[0:2] and fly[3:5] >= date[3:5] and fly[6:] >= date[6:]:
            fly_list.append([fly[0:2], fly[3:5], fly[6:]])
    fly_list = sorted(fly_list, key=itemgetter(2, 1, 0))
    context['fly_list'] = fly_list
    if not fly_list:
        return 'Рейсов нет, попробуйте заново'
    else:
        for number, fly in enumerate(fly_list):
            choose_fly += f'{number + 1} - {fly[0]}-{fly[1]}-{fly[2]}\n'
        return f' Выбирите подходящий вам рейс: \n {choose_fly}'
