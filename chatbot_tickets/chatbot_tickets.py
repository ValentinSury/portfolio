import datetime

import requests
import vk_api
import vk_api.bot_longpoll
import vk_api.utils

from image_ticket import generate_ticket
import handlers_ticket
import settings_ticket
from bd_ticket import Registration, UserState
from pony.orm import db_session


def create_fly(day_quantity):
    """ Функция создающая рейсы """

    one_day = datetime.timedelta(days=day_quantity)
    now = datetime.date.today()
    date_fly_list = []
    for _ in range(5):
        now += one_day
        date_fly_list.append(now.strftime("%d-%m-%Y"))
    return date_fly_list


class TicketBot:
    """ Чатбот в Vk для побора билета по данным предаставленным пользователем
        и для генерации самого билета """

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token

        self.vk = vk_api.VkApi(token=settings_ticket.TOKEN_GROUP)
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.fly_list = {settings_ticket.FLY[0]: create_fly(1),
                         settings_ticket.FLY[1]: create_fly(3)}

    def run(self):
        """ Функция запуска бота """

        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception as err:
                print(err)

    @db_session
    def on_event(self, event):
        """ Функция реагирующая на действие пользователя """

        if event.type != vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            return

        user_id = str(event.message.peer_id)
        text = event.message.text
        state = UserState.get(user_id=user_id)
        if state is not None:
            text_to_send = self.continue_scenario(user_id=user_id, text=text, state=state)
        else:
            for intents in settings_ticket.INTENTS:
                if any(token in text for token in intents['tokens']):
                    if intents['answer']:
                        text_to_send = intents['answer']
                    else:
                        text_to_send = self.start_scenario(scenario_name=intents['scenario'], user_id=user_id)
                    break
            else:
                text_to_send = settings_ticket.DEFAULT_ANSWER
        self.api.messages.send(message=text_to_send,
                               random_id=vk_api.utils.get_random_id(),
                               peer_id=user_id)

    def continue_scenario(self, user_id, text, state):
        """ Функция продолжающая сценарий """

        if text in settings_ticket.INTENTS[1]['tokens']:
            text_to_send = settings_ticket.INTENTS[1]['answer']
            state.delete()
        elif text in settings_ticket.INTENTS[2]['tokens']:
            state.delete()
            text_to_send = self.start_scenario(scenario_name=settings_ticket.INTENTS[2]['scenario'], user_id=user_id)
        else:
            steps = settings_ticket.SCENARIOS[state.scenario_name]['steps']
            step = steps[state.step_name]
            handler = getattr(handlers_ticket, step['handler'])
            handler_result = handler(text=text, context=state.context)
            if handler_result:
                if handler_result == 'No':
                    text_to_send = 'Попробуйте еще раз...'
                    state.delete()
                else:
                    next_step = steps[step['next_step']]
                    if next_step['text'] == 'show_fly':
                        dispatcher_text = handlers_ticket.dispatcher(state.context['city_start'],
                                                                     state.context['city_finish'],
                                                                     state.context['date'], state.context)
                        text_to_send = dispatcher_text
                        if dispatcher_text == 'Рейсов нет, попробуйте заново':
                            state.delete()
                    else:
                        text_to_send = next_step['text']
                    if next_step['next_step']:
                        state.step_name = step['next_step']
                    else:
                        image = generate_ticket(from_city=state.context['city_start'],
                                                to_city=state.context['city_finish'],
                                                date=state.context['number_fly'])
                        self.send_image(image=image, user_id=user_id)
                        Registration(city_start=state.context['city_start'], city_finish=state.context['city_finish'],
                                     fly=state.context['number_fly'], sits=state.context['sits'],
                                     comment=state.context['comment'], number=state.context['number'])
                        state.delete()
            else:
                text_to_send = step['failure_text'].format(**state.context)
        return text_to_send

    def start_scenario(self, scenario_name, user_id):
        """ Функция начинающая сценарий """

        scenario = settings_ticket.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        UserState(user_id=user_id, scenario_name=scenario_name, step_name=first_step,
                  context={'fly_list': self.fly_list})
        return text_to_send

    def send_image(self, image, user_id):
        """ Функция отправляющая изображения билета пользователю """

        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(url=upload_url, files={'photo': ('image.png', image, 'image/png')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**upload_data)
        owner_id = image_data[0]['owner_id']
        media_id = image_data[0]['id']
        attachment = f'photo{owner_id}_{media_id}'
        self.api.messages.send(attachment=attachment,
                               random_id=vk_api.utils.get_random_id(), peer_id=user_id)


if __name__ == '__main__':
    bot = TicketBot(group_id=settings_ticket.GROUP_ID, token=settings_ticket.TOKEN_GROUP)
    bot.run()
