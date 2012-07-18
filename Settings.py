def main():
    print "Mandelbrot Set Viewer - Version 3.0.0 - Ian Mallett - April 2008"
    print ""
    print "Controls:"
    print " 'ESC'    - Quit"
    print " 'V'      - Reset View"
    print " 'R'      - Render current image at arbitrary resolution"
    print " 'A'      - Toggle Antialiasing"
    print " 'E'      - Toggle Edge Finder"
    print " 'C'      - Change Color Scheme: Colored, Red, Green, Blue, Fast B/W"
    print " 'CTRL+Z' - Go back to the previous image."
    print " Mouse Move and Left Click to set current View."
    print " Mouse Right Click to show mouse coordinates."
    print ""
    print "You will be prompted for the screen size.  Large screens are"
    print "very computationally expensive.  Start TINY, then work up to"
    print "a good resolution.  The aspect ratio must be 3:2."
    print "Ex: 300x200"
    print ""
    while True:
        size = raw_input("Enter the Screen's Size: ")
        try:
            x,y = size.split("x")
            width  = abs(int(round(float(x))))
            height = abs(int(round(float(y))))
            if float(width)/float(height) == 1.5:
                return width, height
            else:
                p = 10
                p /= 0
        except:
            print "Well now, let's try that again, shall we?"
