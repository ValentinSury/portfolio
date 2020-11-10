import os
import re
import cv2


weather_re = r'ождь|блачно|асмурно'


def gradient(param='yellow'):
    """ Создание каркаса для изображения с градиентом цвета в зависимости от погоды """

    image = cv2.imread('python_snippets/external_data/probe.jpg')
    if param == 'grey':
        a = 100
        b = 100
        c = 100
        for x in range(0, 256):
            a += 0.6
            b += 0.6
            c += 0.6
            for y in range(0, 512):
                image[x, y] = [a, b, c]
    elif param == 'blue':
        a = 0
        b = 0
        for x in range(0, 256):
            a += 1
            b += 1
            for y in range(0, 512):
                image[x, y] = [255, a, b]
    else:
        a = 0
        for x in range(0, 256):
            a += 1
            for y in range(0, 512):
                image[x, y] = [a, 255, 255]
    return image


def image_maker(data_dict):
    """ Создание изображения с прогнозом погоды """

    weather_re_0 = re.search(weather_re, data_dict['погода'])
    weather_type = weather_re_0.group()
    if weather_type == 'блачно' or weather_type == 'асмурно':
        image = gradient(param='grey')
        weather_image = cv2.imread('python_snippets/external_data/weather_img/cloud.jpg')
        image[0:100, 0:100] = weather_image
    elif weather_type == 'ождь':
        image = gradient(param='blue')
        weather_image = cv2.imread('python_snippets/external_data/weather_img/rain.jpg')
        image[0:100, 0:100] = weather_image
    else:
        image = gradient()
        weather_image = cv2.imread('python_snippets/external_data/weather_img/sun.jpg')
        image[0:100, 0:100] = weather_image

    text = f'{data_dict["день недели"]}, {data_dict["дата"]}: {data_dict["температура"]} градусов'
    cv2.putText(image, data_dict['погода'], (120, 200), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1)
    cv2.putText(image, text, (30, 150), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1)

    cv2.imshow("Image", image)

    path_saved_image = 'saved_image'
    if not os.path.exists(path_saved_image):
        os.mkdir(path_saved_image)
    cv2.imwrite(f'{path_saved_image}/{data_dict["дата"][:2]}.png', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
