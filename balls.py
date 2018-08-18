import tkinter
import random

# константы
WIDTH=640
HEIGHT=480
BG_COLOR="white"
ZERO = 0
MAIN_BALL_RADIUS = 30
MAIN_BALL_COLOR = 'aqua'
INIT_DX = 1
INIT_DY = 1
BAD_COLOR = 'red'
COLORS = ['blue', 'fuchsia', BAD_COLOR ,'pink', BAD_COLOR, 'yellow', 'gold', 'chartreuse']

#класс-конструктор для шариков
class Balls():
    def __init__(self, x, y, r, color, dx=0, dy=0):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy
    def draw(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = self.color,
                           outline = self.color if self.color != BAD_COLOR else 'black')
    def hide(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = BG_COLOR, outline=BG_COLOR)

    def is_collision(self, ball):
        a = abs(self.x + self.dx - ball.x)
        b =  abs(self.y + self.dy - ball.y)
        return (a*a + b*b)**0.5 <= self.r + ball.r

    def move(self):
        #столкновение со стенами
        if (self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= ZERO):
            self.dx = -self.dx
        if (self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dy <= ZERO):
            self.dy = -self.dy
        # столкновление с другими шарами
        for ball in balls:
            if self.is_collision(ball):
                if ball.color != BAD_COLOR:
                    ball.hide()
                    balls.remove(ball)
                    self.dx = -self.dx
                    self.dy = -self.dy
                else:
                    self.dx = self.dy = 0
        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()


# события мыши
def mouse_click(event):
    global main_ball
    if event.num == 1:
            main_ball = Balls(event.x, event.y, MAIN_BALL_RADIUS, MAIN_BALL_COLOR, INIT_DX, INIT_DY)
            main_ball.draw()
            #поворот налево
            if main_ball.dx * main_ball.dy > 0:
                main_ball.dy = -main_ball.dy
            else:
                main_ball.dx = -main_ball.dx
    elif event.num == 2: #поворот направо
        if main_ball.dx * main_ball.dy > 0:
            main_ball.dx = -main_ball.dx
        else:
            main_ball.dy = -main_ball.dy
        #main_ball.hide()

def create_list_of_balls(number):
    lst=[]
    while len(lst) < number:
        next_ball = Balls(random.choice(range(0, WIDTH)),
                          random.choice(range(0, HEIGHT)),
                          random.choice(range(15, 35)),
                          random.choice(COLORS))
        lst.append(next_ball)
        next_ball.draw()
    return lst

# считаем плохие шары
def count_bad_balls(list_of_balls):
    res = 0
    for ball in list_of_balls:
        if ball.color == BAD_COLOR:
            res += 1
    return res


def main():
        if 'main_ball' in globals():
            main_ball.move()
            if len(balls) - num_of_balls == 0:
                canvas.create_text(WIDTH / 2, HEIGHT / 2, text = 'Вы победили!', font = 'Arial 25', fill = 'black')
                main_ball.dy = 0
            elif main_ball.dx == 0:
                canvas.create_text(WIDTH / 2, HEIGHT / 2, text='Вы проиграли!', font='Arial 25', fill='black')
        root.after(10, main)

# корневое окно
root = tkinter.Tk()
root.title("Jumping_balls")
canvas = tkinter.Canvas(root, width = 640, height = 480, bg = BG_COLOR)
canvas.pack()
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Button-2>', mouse_click, '+')
#canvas.bind('<Button-3>', mouse_click, '+')
if 'main_ball' in globals():
    del main_ball
balls = create_list_of_balls(10)
num_of_balls = count_bad_balls(balls)
main()
root.mainloop()
