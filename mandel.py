from PIL import Image

# max_iteration = 100
# x_center = -0.5
# y_center =  0.0
# size = 1000
# scale = 6.0

# im = Image.new("RGB", (size,size))
# for i in xrange(size):
#     if i % 10 == 0:
#         print "busy with line %d" %i
#     for j in xrange(size):
#         x,y = ( x_center + scale*float(i-size/2)/size,
#                   y_center + scale*float(j-size/2)/size
#                 )

#         c = complex(x, y)
#         # we can play with starting number here, fill in (x,y) and you are 1 iteration ahead
#         z = complex(0, 0)  
#         iteration = 0

#         while (abs(z) <= 4.0 and iteration < max_iteration):
#             z = z**2 + c
#             iteration += 1
#         if iteration == max_iteration:
#             color_value = 255
#         else:
#             color_value = iteration*10 % 255
#         im.putpixel( (i,j), (color_value, color_value, color_value))

# im.save("mandelbrot.png", "PNG")


# max_iteration = 100
# x_center = 0.0
# y_center = 0.0
# size = 300
# c = complex(-0.81907, 0.19794)

# im = Image.new("RGB", (size,size))
# for i in xrange(size):
#     if i % 10 == 0:
#         print "busy with line %d" %i
#     for j in xrange(size):
#         x,y = ( x_center + 4.0*float(i-size/2)/size,
#                   y_center + 4.0*float(j-size/2)/size
#                 )

#         z = complex(x, y)
#         iteration = 0

#         while (abs(z) <= 4.0 and iteration < max_iteration):
#             z = z**2 + c
#             iteration += 1
#         if iteration == max_iteration:
#             color_value = 255
#         else:
#             color_value = iteration*10 % 255
#         im.putpixel( (i,j), (color_value, color_value, color_value))

# im.save("julia.png", "PNG")



# Testing different definitions of i^2
max_iteration = 50
x_center = 0.0
y_center = 0.0
size = 1000
cr =-0.81907
ci = 0.19794
cj = 0.0
ck = 0#.190

im = Image.new("RGB", (size,size))
for i in xrange(size):
    if i % 10 == 0:
        print "busy with line %d" %i
    for j in xrange(size):
        x,y = ( x_center + 4.0*float(i-size/2)/size,
                  y_center + 4.0*float(j-size/2)/size
                )

        #a, b, c, d = (0, 0, x, y)  # starting point, quite nice
        a, b, c, d = (0, 0, x, y)  # starting point
        iteration = 0

        while (a**2 + b**2 + c**2 + c**2 <= 8.0 and iteration < max_iteration):
            # Quadernion
            a, b, c, d = a*a - b*b - c*c - d*d + cr, 2*a*b + 2*c*d + ci, 2*a*c - 2*b*d + cj, 2*a*d + 2*b*c + ck
            iteration += 1
        if iteration == max_iteration:
            color_value = 255
        else:
            color_value = iteration*10 % 255
        im.putpixel( (i,j), (color_value, color_value, color_value))

im.save("testjulia.png", "PNG")
