from IPython.display import display, HTML
import time
import math
from matplotlib import cm

# Created at: 23rd October 2018
#         by: Tolga Atam
# Modified at: 5/21/2020
#         by: Yijia Xiong

# Module for drawing classic Turtle figures on Google Colab notebooks.
# It uses html capabilites of IPython library to draw svg shapes inline.
# Looks of the figures are inspired from Blockly Games / Turtle (blockly-games.appspot.com/turtle)

DEFAULT_WINDOW_SIZE = (800, 500)
DEFAULT_SPEED = 4
DEFAULT_TURTLE_VISIBILITY = True
DEFAULT_PEN_COLOR = 'white'
DEFAULT_TURTLE_DEGREE = 270
DEFAULT_BACKGROUND_COLOR = 'black'
DEFAULT_IS_PEN_DOWN = True
DEFAULT_SVG_LINES_STRING = ""
DEFAULT_PEN_WIDTH = 4
VALID_COLORS = ('white', 'yellow', 'orange', 'red', 'green', 'blue', 'purple', 'grey', 'black')
MAPPED_COLORS = None
NUM_COLORS = 0
COLOR_MAP = ('hsv','viridis','gray', 'spring', 'summer', 'autumn', 'winter', 'cool', 'hot', 'ocean',  'terrain', 'brg','gist_rainbow', 'rainbow', 'jet')

SVG_TEMPLATE = """
      <svg width="{window_width}" height="{window_height}">
        <rect width="100%" height="100%" fill="{background_color}"/>
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

SPEED_TO_SEC_MAP = {1: 1.5, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.3, 6: 0.18, 7: 0.12, 8: 0.06, 9: 0.04, 10: 0.02, 11: 0.01, 12: 0.001, 13: 0.0001}


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
    global is_pen_down
    global svg_lines_string
    global pen_width

    if initial_speed not in range(1, 14):
        raise ValueError('initial_speed should be an integer in interval [1,13]')
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

    return TURTLE_SVG_TEMPLATE.format(turtle_color=pen_color, turtle_x=turtle_pos[0], turtle_y=turtle_pos[1], \
                                      visibility=vis, degrees=turtle_degree - 90)


# helper function for generating the whole svg string
def _genereateSvgDrawing():
    return SVG_TEMPLATE.format(window_width=window_size[0], window_height=window_size[1],
                               background_color=background_color, lines=svg_lines_string,
                               turtle=_generateTurtleSvgDrawing())


# helper functions for updating the screen using the latest positions/angles/lines etc.
def _updateDrawing():
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
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

def drawline(x1,y1,x2,y2):
    global svg_lines_string
    svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
            x1=x1, y1=y1, x2=x2, y2=y2, pen_color=pen_color, pen_width=pen_width)
    _updateDrawing()

# makes the turtle move forward by 'units' units
def forward(units):
    alpha = math.radians(turtle_degree)
    ending_point = (turtle_pos[0] + units * math.cos(alpha), turtle_pos[1] + units * math.sin(alpha))

    _moveToNewPosition(ending_point)

def fd(units):
    forward(units)

# makes the turtle move backward by 'units' units
def backward(units):
    forward(-1 * units)

def bk(units):
    forward(-1 * units)

# makes the turtle move right by 'degrees' degrees (NOT radians)
def right(degrees):
    global turtle_degree

    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees should be a number')

    turtle_degree = (turtle_degree + degrees) % 360
    _updateDrawing()

def rt(degrees):
    right(degrees)

# makes the turtle move right by 'degrees' degrees (NOT radians)
def left(degrees):
    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees should be a number')
    right(-1 * degrees)

def lt(degrees):
    right(-1 * degrees)

# raises the pen such that following turtle moves will not cause any drawings
def penup():
    global is_pen_down

    is_pen_down = False
    # TODO: decide if we should put the timout after lifting the pen
    # _updateDrawing()

# lowers the pen such that following turtle moves will now cause drawings
def pendown():
    global is_pen_down

    is_pen_down = True
    # TODO: decide if we should put the timout after releasing the pen
    # _updateDrawing()


# update the speed of the moves, [1,10]
def speed(speed):
    global timeout

    if speed not in range(1, 13):
        raise ValueError('speed should be an integer in the interval [1,13]')
    timeout = _speedToSec(speed)
    # TODO: decide if we should put the timout after changing the speed
    # _updateDrawing()


# move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
def setx(x):
    if not x >= 0:
        raise ValueError('new x position should be nonnegative')
    _moveToNewPosition((x, turtle_pos[1]))


# move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
def sety(y):
    if not y >= 0:
        raise ValueError('new y position should be nonnegative')
    _moveToNewPosition((turtle_pos[0], y))

# retrieve the turtle's currrent 'x' x-coordinate
def getx():
    return(turtle_pos[0])


# retrieve the turtle's currrent 'y' y-coordinate
def gety():
    return(turtle_pos[1])


# move the turtle to a designated 'x'-'y' coordinate
def goto(x, y):
    if not x >= 0:
        raise ValueError('new x position should be nonnegative')
    if not y >= 0:
        raise ValueError('new y position should be nonnegative')
    _moveToNewPosition((x, y))


# switch turtle visibility to ON
def showturtle():
    global is_turtle_visible

    is_turtle_visible = True
    _updateDrawing()


# switch turtle visibility to ON
def hideturtle():
    global is_turtle_visible

    is_turtle_visible = False
    _updateDrawing()


# change the background color of the drawing area; valid colors are defined at VALID_COLORS
def bgcolor(color):
    global background_color

    if not color in VALID_COLORS:
        raise ValueError('color value should be one of the following: ' + str(VALID_COLORS))
    background_color = color
    _updateDrawing()


# change the color of the pen; valid colors are defined at VALID_COLORS
def color(color):
    global pen_color

    #if not color in VALID_COLORS:
    #    raise ValueError('color value should be one of the following: ' + str(VALID_COLORS))
    pen_color = color
    _updateDrawing()

def color_rgb(r,g,b,a=1):
    global pen_color
    pen_color = """rgb({r},{g},{b})""".format(r=r,g=g,b=b)
    _updateDrawing()

# select colormap
def initializeColors(numColors=256,colormap="rainbow"):
    global MAPPED_COLORS
    global NUM_COLORS
    if not colormap in COLOR_MAP:
        raise ValueError('Colormap value should be one of the following: ' + str(COLOR_MAP))
    if not (numColors >0 and numColors < 256):
        raise ValueError('numColors should be an integer between 1 to 255')
    MAPPED_COLORS=cm.get_cmap(colormap,numColors)   
    NUM_COLORS = numColors


def setcolor(n=0):
    global MAPPED_COLORS
    global NUM_COLORS
    if n >= NUM_COLORS or n < 0:
        raise ValueError('color number should be in the range of 0 to the number of colors initialized - 1.')
    r,g,b,alpha=MAPPED_COLORS(n)
    color_rgb(r*255,g*255,b*255,alpha)  

    
# change the width of the lines drawn by the turtle, in pixels
def width(width):
    global pen_width

    if not isinstance(width, int):
        raise ValueError('new width position should be an integer')
    if not width > 0:
        raise ValueError('new width position should be positive')

    pen_width = width
    # TODO: decide if we should put the timout after changing the speed
    # _updateDrawing()
