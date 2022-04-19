import multiprocessing as mp
import time
import pygame

pygame.init()

# функция нагружающая поток, принимает число для работы, номер потока и массив % выполнения потоков
def func(x, p_id, arr):
    s = 0
    # поток начинается с того момента где остановился
    start_x = arr[p_id]
    for j in range(start_x, x):
        s += x ** 500000
        arr[p_id] = j + 1


if __name__ == '__main__':
    sc = pygame.display.set_mode((800, 600))
    window = pygame.image.load('pic/window.bmp')
    button = pygame.image.load('pic/process_button.bmp')
    font = pygame.font.SysFont('Arial', 20)
    # список процессов
    processes = []
    # списко кнопок процессов
    button_rects = []
    # массив выполнения
    working = mp.Array('i', (0, 0, 0, 0, 0, 0, 0, 0))
    for i in range(8):
        processes.append(mp.Process(target=func, args=(100, i, working)))
        button_rects.append(pygame.Rect(174, 113 + i * 43, 85, 29))
    # список состояний 0 - в пуле, 1 - работает, 2 - в ожидании
    states = [0, 0, 0, 0, 0, 0, 0, 0]
    # переменные для отрисовки
    pool_count = 8
    work_count = 0
    sleep_count = 0
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    # при выходе убивает все потоки
                    for pr in processes:
                        if pr.is_alive():
                            pr.kill()
                    exit()
                case pygame.MOUSEBUTTONDOWN if event.button == 1:
                    # нажатия кнопок
                    for i in range(8):
                        if button_rects[i].collidepoint(event.pos):
                            match states[i]:
                                case 0:
                                    processes[i].start()
                                    states[i] = 1
                                case 1:
                                    processes[i].kill()
                                    time.sleep(0.0001)
                                    states[i] = 2
                                case 2:
                                    processes[i] = mp.Process(target=func, args=(100, i, working))
                                    states[i] = 0
        # обнуление вспомогательных переменных для отрисовки
        pool_count = 0
        work_count = 0
        sleep_count = 0
        sc.blit(window, (0, 0))
        # для каждого потока
        for i in range(8):
            # проверка не выполнился ли он до 100%
            if not processes[i].is_alive() and working[i] == 100:
                states[i] = 0
                working[i] = 0
            # отрисовка
            match states[i]:
                case 0:
                    name_text = font.render(f'Поток {i + 1} {working[i]}%', True, (0, 0, 0))
                    name_text_rect = name_text.get_rect(x=60, y=115 + pool_count * 43)
                    st_text = font.render('Вкл', True, (0, 0, 0))
                    st_text_rect = st_text.get_rect(x=202, y=115 + pool_count * 43)
                    # сохраняю ректы кнопок, чтобы было легче с ними работать
                    button_rects[i].x = 174
                    button_rects[i].y = 113 + pool_count * 43
                    sc.blit(button, (41, 108 + pool_count * 43))
                    sc.blit(name_text, name_text_rect)
                    sc.blit(st_text, st_text_rect)
                    pool_count += 1
                case 1:
                    name_text = font.render(f'Поток {i + 1} {working[i]}%', True, (0, 0, 0))
                    name_text_rect = name_text.get_rect(x=311, y=115 + work_count * 43)
                    st_text = font.render('Стоп', True, (0, 0, 0))
                    st_text_rect = st_text.get_rect(x=449, y=115 + work_count * 43)
                    button_rects[i].x = 425
                    button_rects[i].y = 113 + work_count * 43
                    sc.blit(button, (292, 108 + work_count * 43))
                    sc.blit(name_text, name_text_rect)
                    sc.blit(st_text, st_text_rect)
                    work_count += 1
                case 2:
                    name_text = font.render(f'Поток {i + 1} {working[i]}%', True, (0, 0, 0))
                    name_text_rect = name_text.get_rect(x=562, y=115 + sleep_count * 43)
                    st_text = font.render('В пул', True, (0, 0, 0))
                    st_text_rect = st_text.get_rect(x=695, y=115 + sleep_count * 43)
                    button_rects[i].x = 676
                    button_rects[i].y = 113 + sleep_count * 43
                    sc.blit(button, (543, 108 + sleep_count * 43))
                    sc.blit(name_text, name_text_rect)
                    sc.blit(st_text, st_text_rect)
                    sleep_count += 1
        pygame.display.update()
        clock.tick(60)
