from IPython.display import display, HTML
import time
import math
from matplotlib import cm

# Created at: 23rd October 2018
#         by: Tolga Atam
# Modified at: 5/21/2020
#         by: Yijia Xiong
# Modified at: 9/3/2020
#         by: Diego Garza

# Module for drawing classic Turtle figures on Google Colab notebooks.
# It uses html capabilites of IPython library to draw svg shapes inline.
# Looks of the figures are inspired from Blockly Games / Turtle (blockly-games.appspot.com/turtle)

# howdy :)

DEFAULT_WINDOW_SIZE = (800, 500)
DEFAULT_SPEED = 4
DEFAULT_TURTLE_VISIBILITY = True
DEFAULT_PEN_COLOR = 'white'
DEFAULT_TURTLE_DEGREE = 270
DEFAULT_BACKGROUND_COLOR = "black"
DEFAULT_BACKGROUND_COLOR_OPACITY = 1.0
DEFAULT_BACKGROUND_URL = ""
DEFAULT_IS_PEN_DOWN = True
DEFAULT_SVG_LINES_STRING = ""
DEFAULT_PEN_WIDTH = 4
VALID_COLORS = ('white', 'yellow', 'orange', 'red',
                'green', 'blue', 'purple', 'grey', 'black')
MAPPED_COLORS = None
NUM_COLORS = 0
COLOR_MAP = (

    # Perceptually Uniform Sequential
    'viridis', 'plasma', 'inferno', 'magma', 'cividis',

    # Sequential
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',

    #Sequential (2)
    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper',

    # Diverging
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',


    # Cyclic
    'twilight', 'twilight_shifted', 'hsv',

    # Qualitative
    'Pastel1', 'Pastel2', 'Paired', 'Accent',
    'Dark2', 'Set1', 'Set2', 'Set3',
    'tab10', 'tab20', 'tab20b', 'tab20c',

    # Miscellaneous
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar')

SVG_TEMPLATE = """
<head>
<style>
body
{{
    background-image: url("{background_url}");
    background-repeat: no-repeat;
    background-size: {window_width}px {window_height}px
}}
</style>
</head>

<svg width="{window_width}" height="{window_height}">
<rect width="100%" height="100%" fill="{background_color}" fill-opacity="{opacity}"/>
{lines}
{turtle}
</svg>
"""

TURTLE_SVG_TEMPLATE = """
<g visibility={visibility} transform="rotate({degrees},{turtle_x},{turtle_y}) translate({turtle_x}, {turtle_y})">
    <circle stroke="{turtle_color}" stroke-width="3" fill="transparent" r="12" cx="0" cy="0"/>
    <polygon points="0,19 3,16 -3,16" style="fill:{turtle_color};stroke:{turtle_color};stroke-width:2"/>
</g>
"""

SPEED_TO_SEC_MAP = {1: 1.5, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.3, 6: 0.18,
                    7: 0.12, 8: 0.06, 9: 0.04, 10: 0.02, 11: 0.01, 12: 0.001, 13: 0.0001}


# helper function that maps [1,10] speed values to ms delays
def _speedToSec(speed):
    return SPEED_TO_SEC_MAP[speed]


timeout = _speedToSec(DEFAULT_SPEED)

is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
pen_color = DEFAULT_PEN_COLOR
window_size = DEFAULT_WINDOW_SIZE
turtle_pos = (DEFAULT_WINDOW_SIZE[0] // 2, DEFAULT_WINDOW_SIZE[1] // 2)
turtle_degree = DEFAULT_TURTLE_DEGREE
background_color = DEFAULT_BACKGROUND_COLOR
background_url = DEFAULT_BACKGROUND_URL
background_color_opacity = DEFAULT_BACKGROUND_COLOR_OPACITY
is_pen_down = DEFAULT_IS_PEN_DOWN
svg_lines_string = DEFAULT_SVG_LINES_STRING
pen_width = DEFAULT_PEN_WIDTH

drawing_window = None


# construct the display for turtle
def initializeTurtle(initial_speed=DEFAULT_SPEED, initial_window_size=DEFAULT_WINDOW_SIZE):
    global window_size
    global drawing_window
    global timeout
    global is_turtle_visible
    global pen_color
    global turtle_pos
    global turtle_degree
    global background_color
    global background_color_opacity
    global background_url
    global is_pen_down
    global svg_lines_string
    global pen_width

    if initial_speed not in range(1, 14):
        raise ValueError(
            'initial_speed should be an integer in interval [1,13]')
    timeout = _speedToSec(initial_speed)
    if not (isinstance(initial_window_size, tuple) and len(initial_window_size) == 2 and isinstance(
            initial_window_size[0], int) and isinstance(initial_window_size[1], int)):
        raise ValueError('window_size should be a tuple of 2 integers')

    window_size = initial_window_size
    timeout = _speedToSec(initial_speed)

    is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
    pen_color = DEFAULT_PEN_COLOR
    turtle_pos = (window_size[0] // 2, window_size[1] // 2)
    turtle_degree = DEFAULT_TURTLE_DEGREE
    background_color = DEFAULT_BACKGROUND_COLOR
    background_color_opacity = DEFAULT_BACKGROUND_COLOR_OPACITY
    background_url = DEFAULT_BACKGROUND_URL
    is_pen_down = DEFAULT_IS_PEN_DOWN
    svg_lines_string = DEFAULT_SVG_LINES_STRING
    pen_width = DEFAULT_PEN_WIDTH

    drawing_window = display(HTML(_genereateSvgDrawing()), display_id=True)


# helper function for generating svg string of the turtle
def _generateTurtleSvgDrawing():
    if is_turtle_visible:
        vis = 'visible'
    else:
        vis = 'hidden'

    return TURTLE_SVG_TEMPLATE.format(turtle_color=pen_color, turtle_x=turtle_pos[0], turtle_y=turtle_pos[1],
                                      visibility=vis, degrees=turtle_degree - 90)


# helper function for generating the whole svg string
def _genereateSvgDrawing():
    return SVG_TEMPLATE.format(background_url=background_url, window_width=window_size[0],
                               window_height=window_size[1], background_color=background_color,
                               opacity=background_color_opacity, lines=svg_lines_string, turtle=_generateTurtleSvgDrawing())


# helper functions for updating the screen using the latest positions/angles/lines etc.
def _updateDrawing():
    if drawing_window == None:
        raise AttributeError(
            "Display has not been initialized yet. Call initializeTurtle() before using.")
    time.sleep(timeout)
    drawing_window.update(HTML(_genereateSvgDrawing()))


# helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
def _moveToNewPosition(new_pos):
    global turtle_pos
    global svg_lines_string

    start_pos = turtle_pos
    if is_pen_down:
        svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
            x1=start_pos[0], y1=start_pos[1], x2=new_pos[0], y2=new_pos[1], pen_color=pen_color, pen_width=pen_width)

    turtle_pos = new_pos
    _updateDrawing()


# helps in making coordinate system
def _convertx(input_x):
    if not (isinstance(input_x, int) or isinstance(input_x, float)):
        raise ValueError('units should be int or float')
    backend_x = (window_size[0]/2) + input_x
    return backend_x


def _converty(input_y):
    if not (isinstance(input_y, int) or isinstance(input_y, float)):
        raise ValueError('units should be int or float')
    backend_y = (window_size[1]/2) - input_y
    return backend_y


###############################
# Turtle Motion / Move and Draw
################


# makes the turtle move forward by 'units' units
def forward(units):
    if not (isinstance(units, int) or isinstance(units, float)):
        raise ValueError('units should be int or float')
    alpha = math.radians(turtle_degree)
    ending_point = (turtle_pos[0] + units * math.cos(alpha),
                    turtle_pos[1] + units * math.sin(alpha))

    _moveToNewPosition(ending_point)


def fd(units):
    forward(units)


# makes the turtle move backward by 'units' units
def backward(units):
    if not (isinstance(units, int) or isinstance(units, float)):
        raise ValueError('units should be int or float')
    forward(-1 * units)


def back(units):
    backward(units)


def bk(units):
    backward(units)


# makes the turtle turn right by 'degrees' degrees (NOT radians)
def right(degrees):
    global turtle_degree

    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees should be a number')

    turtle_degree = (turtle_degree + degrees) % 360
    _updateDrawing()


def rt(degrees):
    right(degrees)


# makes the turtle move left by 'degrees' degrees (NOT radians)
def left(degrees):
    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees should be a number')
    right(-1 * degrees)


def lt(degrees):
    right(-1 * degrees)


# used to set direction of turtle
def setdirection(degrees):
    global turtle_degree
    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees should be a number')

    turtle_degree = degrees % 360
    _updateDrawing()


# move the turtle to a designated 'x'-'y' coordinate
def goto(given_x, given_y):
    x = _convertx(given_x)
    y = _converty(given_y)
    if not x >= 0:
        raise ValueError('new x position should be within coord system')
    if not y >= 0:
        raise ValueError('new y position should be within coord system')
    _moveToNewPosition((x, y))


def setpos(given_x, given_y):
    goto(given_x, given_y)


def setposition(given_x, given_y):
    goto(given_x, given_y)


# move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
def setx(given_x):
    x = _convertx(given_x)
    if not (isinstance(x, int) or isinstance(x, float)):
        raise ValueError('new x position should be an integer')
    if not x >= 0:
        raise ValueError(
            'new x position should be within {0} and {1}', window_size[0], window_size[0])
    _moveToNewPosition((x, turtle_pos[1]))


# move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
def sety(given_y):
    y = _converty(given_y)
    if not (isinstance(y, int) or isinstance(y, float)):
        raise ValueError('new x position should be an integer')
    if not y >= 0:
        raise ValueError(
            'new y position should be within {0} and {1}', window_size[1], window_size[1])
    _moveToNewPosition((turtle_pos[0], y))


# before calling function, move pen to center of desired circle
def circle(radius, degrees=360, steps=180):
    if not (isinstance(radius, int) or isinstance(radius, float)):
        raise ValueError('radius should be an int or float')
    if not radius >= 0:
        raise ValueError('radius must be positive')
    if not isinstance(steps, int):
        raise ValueError('steps should be an int')
    if not steps >= 0:
        raise ValueError('steps must be non-negative')
    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees should be an int or float')
    if not degrees >= 0:
        raise ValueError('degrees must be non-negative')

    start = position()
    penup()
    forward(radius)
    right(90)
    pendown()
    i = 0
    while i < steps and i != int(degrees * (steps/360)):
        forward((math.pi / steps * 2) * radius)
        right(360 / steps)
        i += 1
    penup()
    left(90+degrees)
    setposition(start[0], start[1])


# from https://trinket.io/python/8875abe323, oval function
def oval(width, height, offset_tilt=None, steps=180):
    if not (isinstance(width, int) or isinstance(width, float)):
        raise ValueError('width should be an int or float')
    if not width >= 0:
        raise ValueError('width must be positive')

    if not (isinstance(height, int) or isinstance(height, float)):
        raise ValueError('height should be an int or float')
    if not height >= 0:
        raise ValueError('height must be positive')

    if not isinstance(steps, int):
        raise ValueError('steps should be an int')
    if not steps >= 0:
        raise ValueError('steps must be positive')

    start = position()
    offset_tilt = 90 + getdirection()
    if offset_tilt != None:
        offset_tilt = offset_tilt

    if not (isinstance(offset_tilt, int) or isinstance(offset_tilt, float)):
        raise ValueError('offset_tilt should be an int or float')
    if not offset_tilt >= 0:
        raise ValueError('offset_tilt must be positive')

    a = width  # ellipse width
    b = height  # ellipse height

    for i in range(steps):
        t = (i+1) * (math.pi / steps * 2)
        x = a * math.sin(t)
        y = b * math.cos(t) - b
        tilt = (360 - offset_tilt) * (math.pi / 180)
        x1 = x * math.cos(tilt) + y * math.sin(tilt) + start[0]
        y1 = x*math.sin(tilt) - y*math.cos(tilt) + start[1]
        goto(x1, y1)


def stamp(pen_width=2, desired_position=None, desired_offset_angle=None):
    starting_position = position()
    if desired_position != None:
        starting_position = desired_position
    offset_angle = getdirection()
    if desired_offset_angle != None:
        offset_angle = desired_offset_angle
    width(pen_width)

    _turtle(start=starting_position,
            offset_angle=offset_angle, pen_width=pen_width)


# new function that draws a line
def drawline(x_1, y_1, x_2, y_2):
    global svg_lines_string
    svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
        x1=_convertx(x_1), y1=_converty(y_1), x2=_convertx(x_2), y2=_converty(y_2), pen_color=pen_color, pen_width=pen_width)
    _updateDrawing()


def regularpolygon(num_sides, side_length=100, initial_angle=0):
    if not isinstance(num_sides, int):
        raise ValueError('num_sides should be an integer')
    if not num_sides >= 0:
        raise ValueError('num_sides must be positive')

    if not (isinstance(side_length, int) or isinstance(side_length, float)):
        raise ValueError('side_length should be an int or float')
    if not side_length >= 0:
        raise ValueError('side_length must be positive')

    if not (isinstance(initial_angle, int) or isinstance(initial_angle, float)):
        raise ValueError('initial_angle should be an int or float')

    penup()
    # get pen to most top left vertex
    alpha = (1/2) * (360 / num_sides)
    setdirection(270-alpha+initial_angle)
    length_to_vertex = (side_length/2) / math.sin(alpha * math.pi/180)
    forward(length_to_vertex)
    # turn to make first side in direction of angle
    setdirection(initial_angle)
    pendown()
    for i in range(0, num_sides):
        forward(side_length)
        right(360/num_sides)
    penup()
    # bring pen back to center of shape & reset direction
    setdirection(90-alpha+initial_angle)
    forward(length_to_vertex)
    setdirection(270)


def arrow(length, angle):
    setdirection(angle)
    forward(length)
    regularpolygon(3, side_length=length/2, initial_angle=angle-90)


# update the speed of the moves, [1,10]
def speed(speed):
    global timeout
    if not (isinstance(speed, int) or isinstance(speed, float)):
        raise ValueError('speed should be a number')
    if speed not in range(1, 14):
        raise ValueError('speed should be an integer in the interval [1,13]')
    timeout = _speedToSec(speed)
    # TODO: decide if we should put the timout after changing the speed
    # _updateDrawing()


####################################
# Turtle Motion / Tell Turtle's State
################


# retrieve the turtle's currrent 'x' x-coordinate
def getx():
    return(round(turtle_pos[0] - (window_size[0]/2)))


# retrieve the turtle's currrent 'y' y-coordinate
def gety():
    return(round((window_size[1]/2) - turtle_pos[1]))


def position():
    x = getx()
    y = gety()
    return (x, y)


def pos():
    position()


def getdirection():
    return turtle_degree


def distance(x_2, y_2):
    x_1, y_1 = position()
    if not (isinstance(x_2, int) or isinstance(x_2, float)):
        raise ValueError('x coordinate should be a number')
    if not (isinstance(y_2, int) or isinstance(y_2, float)):
        raise ValueError('y coordinate should be a number')
    return math.sqrt((abs(x_2 - x_1))**2 + (abs(y_2 - y_1))**2)

#############################
# Pen Control / Drawing State
##############


# lowers the pen such that following turtle moves will now cause drawings
def pendown():
    global is_pen_down

    is_pen_down = True
    # TODO: decide if we should put the timout after releasing the pen
    # _updateDrawing()


# raises the pen such that following turtle moves will not cause any drawings
def penup():
    global is_pen_down

    is_pen_down = False
    # TODO: decide if we should put the timout after lifting the pen
    # _updateDrawing()


def getwidth():
    return pen_width


# change the width of the lines drawn by the turtle, in pixels
def width(width):
    global pen_width
    if not isinstance(width, int):
        raise ValueError('new width position should be an integer')
    if not width > 0:
        raise ValueError('new width position should be positive')
    pen_width = width


def isdown():
    global is_pen_down
    return is_pen_down


#############################
# Pen Control / Color Control
##############


# change the color of the pen; valid colors are defined at VALID_COLORS
def color(color):
    global pen_color

    if not color in VALID_COLORS:
        raise ValueError(
            'color value should be one of the following: ' + str(VALID_COLORS))
    pen_color = color
    _updateDrawing()


def color_rgb(r, g, b, a=1):
    global pen_color
    if not (isinstance(r, int) or isinstance(r, float)):
        raise ValueError('r value should be a number')
    if not (r >= 0 and r < 256):
        raise ValueError('r value should be between 1 to 255')

    if not (isinstance(g, int) or isinstance(g, float)):
        raise ValueError('g value should be a number')
    if not (g >= 0 and g < 256):
        raise ValueError('g value should be between 1 to 255')

    if not (isinstance(b, int) or isinstance(b, float)):
        raise ValueError('b value should be a number')
    if not (b >= 0 and b < 256):
        raise ValueError('b value should be between 1 to 255')

    if not (isinstance(a, int) or isinstance(a, float)):
        raise ValueError('a value should be a number')
    if not (a >= 0.0 and a <= 1.0):
        raise ValueError('a value should be between 0.0 to 1.0')

    pen_color = """rgb({r},{g},{b},{a})""".format(r=r, g=g, b=b, a=a)
    _updateDrawing()


def initializeColors(numColors=256, colormap="rainbow"):
    global MAPPED_COLORS
    global NUM_COLORS
    if not colormap in COLOR_MAP:
        raise ValueError(
            'Colormap value should be one of the following: ' + str(COLOR_MAP))
    if not (isinstance(numColors, int) or isinstance(numColors, float)):
        raise ValueError('numColors value should be a number')
    if not (numColors > 0 and numColors < 256):
        raise ValueError('numColors should be an integer between 1 to 255')
    MAPPED_COLORS = cm.get_cmap(colormap, numColors)
    NUM_COLORS = numColors


def set_color(n=0):
    global MAPPED_COLORS
    global NUM_COLORS
    if not (isinstance(n, int) or isinstance(n, float)):
        raise ValueError('n value should be a number')
    if n >= NUM_COLORS or n < 0:
        raise ValueError(
            'color number should be in the range of 0 to the number of colors initialized - 1.')
    r, g, b, alpha = MAPPED_COLORS(n)
    color_rgb(r*255, g*255, b*255, alpha)


def getcolor():
    return pen_color


######################
# More drawing control
######


def new_window():
    global MAPPED_COLORS
    global NUM_COLORS
    MAPPED_COLORS = None
    NUM_COLORS = 0
    initializeTurtle()


################
# Turtle's state
#########


# switch turtle visibility to OFF
def hideturtle():
    global is_turtle_visible

    is_turtle_visible = False
    _updateDrawing()


def ht():
    hideturtle()


# switch turtle visibility to ON
def showturtle():
    global is_turtle_visible

    is_turtle_visible = True
    _updateDrawing()


def st():
    showturtle()


def isvisible():
    global is_turtle_visible
    return is_turtle_visible


################
# Window Control
########


# change the background color of the drawing area; valid colors are defined at VALID_COLORS
def bgcolor(color):
    global background_color
    global background_url
    global background_color_opacity

    if not color in VALID_COLORS:
        raise ValueError(
            'color value should be one of the following: ' + str(VALID_COLORS))
    background_url = ""
    background_color_opacity = 1.0
    background_color = color
    _updateDrawing()


def bgcolor_rgb(r, g, b, a=1):
    global background_color
    global background_url
    global background_color_opacity

    if not (isinstance(r, int) or isinstance(r, float)):
        raise ValueError('r value should be a number')
    if not (r >= 0 and r < 256):
        raise ValueError('r value should be between 1 to 255')

    if not (isinstance(g, int) or isinstance(g, float)):
        raise ValueError('g value should be a number')
    if not (g >= 0 and g < 256):
        raise ValueError('g value should be between 1 to 255')

    if not (isinstance(b, int) or isinstance(b, float)):
        raise ValueError('b value should be a number')
    if not (b >= 0 and b < 256):
        raise ValueError('b value should be between 1 to 255')

    if not (isinstance(a, int) or isinstance(a, float)):
        raise ValueError('a value should be a number')
    if not (a >= 0.0 and a <= 1.0):
        raise ValueError('a value should be between 0.0 to 1.0')

    background_url = ""
    background_color_opacity = 1.0
    background_color = """rgb({r},{g},{b}, {a})""".format(r=r, g=g, b=b, a=a)
    _updateDrawing()


def bgset_color(n=0):
    global MAPPED_COLORS
    global NUM_COLORS
    if not (isinstance(n, int) or isinstance(n, float)):
        raise ValueError('n value should be a number')
    if n >= NUM_COLORS or n < 0:
        raise ValueError(
            'color number should be in the range of 0 to the number of colors initialized - 1.')
    r, g, b, alpha = MAPPED_COLORS(n)
    bgcolor_rgb(r*255, g*255, b*255, alpha)


# given image address, will set it as background
def bgurl(url):
    global background_url
    global background_color_opacity
    global pen_color

    if not isinstance(url, str):
        raise ValueError('background url should be a string')
    background_url = url
    background_color_opacity = 0.0
    pen_color = "black"
    _updateDrawing()


# delays execution of next object for given delay time
def delay(delay_time):
    time.sleep(delay_time)


#############################
# Settings and Special Methods
##########


def window_width():
    return window_size[0]


def window_height():
    return window_size[1]


###########################################
# helper functions to make turtle stamp (:


def _foot(pos_to_leg, width,  offset_angle=0):
    starting_dir = getdirection()
    initial_pos = position()

    penup()
    right(90)
    forward(pos_to_leg[0])
    left(90)
    forward(pos_to_leg[1])

    right(offset_angle)
    left(90)
    forward((width/4)*(1+math.sqrt(2)))
    right(90)

    pendown()

    forward(width)
    right(45)
    forward(width/2)
    right(45)
    forward(width/2)
    right(45)
    forward(width/2)
    right(45)
    forward(width)

    penup()

    setdirection(starting_dir)
    setposition(initial_pos[0], initial_pos[1])


def _turtle(start, offset_angle, pen_width):
    hideturtle()
    width(pen_width)
    penup()

    goto(start[0], start[1])
    starting_pos = position()
    right(offset_angle)

    a = 7  # width
    b = 15  # height
    pendown()
    oval(a, b, steps=30, offset_tilt=offset_angle)

    ########
    # feet
    #####
    setdirection(offset_angle)
    _foot(pos_to_leg=(a/2, b*5/4), offset_angle=45, width=a)
    _foot(pos_to_leg=(-a/2, b*5/4), offset_angle=-45, width=a)
    _foot(pos_to_leg=(a/2, b*1/2), offset_angle=45+90, width=a)
    _foot(pos_to_leg=(-a/2, b*1/2), offset_angle=-45-90, width=a)

    ###########
    # head
    ####
    forward(2*b)
    left(110)
    circle(a*5/8, degrees=240, steps=20)
    penup()

    ############
    # shell design :)
    #####
    setdirection(offset_angle)
    goto(starting_pos[0], starting_pos[1])

    right(90)
    forward(a/2)
    left(90)
    forward(b)

    pendown()
    regularpolygon(6, side_length=a/2, initial_angle=offset_angle+90)

    setdirection(offset_angle)
    goto(starting_pos[0], starting_pos[1])

    right(90)
    forward(-a/2)
    left(90)
    forward(b)

    pendown()
    regularpolygon(6, side_length=a/2, initial_angle=offset_angle+90)

    setdirection(offset_angle)
    goto(starting_pos[0], starting_pos[1])

    right(90)
    forward(0)
    left(90)
    forward(b*3/2)

    pendown()
    regularpolygon(6, side_length=a*2/3, initial_angle=offset_angle+90)

    setdirection(offset_angle)
    goto(starting_pos[0], starting_pos[1])

    right(90)
    forward(0)
    left(90)
    forward(b*1/2)

    pendown()
    regularpolygon(6, side_length=a*2/3, initial_angle=offset_angle+90)
