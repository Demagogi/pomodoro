import tkinter
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 30
REPS = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():  # command for button reset
	global REPS  # resets everything to starting values
	window.after_cancel(timer)  # stops the timer, timer will get str value after program starts
	canvas.itemconfig(time_text, text="00:00")  # resets the text canvas to 00:00
	REPS = 0
	timer_label.config(text="Timer")  # returns text to "Timer"
	checkmark_label.config(text="")  # removes check marks from last session


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_time():  # this is function for start button
	global REPS
	REPS += 1
	# transform minutes in seconds
	work_sec = WORK_MIN * 60
	short_break_sec = SHORT_BREAK_MIN * 60
	long_break_sec = LONG_BREAK_MIN * 60

	# check witch rep it is to configure is it time for rest or for work
	if REPS % 8 == 0:  # at 8th repeat, its long break time
		count_down(long_break_sec)
		timer_label.config(text="Long Brake", fg=GREEN)
	elif REPS % 2 == 0:  # short brakes are at 1/3/5/7th repeat
		count_down(short_break_sec)
		timer_label.config(text="Short Brake", fg=PINK)
	else:  # if it is not rest time, then it is working time
		count_down(work_sec)
		timer_label.config(text="Work Time", fg=RED)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
# recursive function was needed to call itself
def count_down(count):
	count_min = math.floor(count/60)  # use math module to round up the number
	count_sec = count % 60

	if 9 >= count_sec >= 0:  # dynamic typing - you can change type of  variable during execution
		count_sec = f"0{count_sec}"

	canvas.itemconfig(time_text, text=f"{count_min}:{count_sec}")  # this is the way to change text in canvas

	if count > 0:
		global timer  # we need to make this global because this effect must be stopped at reset_timer() function
		timer = window.after(1000, count_down, count-1)  # function calls itself after 1000 milliseconds
	# with -1 attribute value
	else:
		start_time()
		text = ""
		work_sessions = math.floor(REPS/2)  # work period is every second one, so we can get hold of that and round it
		for _ in range(work_sessions):
			text += "✔"  # adds a checkmark every time the work period is done
		checkmark_label.config(text=text)  # changes the checkmark text


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()  # create window
window.title("Pomodoro")  # change title of the window
window.config(padx=100, pady=100, bg=YELLOW)  # add padding from boarders and background colour

canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)  # create canvas
tomato_photo = tkinter.PhotoImage(file="tomato.png")  # make tomato.png usable in the tkinter gui
canvas.create_image(100, 112, image=tomato_photo)  # create canvas layer with that image from above
time_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))  # create timer layer
canvas.grid(row=1, column=1)  # this is used for actually see stuf on the screen

timer_label = tkinter.Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50, "bold"))  # timer label above photo
timer_label.grid(row=0, column=1)

checkmark_label = tkinter.Label(fg=RED, bg=YELLOW, font=(FONT_NAME, 35, "bold"))  # create checkmark label
checkmark_label.grid(row=3, column=1)

start_button = tkinter.Button(text="Start", command=start_time)  # create button for start
start_button.grid(row=2, column=0)

reset_button = tkinter.Button(text="Reset", command=reset_timer)  # create button for the reset
reset_button.grid(row=2, column=2)


window.mainloop()
