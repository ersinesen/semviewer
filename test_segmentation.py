#
# Segmentation tests
#
# EE Jan '21

import cv2
import numpy as np
from matplotlib import pyplot as plt
import morphsnakes as ms 
import skimage.segmentation as seg
import skimage.color as color
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
from skimage.filters import sobel


DATAPATH = '/mnt/35888f2a-be92-4a2f-8a27-6a8732423f1a/Data/FIB-25'

def Snakes(img):
  img = img / 255.0
  # g(I)
  gimg = ms.inverse_gaussian_gradient(img)

  # Manual initialization of the level set
  init_ls = np.zeros(img.shape, dtype=np.int8)
  init_ls[10:-10, 10:-10] = 1

  # MorphGAC.
  out = ms.morphological_geodesic_active_contour(gimg, 230, init_ls,
                                           smoothing=1, threshold=0.69,
                                           balloon=-1)
  return out


def Watershed(gray):
  ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  # noise removal
  kernel = np.ones((3,3),np.uint8)
  opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
  # sure background area
  sure_bg = cv2.dilate(opening,kernel,iterations=5)
  # Finding sure foreground area
  dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
  ret, sure_fg = cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)
  # Finding unknown region
  sure_fg = np.uint8(sure_fg)
  unknown = cv2.subtract(sure_bg,sure_fg)
  # Marker labelling
  ret, markers = cv2.connectedComponents(sure_fg)
  # Add one to all labels so that sure background is not 0, but 1
  markers = markers+1
  # Now, mark the region of unknown with zero
  markers[unknown==255] = 0
  img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
  markers = cv2.watershed(img,markers)
  gray[markers == -1] = [255]
  return gray


def AdaptiveThresholding(img):
  img = cv2.medianBlur(img,5)

  #ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
  #th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
  #            cv2.THRESH_BINARY,11,2)
  th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
              cv2.THRESH_BINARY, 21, 5)

  return th3


for i in range(4000, 5000, 10):

  IMGPATH = '{}/iso.0{}.png'.format(DATAPATH, i)
  print(IMGPATH)
  img = cv2.imread(IMGPATH,0)

  # use central region
  cx = int(img.shape[1] / 2)
  cy = int(img.shape[0] / 2)
  W = 500
  H = 500
  img = img[cy-H:cy+H, cx-W:cx+H]


  # Otsu's thresholding
  ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

  # Otsu's thresholding after Gaussian filtering
  blur = cv2.GaussianBlur(img,(5,5),0)
  ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

  # remove small ones (black ones desired)
  #kernel = np.ones((3,3),np.uint8)
  #th4 = cv2.dilate(th3, kernel, iterations=3)

  # Adaptive GAussian thresholding
  #th3 = AdaptiveThresholding(img)

  #res = cv2.hconcat([img,th3])
  cv2.imshow('Otsu', th3)
  cv2.waitKey(500)

  # SLIC or felzenszwalb
  col = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
  image_ = slic(col, n_segments=256)
  #image_ = seg.felzenszwalb(col) 
  #image_ = quickshift(col, kernel_size=3, max_dist=6, ratio=0.5)
  #gradient = sobel(img)
  #image_ = watershed(gradient, markers=250, compactness=0.001)

  res = color.label2rgb(image_, col, kind='avg')
  cv2.imshow('SLIC/felzenszwalb', res)
  cv2.waitKey(500)

  # Snakes
  #sn = Snakes(img)
  #cv2.imshow('Snakes', sn)
  #cv2.waitKey(500)

  # Watershed segmentation
  #ws = Watershed(img)
  #cv2.imshow('Watershed', ws)
  #cv2.waitKey(500)

  # plot all the images and their histograms
  #images = [img, 0, th2,
  #          blur, 0, th3]
  #titles = ['Original Noisy Image','Histogram',"Otsu's Thresholding",
  #          'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]

  #for i in range(2):
  #    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
  #    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
  #    plt.subplot(2,3,i*3+2),plt.hist(images[i*3].ravel(),256)
  #    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
  #    plt.subplot(2,3,i*3+3),plt.imshow(images[i*3+2],'gray')
  #    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
  #plt.show()

cv2.destroyAllWindows()
