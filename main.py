from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#ecb390"
RED = "#dd4a48"
GREEN = "#c0d8c0"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None  # Need to set this as a global variable in order to access it later in countdown mechanism


# ---------------------------- TIMER RESET ------------------------------- #

# Reset check marks, reset text, stop timer, change title back
# Hardest part is stopping the timer where we need to call after_cancel()


def reset_timer():
    global timer, reps
    reps = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text=f"00:00")
    timer_label.config(text="T I M E R")
    check_label.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #

# Now that we can get it to count down, we need to tie it to the start button
# This function is responsible for calling the count_down once the start button is pressed
# When we call count_down outside a function, make sure it is after we create the canvas


def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="B R E A K", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="B R E A K", fg=PINK)
    else:
        count_down(work_sec)
        timer_label.config(text="W O R K", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

# We could use this method in principle, but remember that we're in a GUI
# If we think about a command line program, like get our console to do something
# It will only do something if we give it instruction and hit enter, it does not need to keep an eye out for what we do
# But GUI is different because it keeps watching the screen and keep listening for events
# When an event happens, it will react and these types of GUI programs are event driven
# The way it is driven is through our window.mainloop()
# If we have another loop in our program, it won't reach main loop

# import time
#
# count = 5
# while True:
#     time.sleep(1)
#     count -= 1

# We need something to happen on screen and timing mechanism - Tkinter has already thought of this
# We can use the built-in method after to our window widget
# After method takes the amount of time it should wait (ms)
# and after this amount of time, it calls a function that we tell it to, passing in any argument we want to give
# We want this method to repeat itself to loop
# We can achieve this by putting this method call inside a function and have it call itself

# def say_something(a, b, c):
#     print(a)
#     print(b)
#     print(c)
#
# window.after(1000, say_something, 3, 5, 8)


def count_down(count):
    # Now we need to format the count to display it correctly instead of 300 seconds
    # It needs to display "01:35"
    # We can get the minutes by dividing by 60 using floor division
    # Then use modulo operator to get the remaining seconds
    # 245 / 60 = 4 minutes
    # 245 % 60 = 8 seconds

    count_min = count // 60
    count_sec = count % 60

    # Next challenge is - how do we get it to display "5:00" instead of "5:0"?
    # We need to learn about dynamic typing!
    # The 0 is coming from count_sec since it is taking the count in seconds and dividing it by 60
    # It is finding the remainder using the modulo
    # When there is no remainder, it will be equal to 0
    # We could use an if statement to check whenever the seconds is equal to 0, we assign it to a string "00"
    # There is still a bug with this because when it reaches 9 seconds, it will say 0:9 instead of 0:09

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # The way we change text in canvas is different from label, can't use config
    # Tap into the canvas object and call item config method
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    global timer
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        for i in range(reps // 2):
            marks += " ✔"
        check_label.config(text=marks, font=(FONT_NAME, 10, "bold"))


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro Timer")
# Background color is based on hex code
window.config(padx=100, pady=50, bg=YELLOW)

# Canvas Widget allows us to layer things on top of each other, place an image on our program and place text on top
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# We need to use the PhotoImage class in order to read the file which then passes into our canvas.create_image method
tomato_img = PhotoImage(file="tomato.png")
# We need to indicate the x and y positions, so we halved it from our Canvas width and height
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

timer_label = Label(text="T I M E R", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_label = Label(fg=GREEN, bg=YELLOW)
check_label.grid(column=1, row=3)

window.mainloop()

# Notes on Dynamic Typing
# If we try to add an integer to a string, we will see that it is not possible
# So let's create a variable called "a"
# a = 3
# If we change the variable to hold a different type of data
# a = "Hello"
# We see that variable "a" is now a data type string
# Dynamic Typing allows us to change a variable's data type by changing the content

# Python is strongly typed because it holds onto the data type for a variable
# If we do something that is not meant for a string, it will cause a Type Error
# The part where the language is dynamically typed, we can dynamically change the data type of any variable
# Dynamic typing is not available in other languages like Java, C, Swift
