import turtle
import math

anim_speed = 0 # 0 for instant drawing, 6 for default speed
radius = (50)
t_env = turtle.Turtle()
t_duck = turtle.Turtle()
t_wolf = turtle.Turtle()
duck_speed = 1
wolf_speed = math.pi+1
duck_dist = 0.0
wolf_dist = 0.0

duck_state = 1



##### Function Setup #####
def length2angel(rad,len):
    c=2*math.pi*rad #Radius to circunferance
    angel=(len/c)*360 #Arc length to angel
    return angel

def angel2length(angel, rad):
    length=angel*(math.pi/180)*rad
    return length

def getAngle(a,b,c):
    ang=math.degrees(math.atan2(c[1]-b[1],c[0]-b[0])-math.atan2(a[1]-b[1],a[0]-b[0]))
    return ang+360 if ang<0 else ang

def clamp(n, min_value, max_value):
    return max(min_value, min(n, max_value))

def getDistance(a,b):
    dist=math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
    return dist

##### Duck Movment #####
def DuckMove():
    global duck_dist
    global duck_state
    r_prim = (radius*duck_speed)/wolf_speed-0.1

    if duck_state == 1:
        if getDistance(t_duck.pos(), t_env.pos()) < r_prim:
            duck_dist += clamp(getDistance(t_duck.pos(), [0,r_prim]), 0, duck_speed)
            t_duck.setheading(t_duck.towards(0, -(r_prim)))
            t_duck.forward(clamp(getDistance(t_duck.pos(), [0,r_prim]), 0, duck_speed))
        else :
            t_duck.right(90)
            duck_state = 2
    elif duck_state == 2:
        angel_dif = getAngle(t_duck.pos(),(0,0),t_wolf.pos())
        duck_dist += angel2length(clamp(getDistance(t_duck.pos(), [0,r_prim]), 0, duck_speed), r_prim)
        if angel_dif != 180:
            t_duck.circle(-r_prim, extent=clamp(180-angel_dif,-length2angel(r_prim,duck_speed),length2angel(r_prim,duck_speed)))

        angel_dif = getAngle(t_duck.pos(),(0,0),t_wolf.pos())
        print(angel_dif)
        if round(angel_dif) == 180:
            t_duck.setheading(t_wolf.towards(t_duck.pos()))
            duck_state = 3
    elif duck_state == 3:
        duck_dist += duck_speed
        t_duck.forward(duck_speed)


##### Wolf Movment #####
def WolfMove():
    angel_dif = getAngle(t_duck.pos(),(0,0),t_wolf.pos())
    global wolf_dist
    wolf_dist += angel2length(clamp(angel_dif,0,length2angel(radius,wolf_speed)), radius)
    
    if angel_dif<=180:
        t_wolf.circle(-radius, extent=clamp(angel_dif,0,length2angel(radius,wolf_speed)))
    else:
        t_wolf.circle(-radius, extent=-clamp(angel_dif,0,length2angel(radius,wolf_speed)))

##### Run #####

##### Setup Scene #####
t_env.speed(0)
t_duck.speed(anim_speed)
t_wolf.speed(anim_speed)

t_env.hideturtle()
t_env.penup()
t_env.setpos(0,-radius)
t_env.pendown()
t_env.circle(radius)
t_env.penup()
t_env.home()
t_env.pendown()
t_wolf.penup()
t_wolf.setpos(0,radius)

t_duck.showturtle()
t_wolf.showturtle()
t_duck.color('green')
t_wolf.color('red')
t_duck.pendown()
t_wolf.pendown()

##### Turtel Start #####

while getDistance(t_duck.pos(), t_env.pos())<=radius:
    DuckMove()
    WolfMove()

turtle.done()
print(getDistance(t_duck.pos(), t_wolf.pos()))

if getDistance(t_duck.pos(), t_wolf.pos())>20:
    print("Duck Win")
else:
    print("Wolf Win, Reason : Duck Cautch")

print("Duck distance: " + str(duck_dist))
print("Wolf distance: " + str(wolf_dist))