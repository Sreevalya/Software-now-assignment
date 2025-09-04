import turtle
import math
import sys

sys.setrecursionlimit(10000)

def draw_pattern(length, depth, inward=True):
    """
    Recursively draw one modified edge.

    - length: current segment length
    - depth: recursion remaining
    - inward: if True use left-60 / right-120 / left-60 sequence,
              if False use mirrored (right-60 / left-120 / right-60).
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


def draw_polygon_pattern(num_sides, side_length, depth):
    
    # Compute polygon vertices (center at origin), then draw each edge using draw_pattern.
    
    # circumradius so polygon of side_length sits on circle centered at origin
    radius = side_length / (2 * math.sin(math.pi / num_sides))

    # choose start angle so the bottom side is horizontal and centered:
    start_angle = -math.pi / 2 - math.pi / num_sides

    # precompute vertices in CCW order
    verts = []
    for k in range(num_sides):
        theta = start_angle + k * (2 * math.pi / num_sides)
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        verts.append((x, y))

    # move to first vertex
    turtle.penup()
    turtle.goto(verts[0])
    turtle.pendown()

    # draw each edge from verts[i] to verts[i+1]
    for i in range(num_sides):
        x1, y1 = verts[i]
        x2, y2 = verts[(i + 1) % num_sides]

        # heading for this straight edge (degrees)
        dx = x2 - x1
        dy = y2 - y1
        edge_len = math.hypot(dx, dy)
        heading_deg = math.degrees(math.atan2(dy, dx))

        # find midpoint of straight edge and vector from midpoint to center (0,0)
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        # vector from midpoint to center:
        cx = -mx
        cy = -my

        # 2D cross product z = edge_vec x center_vec
        cross = dx * cy - dy * cx

        # If cross > 0, center is on the left of the edge direction (edge vector).
        inward = True if cross > 0 else False

        # position & heading, then draw the modified edge:
        turtle.penup()
        turtle.goto(x1, y1)
        turtle.setheading(heading_deg)
        turtle.pendown()

        draw_pattern(edge_len, depth, inward)

    # ensure final update after drawing
    turtle.update()


def main():
    try:
        num_sides = int(input("Enter the number of sides (recommended => 3): ").strip())
        side_length = float(input("Enter the side length (px): ").strip())
        depth = int(input("Enter the recursion depth (recommended <= 5): ").strip())
    except Exception as e:
        print("Invalid input:", e)
        return

    if  side_length <= 0 or depth < 0:
        print("Please provide valid positive values ( side_length > 0, depth >= 0).")
        return

    # Turtle setup: fast drawing and no animation while drawing
    turtle.setup(width=1.0, height=1.0)   # full window
    turtle.title("Recursive polygon pattern")
    turtle.speed('fastest')
    turtle.hideturtle()
    turtle.tracer(0, 0)   

    # Draw fractal polygon
    draw_polygon_pattern(num_sides, side_length, depth)

    # Keep window open until closed by user
    turtle.done()


if __name__ == "__main__":
    main()
