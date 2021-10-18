from tkinter import *
import tkinter.colorchooser
from PIL import Image, ImageTk, ImageGrab
from datetime import datetime

# initialize tk
# create a root
# test the app to ensure the tkinter app is working
class PixelApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Pixel Art')

        cell_length = 50
        grid_width = 20
        grid_height = 10

        self.drawing_grid = Canvas(self.root)
        self.drawing_grid.grid(column=0, row=0, sticky=(N, E, S, W))
        
        self.col_picker = tkinter.colorchooser.Chooser(self.root)

        self.is_pen_selected = False
        self.is_eraser_selected = False

        # frame gives better customization on shape, size, dimensions and appearance compared to button
        # use highlight to create a background to the widget with thickness 1, thin black border

        # use a nested for in loop to draw the grid
        self.cells = []
        for x in range(0, grid_width):
            for y in range(0, grid_height):
                cell = Frame(self.drawing_grid, width=cell_length, height=cell_length, bg='white', highlightbackground='black', highlightcolor='black', highlightthickness='1')   
                cell.grid(column = x, row = y)
                # <Button-1> is Left Mouse Button
                cell.bind('<Button-1>', self.tap_cell)
                self.cells.append(cell)
        
        # create the control panel
        control_frame = Frame(self.root, height=cell_length)        

        # column 0 row 1 to be just beneath the drawing grid at 0, 0
        control_frame.grid(column=0, row=1, sticky=(N, E, S, W))

        # new project button
        new_button = Button(control_frame, text='New', command=self.new_button)
        new_button.grid(column=0, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)

        # save project button
        save_button = Button(control_frame, text='Save', command=self.save_button)
        # same row, but across 2 columns. Act like the control panel has 20 columns too
        save_button.grid(column=2, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)

        # pen button
        # self.pen_image = PhotoImage(file='pencil.png')
        pen_img = Image.open('pencil.png')
        new_pen = pen_img.resize((100,50),Image.ANTIALIAS)
        self.pen_image = ImageTk.PhotoImage(new_pen)
        pen_button = Button(control_frame, text='Pen', command=self.pen_button, image=self.pen_image, width=100, height=50)
        pen_button.grid(column=8, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)

        # erase button
        # tried to fix resolution with PIL
        er_img = Image.open('eraser.png')
        new_er = er_img.resize((100,50),Image.ANTIALIAS)
        self.erase_image = ImageTk.PhotoImage(new_er)
        #self.erase_image = PhotoImage(file='eraser.png')
        erase_button = Button(control_frame, text='Erase', image=self.erase_image, width=100, height=50, command=self.erase_button)
        erase_button.grid(column=10, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)

        # colour button
        
        self.pen_colour = None
        self.colour_box = Frame(control_frame, borderwidth=2, relief='raised', bg='white')
        # have to be more specific with positioning and size as buttons have some context based on button content, so for now pad with sticky
        self.colour_box.grid(column=15,row=0, sticky=(N,E,S,W), padx=5, pady=5)
        
        colour_button = Button(control_frame, text='Pick Colour', command=self.colour_button)
        colour_button.grid(column=17, row=0, columnspan=3, sticky=(N, E, S, W), padx=5, pady=5)


        
        # specify a minimum size for rows and columns
        cols, rows = control_frame.grid_size()
        for col in range(0, cols):
            control_frame.columnconfigure(col, minsize = cell_length)
        # only one row but sure
        control_frame.rowconfigure(col, minsize=cell_length)
        # make the buttons take up 2 columns each for better spacing, 3 for colour


    
    def tap_cell(self, event):
        # bind function passes in Event param automatically
        print('cell tapped {}'.format(event))
        # each of these cells is a frame widget
        # when you tap on a cell the info is part of the cell
        widget = event.widget
        index = self.cells.index(widget)
        selected_cell = self.cells[index]

        if self.is_pen_selected:
            if self.pen_colour is not None:
                selected_cell['bg'] = self.pen_colour
        elif self.is_eraser_selected:
            selected_cell['bg'] = 'white'

    def new_button(self):
        # reset everything to default
        self.is_pen_selected = False
        self.is_eraser_selected = False
        self.pen_colour = None
        for cell in self.cells:
            cell['bg'] = 'white'        
        self.colour_box['bg'] = 'white'
        

    def save_button(self):
        # save the contents of the drawing grid
        # get dims of the grid, screenshot the dims
        # save as a png file
        # uses the Pillow lib
        # know the dims should be 1000x500, but could be affected by your screen size
        # x and y are not zero, use window info winfo and any window borders like title
        x = self.root.winfo_rootx() + self.drawing_grid.winfo_x()
        y = self.root.winfo_rooty() + self.drawing_grid.winfo_y() + 35
        
        width = 1000 + x
        height = 500 + y

        image_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S' + '.png')
        _ = ImageGrab.grab(bbox = (x,y,width,height)).save(image_name)


    
    def pen_button(self):
        self.is_eraser_selected = False
        self.is_pen_selected = True

    def erase_button(self):            
        self.is_eraser_selected = True
        self.is_pen_selected = False    

    def colour_button(self):
        # import the colour picker from tkinter        
        # can store results of the colour chooser, which are set when the colour chooser is shown
        colour_info = self.col_picker.show()
        # colour info returns a tuple((r,g,b), '#hexdec')
        # cancel counts as a complete event, but returns (None, None)
        print(colour_info[1])
        if colour_info[1] is None:
            return
        print(colour_info[1])
        self.pen_colour = colour_info[1]
        self.colour_box['bg'] = colour_info[1]
        

root = Tk()
PixelApp(root)
root.mainloop()