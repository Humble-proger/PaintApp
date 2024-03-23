
# Импортирт классов библиотеки kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import (Line, Ellipse, Color, Rectangle)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
#Импорт функции для получения случайного числа. Используется для получения случайного цвета
from random import randint
'''
Импорт функции и класса Tkinter для создания простого диалогого окна в Windows.
В kivy есть кроссплатформенный вариант диалогого окна.
Если проект требует импортирование на телефоны требуется этот механизм дописать
'''
from tkinter.filedialog import asksaveasfilename
from tkinter import Tk

# Изменение параметров окна приложения
Config.set("graphics", "resizable", "0") # Размер окна не изменяется
Config.set("graphics", "width", 800) # Ширина окна 800 пикселей
Config.set("graphics", "height", 600) # Высота окна 600 пикселей

# Создание окна Tkinter для диалогого окна
root = Tk()
root.withdraw() # При создании скрывается

class Canvas(Widget): # Класс Canvas это виджет(пространство) в котором происходит рисование
    """
    Значение переменной mode равно выбранному инструменту
    1 - Обычная кисть
    2 - Рисование прямоугольника (С задержанием мыши. Анимации нету)
    3 - Кисть с другим текстурай нажима (в форме квадрата) 
    
    Значение переменной color равно выбранному цвету.
    Представляется в виде картежа, в следующем формате (Red, Green, Blue, Alpha). Т.е. имеет формат RGBA
    Где параметры Red, Green, Blue, Alpha задаются в диапозоне от 0 до 1

    Для перевода из стандартного формата можно поделить на максимальное значение 255 и получить значение в данном формате 
    
    Значение переменной rad равно радиусу кисти в пикселях
    """
    mode = 1
    color = (1,1,1,1)
    rad = 20
    
    # Инициализация класса
    def __init__(self):
        super(Canvas, self).__init__()
        self.create_background() # перекрашивание цвета фона в белый(по умолчанию)
        self.change_color((randint(1,100)/100,randint(1,100)/100,randint(1,100)/100,1)) # Меняется текущий цвет кисти на случайный
    
    """
    Функция класса def on_touch_down(self, touch). 
    Вызывается при нажатии левой кнопки мыши по виджету. 
    self - экземпляр класса, touch - структура хранящая свойства мышки например координаты мыши.
    """
    def on_touch_down(self, touch):
        with self.canvas: # Для данного холста виджета выполняются операции
            if touch.y  < 600*0.9 - self.rad: # Если курсор расположен внутри области редактирования
                if self.mode == 1: # Если выбрана обыная кисть
                    Ellipse(pos=(touch.x - self.rad/2, touch.y - self.rad/2), size=(self.rad, self.rad)) # Создаётся круг с радиусом rad на координатах мыши
                    """
                    Создаётся списочек с точками
                    Используется для сохранение пути мыши.
                    Это используется для эмитации длительного нажатия на кисть
                    """
                    touch.ud['line'] = Line(points=(), width = self.rad)
                elif self.mode == 2: # Если выбран прямоугольник
                    touch.ud["rectangle"] = Rectangle(pos=(touch.x, touch.y), size = (0, 0)) # Также создаётся список с точками
                elif self.mode == 3: # Если выбрана кисть с другой формой
                    #self.set_color((1,1,1,1))
                    Rectangle(pos=(touch.x - self.rad/2, touch.y - self.rad/2), size=(self.rad, self.rad)) # Создаётся квадрат с центром на координатах мыши
                    touch.ud['gum'] = Line(points=(), width=self.rad, cap="square", joint="bevel", close=False) # Также создаётся список с точками
    
    """
    Функция класса on_touch_move(self, touch). 
    Вызывается при удержании левой кнопки мыши по виджету. 
    self - экземпляр класса, touch - структура хранящая свойства мышки например координаты мыши.
    """
    def on_touch_move(self, touch):
        # Если курсор расположен внутри области редактирования
        if touch.y  < 600*0.9 - self.rad: 
            if self.mode == 1: # Если выбрана обычная кисть
                if 'line' in touch.ud:
                    touch.ud['line'].points += (touch.x, touch.y)
            elif self.mode == 3: # Если выбрана кисть с другой формой
                if 'gum' in touch.ud:
                    touch.ud['gum'].points += (touch.x, touch.y)
    """
    Функция класса on_touch_up(self, touch). 
    Вызывается при отпусткании левой кнопки мыши. 
    self - экземпляр класса, touch - структура хранящая свойства мышки например координаты мыши.
    """
    def on_touch_up(self, touch):
        if touch.y < 600*0.9 - self.rad: # Если курсор расположен внутри области редактирования
            if self.mode == 2: # Выбран прямоугольник
                touch.ud['rectangle'].size = (touch.x - touch.ud['rectangle'].pos[0], touch.y - touch.ud['rectangle'].pos[1]) # Создаётся прямоуголиник
    """
    Функция класса create_background(self). 
    Вызывается для создания фона виджета.
    По умолчанию цвет фона белый 
    self - экземпляр класса
    """
    def create_background(self):
        with self.canvas: # Для данного холста виджета выполняются операции
            Color(1,1,1,1) # Устанавливается цвет
            Rectangle(pos=(0, 0), size=(800, 600*0.9)) # Создаётся прямоугольник с фоном
        self.set_color(self.color) # Установка цвета
    
    """
    Функция класса change_color(self, color). 
    Вызывается для изменения текущего цвета кисти. 
    self - экземпляр класса, color - цвет
    """
    def change_color(self, color):
        self.canvas.add(Color(*color))
        self.color = color
    
    """
    Функция класса set_color(self, color). 
    Вызывается для изменения цвета без сохранения в переменную self.color. 
    self - экземпляр класса, color - цвет
    """
    def set_color(self, color):
        self.canvas.add(Color(*color))


class PaintApp(App): # Класс PaintApp это основной виджет(пространство) в котором происходит сборка приложения
    """
    Значение переменной max_rad равно максимальному радиусу кисти в пикселях
    Значение переменной min_rad равно минимальному радиусу кисти в пикселях
    Значение переменной step равно шагу увеличения/уменьшения радиуса кисти
    """
    max_rad = 100
    min_rad = 1
    step = 2

    def build(self): # Сборка приложения
        bl = BoxLayout(orientation="vertical") # Пространство которое организует виджеты последовательно орентирован вертикально 
        menu = GridLayout(cols=3, size_hint=(1, 0.1)) # Пространство которое организует виджеты в виде сетки с количесвом колонок 3 и ограниченным размером по вертикали в 10%
        tools = GridLayout(cols=4) # Пространство которое организует виджеты в виде сетки с количесвом колонок 4
        func_buttons = GridLayout(cols=4) # Пространство которое организует виджеты в виде сетки с количесвом колонок 4
        
        '''
        Добавление кнопок в пространство tools
        Где в on_press передаётся функция вызывающая при нажатии на кнопку
        background_normal - передаётся путь к изображению, при нормальном состоянии
        '''
        tools.add_widget( Button(on_press=self.switch_buttons, background_normal="brush-icon1.png") )
        tools.add_widget( Button(on_press=self.switch_buttons, background_normal="rect.png") )
        tools.add_widget( Button(on_press=self.switch_buttons, background_normal="brush-icon2.png") )
        
        '''
        Аналогичное добавление кнопок в пространство func_buttons
        background_color - устанавливается цвет кнопки
        '''
        func_buttons.add_widget(Button(text="Clear", on_press=self.clear_canvas, background_color=(42/255, 157/255, 143/255, 1)))
        func_buttons.add_widget(Button(text="Save", on_press=self.save_img, background_color=(42/255, 157/255, 143/255, 1)))
        func_buttons.add_widget(Button(text="+", on_press=self.add_rad, background_color=(42/255, 157/255, 143/255, 1)))
        func_buttons.add_widget(Button(text="-", on_press=self.sub_rad, background_color=(42/255, 157/255, 143/255, 1))) 
        colors = GridLayout(cols=8) # Пространство которое организует виджеты в виде сетки с количесвом колонок 8
        # Цикл, который формирует 16 кнопок с случайными цветами в пространство colors
        for i in [(randint(1,100)/100, randint(1,100)/100, randint(1,100)/100, 1) for i in range(16)]:
            colors.add_widget( Button(background_color=(i[0], i[1], i[2], 1), background_normal = '', on_press=self.chenge_canvas_color) )
        self.c = Canvas() # Создаётся объект (Холст)
        self.c.mode = 1 # Устанавливается начальный инструмент
        
        #Формируеся меню путём объединения пространств
        menu.add_widget(tools)
        menu.add_widget(func_buttons)
        menu.add_widget(colors)
        
        #Формируеся полный виджет путём объединения пространств меню и холста
        bl.add_widget(menu)
        bl.add_widget(self.c)
        return bl
    # Функция очищающая холст
    def clear_canvas(self, instance):
        self.c.canvas.clear() # Очищается всё что есть на холсте
        self.c.create_background() # Создаётся фон
    # Функция сохраняющая изображение
    def save_img(self, instance):
        path_file = asksaveasfilename(filetypes=[("PNG File", "*.png")]) # Вызывается диалоговое окно на запрос пути к сохранению файла
        path_file = path_file.split('.')[0] + ".png" # Изменяется формат файла при указании неверного
        self.c.export_to_png(path_file) # Экспортируется изображение по данному пути
    # Функция изменяющая текущий инструмент
    # instance - ссылка на объект вызвавший функцию
    def switch_buttons(self, instance):
        if instance.background_normal == "brush-icon1.png": # Если функцию вызвала кнопка обычной кисти
            self.c.mode = 1 # Устанавливается режим обычной кисти
            self.c.set_color(self.c.color) # Изменяется текущий цвет кисти
        elif instance.background_normal == "rect.png": # Если функцию вызвала кнопка прямоугольника
            self.c.mode = 2 # Устанавливается режим прямоугольника
            self.c.set_color(self.c.color) # Изменяется текущий цвет кисти
        else: # иначе
            self.c.mode = 3 # Устанавливается режим кисти с другой формой кисти
    # Увеличение текущего радиуса кисти на шаг step
    def add_rad(self, instance):
        if self.c.rad + self.step <= self.max_rad: # Если не превзойдён лимит
            self.c.rad += self.step # Увеличиваем радиус
    # Уменьшение текущего радиуса кисти на шаг step
    def sub_rad(self, instance):
        if self.c.rad - self.step >= self.min_rad: # Если не превзойдён лимит
            self.c.rad -= self.step # Уменьшаем радиус

    #Изменить цвет кисти
    def chenge_canvas_color(self, instance):
        color = instance.background_color # Берётся цвет кнопки
        self.c.change_color((color[0], color[1], color[2], 1)) # Изменяется цвет кисти



if __name__ == "__main__": # Если данный файла является главным т.е. он не запущен или импортирован с других файлов
    PaintApp().run() # Запускаем приложение