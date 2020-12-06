from PIL import Image
import matplotlib.pyplot as pyplot
import numpy as numpy
import math

def negative(image_path):
    img = pyplot.imread(image_path)
    arr255 = numpy.zeros(img.shape)
    arr255[:,:] = 255 #make every val 255
    arr255 = arr255.astype(numpy.uint8)
    negImg = arr255 - img
    negImgFinal = Image.fromarray(negImg)
    return negImgFinal

# for 128, 64, 32, 16, 8, 4, or 2 bits/pixel
def reduceBits(image_path, count):
    img = pyplot.imread(image_path)
    mask = (255 << count)
    result = img&mask
    resultFinal = Image.fromarray(result)
    return resultFinal

#helper image
def saturated_sum(image1, image2):
    img1copy = numpy.copy(image1)
    img1copy = img1copy.astype('uint16')
    img2copy = numpy.copy(image2)
    img2copy = img2copy.astype('uint16')
    output = img1copy+img2copy
    for row in range(output.shape[0]):
        for col in range(output.shape[1]):
            if output[row,col] < 0:
                output[row,col] = 0
            elif output[row,col] > 255:
                output[row,col] = 255
            else:
                continue
    output = output.astype(numpy.uint8)
    return output

def brighten(image_path, brightVal):
    img = pyplot.imread(image_path)
    addend = numpy.zeros(img.shape)
    addend[:,:] = brightVal
    addend = addend.astype(numpy.uint8)
    brightenImg = saturated_sum(img,addend)
    brightenImgFinal = Image.fromarray(brightenImg)
    return brightenImgFinal

def histogramEqual(image_path):
    image = pyplot.imread(image_path)
    hist = numpy.zeros(256) # freq vals for all pixel intensities
    M = image.shape[0] #rows
    N = image.shape[1] #cols
    for row in range(M):
        for col in range(N):
            pix_intensity = image[row,col] #intensity at pix
            hist[pix_intensity] +=1
    #hist
    cumulative_sum = numpy.cumsum(hist, dtype=float)
    cumulative_sum = (256-1)*cumulative_sum/cumulative_sum[255]
    #round to nearest integer
    cumulative_sum = numpy.around(cumulative_sum, decimals=0)
    cumulative_sum = cumulative_sum.astype('uint8')
    histEqual_image = numpy.copy(image)
    for row in range(M):
        for col in range(N):
            old_intensity = histEqual_image[row,col]
            #old_intensity becomes index to access new intensity
            #based on histogram equalization
            histEqual_image[row,col] = cumulative_sum[old_intensity]
    histEqual_imageFinal = Image.fromarray(histEqual_image)
    return histEqual_imageFinal

def gammaCorrection(image_path,gamma=1,constant=1):
    image = pyplot.imread(image_path)
    img_copy = numpy.copy(image)
    img_copy = img_copy.astype('float')
    scale = float(img_copy.max() - img_copy.min())
    modified_img = scale*constant*((img_copy/scale)**gamma)
    #print(f"gamma={gamma}, constant={constant}")
    modified_img = modified_img.astype('uint8')
    gammaFinal = Image.fromarray(modified_img)
    return gammaFinal

def histogramLocalEqual(image_path,neighborhood_size):
    f = pyplot.imread(image_path)
    n = neighborhood_size # kernel rows = cols
    offset = int((n-1)/2)
    #print(offset)
    f_padded = numpy.pad(f, ((offset,offset),(offset,offset)), 'constant')

    M = f_padded.shape[0] #image rows
    N = f_padded.shape[1] #image cols
    image_mod = numpy.zeros(f_padded.shape) #padded output image

    for startx in range(M-n+1):
        for starty in range(N-n+1):
            hist_local_helper(f_padded,image_mod,neighborhood_size,offset,startx,starty)
    image_mod2 = image_mod[offset:(M-offset+1),offset:(N-offset+1)]
    image_mod2Final = Image.fromarray(image_mod2)
    return image_mod2Final

def hist_local_helper(inputimage, outputimage, neighborhood_size, offsetlocal, x, y):
    index_array = numpy.linspace(start=-1*offsetlocal,stop=offsetlocal,num=neighborhood_size,dtype=numpy.int)
    localx = x+offsetlocal
    localy = y+offsetlocal
    hist = numpy.zeros(256)
    sumOfProducts = 0
    for s in index_array:
        for t in index_array:
            pix_intensity = inputimage[localx-s,localy-t]
            hist[pix_intensity] +=1
    cumulative_sum = numpy.cumsum(hist, dtype=float)
    cumulative_sum = (256-1)*cumulative_sum/cumulative_sum[255]
    #round to nearest integer
    cumulative_sum = numpy.around(cumulative_sum, decimals=0)
    cumulative_sum = cumulative_sum.astype('uint8')
    old_intensity = inputimage[localx,localy]
    outputimage[localx,localy] = cumulative_sum[old_intensity]

def boxKernelMaker(boxKernSize):
    boxkernel1d = numpy.ones((boxKernSize,),dtype=numpy.int)
    return boxkernel1d

def convolution_localx(inumpyutimage, outputimage, w, offsetlocal, x, y):
    index_array = numpy.linspace(start=-1*offsetlocal,stop=offsetlocal,num=w.shape[0],dtype=numpy.int)
    localx = x+offsetlocal
    localy = y
    sumOfProducts = 0
    for s in index_array:
        sumOfProducts += w[s+offsetlocal]*inumpyutimage[localx-s,localy]
    #print(sumOfProducts)        
    outputimage[localx,localy] = sumOfProducts

def convolution_localy(inumpyutimage, outputimage, w, offsetlocal, x, y):
    index_array = numpy.linspace(start=-1*offsetlocal,stop=offsetlocal,num=w.shape[0],dtype=numpy.int)
    localx = x
    localy = y+offsetlocal
    sumOfProducts = 0
    for t in index_array:
        sumOfProducts += w[t+offsetlocal]*inumpyutimage[localx,localy-t]
    #print(sumOfProducts)        
    outputimage[localx,localy] = int(sumOfProducts)

def smoothBox(image_path, kernelSize):
    f = pyplot.imread(image_path)
    w = boxKernelMaker(kernelSize)
    n = w.shape[0] # kernel rows = cols
    offset = int((n-1)/2)
    #n for box
    rowVector = w/n
    colVector = w.reshape(-1,1)/n
    #print(offset)
    f_padded = numpy.pad(f, ((offset,offset),(offset,offset)), 'constant')

    M = f_padded.shape[0] #image rows
    N = f_padded.shape[1] #image cols
    image_mod1 = numpy.zeros(f_padded.shape) #padded output image
    image_mod2 = numpy.zeros(f_padded.shape) #padded output image

    #this is for the col vector
    for startx in range(M-n+1):
        for starty in range(N):
            convolution_localx(f_padded,image_mod1,colVector,offset,startx,starty)
    
    #this is for the row vector
    for startx in range(M):
        for starty in range(N-n+1):
            convolution_localy(image_mod1,image_mod2,rowVector,offset,startx,starty)
    
    image_mod3 = image_mod2[offset:(M-offset+1),offset:(N-offset+1)]
    image_mod3Final = Image.fromarray(image_mod3)
    return image_mod3Final

def gaussianKernelMaker(gauKernSize):
    gausKernel1d = numpy.zeros(gauKernSize,dtype=numpy.int)
    for i in range(gauKernSize):
        gausKernel1d[i] = math.comb(gauKernSize-1,i)
    return gausKernel1d

def gaussianFilter(f, kernelSize):
    w = gaussianKernelMaker(kernelSize)
    n = w.shape[0] # kernel rows = cols 
    offset = int((n-1)/2)
    sum = numpy.sum(w)
    rowVector = w/sum
    colVector = w.reshape(-1,1)/sum
    #print(offset)
    f_padded = numpy.pad(f, ((offset,offset),(offset,offset)), 'constant')

    M = f_padded.shape[0] #image rows
    N = f_padded.shape[1] #image cols
    image_mod1 = numpy.zeros(f_padded.shape) #padded output image
    image_mod2 = numpy.zeros(f_padded.shape) #padded output image

    #this is for the col vector
    for startx in range(M-n+1):
        for starty in range(N):
            convolution_localx(f_padded,image_mod1,colVector,offset,startx,starty)
    
    #this is for the row vector
    for startx in range(M):
        for starty in range(N-n+1):
            convolution_localy(image_mod1,image_mod2,rowVector,offset,startx,starty)
    
    image_mod3 = image_mod2[offset:(M-offset),offset:(N-offset)]
    return image_mod3

def smoothGaussian(image_path, kernelSize):
    f = pyplot.imread(image_path)
    image_mod3 = gaussianFilter(f,kernelSize)
    image_mod3Final = Image.fromarray(image_mod3)
    return image_mod3Final

def statistical_local(inputimage, outputimage, neighborhoodSize, offsetlocal, x, y, index):
    index_array = numpy.linspace(start=-1*offsetlocal,stop=offsetlocal,num=neighborhoodSize,dtype=numpy.int)
    localx = x+offsetlocal
    localy = y+offsetlocal
    statArr = numpy.array([], dtype=numpy.int)
    for s in index_array:
        for t in index_array:
            statArr = numpy.append(statArr, inputimage[localx-s,localy-t])
    statArr = numpy.sort(statArr)
    outputimage[localx,localy] = statArr[index]

def statisticalFilter(image_path,neighborhoodSize, statCode):
    f = pyplot.imread(image_path)
    n = neighborhoodSize # kernel rows = cols
    offset = int((n-1)/2)
    #print(offset)
    f_padded = numpy.pad(f, ((offset,offset),(offset,offset)), 'constant')

    M = f_padded.shape[0] #image rows
    N = f_padded.shape[1] #image cols
    image_mod = numpy.zeros(f_padded.shape) #padded output image
    
    statIndex = -1
    if(statCode == 0):
        statIndex = 0
    elif(statCode == 1):
        statIndex = (neighborhoodSize**2-1)/2
        statIndex = int(statIndex)
    elif(statCode == 2):
        statIndex = neighborhoodSize**2-1

    for startx in range(M-n+1):
        for starty in range(N-n+1):
            statistical_local(f_padded,image_mod,neighborhoodSize,offset,startx,starty, statIndex)
    image_mod2 = image_mod[offset:(M-offset+1),offset:(N-offset+1)]
    
    image_mod2Final = Image.fromarray(image_mod2)
    return image_mod2Final

def unsharpFilter(image_path, kernelSize):
    image = pyplot.imread(image_path)
    blurredImage = gaussianFilter(image,kernelSize) #image and image_path
    mask = (image-blurredImage)
    sharpenedImage = saturated_sum(image,mask)
    sharpenedImageFinal = Image.fromarray(sharpenedImage)
    return sharpenedImageFinal

def laplacianKernelMaker(lapkernelSize):
    lapKernel = numpy.ones((lapkernelSize,lapkernelSize),dtype=numpy.int)
    offset = int((lapkernelSize-1)/2)
    lapKernel[offset,offset] = 1-lapkernelSize**2
    return lapKernel

def sharpenLaplacian(image_path,kernelSize):
    f = pyplot.imread(image_path)
    w = laplacianKernelMaker(kernelSize)
    n = w.shape[0] # kernel rows = cols
    offset = int((n-1)/2)
    f_padded = numpy.pad(f, ((offset,offset),(offset,offset)), 'constant')
    M = f_padded.shape[0] #image rows
    N = f_padded.shape[1] #image cols
    image_mod = numpy.zeros(f_padded.shape) #padded output image
    
    for startx in range(M-n+1):
        for starty in range(N-n+1):
            convolution_local(f_padded,image_mod,w,offset,startx,starty)
    image_mod2 = image_mod[offset:(M-offset),offset:(N-offset)]

    image_mod3 = saturated_sum(f,image_mod2)
    image_mod3Final = Image.fromarray(image_mod3)
    return image_mod3Final

def convolution_local(inputimage, outputimage, w, offsetlocal, x, y):
    index_array = numpy.linspace(start=-1*offsetlocal,stop=offsetlocal,num=w.shape[0],dtype=numpy.int)
    localx = x+offsetlocal
    localy = y+offsetlocal
    sumOfProducts = 0
    for s in index_array:
        for t in index_array:
            sumOfProducts += w[s+offsetlocal,t+offsetlocal]*inputimage[localx-s,localy-t]
    sumOfProducts = int(sumOfProducts)
    outputimage[localx,localy] = sumOfProducts
