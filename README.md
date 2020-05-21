Turtle Module for Google Colab notebooks
===================
This module was forked from Tolga Atam's original work. I found it when I was trying to introducing turtle drawing to my kids. It was a nice piece of work. However the colors available for the pen were limited. Maybe Tolga wanted to keep it as simple as possible. But personly I like those figures with repeating simple shapes in gradient colors. That was what fascinated me when I played with the turtle drawing system many years ago. This project was not very active and its pip installation is outdated as well. So I decided to add those functions myself.

Beside the color functions, I also added some functions with shorten names, i.e. fd(), bk(), rt() and lt(). People used the old logo language would know why I did that :) I also remove the requirement of integer argument for those functions. It is not necessory but does cause confusion for the kids.

Download from Github
----
Create an empty code cell and type:

    !wget -O Turtle.py https://raw.githubusercontent.com/YijiaXiong/ColabTurtle/master/ColabTurtle/Turtle.py

Run the code cell. 
This should download the Turtle.py file to your Colab drive. You can double check it by clicking the files icon on the left panel.


Usage
----
In any code cell, import like following:

    from Turtle import *

Then you can initialize the plotting area as this:

    initializeTurtle()


A few functions were added to enable the use of gradient colors. First, a color palette need to be initialized as this:

    initializeColors(numColors, colormap)
    
Then you can call setcolor(n) to set the pen color as the nth color in the palette.

Here is a demo code:

    initializeTurtle(initial_speed=13)

    def square(n):
      penup()
      forward(n/2)
      right(90)
      backward(n/2)
      pendown()
      for i in range(4):
        forward(n)
        right(90)
      penup()
      forward(n/2)
      right(90)
      forward(n/2)
      right(180)
      pendown()
      
    hideturtle()
    width(1)
    initializeColors(60,"rainbow") #set a palette of 60 colors with the rainbow colormap
    for i in range(60):
      setcolor(i)
      n = 5+ i* 5
      square(n)
      right(3)

The output should be like this:
![Image of turtleoutput](https://github.com/YijiaXiong/ColabTurtle/blob/master/turtleoutput.png).

