'''
Инструкция к использованию:

Для запуска примера запустите этот файл и напишите номер примера. 
При вводе нуля программа завершится.
'''

'''
Общая информация, взятая с официальной документации:

*pyglet* --- это кроссплатформенная библиотека для работы с окнами и мультимедиа на Python,
предназначенная для разработки игр и других визуально насыщенных приложений. Она поддерживает
работу с окнами, обработку событий пользовательского интерфейса, игровые контроллеры и джойстики,
графику OpenGL, загрузку изображений и видео, а также воспроизведение звуков и музыки.
pyglet работает в Windows, OS X и Linux.

В докладе будет рассматриваться версия *pyglet 2.x*.
'''

'''
Для начала скачаем pyglet
pip install pyglet
'''

import pyglet, random, time


''' 
1. По традиции, напишем программу выводящую "Hello, World!" на экран.
'''
def hello_world():
    ''' Сначала мы создаем объект класса Window, он отвечает за наше окно. '''
    window = pyglet.window.Window(800, 600)

    '''
    Благодаря Label, мы можем выводить текст и работать с ним.
    
    Параметры:
        font_size -- размер шрифта,
        x, y -- координты расположения текста на эране,
        anchor_x, anchor_y -- отвечают за относительную ориентацию текста,
        color -- цвет,
        rotation -- угол поворота в градусах,
        ...
    '''
    label = pyglet.text.Label('Hello, world!', 
                              font_size=40, 
                              x=window.width//2, y=window.height//2, 
                              anchor_x='center', anchor_y='center', 
                              color=(170, 40, 20, 255), 
                              rotation=50)


    ''' Декоратор реализующий метод on_draw у window, отвечающий за вывод на экран. '''
    @window.event
    def on_draw():
        window.clear()
        label.draw()
        
    ''' Запуск event_loop, цикла обработки событий. '''
    pyglet.app.run()


'''
2. Теперь ознакомимся немного с загрузкой ресурсов, картинками, звуками, анимациями и спрайтами.
'''
def visual_example():
    window = pyglet.window.Window(800, 600)

    ''' Устанавливаем путь и затем вызываем reindex, чтобы обновить его. '''
    pyglet.resource.path= ['./resources']
    pyglet.resource.reindex()

    ''' Уже знакомые нам anchor. '''
    def to_mid(image):
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

    ''' Загрузка звука. '''
    sound = pyglet.resource.media('Naruto_-_Ending_1_Wind_[_YouConvert.net_].mp3', streaming=False)

    ''' Добавляем его в плеер. '''
    media_player = pyglet.media.Player()
    media_player.queue(sound)


    ''' Загрузка картинки. '''
    image = pyglet.resource.image('Timur.png')
    to_mid(image)

    ''' Загрузка анимации. '''
    images = []
    for i in range(1, 20):
        img = pyglet.resource.image(f'smoke/image-{i}.png')
        to_mid(img)
        images.append(img)

    ''' Создаем бесконечную анимацию по кадрам. '''
    animation = pyglet.image.Animation.from_image_sequence(images, duration=0.1, loop=True)


    ''' Удобный способ группировать и отображать спрайты, просто добавляем их в один batch. '''
    batch = pyglet.graphics.Batch()

    ''' Создаем спрайты из картинки и анимации, указываем их расположение и batch. '''
    image_sprite = pyglet.sprite.Sprite(img=image, x=window.width // 2, y=window.height // 2, batch=batch)

    smoke_sprite = pyglet.sprite.Sprite(img=animation, x=340, y=350, batch=batch)

    @window.event
    def on_draw():
        window.clear()
        ''' Рисуем все сразу! '''
        batch.draw()

    ''' 
    Запускаем плеер, можно было бы и запустить отдельно звук, но тогда его нельзя было прервать. 
    Мы можем добавить больше песен в player и подавать ему генератор на очередь.
    '''
    media_player.play()

    pyglet.app.run()

    ''' Ставим на паузу. '''
    media_player.pause()

'''
3. Самое время показать взаимодействие с клавиатурой и построение геометрических фигур.
Для этого создадим рисовалку. На мышь рисовать, на пробел очищать.
'''
def handle_inputs_example():
    global last_x, last_y, lines
    from pyglet import shapes
    from pyglet.window import key

    ''' Мы можем дававть имя окну. '''
    window = pyglet.window.Window(800, 600, "Рисовалка")
    batch = pyglet.graphics.Batch()

    
    lines = []
    last_x, last_y = None, None

    ''' Мы можем обрабатывать ввод через event окна. '''
    ''' Обрабатываем нажатие на мышь. '''
    '''  '''
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        global last_x, last_y
        last_x, last_y = x, y 

    ''' Обрабатываем рисование мышью. '''
    @window.event
    def on_mouse_drag(x, y, dx, dy, button, modifiers):
        global last_x, last_y
        if last_x is not None and last_y is not None:
            line = shapes.Line(last_x, last_y, x, y, width=2, color=(50, 50, 50), batch=batch)
            lines.append(line)
            last_x, last_y = x, y

    ''' Обрабатываем отжатие кнопки мыши. '''
    @window.event
    def on_mouse_release(x, y, button, modifiers):
        global last_x, last_y
        last_x, last_y = None, None

    ''' Таким же образом можно обрабатывать и клавиатуру. '''
    @window.event
    def on_key_press(symbol, modifiers):
        global lines
        ''' Используем специльные константы из key. '''
        if symbol == key.SPACE:
            for line in lines:
                line.delete()

    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    pyglet.app.run()


'''
4. Напишем простую программку, тест на реакцию. Здесь мы затронем создание виджетов, 
работу со временем и расписанием.
'''
def reaction_test_example():
    window = pyglet.window.Window(800, 600, caption="Тест на реакцию")
    batch = pyglet.graphics.Batch()


    ''' Загружаем изображения. '''
    pyglet.resource.path= ['./resources']
    pyglet.resource.reindex()
    pressed = pyglet.resource.image("button_down.png")
    depressed = pyglet.resource.image("button_up.png")


    ''' Пишем хэндлеры для виджета.'''
    global game_status, start_time
    game_status = 0
    start_time = None
    
    def push_button_handler():
        global game_status, start_time
        if game_status == 1:
            reaction_time = time.time() - start_time
            reaction_time_label.text = f"Ваше время реакции: {reaction_time:.3f} сек."
            game_status = 2
        elif game_status == 0:
            reaction_time_label.text = "Рано! Ждите активации кнопки."
        elif game_status == 2:
            pyglet.gl.glClearColor(0, 0, 0, 0)
            pyglet.clock.schedule_once(activate_button, random.uniform(2, 5))
            game_status = 0
            

    ''' Он нам не нужен, но мы МОЖЕМ. '''
    def release_button_handler():
        pass

    ''' Создаем frame для хранения и разделения виджетов. '''
    frame = pyglet.gui.Frame(window, order=4)

    ''' Создаем виджет pushbutton. '''
    button = pyglet.gui.PushButton(
        x=window.width // 2 - pressed.width // 2,
        y=window.height // 2,
        pressed=pressed,
        depressed=depressed,
        batch=batch,
    )

    reaction_time_label = pyglet.text.Label(
        text="Время реакции: ",
        font_name="Arial",
        font_size=18,
        x=window.width // 2,
        y=window.height // 2 - 50,
        anchor_x="center",
        anchor_y="center",
        batch=batch
    )

    ''' Устанавливем хэндлеры. '''
    button.set_handler('on_press', push_button_handler)
    ''' Так же у pushbutton есть on_release хэндлер, но нам не нужен. '''
    button.set_handler('on_release', release_button_handler)
    ''' Добавляем хэдлер в frame. '''
    frame.add_widget(button)


    ''' Создаем функцию, с помощью которой будет запускаться таймер. '''
    def activate_button(dt):
        """ Активация кнопки с изменением цвета текста. """
        global game_status, start_time
        game_status = 1
        pyglet.gl.glClearColor(0.8, 0.2, 0.2, 1.0)
        start_time = time.time()

    ''' Записываем в рассписание активацию кнопки через случайное время (2–5 секунд). '''
    pyglet.clock.schedule_once(activate_button, random.uniform(2, 5))
    ''' 
    pyglet предоставляет много разных schedule методов
    https://pyglet.readthedocs.io/en/latest/modules/clock.html#pyglet.clock.Clock.schedule
    '''

    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    pyglet.app.run()

'''
Мы написали несколько не сложных, но полезных для понимания основ, программ на pyglet.
Также можно посмотреть мой проект, который целиком написан на данной библиотеке:

https://github.com/Yaitco/flappy-parrot

Да, возможно это читерство убивать двух зайцев сразу... Но так получилось... Я не специально...

''''''
За более подромным описанием методов стоит обращаться в документацию:

https://pyglet.readthedocs.io

Пожалуй, на этом все, спасибо за то, что дочитали до конца!
'''

NUM_EXAMPLES = {
    '1': hello_world,
    '2': visual_example,
    '3': handle_inputs_example,
    '4': reaction_test_example,
}

if __name__ == '__main__':
    command = input("Введите номер примера или 0 для завершения: ")
    while command != '0':
        func = NUM_EXAMPLES.get(command)
        if func is None:
            print(f"Команды '{command}' -- не существует")
        else:
            func()
        command = input("Введите номер примера или 0 для завершения: ")