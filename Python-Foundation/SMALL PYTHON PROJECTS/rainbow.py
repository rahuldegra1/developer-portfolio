import time, sys

try:
    import bext
except ImportError:
    sys.exit()

print("Rainbow")
print("Press CTRL-C to stop.")
time.sleep(3)

indent = 0  # How many spaces to indent
indenIncreasing = True

try:
    while True:  # main program loop
        print(" " * indent, end="")
        bext.fg("red")
        print("##", end="")
        bext.fg("yellow")
        print("##", end="")
        bext.fg("green")
        print("##", end="")
        bext.fg("blue")
        print("##", end="")
        bext.fg("cyan")
        print("##", end="")
        bext.fg("purple")
        print("##")

        if indenIncreasing:
            # increase the number of spaces:
            indent = indent + 1
            if indent == 200:  # (!) change this to 10 or 30.
                # change directions
                indenIncreasing = False
        else:
            # decrease the number
            indent = indent - 1
            if indent == 0:
                # change direction
                indenIncreasing = True

            time.sleep(0.02)  # add a slight pause..
except KeyboardInterrupt:
    sys.exit()  # When CTRL-C  id pressed, end the program.
