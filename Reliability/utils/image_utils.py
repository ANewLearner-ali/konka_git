import os

import cv2
import time
import numpy as np


A_HASH = 1
P_HASH = 2
D_HASH = 3
HISTOGRAM = 4

SIZE = 16                   # 压缩后的默认大小
SIMILARITY_RATE = 0.85      # 默认的相似阈值


# 均值哈希算法, 需要传入cv2的image对象
def aHash(img):
    img = cv2.resize(img, (SIZE, SIZE))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    np_mean = np.mean(gray)  # 求numpy.ndarray平均值
    ahash_01 = (gray > np_mean) + 0  # 大于平均值=1，否则=0
    ahash_list = ahash_01.reshape(1, -1)[0].tolist()  # 展平->转成列表
    ahash_str = ''.join([str(x) for x in ahash_list])
    return ahash_str


# 感知哈希算法, 需要传入cv2的image对象
def pHash(img):
    img = cv2.resize(img, (64, 64))  # 默认interpolation=cv2.INTER_CUBIC
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dct = cv2.dct(np.float32(gray))
    dct_roi = dct[0:SIZE, 0:SIZE]  # opencv实现的掩码操作

    avreage = np.mean(dct_roi)
    phash_01 = (dct_roi > avreage) + 0
    phash_list = phash_01.reshape(1, -1)[0].tolist()
    phash_str = ''.join([str(x) for x in phash_list])
    return phash_str


# 差分哈希算法, 需要传入cv2的image对象，默认的hash算法
def dHash(img):
    img = cv2.resize(img, (SIZE + 1, SIZE))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    hash_str0 = []
    for i in range(SIZE):
        hash_str0.append(gray[:, i] > gray[:, i + 1])
    hash_str1 = np.array(hash_str0) + 0
    hash_str2 = hash_str1.T
    hash_str3 = hash_str2.reshape(1, -1)[0].tolist()
    dhash_str = ''.join([str(x) for x in hash_str3])
    return dhash_str


# 计算汉明距离，需要传入两个hash字符串
def hammingDist(s1, s2):
    assert len(s1) == len(s2)
    dif_len = sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])
    return dif_len


# 通过得到RGB每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


# ！！！ 一般用这个方法就可以了，传入两张图片的路径或者两个cv2的image对象，默认采用差分哈希算法 ！！！
# 建议传文件路径比较
def similarity(img_path1, img_path2, mode=P_HASH):
    if isinstance(img_path1, str):
        raw_img1 = img_path1
        raw_img2 = img_path2
        img1 = get_img(raw_img1)
        img2 = get_img(raw_img2)
    else:
        img1 = img_path1
        img2 = img_path2
    if mode == HISTOGRAM:
        ret = classify_hist_with_split(img1, img2)
    else:
        if mode == A_HASH:
            hash_str1 = aHash(img1)
            hash_str2 = aHash(img2)
        elif mode == P_HASH:
            hash_str1 = pHash(img1)
            hash_str2 = pHash(img2)
        else:
            hash_str1 = dHash(img1)
            hash_str2 = dHash(img2)
        # ret = 1 - hammingDist(hash_str1, hash_str2) * 1. / (32 * 32 / 4)
        ret = 1 - hammingDist(hash_str1, hash_str2) * 1. / (SIZE * SIZE)
    return ret


# 优化后的图片读取方法，并支持区域截图
# 获取cv2的image对象，需要传入图片路径或者cv2的image对象，tag_crop_para是在tag_img中的区域截图，如
# percent_mode:     {'left':0.5, 'top': 0.5, 'right': 0.8, 'bottom': 0.8}       0 <= val <= 1
# pixel_mode:       {'left':0.5, 'top': 0.5, 'right': 0.8, 'bottom': 0.8}       0 <= val <= height(width)
def get_img(tag_img, tag_crop_para=None, clear_temp=True):
    if isinstance(tag_img, str):
        file = tag_img
        tag_img = cv2.imread(file)
        file_tmp = f'img_tmp_{time.time()}.jpg'
        if tag_img is None:
            with open(file, 'rb') as f:
                b = f.read()
            with open(file_tmp, 'wb') as f:
                f.write(b)
            tag_img = cv2.imread(file_tmp)
            try:
                if clear_temp:
                    os.remove(file_tmp)
            except:
                pass
    if tag_crop_para is not None:
        height = len(tag_img)
        width = len(tag_img[0])
        for key in tag_crop_para:
            if tag_crop_para[key] > 1:
                height = 1
                width = 1
                break
        tag_img = tag_img[int(tag_crop_para['top'] * height): int(tag_crop_para['bottom'] * height),
                  int(tag_crop_para['left'] * width): int(tag_crop_para['right'] * width)]
    return tag_img


# 优化后的图片保存方法
def write_img(save_path: str, img, clear_temp: bool = True):
    file_tmp = f'img_w_tmp_{time.time()}.jpg'
    cv2.imwrite(file_tmp, img)
    with open(file_tmp, 'rb') as f:
        b = f.read()
    with open(save_path, 'wb') as f:
        f.write(b)
    if clear_temp:
        try:
            if clear_temp:
                os.remove(file_tmp)
        except:
            pass


# 从files的图片库中，找出index从left到right中tag_img第一次出现的index
def find_first_show(files, left, right, tag_img, tag_crop_paras=None):
    tag_img = get_img(tag_img, tag_crop_paras)
    while left <= right:
        img = get_img(files[left], tag_crop_paras)
        similarity_val = similarity(img, tag_img)
        if similarity_val > SIMILARITY_RATE:
            return left
        left += 1
    return None


# 从files的图片库中，找出index从left到right中tag_img1第一次出现的index和tag_img2第一次出现的index，方法待完善，没有截图选项
def get_first_to_first(files, left, right, tag_img1, tag_img2):
    index1 = find_first_show(files, left, right, tag_img1)
    if index1 is None:
        return None
    index2 = find_first_show(files, index1, right, tag_img2)
    if index2 is None:
        return None
    return [index1, index2]


# 从files的图片库中，找出index从left到right中tag_img1最后一次出现的index和tag_img2第一次出现的index，会返回多组数据，如
# [[2,4], [6,10]]
def get_last_to_first(files, left, right, tag_img1, tag_img2, tag_crop_paras1=None, tag_crop_paras2=None):
    print('get_last_to_first :', left, right, tag_img1, tag_img2, tag_crop_paras1, tag_crop_paras2)
    found_1_flag = False
    index1 = None
    ret = []
    tag_img1 = get_img(tag_img1, tag_crop_paras1)
    tag_img2 = get_img(tag_img2, tag_crop_paras2)
    while left <= right:
        img_start = get_img(files[left], tag_crop_paras1)
        img_end = get_img(files[left], tag_crop_paras2)
        similarity_1 = similarity(img_start, tag_img1)
        similarity_2 = similarity(img_end, tag_img2)
        if similarity_1 >= SIMILARITY_RATE or similarity_2 >= SIMILARITY_RATE:
            if found_1_flag:
                if similarity_2 >= SIMILARITY_RATE:
                    index2 = left
                    ret.append([index1, index2])
                    found_1_flag = False
                elif similarity_1 >= SIMILARITY_RATE:
                    index1 = left
            else:
                if similarity_1 >= SIMILARITY_RATE:
                    index1 = left
                    found_1_flag = True
        left += 1
    return ret


def match_coordinate(pic_ori, pic_temp, method=cv2.TM_SQDIFF_NORMED):
    """
    图片匹配，pic_ori图片在pic_temp模板图片中查找出最匹配的区域，并返回坐标
    """
    # target = cv2.imread(pic_ori, 0)
    # tpl = cv2.imread(pic_temp, 0)
    target = get_img(pic_ori)
    tpl = get_img(pic_temp)
    th, tw = tpl.shape[:2]
    result = cv2.matchTemplate(target, tpl, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print "min_val:", min_val, "max_val:", max_val, "min_loc:", min_loc, "max_loc:", max_loc
    if method == cv2.TM_SQDIFF_NORMED:
        tl = min_loc
    elif method in [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]:
        tl = max_loc
    br = (tl[0] + tw, tl[1] + th)
    cv2.rectangle(target, tl, br, (0, 0, 255), 10)
    return tl[0], tl[1], tl[0] + tw, tl[1] + th
