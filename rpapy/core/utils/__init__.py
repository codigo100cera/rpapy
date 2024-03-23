import sys
import warnings


def draw_outline(x, y, backend):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from pywinauto import Desktop

    Desktop(backend=backend).from_point(x, y).draw_outline(thickness=3)