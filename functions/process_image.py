import cv2
import numpy as np

# check if small box is in big box
def contained(big, small):
    # big corners
    x,y,w,h = big;
    big_tl = [x, y];
    big_br = [x+w, y+h];

    # small corners
    x,y,w,h = small;
    small_tl = [x, y];
    small_br = [x+w, y+h];

    # check
    if small_tl[0] > big_tl[0] and small_br[0] < big_br[0]:
        if small_tl[1] > big_tl[1] and small_br[1] < big_br[1]:
            return True;
    return False;

# load image
img = cv2.imread("numbers.png");

# change to hue colorspace
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);
h,s,v = cv2.split(hsv);

# use clahe to improve contrast 
# (the contrast is pretty good already, so not much change, but good habit to have here)
clahe = cv2.createCLAHE(clipLimit = 10) 
contrast = clahe.apply(v);

# rescale
scale = 2.0;
h, w = img.shape[:2];
h = int(h * scale);
w = int(w * scale);
contrast = cv2.resize(contrast, (w,h), cv2.INTER_LINEAR);
img = cv2.resize(img, (w,h), cv2.INTER_LINEAR);

# use canny
canny = cv2.Canny(contrast, 10, 60);

# show
cv2.imshow('i', img);
cv2.imshow('v', v);
cv2.imshow('c', contrast);
cv2.imshow("canny", canny);
cv2.waitKey(0);

# try to fill in contours
# contours
_, contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);

# filter contours by size
# filter out noisy bits and the big grid boxes
filtered = [];
for contour in contours:
    perimeter = cv2.arcLength(contour, True);
    if 50 < perimeter and perimeter < 750:
        filtered.append(contour);

# draw contours again
# create a mask of the contoured image
mask = np.zeros_like(contrast);
mask = cv2.drawContours(mask, filtered, -1, 255, -1);

# close to get rid of annoying little gaps
kernel = np.ones((3,3),np.uint8)
mask = cv2.dilate(mask,kernel,iterations = 1);
mask = cv2.erode(mask,kernel, iterations = 1);

# contours
_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);

# alright, hierarchy is being stupid, plan B
# SUUUUUPEEERRR JAAAANK
outer_cntrs = [a for a in range(len(contours))];
children = [];
for a in range(len(contours)):
    if a in outer_cntrs:
        # get current box
        big_box = cv2.boundingRect(contours[a]);
        # check against all other boxes
        for b in range(0, len(contours)):
            if b in outer_cntrs:
                small_box = cv2.boundingRect(contours[b]);
                # remove any children
                if contained(big_box, small_box):
                    outer_cntrs.remove(b);
                    children.append(contours[b]);

# # select by hierarchy
top_cntrs = [];
for a in range(len(contours)):
    if a in outer_cntrs:
        top_cntrs.append(contours[a]);

# create a mask of the contoured image
mask = np.zeros_like(contrast);
mask = cv2.drawContours(mask, top_cntrs, -1, 255, -1);
mask = cv2.drawContours(mask, children, -1, 255, -1);

# close
kernel = np.ones((3,3),np.uint8)
mask = cv2.dilate(mask,kernel,iterations = 1);
mask = cv2.erode(mask,kernel, iterations = 1);

# do contours agains because opencv is being super difficult
# honestly, at this point, a fill method would've been better
# contours
_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);

# fill in
for con in contours:
    cv2.fillPoly(mask, pts = [con], color=(255));
for con in children:
    cv2.fillPoly(mask, pts = [con], color=(0));

# resize back down
h, w = mask.shape;
h = int(h / scale);
w = int(w / scale);
mask = cv2.resize(mask, (w,h));

# show
cv2.imshow("mask", mask);
cv2.waitKey(0);

# save
cv2.imwrite("filled.png", mask);
