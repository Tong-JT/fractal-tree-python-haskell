from tkinter import *
import math
from tkinter.scrolledtext import ScrolledText
import LSystem
import TreeCanvas

# Sources used:
# https://stackoverflow.com/questions/39266081/how-to-draw-recursive-tree-on-tkinter
# https://ahradwani.com/2019/11/05/python-and-lindenmayer-system-p3/

class Main:
    width = 400
    height = 600
    lineLength = 60   

    def __init__(self):
        self.LSystem = LSystem.LSystem()
        self.initialiseUI()

    def initialiseUI(self):
        window = Tk()
        window.title("L-System Tree Generator")
        window.geometry(f"{self.width + 300}x{self.height}")

        icon = PhotoImage(file='tree.png')
        window.iconphoto(False, icon)

        frame = Frame(window)
        frame.pack(fill=BOTH, expand=True)

        canvas = Canvas(frame, width=self.width, height=self.height, bg="white")
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.canvas = TreeCanvas.Canvas(canvas)

        menu = Frame(frame)
        menu.pack(side=LEFT, padx=20, fill=BOTH, expand=True)

        Label(menu, text="Number of layers: ").pack(anchor=E, fill=X, pady=5)
        self.layers = Scale(menu, from_=1, to=4, orient=HORIZONTAL)
        self.layers.pack(fill=X)

        Label(menu, text="Angle (degrees): ").pack(anchor=E, fill=X, pady=5)
        self.angle = IntVar()
        Entry(menu, textvariable=self.angle, justify=RIGHT).pack(fill=X)

        Label(menu, text="Enter line scale (0 to 1): ").pack(anchor=E, fill=X, pady=5)
        self.scale = Scale(menu, from_=0.1, to=1, orient=HORIZONTAL, resolution=0.1)
        self.scale.pack(fill=X)

        Label(menu, text="Branching rule:").pack(anchor=E, fill=X, pady=5)
        
        ruleMenu = Frame(menu)
        ruleMenu.pack(anchor=E, fill=X)

        Label(ruleMenu, text="F=").pack(side=LEFT, anchor=E)
        self.rule = StringVar()
        self.rule.set(self.LSystem.rule)
        entry = Entry(ruleMenu, textvariable=self.rule, justify=RIGHT)
        entry.pack(fill=X, expand=True)

        Button(menu, text="Create Tree", command=self.processInputs).pack(pady=10, fill=X)

        Label(menu, text="Notes").pack(anchor=W, pady=5)

        T = ScrolledText(menu, height=15, wrap=WORD)
        note = (
            "This generator supports equations which follow the L-System syntax. Here are some to get you started:\n\n"
            "F = F[+F]F[-F][F]\n"
            "F = F[+F]-F[-F][F]\n"
            "F = F[+F[+F]-F]\n\n"
            "Key:\n"
            "F: Move forward by one step.\n"
            "+: Turn left by a specified angle.\n"
            "-: Turn right by a specified angle.\n"
            "[ ]: Enclose a sequence of operations to be repeated or branched.\n"
        )
        T.insert(END, note)
        T.config(state=DISABLED)
        T.pack(pady=5)

        window.mainloop()

    def processInputs(self):
        self.canvas.canvas.delete("line")

        try:
            layers = self.layers.get()
            angle = math.radians(self.angle.get())
            scale = self.scale.get()
            rule = self.rule.get()
        except ValueError:
            print("Invalid input values")
            return

        self.LSystem.rule = rule
        axiomString = self.LSystem.buildLSystemString('F', layers)

        self.canvas.drawTree(axiomString, self.width / 2, self.height, self.lineLength, math.pi / 2, angle, scale)


if __name__ == "__main__":
    Main()