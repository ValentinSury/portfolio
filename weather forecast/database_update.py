import peewee

db = peewee.SqliteDatabase('weather.db')


class DbWeather(peewee.Model):
    date = peewee.CharField()
    weather = peewee.CharField()

    class Meta:
        database = db


db.create_tables([DbWeather])


def put_weather_in_db(weather_list):
    """ Сохранения значений погоды в БД """

    for item in weather_list:
        item_0 = f'{item["погода"]}, температура {item["температура"]} градусов'
        add_in_db = DbWeather.get_or_create(date=item['дата'], defaults={'weather': item_0})
        if not add_in_db[1]:
            changed_data = DbWeather.get(DbWeather.id == add_in_db[0])
            if changed_data.weather != item_0:
                changed_data.weather = item_0
                changed_data.save()


def take_weather_from_db():
    """ Получение значений погоды из БД """

    for cond in DbWeather.select().where(DbWeather.date.between(15, 20)):
        print(f'Число: {cond.date}, погода: {cond.weather}')
