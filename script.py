import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    edges = []
    step = 0.1
    for command in commands:
        if command[0] == 'push':
            stack.append( [x[:] for x in stack[-1]] )
        elif command[0] == 'pop':
            stack.pop()
        elif command[0] == 'move':
            t = make_translate(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif command[0] == 'rotate':
            theta = float(command[2]) * (math.pi / 180)
            
            if command[1] == 'x':
                t = make_rotX(theta)
            elif command[1] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif command[0] == 'scale':
            t = make_scale(float(command[1]), float(command[2]), float(command[3]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif command[0] == 'box':
            add_box(edges,
                    float(command[1]), float(command[2]), float(command[3]),
                    float(command[4]), float(command[5]), float(command[6]))
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
        elif command[0] == 'sphere':
            add_sphere(edges,
                       float(command[1]), float(command[2]),
                       float(command[3]), float(command[4]), step)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
        elif command[0] == 'torus':
            add_torus(edges,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[0]), step)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
        elif command[0] == 'line':
            add_edge( edges,
                      float(command[1]), float(command[2]), float(command[3]),
                      float(command[4]), float(command[5]), float(command[6]) )
        elif command[0] == 'save':
            save_extension(screen, command[0])
        elif command[0] == 'display':
            display(screen)
            
        print command
        
