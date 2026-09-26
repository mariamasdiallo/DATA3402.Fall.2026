
import math


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]

    def v_line(self, x, y, w, **kargs):
        for i in range(x, x+w):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y, y+h):
            self.set_pixel(x, i, **kargs)

    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1, y2):
            x = int(slope * y)
            self.set_pixel(x, y, **kargs)

    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Shape:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def perimeter_points(self):
        raise NotImplementedError

    def contains(self, x, y):
        raise NotImplementedError

    def paint(self, canvas):
        raise NotImplementedError

    def overlaps(self, other):
        for x, y in self.perimeter_points():
            if other.contains(x, y):
                return True

        for x, y in other.perimeter_points():
            if self.contains(x, y):
                return True

        return False


class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        Shape.__init__(self, x, y)
        self.__length = length
        self.__width = width

    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def perimeter_points(self):
        x = self.get_x()
        y = self.get_y()

        return [(x, y),
                (x + self.__length, y),
                (x + self.__length, y + self.__width),
                (x, y + self.__width)]

    def contains(self, x, y):
        return (self.get_x() <= x <= self.get_x() + self.__length and
                self.get_y() <= y <= self.get_y() + self.__width)

    def paint(self, canvas):
        x = self.get_x()
        y = self.get_y()

        for i in range(self.__length + 1):
            canvas.set_pixel(y, x + i)
            canvas.set_pixel(y + self.__width, x + i)

        for i in range(self.__width + 1):
            canvas.set_pixel(y + i, x)
            canvas.set_pixel(y + i, x + self.__length)

    def __repr__(self):
        return ("Rectangle(" + repr(self.__length) + ", " +
                repr(self.__width) + ", " +
                repr(self.get_x()) + ", " +
                repr(self.get_y()) + ")")


class Circle(Shape):
    def __init__(self, radius, x, y):
        Shape.__init__(self, x, y)
        self.__radius = radius

    def area(self):
        return math.pi * self.__radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.__radius

    def get_radius(self):
        return self.__radius

    def perimeter_points(self):
        points = []

        for i in range(16):
            angle = 2 * math.pi * i / 16
            x = self.get_x() + self.__radius * math.cos(angle)
            y = self.get_y() + self.__radius * math.sin(angle)
            points.append((x, y))

        return points

    def contains(self, x, y):
        distance = ((x - self.get_x())**2 +
                    (y - self.get_y())**2)

        return distance <= self.__radius**2

    def paint(self, canvas):
        for x, y in self.perimeter_points():
            canvas.set_pixel(round(y), round(x))

    def __repr__(self):
        return ("Circle(" + repr(self.__radius) + ", " +
                repr(self.get_x()) + ", " +
                repr(self.get_y()) + ")")


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        Shape.__init__(self, x1, y1)
        self.__x2 = x2
        self.__y2 = y2
        self.__x3 = x3
        self.__y3 = y3

    def area(self):
        x1 = self.get_x()
        y1 = self.get_y()

        return abs((x1 * (self.__y2 - self.__y3) +
                    self.__x2 * (self.__y3 - y1) +
                    self.__x3 * (y1 - self.__y2)) / 2)

    def perimeter(self):
        x1 = self.get_x()
        y1 = self.get_y()

        a = math.sqrt((self.__x2 - x1)**2 + (self.__y2 - y1)**2)
        b = math.sqrt((self.__x3 - self.__x2)**2 +
                      (self.__y3 - self.__y2)**2)
        c = math.sqrt((x1 - self.__x3)**2 +
                      (y1 - self.__y3)**2)

        return a + b + c

    def get_x2(self):
        return self.__x2

    def get_y2(self):
        return self.__y2

    def get_x3(self):
        return self.__x3

    def get_y3(self):
        return self.__y3

    def perimeter_points(self):
        return [(self.get_x(), self.get_y()),
                (self.__x2, self.__y2),
                (self.__x3, self.__y3)]

    def contains(self, x, y):
        x1, y1 = self.get_x(), self.get_y()
        x2, y2 = self.__x2, self.__y2
        x3, y3 = self.__x3, self.__y3

        d1 = (x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)
        d2 = (x - x3) * (y2 - y3) - (x2 - x3) * (y - y3)
        d3 = (x - x1) * (y3 - y1) - (x3 - x1) * (y - y1)

        negative = d1 < 0 or d2 < 0 or d3 < 0
        positive = d1 > 0 or d2 > 0 or d3 > 0

        return not (negative and positive)

    def paint(self, canvas):
        points = self.perimeter_points()

        for i in range(3):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % 3]

            steps = int(max(abs(x2 - x1), abs(y2 - y1)))

            for j in range(steps + 1):
                if steps == 0:
                    x, y = x1, y1
                else:
                    x = x1 + (x2 - x1) * j / steps
                    y = y1 + (y2 - y1) * j / steps

                canvas.set_pixel(round(y), round(x))

    def __repr__(self):
        return ("Triangle(" + repr(self.get_x()) + ", " +
                repr(self.get_y()) + ", " +
                repr(self.__x2) + ", " +
                repr(self.__y2) + ", " +
                repr(self.__x3) + ", " +
                repr(self.__y3) + ")")


class CompoundShape(Shape):
    def __init__(self, shapes):
        Shape.__init__(self, 0, 0)
        self.shapes = shapes

    def paint(self, canvas):
        for s in self.shapes:
            s.paint(canvas)

    def __repr__(self):
        return "CompoundShape(" + repr(self.shapes) + ")"


class RasterDrawing:
    def __init__(self):
        self.shapes = dict()
        self.shape_names = list()

    def add_shape(self, name, shape):
        self.shapes[name] = shape

        if name not in self.shape_names:
            self.shape_names.append(name)

    def paint(self, canvas):
        for name in self.shape_names:
            self.shapes[name].paint(canvas)

    def update(self, canvas):
        canvas.clear_canvas()
        self.paint(canvas)

    def save(self, filename):
        f = open(filename, "w")

        for name in self.shape_names:
            f.write(name + "|" + repr(self.shapes[name]) + "\n")

        f.close()


def raster_loader(filename):
    drawing = RasterDrawing()

    f = open(filename, "r")

    for line in f:
        name, shape = line.strip().split("|", 1)
        drawing.add_shape(name, eval(shape))

    f.close()

    return drawing
