#!/usr/bin/python

def mnist_read(imgFile, labelFile):
    # Modified from https://gist.github.com/akesling/5358964
    import struct
    import numpy as np
    with open(labelFile, 'rb') as fileLabel:
        magic, num = struct.unpack(">II", filelabel.read(8))
        label = np.fromfile(fileLabel, dtype=np.int8)
    with open(imgFile, 'rb') as fileImg:
        magic, num, rows, cols = struct.unpack(">IIII", fileImg.read(16))
        img = np.fromfile(fileImg, dtype=np.int8).reshape(len(label), rows, cols)
    if len(label) == len(img):
        data = lambda idx: (label[idx], img[idx])
        for iCnt in xrange(len(label)):
            yield data(iCnt)
    else:
        print '[Error] The Image file is not compatible with the Label file.  Please check them and try them again.  Thank you!'

def mnist_show(imgMat):
    # 
    from matplotlib import pyplot
    import matplotlib as mpl
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    imgplot = ax.imshow(image, cmap=mpl.cm.Greys)
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    pyplot.show()


if __name__ == '__main__':
    targetFiles = ['train-images-idx3-ubyte', 'train-labels-idx1-ubyte', 't10k-images-idx3-ubyte', 't10k-labels-idx1-ubyte']
    destDir = './'
    import os
    remainFiles = list()
    for obj in targetFiles:
        if not os.path.exists(destDir + obj):
            remainFiles.append(obj)
    if len(remainFiles) == 0:
        print '[Status] All candidates exist in destination.  Go ahead.'
    else:
        print 'Download target MNIST files...'
        import urllib
        urlrepo = "http://yann.lecun.com/exdb/mnist/"
        extFormat = '.gz'
        for obj in remainFiles:
            urllib.urlretrieve(urlrepo + obj + extFormat, filename="./" + obj + extFormat)
        print '[Status] Download complete.'

        print
        print '[Status] Unzipping datasets...'
        import gzip
        for obj in remainFiles:
            inFile = gzip.open(destDir + obj + extFormat, 'rb')
            outFile = open(destDir + obj, 'wb')
            outFile.write(inFile.read())
            inFile.close()
            outFile.close()
        print '[Status] Unzipping step is complete.'
