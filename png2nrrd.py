# 
# Convert png images to nrrd
#
# - example output at https://drive.google.com/file/d/1EC9fPdxWJdBmKdUjiUpAYeaKhdVJoIL-/view?usp=sharing
#
# - correct header for three.js
#   example: 
# NRRD0004
# # Complete NRRD file format specification at:
# # http://teem.sourceforge.net/nrrd/format.html
# type: short
# dimension: 3
# space: left-posterior-superior
# sizes: 1000 1000 100
# space directions: (0.93750000000000022,0,0) (0,-0.93750000000000022,0) (0,0,-1.5000000000000004)
# kinds: domain domain domain
# endian: little
# encoding: ascii
# space origin: (-119.53000000000002,119.53000000000007,84.000000000000028)
#
# EE Jan '21
#

import numpy as np
import nrrd
import cv2


DATAPATH = '/mnt/35888f2a-be92-4a2f-8a27-6a8732423f1a/Data/FIB-25'
START = 4000
NUMIMG = 34
STEP = 10
W = 250
H = 250

# Treat this data array as a 3D volume using C-order indexing
data = np.zeros((NUMIMG, 2*W, 2*H))
index = 0
for i in range(START, START+ (NUMIMG*STEP), STEP):
  IMGPATH = '{}/iso.0{}.png'.format(DATAPATH, i)
  print(IMGPATH)
  img = cv2.imread(IMGPATH,0)

  # use central region
  cx = int(img.shape[1] / 2)
  cy = int(img.shape[0] / 2)
  img = img[cy-H:cy+H, cx-W:cx+H]

  data[index,:,:] = img
  index += 1

# Save the NRRD object with the correct index order
header = {}
header['encoding'] = 'ascii'
nrrd.write('output2.nrrd', data, header=header, index_order='C')

