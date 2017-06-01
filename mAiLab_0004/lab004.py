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
    plt.show()

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

    # Question 2
    target = list(mnist_read('train-images-idx3-ubyte', 'train-labels-idx1-ubyte'))
    label1, img1 = target[0]
    mnist_show(img1)
    print mnist_im2str(img1)

    # Question 3
    import numpy as np
    imgMat = np.zeros([28, 28])
    labels = list()
    for i in range(10):
        label, img = target[i]
        imgMat += img
        labels.append(label)
    imgMat = imgMat / 10
    print mnist_im2str(imgMat.astype(np.uint8))
    mnist_show(imgMat)

    # Question 4
    print '[Result] Labels:', labels
    print '[Result] Mean of labels:{:.2f}'.format(np.mean(labels))

    # Question 5
    newSize = 32
    newImg = np.zeros([newSize, newSize])
    rawSize = img1.shape[0]
    firstLabel = (newSize - rawSize) / 2
    for iRow in range(rawSize):
        for iCol in range(rawSize):
            newImg[iRow+firstLabel, iCol+firstLabel] = img1[iRow, iCol]
    mnist_show(newImg)
    print mnist_im2str(newImg.astype(np.uint8))

    # Advanced 1
    '''
    Matplotlib doesn't support the BMP-format, so we should choose PIL/Pillow to do BMP-saving.
    '''
    from PIL import Image
    outputFig = Image.fromarray(img1)
    outputFig.save('advfig.bmp')
