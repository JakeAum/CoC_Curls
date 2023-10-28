import tkinter as tk
#import capture_video as cv
import rep_counter as rc

# TODO make video show up in gui as overlay
# TODO add a button to kill the video loop
# TODO 
# TODO try CustomTkineter to make the gui pretty
# TODO get the output calculations to show up in the gui
# TODO make video run more smoothly


#def run_repcounter():
    #subprocess.run(['python', 'rep_counter.py'])
    
def getInputs():
    weight = entryWeight.get()
    arm = entryArm.get()
    weightGUI = int(weight)
    armGUI = str(arm)
    print(weightGUI, armGUI)
    return weightGUI, armGUI

    rc.count_reps(weightGUI, armGUI)#

def buttonAction():
    weightGUI, armGUI = getInputs()
    
    

window = tk.Tk()

labelWeight = tk.Label(text="How Much Weight? [Lbs]")
entryWeight= tk.Entry()

labelArm = tk.Label(text="Which arm are you using? [left or right]")
entryArm= tk.Entry()

button2 = tk.Button(
    text="Start Rep Counter",
    width=10,
    height=5,
    command=buttonAction
)

labelWeight.pack()
entryWeight.pack()
labelArm.pack()
entryArm.pack()
button2.pack()

window.mainloop()


# Instead of console prints i think ill map text onto the CV image for the user to see
#|--------------------------------------------------|
#|print(f"Since you were able to {weight}lbs")       |
#|print(f"for {reps} on curls with RPE of {rpe}/10")|
#|print(f"Your current max is {max}lbs, WAY TO GO!!!)|
#|--------------------------------------------------|
