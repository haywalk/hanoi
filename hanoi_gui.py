'''
Graphical Towers of Hanoi solver
Hayden Walker (www.haywalk.ca)
2022-12-07
'''

from tkinter import *
import tkinter.messagebox as messagebox
from hanoi import * # hanoi solver is in the other file

class HanoiSolver:

    def __init__(self, master):
        '''
        Initialize the window
        '''

        # OPTIONS
        self.title = 'The Tower of Hanoi'
        self.delay = 500
        self.max_disks = 10
        self.canv_width = 500
        self.canv_height = 300
        self.disk_height = 20
        self.disk_width_increment = 14
        self.base_height = 50
        self.base_colour = '#cd853f'
        self.stack_width = 10
        self.stack_height = 200
        self.space_between = 100
        self.colours = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

        # create window
        master.resizable(False, False)
        master.title(self.title)
        self.root = master

        # create toolbar
        self.toolbar = Frame(master, relief = RAISED)
        self.toolbar.pack(side = TOP, fill = X)

        # create canvas
        self.canv = Canvas(width = self.canv_width, height = self.canv_height, bg = "white")
        self.canv.pack()

        # add label for entry field
        Label(self.toolbar, text = "Number of disks: ").pack(side = LEFT)

        # create entry field for number of disks
        self.enternum = Entry(self.toolbar, width = 7)
        self.enternum.pack(side = LEFT)
        self.enternum.insert(0, str(self.max_disks))

        # add buttons
        Button(self.toolbar, text = "About", command = self.about).pack(side = RIGHT)
        Button(self.toolbar, text = "Next Step", command = self.next_step).pack(side = RIGHT)
        Button(self.toolbar, text = "Previous Step", command = self.prev_step).pack(side = RIGHT)
        Button(self.toolbar, text = 'Stop', command = self.stop).pack(side = RIGHT)
        Button(self.toolbar, text = 'Start', command = self.auto).pack(side = RIGHT)
        Button(self.toolbar, text = 'Reset', command = self.generate).pack(side = RIGHT)

        # Nothing has been generated yet
        self.state = 0
        self.num_disks = self.max_disks
        self.states = []
        self.auto_running = True

        # draw the towers
        self.generate()

    def generate(self):
        '''
        Generate the states and draw the first state
        '''

        try:
            self.num_disks = min(int(self.enternum.get()), self.max_disks)
        except:
            self.num_disks = self.max_disks

        self.state = 0
        self.states = hanoi(self.num_disks)
        self.draw_current_state()

    def prev_step(self):
        '''
        Go back to previous state
        '''

        self.state -= 1

        if self.state < 0:
            self.state = len(self.states) - 1

        self.draw_current_state()

    def next_step(self):
        '''
        Advance the state by one
        '''

        self.state = (self.state + 1) % len(self.states)
        self.draw_current_state()

    def get_stack_coordinate(self, stack_num):
        '''
        Return the x-coordinate of one of the stacks
        (the coordinate is the coordinate of the left side
        of its 'post'/'rod')

        With width x, we have
        1/6 * x | 1/3 * x | 1/3 * x | 1/6 * x
        so that each rod has the same amount of space
        '''
        return (self.canv_width // 3) * stack_num + (self.canv_width // 6)

    def draw_base(self):
        '''
        Draw the base (the empty stacks)
        '''

        # draw the bottom
        self.canv.create_rectangle(
                0, self.canv_height - self.base_height, self.canv_width, self.canv_height,
                outline = self.base_colour,
                fill = self.base_colour
            )

        # draw the empty stacks
        for i in range(3):
            # get the starting x-coordinate
            start_x = self.get_stack_coordinate(i)

            # draw the empty stack
            self.canv.create_rectangle(
                    start_x, self.canv_height - self.base_height - self.stack_height, start_x + self.stack_width, self.canv_height - self.base_height,
                    outline = self.base_colour,
                    fill = self.base_colour
                )

    def draw_stack(self, stack_num, current_stacks):
        '''
        Draw one of the stacks
        '''

        # find the center of the post
        center = self.get_stack_coordinate(stack_num) + (self.stack_width // 2)

        # get starting y-coordinate
        y = self.stack_height + self.base_height - (self.disk_height * len(current_stacks[stack_num]))

        # draw each disk in the stack
        for index in range(len(current_stacks[stack_num])):
            # get the disk's value
            value = current_stacks[stack_num][::-1][index]

            # get its width
            width = self.disk_width_increment * value + self.disk_width_increment;

            # draw a rectangle
            self.canv.create_rectangle(
                    center - (width // 2), y, center + (width // 2), y + self.disk_height,
                    fill = self.colours[(value - 1) % len(self.colours)]
                )

            # increment y-coordinate
            y += self.disk_height


    def draw_current_state(self):
        '''
        Draw the current state
        '''
        # clear the canvas
        self.canv.delete(ALL)

        # draw the base
        self.draw_base()

        # get the state to draw
        to_draw = self.states[self.state]

        # draw the stakcs
        for i in range(3):
            self.draw_stack(i, to_draw)

        # draw move counter
        self.canv.create_text(self.canv_width // 2, self.canv_height - (self.base_height // 2), text = f'Moves: {self.state}')

    def auto_step(self):
        '''
        Step through the solution with a time delay
        '''
        # stop if done or stopped
        if self.state == len(self.states) - 1 or not self.auto_running:
            self.auto_running = False
            return

        # advance a step
        self.next_step()

        # delay before repeating
        self.root.after(self.delay, self.auto_step)

    def auto(self):
        '''
        Start auto-solving
        '''
        self.auto_running = True
        self.root.after(self.delay, self.next_step)
        self.root.after(2 * self.delay, self.auto_step)

    def stop(self):
        '''
        Stop auto-solving
        '''
        self.auto_running = False

    def about(self):
        messagebox.showinfo("About", "Tower of Hanoi Solver\nHayden Walker, December 2022\ngithub.com/haywalk/hanoi")

# start the program
root = Tk()
window = HanoiSolver(root)
root.mainloop()
