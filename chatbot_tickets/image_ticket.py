from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


TICKET_IMAGE = 'extra_files/fly_ticket.png'
TICKET_FONT = 'extra_files/Roboto-Regular.ttf'
FONT_SIZE = 22
BLACK = (0, 0, 0, 255)
FROM_OFFSET = (190, 565)
TO_OFFSET = (190, 595)
DATE_OFFSET = (190, 500)


def generate_ticket(from_city, to_city, date):
    """ Функция генерирующая изображения билета с данными введенными пользователем данными """

    base = Image.open(TICKET_IMAGE).convert('RGBA')
    font = ImageFont.truetype(TICKET_FONT, FONT_SIZE)

    draw = ImageDraw.Draw(base)
    draw.text(FROM_OFFSET, from_city, font=font, fill=BLACK)
    draw.text(TO_OFFSET, to_city, font=font, fill=BLACK)
    draw.text(DATE_OFFSET, date, font=font, fill=BLACK)

    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file
