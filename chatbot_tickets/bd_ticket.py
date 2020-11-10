from pony.orm import Database, Required, Json
from settings_ticket import DB_CONF

db_ticket = Database()
db_ticket.bind(**DB_CONF)


class UserState(db_ticket.Entity):
    """ Состояние пользователя внутри сценария """

    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class Registration(db_ticket.Entity):
    """ Заявка на регистрацию """

    city_start = Required(str)
    city_finish = Required(str)
    fly = Required(str)
    sits = Required(str)
    comment = Required(str)
    number = Required(str)


db_ticket.generate_mapping(create_tables=True)
