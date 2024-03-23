from turtle import width
from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import (Line, Ellipse, Color, Rectangle)
from random import randint
from tkinter.filedialog import asksaveasfilename
from tkinter import Tk

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", 800)
Config.set("graphics", "height", 600)

root = Tk()
root.withdraw()

class Canvas(Widget):
    mode = 1
    color = (1,1,1,1)
    rad = 20
    def __init__(self):
        super(Canvas, self).__init__()
        self.create_background()
        self.change_color((randint(1,100)/100,randint(1,100)/100,randint(1,100)/100,1))
    def on_touch_down(self, touch):
        with self.canvas:
            if touch.y  < 600*0.9 - self.rad:
                if self.mode == 1:
                    Ellipse(pos=(touch.x - self.rad/2, touch.y - self.rad/2), size=(self.rad, self.rad))
                    touch.ud['line'] = Line(points=(), width = self.rad)
                elif self.mode == 2:
                    touch.ud["rectangle"] = Rectangle(pos=(touch.x, touch.y), size = (0, 0))
                elif self.mode == 3:
                    #self.set_color((1,1,1,1))
                    Rectangle(pos=(touch.x - self.rad/2, touch.y - self.rad/2), size=(self.rad, self.rad))
                    touch.ud['gum'] = Line(points=(), width=self.rad, cap="square", joint="bevel", close=False)
    def on_touch_move(self, touch):
        if touch.y  < 600*0.9 - self.rad: 
            if self.mode == 1:
                if 'line' in touch.ud:
                    touch.ud['line'].points += (touch.x, touch.y)
            elif self.mode == 3:
                if 'gum' in touch.ud:
                    touch.ud['gum'].points += (touch.x, touch.y)
    def on_touch_up(self, touch):
        if touch.y < 600*0.9 - self.rad:
            if self.mode == 2:
                touch.ud['rectangle'].size = (touch.x - touch.ud['rectangle'].pos[0], touch.y - touch.ud['rectangle'].pos[1])
    def create_background(self):
        with self.canvas:
            Color(1,1,1,1)
            Rectangle(pos=(0, 0), size=(800, 600*0.9))
        self.set_color(self.color)
    def change_color(self, color):
        self.canvas.add(Color(*color))
        self.color = color
    def set_color(self, color):
        self.canvas.add(Color(*color))


class PaintApp(App):
    max_rad = 100
    min_rad = 1
    step = 2


    
    def build(self):
        bl = BoxLayout(orientation="vertical")
        menu = GridLayout(cols=3, size_hint=(1, 0.1))
        tools = GridLayout(cols=4)
        func_buttons = GridLayout(cols=4)
        
        tools.add_widget( Button(on_press=self.switch_buttons, background_normal="brush-icon1.png") )
        tools.add_widget( Button(on_press=self.switch_buttons, background_normal="rect.png") )
        tools.add_widget( Button(on_press=self.switch_buttons, background_normal="brush-icon2.png") )
        
        func_buttons.add_widget(Button(text="Clear", on_press=self.clear_canvas, background_color=(42/255, 157/255, 143/255, 1)))
        func_buttons.add_widget(Button(text="Save", on_press=self.save_img, background_color=(42/255, 157/255, 143/255, 1)))
        func_buttons.add_widget(Button(text="+", on_press=self.add_rad, background_color=(42/255, 157/255, 143/255, 1)))
        func_buttons.add_widget(Button(text="-", on_press=self.sub_rad, background_color=(42/255, 157/255, 143/255, 1))) 
        colors = GridLayout(cols=8)
        for i in [(randint(1,100)/100, randint(1,100)/100, randint(1,100)/100, 1) for i in range(16)]:
            colors.add_widget( Button(background_color=(i[0], i[1], i[2], 1), background_normal = '', on_press=self.chenge_canvas_color) )
        self.c = Canvas()
        self.c.mode = 1
        
        menu.add_widget(tools)
        menu.add_widget(func_buttons)
        menu.add_widget(colors)
        
        bl.add_widget(menu)
        bl.add_widget(self.c)
        return bl
    def clear_canvas(self, instance):
        self.c.canvas.clear()
        self.c.create_background()
    def save_img(self, instance):
        path_file = asksaveasfilename(filetypes=[("PNG File", "*.png")])
        path_file = path_file.split('.')[0] + ".png"
        self.c.export_to_png(path_file)
    def switch_buttons(self, instance):
        if instance.background_normal == "brush-icon1.png":
            self.c.mode = 1
            self.c.set_color(self.c.color)
        elif instance.background_normal == "rect.png":
            self.c.mode = 2
            self.c.set_color(self.c.color)
        else:
            self.c.mode = 3
    def add_rad(self, instance):
        if self.c.rad + self.step <= self.max_rad:
            self.c.rad += self.step
    def sub_rad(self, instance):
        if self.c.rad - self.step >= self.min_rad:
            self.c.rad -= self.step

    
    def chenge_canvas_color(self, instance):
        color = instance.background_color
        self.c.change_color((color[0], color[1], color[2], 1))



if __name__ == "__main__":
    PaintApp().run()