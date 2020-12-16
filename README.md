# Turtle Module for Colab notebooks

This module was forked from YijiaXiong's work, which was forked from tolgaatam's original work. I found both of these modules when looking for turtle in Colab. Both are really great. tolgaatam's original work was a great foundation to make simple drawings. YijiaXiong added many color functionalities as well as integrating some shortened function names. 

I added quite a bit of the type arguments back just to make sure things work well. I added in a circle and oval function. Also created a regular polygon, arrow, and stamp function. Added in a distance function. I restructured and added in simple functions that mimic the python turtle documentation. I restructured the code to follow the layout of the original Turtle graphics Python documentation in order to emphasize what is similar or different, for those familiar with the original.

Most of the program is still the same, so I'm going to adapt YijiaXiong's readme.

## Download from Github

Create an empty code cell and type:

    !wget -O Turtle.py https://raw.githubusercontent.com/diego2500garza/ColabTurtle/master/ColabTurtle/Turtle.py

Run the code cell...
This should download the Turtle.py file to your Colab drive. You can double check it by clicking the files icon on the left panel. 

# Usage

In any code cell, import like following:

    from Turtle import *

Then initialize the plotting area as this:

    initializeTurtle()

From here you can play with the turtle functions: forward(distance), backward(distance),right(distance),left(distance), color("red"), penup(),pendown(). For example, this code will draw a red triangle:

    initializeTurtle()
    color("red")
    for i in range(3):
      forward(100)
      right(120)

To use the gradient colors, a color palette need to be initialized first as this:

    initializeColors(numColors, colormap)
    
Then a call to set_color(n) will set the pen color as the nth color in the palette. 

Here is a simple code to demostrate the usage:

    initializeTurtle(initial_speed=13)
    hideturtle()
    width(1)
    initializeColors(60,"rainbow") #set a palette of 60 colors with the rainbow colormap
    backward(100)
    for i in range(180):
      set_color(i%60)
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
      set_color(i)
      n = 5+ i* 5
      square(n)
      right(3)

The output should looks like this:
![Image of turtleoutput](https://github.com/diego2500garza/ColabTurtle/blob/master/turtleoutput.png).

