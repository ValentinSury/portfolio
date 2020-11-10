from unittest import TestCase
from unittest.mock import patch, Mock
from copy import deepcopy

from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent
import settings_ticket
from chatbot_tickets import TicketBot, create_fly


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()
    return wrapper


class TestChatbotTickets(TestCase):
    """ Тест имитирующий и проверяющий ввод данных пользователем """

    RAW_EVENT = {'type': 'message_new', 'object':
        {'message': {'date': 1591223534, 'from_id': 326557329, 'id': 170, 'out': 0, 'peer_id': 326557329,
                     'text': 'Привет', 'conversation_message_id': 169, 'fwd_messages': [], 'important': False,
                     'random_id': 0, 'attachments': [], 'is_hidden': False},
         'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'open_photo'],
                         'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 3}},
                 'group_id': 195646945, 'event_id': '0d899db4ad5fea8848f548bd3801e4f02604f652'}

    def test_run(self):
        count = 5
        elem = []
        events = [elem] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock
        with patch('chatbot_tickets.vk_api.VkApi'):
            with patch('chatbot_tickets.vk_api.bot_longpoll.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = TicketBot(' ', ' ')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(elem)
                assert bot.on_event.call_count == count

    INPUTS = [
        'ей',
        'привет',
        'помоги',
        'билет',
        'Москва',
        '12',
        'Лондон',
        '01-02-2020',
        '2',
        '2',
        'коментарий',
        'да',
        '9777994777'
    ]
    ALLOWED_CITIES = deepcopy(settings_ticket.CITIES)
    ALLOWED_CITIES.remove('Москва')
    date_fly = create_fly(1)
    CHOOSE_FLY_OUTPUT = ' Выбирите подходящий вам рейс: ' \
                        f'\n 1 - {date_fly[0]}\n2 - {date_fly[1]}\n3 - {date_fly[2]}\n4 - {date_fly[3]}\n5 - {date_fly[4]}\n'
    EXPECTED_OUTPUTS = [
        settings_ticket.DEFAULT_ANSWER,
        settings_ticket.INTENTS[0]['answer'],
        settings_ticket.INTENTS[1]['answer'],
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step1']['text'],
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step2']['text'],
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step2']['failure_text'].format(cities=ALLOWED_CITIES),
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step3']['text'],
        CHOOSE_FLY_OUTPUT,
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step5']['text'],
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step6']['text'],
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step7']['text'],
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step8']['text'],
        settings_ticket.SCENARIOS['scenario_tick']['steps']['step9']['text']
    ]

    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('chatbot_tickets.vk_api.VkApi'):
            with patch('chatbot_tickets.vk_api.bot_longpoll.VkBotLongPoll', return_value=long_poller_mock):
                bot = TicketBot(' ', ' ')
                bot.api = api_mock
                bot.send_image = Mock()
                bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        for real, expec in zip(real_outputs, self.EXPECTED_OUTPUTS):
            print(real)
            print('-' * 50)
            print(expec)
            print('-' * 50)
            print(real == expec)
            print('_' * 50)
        assert real_outputs == self.EXPECTED_OUTPUTS
