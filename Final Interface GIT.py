# Importing all nessecary libraries
import serial # To transfer data from arduino into python.
import tkinter as tk # Used to create the GUI windows and canvas.
from tkinter import ttk # Need to check if this library is actually used in the code.
from tkinter import Tk, OptionMenu, StringVar, Label, Button # Tk used to create the GUI window, StringVar used for 
from tkinter.ttk import Progressbar, Combobox, Style
import threading
import math

app = tk.Tk()

# Making the GUI window a fullscreen
app.attributes('-fullscreen', True)  # This is for fullscreen with no tabs
app.title("Palpation Interface")

# Calculation of the size of the GUI fullscreen window created
width = app.winfo_screenwidth() # Width = 1536
print(width)
height = app.winfo_screenheight()  # Height = 864
print(height)

# We first need to specify a canvas widget, to be able to draw and pack shapes
canvas = tk.Canvas(app, width=1100, height=780)
canvas.pack()

# Create dropdown menu for sequences
sequence_selected = StringVar()

# Dropdown widget created using the Combobox function
dropdown = Combobox(app, width=30)
dropdown.set('Select Sequence')
dropdown.pack(pady=30, padx=30)
dropdownx = width - width
dropdowny = height - height
dropdown.place(x=dropdownx, y=dropdowny, anchor='nw')
dropdown['values'] = (' Sequence 1', ' Sequence 2', ' Sequence 3')

# Create a progress bar to shown progress of the sequence
the_progress = Progressbar(app, orient='horizontal', length=200, mode='determinate', maximum=8)
the_progress.pack(pady=12, padx=10)
progressx = width 
progressy = height
the_progress.place(x=progressx, y=progressy, anchor='se')

# Create a Serial object
ser = serial.Serial('COM3', 9600)  # replace with the appropriate port and baud rate

# Define the value ranges for green, yellow, and red
yellow_threshold = 1000 
red_threshold = 2000

# Draw grid axis on the circle
num_lines = 8
radius = 325
center_x = 1536/2
center_y = 864/2
x_cords = [0.0]*8
y_cords = [0.0]*8

# Styling and configuration of the pressure bar for different coloursz        
style = Style()
style.theme_use('clam')
style.configure('green.Vertical.TProgressbar', foreground='green', background='green')
style.configure('yellow.Vertical.TProgressbar', foreground='yellow', background='yellow')
style.configure('red.Vertical.TProgressbar', foreground='red', background='red')

currentSeq = [0]

def input1(ser, label, pressure, x_cords, y_cords, dropdown, the_progress):
    global currentSeq
    def update_progress_bar_with_sensor_array(sensorArray):
        global currentSeq
        if sensorArray[currentSeq[0]] > 20:
            the_progress.step(1)
            currentSeq.pop(0)
        return currentSeq
    def on_combobox_selected(the_progress):
        global currentSeq
        selected_value = dropdown.get() # Get the selected value from the dropdown
        if selected_value == ' Sequence 1':
            canvas.delete("my_text")
            canvas.create_text(550,20,text="Sequence 1",tags="my_text", anchor='center', font=('arial', 20))
            currentSeq = [0,2,3,4,5,6,7]
        elif selected_value == ' Sequence 2':
            canvas.delete("my_text")
            canvas.create_text(550,20,text="Sequence 2",tags="my_text", anchor='center', font=('arial', 20))
            currentSeq = [7,6,5,4,3,2,0]
        elif selected_value == ' Sequence 3':
            canvas.delete("my_text")
            canvas.create_text(550,20,text="Sequence 3",tags="my_text", anchor='center', font=('arial', 20))
            currentSeq = [0,2,3,7,6,5,4]
        else:
            canvas.delete("my_text")
            canvas.create_text(150,150,text="NA",tags="my_text")
            currentSeq = [0]
            
    while True:
        data = ser.readline().decode('ascii').rstrip()
        values = data.split(',')  # split the data string into a list of values
        print(values)
        sensor1 = int(values[0])
        sensor2 = int(values[0]) # Create a variable for the each seperated value
        sensor3 = int(values[1])
        sensor4 = int(values[2])
        sensor5 = int(values[3])
        sensor6 = int(values[4])
        sensor7 = int(values[5])
        sensor8 = int(values[6])
        sensor9 = int(values[-1])
        sensor2 = int(sensor2) # Turn data into integer to allow for data processing
        sensor3 = int(sensor3)
        sensor4 = int(sensor4)
        sensor5 = int(sensor5)
        sensor6 = int(sensor6) 
        sensor7 = int(sensor7)
        sensor8 = int(sensor8)
        sensor9 = int(sensor9)
        force1 = ((15.936)*(math.exp(sensor2*0.1096))) # Multiply the sensor data by the exponential formula derived from the excel sheet
        force1 = round(force1) # Round the values of the variable to the nearest integer
        force2 = ((15.936)*(math.exp(sensor3*0.1096)))
        force2 = round(force2) 
        force3 = ((15.936)*(math.exp(sensor4*0.1096)))
        force3 = round(force3)
        force4 = ((15.936)*(math.exp(sensor5*0.1096)))
        force4 = round(force4)
        force5 = ((15.936)*(math.exp(sensor6*0.1096)))
        force5 = round(force5)
        force6 = ((15.936)*(math.exp(sensor7*0.1096)))
        force6 = round(force6)
        force7 = ((15.936)*(math.exp(sensor8*0.1096)))
        force7 = round(force7) 
        force8 = ((15.936)*(math.exp(sensor9*0.1096)))
        force8 = round(force8) 
    
        label.config(text=sensor1)
        
        if (force1 < 18): # When the value from the sensor is below 16 (since the value of e^0 is 1) remove the measurement to remove the error
            force1 = 0
        if (force2 < 18): 
            force2 = 0
        if (force3 < 18): 
            force3 = 0
        if (force4 < 18): 
            force4 = 0  
        if (force5 < 18): 
            force5 = 0
        if (force6 < 18): 
            force6 = 0
        if (force7 < 18): 
            force7 = 0 
        if (force8 < 18): 
            force8 = 0 
        if (force1 > 1000): # When the value from the sensor is greater than 1000
            force1 = round(force1+(force1*0.2)) # scale the extra added values by the value of the force applied to account for the treadline
        if (force2 > 1000): 
            force2 = round(force2+(force2*0.2)) 
        if (force3 > 1000): 
            force3 = round(force3+(force3*0.2)) 
        if (force4 > 1000): 
            force4 = round(force4+(force4*0.2)) 
        if (force5 > 1000): 
            force5 = round(force5+(force5*0.2))
        if (force6 > 1000): 
            force6 = round(force6+(force6*0.2)) 
        if (force7 > 1000): 
            force7 = round(force7+(force7*0.2)) 
        if (force8 > 1000): 
            force8 = round(force8+(force8*0.2))
        print('Sensor 2:', force1, 'grams') # Print The sensor data with units
        print('Sensor 3:', force2, 'grams')
        print('Sensor 4:', force3, 'grams')
        print('Sensor 5:', force4, 'grams')
        print('Sensor 6:', force5, 'grams')
        print('Sensor 7:', force6, 'grams')
        print('Sensor 8:', force7, 'grams')
        print('Sensor 9:', force8, 'grams')
        print(sensor2)
        print(sensor3)
        print(sensor4)
        print(sensor5)
        print(sensor6)
        print(sensor7)
        print(sensor8)
        print(sensor9)
        
        if force1 > 20:
            pressure['value'] = int(force1)
            canvas.delete("small_circle")
            create_small_circle(x_cords[0], y_cords[0], 10, canvas)
        elif force2 > 20:
            pressure['value'] = int(force2)
            canvas.delete("small_circle")
            create_small_circle(x_cords[1], y_cords[1], 10, canvas)
        elif force3 > 20:
            pressure['value'] = int(force3)
            canvas.delete("small_circle")
            create_small_circle(x_cords[2], y_cords[2], 10, canvas)
        elif force4 > 20:
            pressure['value'] = int(force4)
            canvas.delete("small_circle")
            create_small_circle(x_cords[3], y_cords[3], 10, canvas)
        elif force5 > 20:
            pressure['value'] = int(force5)
            canvas.delete("small_circle")
            create_small_circle(x_cords[4], y_cords[4], 10, canvas)
        elif force6 > 20:
            pressure['value'] = int(force6)
            canvas.delete("small_circle")
            create_small_circle(x_cords[5], y_cords[5], 10, canvas)
        elif force7 > 20:
            pressure['value'] = int(force7)
            canvas.delete("small_circle")
            create_small_circle(x_cords[6], y_cords[6], 10, canvas)
        elif force8 > 20:
            pressure['value'] = int(force8)
            canvas.delete("small_circle")
            create_small_circle(x_cords[7], y_cords[7], 10, canvas)
        else:
            pressure['value'] = 0
            canvas.delete("small_circle")

        pressure.step(pressure['value'])
        if pressure['value'] >= red_threshold:
            pressure['style'] = 'red.Vertical.TProgressbar'
        elif pressure['value'] >= yellow_threshold:
            pressure['style'] = 'yellow.Vertical.TProgressbar'
        else:
            pressure['style'] = 'green.Vertical.TProgressbar'
            
        dropdown.bind("<<ComboboxSelected>>", on_combobox_selected)
        sensorArray = [sensor2,sensor3,sensor4,sensor5,sensor6,sensor7,sensor8,sensor9]
        print("Sensor array", sensorArray)
        print("Current Sequence", currentSeq)
        if len(currentSeq) > 0: 
            currentSeq = update_progress_bar_with_sensor_array(sensorArray)
        else:
            the_progress['value'] = 0

# Creating the label with text
label = Label(app, text="", font=("sans-serif", 20), fg="purple")
label.pack(pady=20)
temperaturex = width - 1300
temperaturey = height - 5
label.place(x=temperaturex, y=temperaturey, anchor='sw')

# Create a pressure bar and placement of the of the widget
the_pressure = Progressbar(app, orient='vertical', length=200, mode='determinate', maximum=3000)
the_pressure.pack(pady=12, padx=10)
pressurex = width - 1450
pressurey = height - 300
the_pressure.place(x=pressurex, y=pressurey, anchor='sw')

# Starting the serial thread
serial_thread = threading.Thread(target=input1, args=(ser, label, the_pressure, x_cords, y_cords, dropdown, the_progress), daemon=True)
serial_thread.start()

# Creating label for temperature text and its placement
temp = Label(app, font=('calibri', 20), text='Temperature:', fg='purple')
temp_textx = width - 1530
temp_texty = height - 5
temp.place(x=temp_textx, y=temp_texty, anchor='sw')

# Defining the close and stop function close the screen and close the serial port
def close():
    print("CLOSED") # Print in the console to show the button has been pushed
    ser.close() # Unote this to close th COM port instead of unplugging
def stop():
    print("STOPPED")
    app.destroy() # This command closes the interface window
    
# Create a button to execute the stop and close function
button = Button(app, text = 'STOP', bg='red', command = lambda: [close(), stop()]) # This implements a button with various features
buttonx = width - 0
buttony = height - height
button.pack(pady=20) # This determines the position of the button
button.place(x=buttonx, y=buttony, anchor='ne')




# Draw a large circle
def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1)

def create_small_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1,fill="green",tags="small_circle")

circle = create_circle(768, 432, 325, canvas)



for i in range(num_lines):
    angle = i * math.pi * 2 / num_lines
    x = center_x + math.sin(angle) * radius
    y = center_y + math.cos(angle) * radius
    x_cords[i] = center_x + math.sin(angle) * radius/2
    y_cords[i] = center_y + math.cos(angle) * radius/2
# =============================================================================
# To remove the lines please thank you
#     canvas.create_line(center_x, center_y, x, y)
#     circle = create_circle(x_cords[i], y_cords[i], 10, canvas)
# =============================================================================

# Define a function to update the position of the small circle
def update_position(array_x, array_y):
    # Delete the old small circle, if it exists
    canvas.delete("small_circle")

    # Draw the new small circle on top of the large circle
    create_small_circle(array_x, array_y, 10, canvas)

# Keep Running the window
app.mainloop()