import math

class Canvas:

    def __init__(self, canvas):
        self.canvas = canvas

    def drawTree(self, axiomString, x, y, lineLength, centerline, angle, scale):
        stack = []
        for symbol in axiomString:
            if symbol == 'F':
                x2 = x + math.cos(centerline) * lineLength
                y2 = y - math.sin(centerline) * lineLength
                self.canvas.create_line(x, y, x2, y2, tags="line")
                x, y = x2, y2
                lineLength *= scale
            elif symbol == '+':
                centerline += angle
            elif symbol == '-':
                centerline -= angle
            elif symbol == '[':
                stack.append((centerline, x, y, lineLength))
            elif symbol == ']':
                centerline, x, y, lineLength = stack.pop()