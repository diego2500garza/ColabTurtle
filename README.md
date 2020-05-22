Turtle Module for iPython/Colab notebooks
===================
This module was forked from Tolga Atam's original work. I found it when I was trying to introducing turtle drawing to my kids. It was a nice piece of work. However the colors available for the pen were limited. Maybe Tolga wanted to keep it as simple as possible. But personly I like those figures with repeating simple shapes in gradient colors. That was what fascinated me when I played with the turtle drawing system many years ago. This project was not very active and its pip installation is outdated as well. So I decided to add those functions myself.

Beside the color functions, I also added some functions with shorten names, i.e. fd(), bk(), rt() and lt(). People used the old logo language would know why I did that :) I remove the requirement of integer argument for those functions. It is not necessory but does cause confusion for the kids.

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

Then initialize the plotting area as this:

    initializeTurtle()

From here you can play with the turtle functions: forward(distance), backward(distance),right(distance),left(distance), fd(distance),bk(distance),rt(distance),lt(distance), color("red"), penup(),pendown(). For example, this code will draw a red triangle:

    initializeTurtle()
    color("red")
    for i in range(3)
      forward(100)
      right(120)

To use the gradient colors, a color palette need to be initialized first as this:

    initializeColors(numColors, colormap)
    
Then a call to setcolor(n) will set the pen color as the nth color in the palette. 

Here is a simple code to demostrate the usage:

    initializeTurtle(initial_speed=13)
    hideturtle()
    width(1)
    initializeColors(60,"hsv") #set a palette of 60 colors with the rainbow colormap
    backward(100)
    for i in range(180):
      setcolor(i%60)
      forward(200)
      right(145)

Play with the angle of the last statement to see how the figure pattern changes with it. Try to change the angle by one degree. What would happen when it is set to 150?

And here is a classic turtle figure:

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
    initializeColors(61,"rainbow") #set a palette of 60 colors with the rainbow colormap
    for i in range(61):
      setcolor(i)
      n = 5+ i* 5
      square(n)
      right(3)

The output should looks like this:
![Image of turtleoutput](https://github.com/YijiaXiong/ColabTurtle/blob/master/turtleoutput.png).

