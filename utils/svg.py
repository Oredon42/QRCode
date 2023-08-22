import xml.etree.cElementTree as ET

from utils.structures import ModuleType

import numpy as np

def writeSVG(filepath: str, data: np.array, width: int) -> None:
    """ Write QRCode image svg of width to filepath. """

    matrix_width = data.shape[0]
    module_size = width / matrix_width

    svg_elt = ET.Element("svg")
    svg_elt.set("xmlns", "http://www.w3.org/2000/svg")
    svg_elt.set("version", "1.1")
    svg_elt.set("width", str(width))
    svg_elt.set("height", str(width))

    for y in range(matrix_width):
        for x in range(matrix_width):
            if data[y][x] == ModuleType.Dark:
                rect_elt = ET.SubElement(svg_elt, "rect")
                rect_elt.set("width", str(module_size))
                rect_elt.set("height", str(module_size))
                rect_elt.set("x", str(x * module_size))
                rect_elt.set("y", str(y * module_size))

    tree = ET.ElementTree(svg_elt)
    tree.write(filepath)