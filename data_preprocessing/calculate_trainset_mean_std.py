import numpy as np
from os.path import isdir
from glob import glob
import cv2
import timeit
import multiprocessing as mp
import argparse

# number of channels of the dataset image, 3 for color jpg, 1 for grayscale img
# you need to change it to reflect your dataset
CHANNEL_NUM = 3

def split(a, n):
    k, m = divmod(len(a), n)
    answer=[]
    for i in range(n):
        answer.append(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)])
    return answer


def cal_dir_stat(im_pth):
    global CHANNEL_NUM
    pixel_num = 0 # store all pixel number in the dataset
    channel_sum = np.zeros(CHANNEL_NUM)
    channel_sum_squared = np.zeros(CHANNEL_NUM)

    for i, path in enumerate(im_pth):
        if i%1000==0:
            print(i)
        im = cv2.imread(path) # image in M*N*CHANNEL_NUM shape, channel in BGR order
        im = im/255.0
        pixel_num += (im.size/CHANNEL_NUM)
        channel_sum += np.sum(im, axis=(0, 1))
        channel_sum_squared += np.sum(np.square(im), axis=(0, 1))

    return [pixel_num, channel_sum, channel_sum_squared]

def cal_dir_stat_parallel(root):
    global CHANNEL_NUM
    im_pths = glob(root+'/*')
    print('number of files in folder are:')
    print(root)
    print(len(im_pths))
    num_cores = mp.cpu_count()
    im_pths_split = split(im_pths, num_cores)

    print('getting mean rgb values')
    pool = mp.Pool(num_cores)
    results = pool.map(cal_dir_stat,[im_pth for im_pth in im_pths_split])
    pool.close()

    pixel_num_total = 0 # store all pixel number in the dataset
    channel_sum_total = np.zeros(CHANNEL_NUM)
    channel_sum_squared_total = np.zeros(CHANNEL_NUM)
    for result in results:
        pixel_num_total +=result[0]
        channel_sum_total +=result[1]
        channel_sum_squared_total +=result[2]

    bgr_mean = channel_sum_total / pixel_num_total
    bgr_std = np.sqrt(channel_sum_squared_total / pixel_num_total - np.square(bgr_mean))

    # change the format from bgr to rgb
    rgb_mean = list(bgr_mean)[::-1]
    rgb_std = list(bgr_std)[::-1]
    print("mean:{}\nstd:{}".format(rgb_mean, rgb_std))
    return rgb_mean, rgb_std
