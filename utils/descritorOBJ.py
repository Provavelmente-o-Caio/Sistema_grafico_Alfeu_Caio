from PyQt6.QtGui import QColor

from models.wireframe import Wireframe
from utils.types import ObjectType


class DescritorOBJ():
    def __init__(self):
        self.objs = []

    def export_file(self):
        f = open("files/export.obj", "w")
        f.write("#Sistema Gráfico Alfeu e Caio\n")
        f.write("mtllib material.mtl\n\n")
        for obj in self.objs:
            f.write(f"o {obj.get_name().replace(' ', '_')}\n")
            coordinates = obj.export_coordinates()
            for coordinate in coordinates:
                f.write("v ")
                x, y = coordinate
                f.write(f"{x:.6f} {y:.6f} ")
                f.write("0.000000\n")
            color = obj.get_color()
            color_name = next((name for name in QColor.colorNames() if QColor(name).name() == color), color)
            f.write(f"usemtl {color_name}\n")
            if obj.get_obj_type().name == "DOT":
                f.write("p ")
            elif obj.get_obj_type().name == "POLYGON":
                f.write("f ")
            else:
                f.write("l ")
            counter = len(coordinates)
            for c in coordinates:
                f.write(f"-{counter} ")
                counter -= 1
            f.write("\n")
            f.write("\n")

        f.close()

        f = open("files/material.mtl", "w")
        for color_name in QColor.colorNames():
            color = QColor(color_name)
            f.write(f"newmtl {color_name}\n")
            f.write(f"Kd {color.redF():.6f} {color.greenF():.6f} {color.blueF():.6f}\n")
            f.write("\n")

    def import_file(self, path):
        self.objs = []
        f = open(path, "r")
        lines = f.readlines()
        f.close()

        name = "unnamed_object"
        type = ""
        coordinates = []
        color = ""

        for line in lines:
            if line.startswith("o "):
                self.create_object(name, type, coordinates, color)
                name = " ".join(line.split()[1:])
                type = ""
                color = ""
                coordinates = []
            elif line.startswith("v "):
                coordinates.append((float(line.split()[1]), float(line.split()[2])))
            elif line.startswith("p "):
                type = "DOT"
            elif line.startswith("l "):
                type = "LINE"
            elif line.startswith("f "):
                type = "POLYGON"
            elif line.startswith("usemtl "):
                color = line.split()[1]

        self.create_object(name, type, coordinates, color)

        return self.objs

    def create_object(self, name, type, coordinates, color):
        if coordinates and type:
            obj = None
            if type == "DOT":
                obj = Wireframe(name, ObjectType.DOT, coordinates)
            elif type == "LINE":
                obj = Wireframe(name, ObjectType.LINE, coordinates)
            elif type == "POLYGON":
                obj = Wireframe(name, ObjectType.POLYGON, coordinates)
            if color != "":
                obj.set_color(QColor(color))
            else:
                obj.set_color(QColor("grey"))
            self.objs.append(obj)
