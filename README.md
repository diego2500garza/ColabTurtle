Turtle Module for Google Colab notebooks
===================

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

    initializeTurtle(initial_speed=8)
    n=5
    #color_rgb(255,100,100)
    color("rgb(255,100,100)")
    hideturtle()
    width(1)
    def square(n):
      penup()
      forward(n//2)
      right(90)
      backward(n//2)
      pendown()
      for i in range(4):
        forward(n)
        right(90)
      penup()
      forward(n//2)
      right(90)
      forward(n//2)
      right(180)
      pendown()

    initializeColors(60,"rainbow")
    for i in range(60):
      setcolor(i)
      square(n)
      right(3)
      n = 5+ i* 5

The output should be like this:
![Image of turtleoutput](https://github.com/YijiaXiong/ColabTurtle/blob/master/turtleoutput.png).

Have fun drawing!
