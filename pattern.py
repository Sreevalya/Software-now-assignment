#!/usr/bin/env python3
# Draw recursive inward/outward pattern on each edge of a regular polygon.

import turtle
import math
import sys

# allow deeper recursion for higher depth values
sys.setrecursionlimit(10000)

def draw_pattern(length: float, depth: int, inward: bool = True):
    """
    Recursively draw one edge with indentation.

    - length: current segment length
    - depth: recursion depth (0 = straight line)
    - inward: True = indentation points inward, False = mirrored outward
    """
    if depth == 0:
        turtle.forward(length)
        return

    third = length / 3.0

    # left third
    draw_pattern(third, depth - 1, inward)

    if inward:
        turtle.left(60)
        draw_pattern(third, depth - 1, inward)
        turtle.right(120)
        draw_pattern(third, depth - 1, inward)
        turtle.left(60)
    else:
        # mirror the turns if indentation should be the other way
        turtle.right(60)
        draw_pattern(third, depth - 1, inward)
        turtle.left(120)
        draw_pattern(third, depth - 1, inward)
        turtle.right(60)

    # right third
    draw_pattern(third, depth - 1, inward)


def draw_polygon_pattern(num_sides: int, side_length: float, depth: int):

    """

    Compute vertices of a regular polygon and draw its edges with recursive pattern.

    """

    # circumradius
    radius = side_length / (2 * math.sin(math.pi / num_sides))

    # start angle: bottom side horizontal
    start_angle = -math.pi / 2 - math.pi / num_sides

    # precompute vertices in CCW order
    verts = []
    for k in range(num_sides):
        theta = start_angle + k * (2 * math.pi / num_sides)
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        verts.append((x, y))

     # adjust window so drawing fits

    xs = [v[0] for v in verts]

    ys = [v[1] for v in verts]

    pad_x = max(20, (max(xs) - min(xs)) * 0.15)

    pad_y = max(20, (max(ys) - min(ys)) * 0.15)

    screen = turtle.Screen()

    screen.title("Recursive Polygon Pattern")

    screen.setworldcoordinates(min(xs) - pad_x, min(ys) - pad_y, max(xs) + pad_x, max(ys) + pad_y)

    # draw each edge with recursion
    for i in range(num_sides):
        x1, y1 = verts[i]
        x2, y2 = verts[(i + 1) % num_sides]

        # heading for this straight edge (degrees)
        dx, dy = x2 - x1, y2 - y1
        edge_len = math.hypot(dx, dy)
        heading = math.degrees(math.atan2(dy, dx))

        # midpoint to center vector

        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        cx, cy = -mx, -my
        
        # cross product: determines if center lies to the left or right
        cross = dx * cy - dy * cx

        inward = cross > 0

        # position & heading, then draw the modified edge:
        turtle.penup()
        turtle.goto(x1, y1)
        turtle.setheading(heading)
        turtle.pendown()

        draw_pattern(edge_len, depth, inward)

    # ensure final update after drawing
    turtle.update()


def main():
    try:
        num_sides = int(input("Enter number of sides (=> 3): ").strip())
        side_length = float(input("Enter side length (pixels > 0): ").strip())
        depth = int(input("Enter the recursion depth (>=0): ").strip())
    except ValueError:
        print("Invalid input: please enter numbers.")
        return

    if num_sides < 3 or side_length <= 0 or depth < 0:
        print("Invalid values: sides>=3, side_length>0, depth>=0 required.")
        return

    # turtle setup

    turtle.speed("fastest")
    turtle.hideturtle()
    turtle.tracer(0, 0)   

    # Draw
    draw_polygon_pattern(num_sides, side_length, depth)

    # Keep window open
    turtle.done()


if __name__ == "__main__":
    main()
