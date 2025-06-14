from operator import is_
from PyQt6.QtGui import QColor

from models.wireframe import Wireframe
from models.wireframe_3d import Wireframe_3D
from models.point_3d import Point3D
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
            color = obj.get_color()
            color_name = next((name for name in QColor.colorNames() if QColor(name).name() == color), color)
            if isinstance(obj, Wireframe):
                coordinates = obj.export_coordinates()
                for coordinate in coordinates:
                    f.write("v ")
                    x, y = coordinate
                    f.write(f"{x:.6f} {y:.6f} ")
                    f.write("0.000000\n")
                f.write(f"usemtl {color_name}\n")
                if obj.get_obj_type().name == "DOT":
                    f.write("p ")
                elif obj.get_obj_type().name == "POLYGON":
                    f.write("f ")
                elif obj.get_obj_type().name == "CURVE":
                    f.write("c ")
                elif obj.get_obj_type().name == "CURVE_BSPLINE":
                    f.write("b ")
                else:
                    f.write("l ")
                counter = len(coordinates)
                for c in coordinates:
                    f.write(f"-{counter} ")
                    counter -= 1
            elif isinstance(obj, Wireframe_3D):
                points = obj.export_coordinates()
                edges = obj.get_edges()
                for point in points:
                   x, y, z = point.get_coordinates()
                   f.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
                f.write(f"usemtl {color_name}\n")
                for edge in edges:
                    f.write(f"l {edge[0]} {edge[1]}\n")

            f.write("\n\n")

        f.close()

        f = open("files/material.mtl", "w")
        for color_name in QColor.colorNames():
            color = QColor(color_name)
            f.write(f"newmtl {color_name}\n")
            f.write(f"Kd {color.redF():.6f} {color.greenF():.6f} {color.blueF():.6f}\n")
            f.write("\n")

    def import_file(self, path, fill:bool = False):
        self.objs = []
        f = open(path, "r")
        lines = f.readlines()
        f.close()

        name = "unnamed_object"
        type = ""
        coordinates = []
        coordinates_3d = []
        edges = []
        color = ""
        is_3d = False

        for line in lines:
            if line.startswith("o "):
                if is_3d:
                    self.create_object(name, type, coordinates_3d, edges, color, fill)
                else:
                    self.create_object(name, type, coordinates, color=color, fill=fill)
                name = " ".join(line.split()[1:])
                type = ""
                color = ""
                coordinates = []
                coordinates_3d = []
                edges: list[tuple[float, float]] = []
                is_3d = False
            elif line.startswith("v "):
                coordinates.append((float(line.split()[1]), float(line.split()[2])))
                coordinates_3d.append(Point3D([(int(float(line.split()[1])), int(float(line.split()[2])), int(float(line.split()[3])))]))
                if int(float(line.split()[3])) != 0:
                    is_3d = True
            elif line.startswith("p "):
                type = "DOT"
            elif line.startswith("l "):
                if is_3d:
                    edges.append((float(line.split()[1]), float(line.split()[2])))
                    type = "POLYGON_3D"
                else:
                    type = "LINE"
            elif line.startswith("f "):
                type = "POLYGON"
            elif line.startswith("c "):
                type = "CURVE"
            elif line.startswith("b "):
                type = "CURVE_BSPLINE"
            elif line.startswith("usemtl "):
                color = line.split()[1]

        print(is_3d)
        if is_3d:
            self.create_object(name, type, coordinates_3d, edges, color, fill)
        else:
            self.create_object(name, type, coordinates, color=color, fill=fill)

        return self.objs

    def create_object(self, name, type, coordinates, edges = [], color = "", fill:bool = False):
        if coordinates and type:
            obj = None
            if type == "DOT":
                obj = Wireframe(name, ObjectType.DOT, coordinates)
            elif type == "LINE":
                obj = Wireframe(name, ObjectType.LINE, coordinates)
            elif type == "POLYGON":
                obj = Wireframe(name, ObjectType.POLYGON, coordinates, fill)
            elif type == "POLYGON_3D":
                obj = Wireframe_3D(name, ObjectType.POLYGON_3D, coordinates, edges, fill)
            elif type == "CURVE":
                obj = Wireframe(name, ObjectType.CURVE, coordinates, fill)
            elif type == "CURVE_BSPLINE":
                obj = Wireframe(name, ObjectType.CURVE_BSPLINE, coordinates, fill)
            print(color)
            if color != "":
                obj.set_color(QColor(color))
            else:
                obj.set_color(QColor("grey"))
            self.objs.append(obj)
