from PIL import Image
import numpy as np
import pickle
import os.path
import math

# Testing different definitions of i^2
max_iteration = 40
x_center = 0.0
y_center = 0.0
z_center = 0.0
size = 300
cr =-0.81907
ci = 0.19794
cj = 0.0
ck = 0#.190

g = {}  # light distribution / gaussian table with sigma as key

def gaussian2d(gaussian_size=10, sigma=1):
    """
    G(x,y) = 1 / (2*pi*sigma^2) * exp(-(x^2+y^2) / (2*sigma^2))
    """
    def gauss(x, y, sigma):
        return 1 / (2*math.pi*sigma**2) * math.exp(-(x**2+y**2) / (2*sigma**2))
    gaussian_size_half = gaussian_size / 2
    if not sigma in g:
        # calculate
        print "calc gaussian for sigma=%f" % sigma
        gaussian = np.zeros([gaussian_size, gaussian_size])
        for x in xrange(gaussian_size):
            for y in xrange(gaussian_size):
                gaussian[x,y] = gauss(x-gaussian_size_half,
                                      y-gaussian_size_half, sigma)
        print gaussian
        g[sigma] = gaussian
    return g[sigma]

circle_size = 50
circle = np.zeros([circle_size,circle_size])
circle_area = 1.0 / (math.pi * (circle_size / 2) ** 2)  # the sum of all is (about) 1.. close enough
for x in xrange(circle_size):
    for y in xrange(circle_size):
        xx = (float(x-circle_size/2)/(circle_size/2)) ** 2
        yy = (float(y-circle_size/2)/(circle_size/2)) ** 2
        if xx + yy <= 1:
            circle[x, y] = circle_area

def equallightdist(size, radius):
    """size is the gridsize, radius is the radius of the circle to be

    scale the circle on radius sized circle, this makes an anti-aliased circle 
    """
    if not radius in g:
        #calc circle for radius
        dist = np.zeros([size,size])
        for x in xrange(circle_size):
            for y in xrange(circle_size):
                # coordinates in dist
                i = int((size-radius)/2.0 + radius*float(x)/circle_size) 
                j = int((size-radius)/2.0 + radius*float(y)/circle_size) 
                dist[i, j] += circle[x, y]
        g[radius] = dist
        print dist
    return g[radius]
    

def calc_fractal():
    data = np.zeros([size, size, size])  # 3d
    # calculate 3d object
    for i in xrange(size):
        if i % 1 == 0:
            print "busy with plane %d of %d" % (i, size)
        for j in xrange(size):
            for k in xrange(size):
                x,y,z = ( x_center + 4.0*float(i-size/2)/size,
                          y_center + 4.0*float(j-size/2)/size,
                          z_center + 4.0*float(k-size/2)/size
                          )

                #a, b, c, d = (0, 0, x, y)  # starting point, quite nice
                a, b, c, d = (x, y, 0, z)  # starting point
                iteration = 0

                while (a**2 + b**2 + c**2 + c**2 <= 8.0 and iteration < max_iteration):
                    # Quadernion
                    a, b, c, d = a*a - b*b - c*c - d*d + cr, 2*a*b + 2*c*d + ci, 2*a*c - 2*b*d + cj, 2*a*d + 2*b*c + ck
                    iteration += 1
        # if iteration == max_iteration:
        #     color_value = 255
        # else:
        #     color_value = iteration*10 % 255

                data[i,j,k] = iteration

    print 'saving pickle'
    pickle_file = open(pickle_filename, 'wb')
    pickle.dump(data, pickle_file)
    pickle_file.close()
    return data

pickle_filename = 'fractal.pickle'

if os.path.exists(pickle_filename):
    print 'loading fractal'
    pickle_file = open(pickle_filename, 'r')
    data = pickle.load(pickle_file)
    pickle_file.close()
else:
    print 'calculating fractal'
    data = calc_fractal()

# make picture of 3d object in float
#size = len(data)
focus_depth = size/2  # the middle plane
gaussian_size = 7
gaussian_size_half = gaussian_size // 2
image_size = 2*size  #200

def data_to_image():
    print 'map 3d data on image, focus depth=%d' % focus_depth
    image_data = np.zeros([image_size, image_size])
    max_seen = 0.0
    for i in xrange(size):
        if i % 1 == 0:
            print 'busy with focus_depth %d, data row %d of %d' % (focus_depth, i, size)
        for j in xrange(size):
            for k in reversed(xrange(focus_depth-5,focus_depth+5)):  # from back to front
                x = i*image_size/size
                y = j*image_size/size
                if data[i, j, k] == max_iteration:
                    #image_data[x, y] = image_data[x, y] * (size-1) / size  # make back darker
                    pass
                else:
                    # TODO: gaussian blob
                    #image_data[x, y] += data[i, j, k]
                    radius = min(2.0+10*float(abs(focus_depth-k)) / (size/2), gaussian_size)
            
                    distribution = equallightdist(size=gaussian_size, radius=radius)#gaussian2d(gaussian_size=gaussian_size, sigma=1)
                    xstart = x - gaussian_size_half
                    xend = xstart + gaussian_size
                    ystart = y - gaussian_size_half
                    yend = ystart + gaussian_size
                    if xstart >= 0 and ystart >= 0 and xend < image_size and yend < image_size:
                        #print xstart, xend, ystart, yend
                        image_data[xstart:xend, ystart:yend] += data[i,j,k] * distribution
                        print image_data[xstart:xend, ystart:yend]
                    else:
                        print xstart, xend, ystart, yend

                    # for gx in xrange(gaussian_size):
                    #     for gy in xrange(gaussian_size):
                    #         imx = x-gaussian_size_half+gx
                    #         imy = y-gaussian_size_half+gy
                    #         if (imx < image_size and
                    #             imx >= 0 and
                    #             imy < image_size and
                    #             imy >= 0):

                    #             image_data[imx, imy] += data[i,j,k] * distribution[gx, gy]
                    #             if image_data[imx, imy] > max_seen:
                    #                 max_seen = image_data[imx, imy]+10
                    #                 print "max: %f" % max_seen

    max_seen = image_data[imx, imy].max()

    print 'saving image'
    # now draw on an image
    im = Image.new("RGB", (image_size,image_size))
    image_data = (image_data *255 / max_seen).astype('B')  # normalize to 256
    for x in xrange(image_size):
        for y in xrange(image_size):
            im.putpixel( (x,y), (image_data[x,y], image_data[x,y], image_data[x,y]))
    im.save("images/julia3d_%4d.png" % focus_depth, "PNG")

while focus_depth < size:
    data_to_image()
    focus_depth += 1
