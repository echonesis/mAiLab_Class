#!/usr/bin/python

def mnist_read(imgFile, labelFile):
    # Modified from https://gist.github.com/akesling/5358964
    import struct
    import numpy as np
    with open(labelFile, 'rb') as fileLabel:
        magic, num = struct.unpack(">II", fileLabel.read(8))
        label = np.fromfile(fileLabel, dtype=np.int8)
    with open(imgFile, 'rb') as fileImg:
        magic, num, rows, cols = struct.unpack(">IIII", fileImg.read(16))
        # For 16-bit, use UINT8
        img = np.fromfile(fileImg, dtype=np.uint8).reshape(len(label), rows, cols)
    if len(label) == len(img):
        data = lambda idx: (label[idx], img[idx])
        for iCnt in xrange(len(label)):
            yield data(iCnt)
    else:
        print '[Error] The Image file is not compatible with the Label file.  Please check them and try them again.  Thank you!'

def mnist_show(imgMat):
    import matplotlib.pyplot as plt
    plt.imshow(imgMat, cmap='Greys')
    #plt.show()

def mnist_im2str(imgMat):
    '''
    Convert image to 16-based number matrices
    '''
    strResult = list()
    for iRow in imgMat:
        tmpResult = list()
        for iCol in iRow:
            tmpResult.append('{:02X}'.format(iCol))
        strResult.append(' '.join(tmpResult))
    return '\n'.join(strResult)

def mnist_padding(imgMat, pad_size):
    import numpy as np
    # padding for extending the originial image and fill with zeros
    newSize = pad_size
    newImg = np.zeros([newSize, newSize])
    rawSize = imgMat.shape[0]
    firstLabel = (newSize - rawSize) / 2
    for iRow in range(rawSize):
        for iCol in range(rawSize):
            newImg[iRow+firstLabel, iCol+firstLabel] = imgMat[iRow, iCol]
    return newImg

def G_filter(imgMat, conv_filter):
    import numpy as np
    #conv_filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    conv_size = conv_filter.shape[0]
    newImg = np.zeros([imgMat.shape[0]-conv_size+1, imgMat.shape[1]-conv_size+1])
    for iRow in range(newImg.shape[0]):
        for iCol in range(newImg.shape[1]):
            newImg[iRow, iCol] = sum(sum(np.multiply(imgMat[iRow:iRow+conv_size, iCol:iCol+conv_size], conv_filter))) / np.prod(conv_filter.shape)
    return newImg

def Gx(imgMat, conv_filter=None):
    import numpy as np
    if conv_filter is None:
        conv_filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    return G_filter(imgMat, conv_filter)

def Gy(imgMat, conv_filter=None):
    import numpy as np
    if conv_filter is None:
        conv_filter = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    return G_filter(imgMat, conv_filter)

def genSobelFilter(filter_size):
    import numpy as np
    # Based on Sobel filter kernel
    # the ordering would be from left to right, from up to bottom as https://en.wikipedia.org/wiki/Sobel_operator
    result = list()
    # For G_x
    if filter_size % 2 == 1:
        tmpResult = list()
        flist = range(filter_size / 2, -1*filter_size/2, -1)
        print 'FList:', flist
        for i in range(filter_size):
            if i == 0:
                tmpResult.append(flist)
            elif i <= filter_size / 2:
                newList = flist[:]
                for i in range(len(newList)):
                    if newList[i] > 0:
                        newList[i] = newList[i] + 1
                    elif newList[i] < 0:
                        newList[i] = newList[i] - 1
                tmpResult.append(newList)
                flist = newList[:]

            else:
                newList = flist[:]
                for i in range(len(newList)):
                    if newList[i] > 0:
                        newList[i] = newList[i] - 1
                    elif newList[i] < 0:
                        newList[i] = newList[i] + 1
                tmpResult.append(newList)
                flist = newList[:]
        gx_filter = np.array(tmpResult)
        gy_filter = gx_filter.transpose()
        result = [gx_filter, gy_filter]

    else:
        print '[Error] The Sobel filter generation is failed.'
        print '        Please try another filter size number.  Thanks.'
    return result

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    # Question 1
    # Filter Settings
    target = list(mnist_read('train-images-idx3-ubyte', 'train-labels-idx1-ubyte'))
    plt.figure()
    for i in range(5):
        label, img = target[i]
        Gx_result = Gx(mnist_padding(img, 30))
        #print mnist_im2str(Gx_result.astype(np.uint8))
        Gx_result.astype(np.uint8)
        Gy_result = Gy(mnist_padding(img, 30))
        Gy_result.astype(np.uint8)
        #plt.figure()
        plt.subplot(2, 5, i+1)
        mnist_show(Gx_result)
        #plt.show()
        plt.subplot(2, 5, i+6)
        #plt.figure()
        mnist_show(Gy_result)
        #plt.show()
    plt.show()

    # Question 2
    label1, img1 = target[0]
    testcase = [(32, 5), (34, 7), (36, 9)]
    for obj in testcase:
        paddingResult = mnist_padding(img1, obj[0])
        sobelFilter = genSobelFilter(obj[1])
        Gx_result = G_filter(paddingResult, sobelFilter[0])
        Gy_result = G_filter(paddingResult, sobelFilter[1])
        print 'For case:', obj
        print 'Gx result matrix:'
        print mnist_im2str(Gx_result.astype(np.uint8))
        print 'Gy result matrix:'
        print mnist_im2str(Gy_result.astype(np.uint8))

        # I need figures to explain the filtering effect.
        plt.figure()
        plt.subplot(2, 1, 1)
        mnist_show(Gx_result)
        plt.subplot(2, 1, 2)
        mnist_show(Gy_result)
        plt.show()

    # Advanced Question 1
    '''
    For edge detection, we need to figure out the boundary between two classes.
    And that's why we set positive and negative weights at the opposite sides of the middle line.
    If all the regions are so-called flat, most of values would remain at the same level, and we will get no spike points away from zero.
    However, if the so-called edge appears, one side would be different from the other side, and the weighted value would be obvious higher or lower than zero.
    The principle is similar to the Haar kernel, and the Haar is much simpler since Sobel filter considers the region information.
    '''
