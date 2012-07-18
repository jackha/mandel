try:
    import psyco
    psyco.full()
except:
    pass
import pygame
from pygame.locals import *
import sys, os
from math import *
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

import Settings
width, height = 800, 600  #Settings.main()
print ""

Screen = (width,height)
pygame.display.set_caption("Mandelbrot Set Viewer - Ian Mallett - v.3.0.0 - 2008")
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
Surface = pygame.display.set_mode(Screen)

Font  = pygame.font.SysFont("Times New Roman.ttf",12,False,False)
iFont = pygame.font.SysFont("Times New Roman.ttf",12,False,True)

MandelbrotSetSection = pygame.Surface(Screen)

MaxIteration = 255

Antialias = False
Edge = False
ColourScheme = 1

ViewRect = [-3.0,-1.5,4.5,3.0]
ViewRects = [ViewRect]
ViewImages = []

ColourPalette = [(241, 233, 191), (248, 201, 95), (255, 170, 0), (204, 108, 0), (153, 87, 0), (106, 52, 3), (66, 30, 15), (25, 7, 26), (25, 7, 26), (9, 1, 47), (4, 4, 73), (0, 7, 100), (12, 44, 138), (24, 82, 177), (57, 125, 209), (134, 181, 229), (211, 236, 248)]

def CalculateMandelbrotSet(viewrect,Dimensions=(Screen[0],Screen[1]),printprogress=False,writecoordinates=False,writezoom=False):
    Image = pygame.Surface(Dimensions)
    Image.fill((0,0,0))
    if printprogress: line = 0
    for ypixel in xrange(Dimensions[1]):
        for xpixel in xrange(Dimensions[0]):
            x = viewrect[0] + (viewrect[2]*(float(xpixel)/float(Dimensions[0])))
            y = viewrect[1] + (viewrect[3]*(float(ypixel)/float(Dimensions[1])))
            z = complex(x,y)
            c = z
            Colour = (0,0,0)
            iteration = 0
            while iteration < MaxIteration:
                z = (z*z)+c
                if abs(z) > 2: break
                iteration += 1
            if iteration == MaxIteration:
                Colour = (0,0,0)
            else:
                if ColourScheme == 1:
                    index = iteration % 17
                    Colour = ColourPalette[index]
                elif ColourScheme == 2:
                    Colour = (iteration,0,0)
                elif ColourScheme == 3:
                    Colour = (0,iteration,0)
                else:
                    Colour = (0,0,iteration)
            Image.set_at((xpixel,Dimensions[1]-ypixel),Colour)
        if printprogress:
            sys.stdout.write(  "Rendered Line " + str(line) + " ("+str(int(round(float(line)/float(Dimensions[1])*100)))+"% Complete)" + "\r"  )
            sys.stdout.flush()
            line += 1
    if Edge:
        Image = pygame.transform.laplacian(Image)
    if Antialias:
        Image = pygame.transform.smoothscale(Image,(Dimensions[0]*2,Dimensions[1]*2))
        Image = pygame.transform.smoothscale(Image,Dimensions)
    if writecoordinates:
        DrawCoordinates(Image)
    if writezoom:
        DrawZoom(Image)
    pygame.event.clear()
    return Image
DrawingRect = False
def RenderImage():
    Continue = raw_input("You have selected to render an image.  Do you wish to continue? (y/n): ")
    if Continue == "y":
        drawcoordinates = raw_input("Do you want to label the boundaries? (y/n): ")
        if drawcoordinates == "y": drawcoordinates = True
        else: drawcoordinates = False
        drawzoom = raw_input("Do you want to label the zoom factor? (y/n): ")
        if drawzoom == "y": drawzoom = True
        else: drawzoom = False
        while True:
            size = raw_input("Enter the Render Size: ")
            try:
                x,y = size.split("x")
                width  = abs(int(round(float(x))))
                height = abs(int(round(float(y))))
                if float(width)/float(height) == 1.5:
                    break
                else:
                    p = 10
                    p /= 0
            except:
                print "Well now, let's try that again, shall we?"
        print "Rendering..."
        Image = CalculateMandelbrotSet(ViewRect,(width,height),True,drawcoordinates,drawzoom)
        sys.stdout.write(  "Rendered Line " + str(height) + " (100% Complete)")
        sys.stdout.flush()
        print ""
        print "Render Complete!"
        print "Saving..."
        pygame.image.save(Image,"Mandelbrot Set Image.png")
        print 'Image saved as "Mandelbrot Set Image.png"'
    print ""
keypress = False
def GetInput():
    global ViewRect, ViewRects, ViewImages, DrawingRect, mpos, mpress, MandelbrotSetSection, Antialias, Edge, ColourScheme, keypress
    key = pygame.key.get_pressed()
    mpos = pygame.mouse.get_pos()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()
    if mpress[0]:
        if DrawingRect == False:
            DrawingRect = [mpos[0],mpos[1]]
    else:
        if DrawingRect != False:
            DrawingRect.append(mpos[0])
            DrawingRect.append(mpos[1])
            PixelWidth  = abs(mpos[0]-float(DrawingRect[0]))
            PixelHeight = abs(PixelWidth*(2.0/3.0))
            XSpan = ViewRect[2]*(PixelWidth /float(Screen[0]))
            YSpan = ViewRect[3]*(PixelHeight/float(Screen[1]))
            XPos  = ViewRect[0] + (ViewRect[2]*(DrawingRect[0]/float(Screen[0])))
            YPos  = ViewRect[1] + (ViewRect[3]*((Screen[1]-(DrawingRect[1]+PixelHeight))/float(Screen[1])))
            ViewRect = [XPos,YPos,XSpan,YSpan]
            MandelbrotSetSection = CalculateMandelbrotSet(ViewRect)
            ViewRects.append(ViewRect)
            ViewImages.append(MandelbrotSetSection)
        DrawingRect = False
    if key[K_r]:
        RenderImage()
        pygame.event.clear()
    if key[K_v]:
        ViewRect = [-2,-1,3,2]
        MandelbrotSetSection = CalculateMandelbrotSet(ViewRect)
    if key[K_a]:
        Antialias = not Antialias
        MandelbrotSetSection = CalculateMandelbrotSet(ViewRect)
    if key[K_e]:
        Edge = not Edge
        MandelbrotSetSection = CalculateMandelbrotSet(ViewRect)
    if key[K_c]:
        ColourScheme += 1
        if ColourScheme == 6: ColourScheme = 1
        MandelbrotSetSection = CalculateMandelbrotSet(ViewRect)
    if (key[K_LCTRL] or key[K_RCTRL]) and key[K_z] and len(ViewRects) > 1:
        if not keypress:
            ViewRect = ViewRects[-2:-1][0]
            ViewRects = ViewRects[:-1]
            MandelbrotSetSection = ViewImages[-2:-1][0]
            ViewImages = ViewImages[:-1]
            keypress = True
    else:
        keypress = False
i = iFont.render("i",True,(255,255,255))
p = Font.render(")",True,(255,255,255))
def DrawText(Text):
    TextSurfaces = []
    Italic = False
    for t in Text:
        if Italic: TextSurface = iFont.render(t,True,(255,255,255))
        else:      TextSurface =  Font.render(t,True,(255,255,255))
        TextSurfaces.append(TextSurface)
        Italic = not Italic
    Width = 0
    for t in TextSurfaces:
        Width += t.get_width()
    surface = pygame.Surface((Width+10,13))
    surface.fill((50,50,50))
    surface.set_alpha(192)
    position = 5
    for t in TextSurfaces:
        surface.blit(t,(position,2))
        position += t.get_width()
    return surface
def DrawZoom(image):
    Size = image.get_size()
    Zoom = 3.0/ViewRect[2]
    surface = DrawText(["Zoom Factor: "+AddCommas(str(int(round(Zoom))))+"x"])
    image.blit(surface,(Size[0]-2-surface.get_width(),Size[1]-30))
def DrawCoordinates(image):
    Size = image.get_size()
    LeftBound   = str(round(ViewRect[0]            ,10))
    RightBound  = str(round(ViewRect[0]+ViewRect[2],10))
    BottomBound = str(round(ViewRect[1]            ,10))
    TopBound    = str(round(ViewRect[1]+ViewRect[3],10))
    surface = DrawText(["("+LeftBound+", "+TopBound,"i",")"]);    image.blit(surface,(2,2))
    surface = DrawText(["("+LeftBound+", "+BottomBound,"i",")"]); image.blit(surface,(2,Size[1]-(13+2)))
    surface = DrawText(["("+RightBound+", "+TopBound,"i",")"]);   image.blit(surface,(Size[0]-2-surface.get_width(),2))
    surface = DrawText(["("+RightBound+", "+BottomBound,"i",")"]);image.blit(surface,(Size[0]-2-surface.get_width(),Size[1]-(13+2)))
def AddCommas(string):
    string = list(string);string.reverse()
    new = []
    counter = 1
    for char in string:
       new.append(char)
       if counter == 3: new.append(",");counter = 0
       counter += 1
    new.reverse()
    newstring = ""
    for char in new: newstring += char
    if newstring.startswith(","): newstring = newstring[1:]
    return newstring
def Draw():
    #Draw the Mandelbrot Set Section
    Surface.blit(MandelbrotSetSection,(0,0))
    #Draw the selecting/Zoom Rectangle
    if DrawingRect != False:
        TopLeft = (DrawingRect[0],DrawingRect[1])
        Width   = mpos[0]-DrawingRect[0]
        Height = Width*(2.0/3.0)
        pygame.draw.rect(Surface,(255,255,0),(TopLeft[0],TopLeft[1],Width,Height),1)
    #Draw Coordinates
    DrawCoordinates(Surface)
    #Draw Zoom Factor
    DrawZoom(Surface)
    #Draw Mouse Coordinates (If Mouse Right Click)
    if mpress[2]:
        x = round(((float(mpos[0])/float(Screen[0]))*ViewRect[2])+ViewRect[0],10)
        y = round(((float(Screen[1]-mpos[1])/float(Screen[1]))*ViewRect[3])+ViewRect[1],10)
        surface = DrawText(["("+str(x)+", "+str(y),"i",")"])
        Surface.blit(surface,(mpos[0]+2,mpos[1]-6))
    #Flip to the Screen
    pygame.display.flip()
MandelbrotSetSection = CalculateMandelbrotSet(ViewRect)
ViewImages.append(MandelbrotSetSection)
def main():
    global Surface
    while True:
        GetInput()
        Draw()
if __name__ == '__main__': main()
