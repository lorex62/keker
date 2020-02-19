import os
import sys

import pygame
import requests

coords = input('Введите координаты через запятую без пробелов: ').strip()
a = input('Введите маштаб(от 0 до 17): ')
zoomout = int(a.split('.')[0])
response = None
map_request = "https://static-maps.yandex.ru/1.x/?ll={0}&size=450,450&z={1}&l=sat".format(coords, str(zoomout))

# Инициализируем pygame
pygame.init()
running = True
while running:
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen = pygame.display.set_mode((450, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if zoomout <= 16:
                    zoomout += 1
                    map_request = "https://static-maps.yandex.ru/1.x/?ll={0}&size=450,450&z={1}&l=sat".format(coords,
                                                                                                          str(zoomout
                                                                                                              ))
            elif event.key == pygame.K_DOWN:
                if zoomout >= 1:
                    zoomout -= 1
                    map_request = "https://static-maps.yandex.ru/1.x/?ll={0}&size=450,450&z={1}&l=sat".format(coords,
                                                                                                          str(zoomout
                                                                                                              ))
    pygame.display.flip()
pygame.quit()
