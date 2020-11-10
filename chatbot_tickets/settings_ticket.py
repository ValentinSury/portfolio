TOKEN_GROUP = '01907d16c7c4789d20f299d7bc57be1d7b50945e7e922f3b64bbd8b2947a6169779bb135be020931e73fe'
GROUP_ID = 195646945

INTENTS = [
    {
        'name': 'Приветствие',
        'tokens': ('привет', 'здравствуй', 'здравствуйте'),
        'scenario': None,
        'answer': 'Здравствуйте, для справки напишите help'
    },
    {
        'name': 'Справка',
        'tokens': ('помоги', 'помощь', 'help'),
        'scenario': None,
        'answer': 'Бот поможет вам найти билет, '
    },
    {
        'name': 'Билеты',
        'tokens': ('билет', 'ticket', 'заказ'),
        'scenario': 'scenario_tick',
        'answer': None
    }
]

CITIES = ['Москва', 'Лондон']
FLY = ['моск-лонд', 'лонд-моск']

SCENARIOS = {
    'scenario_tick': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Введите город отправления.',
                'failure_text': 'У нас нет такого города, есть {cities}, выбирите!',
                'handler': 'handler_city_start',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите город назначения.',
                'failure_text': 'У нас нет такого города, есть {cities}, выбирите!',
                'handler': 'handler_city_finish',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите дату вылета в формате дд-мм-гггг',
                'failure_text': 'Вы ввели дату в неправильноим формате, введите еще раз!',
                'handler': 'handler_date',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'show_fly',
                'failure_text': 'Давай еще раз',
                'handler': 'handler_fly',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'Выберите количество мест от 1 до 5',
                'failure_text': 'Вы ввели неправильное количество мест',
                'handler': 'handler_sits',
                'next_step': 'step6'
            },
            'step6': {
                'text': 'Напишите коментарий в произвольной форме',
                'failure_text': None,
                'handler': 'handler_comment',
                'next_step': 'step7'
            },
            'step7': {
                'text': 'Данные верны?',
                'failure_text': 'Попробуйте еще раз',
                'handler': 'handler_correct_data',
                'next_step': 'step8'
            },
            'step8': {
                'text': 'Напишите номер телефона без восьмерки',
                'failure_text': 'Вы ввели номер некоректно',
                'handler': 'handler_phone_number',
                'next_step': 'step9'
            },
            'step9': {
                'text': 'Вот ваш билет, хорошего полета!',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }
        }
    }
}

DEFAULT_ANSWER = 'Мы не знаем как на это ответить. Для справки напишите help'

DB_CONF = dict(provider='postgres', user='postgres', host='localhost', database='chatbot_ticket', password='0000')
