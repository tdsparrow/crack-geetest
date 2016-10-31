#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from uuid import uuid4
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def home_page():
    driver = webdriver.Chrome()
    driver.get("http://gsxt.hljaic.gov.cn/index.jspx")

    input_el = driver.find_element_by_id("searchText")
    input_el.clear()
    input_el.send_keys(u"中国移动")

    search_el = driver.find_element_by_id("u85")
    search_el.click()
    time.sleep(1)

    captcha_el = driver.find_element_by_class_name("gt_box")
    location = captcha_el.location
    size = captcha_el.size
    left = int(location['x'] - 92)
    top = int(location['y'])
    right = int(location['x'] - 92 + size['width'])
    bottom = int(location['y'] + size['height'])

    dragger = driver.find_element_by_class_name("gt_slider_knob")
    driver.save_screenshot('screenshot1.png')
    img = Image.open('screenshot1.png')
    img = img.crop((left, top, right, bottom))
    img.save('screenshot1.png')
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(dragger, 5, 0).perform()
    time.sleep(3)

    driver.save_screenshot('screenshot2.png')
    img = Image.open('screenshot2.png')
    img = img.crop((left, top, right, bottom))
    img.save('screenshot2.png')

    x = calc_side_position()
    time.sleep(1)
    dragger = driver.find_element_by_class_name("gt_slider_knob")
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(dragger, x, 0).perform()
    time.sleep(10)
    driver.close()


def calc_side_position():
    img1 = Image.open("./screenshot1.png")
    img2 = Image.open("./screenshot2.png")
    w1, h1 = img1.size
    w2, h2 = img2.size
    if w1 != w2 or h1 != h2:
        return False
    left = 0
    flag = False
    for i in xrange(45, w1):
        for j in xrange(h1):
            if not is_equal(img1, img2, i, j):
                left = i
                flag = True
                break
        if flag:
            break
    if left == 45:
        left -= 2
    return left


def is_equal(img1, img2, x, y):
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    print(pix1, pix2)
    if abs(pix1[0] - pix2[0] < 50) and abs(pix1[1] - pix2[1] < 50) and abs(pix1[2] - pix2[2] < 50):
        return True
    else:
        return False


def slice_image(path="./", slice_name="SLICE"):
    positions = [(-157, -58), (-145, -58), (-265, -58), (-277, -58),
                 (-181, -58), (-169, -58), (-241, -58), (-253, -58),
                 (-109, -58), (-97, -58), (-289, -58), (-301, -58), (-85, -58),
                 (-73, -58), (-25, -58), (-37, -58), (-13, -58), (-1, -58),
                 (-121, -58), (-133, -58), (-61, -58), (-49, -58), (-217, -58),
                 (-229, -58), (-205, -58), (-193, -58), (-145, 0), (-157, 0),
                 (-277, 0), (-265, 0), (-169, 0), (-181, 0), (-253, 0),
                 (-241, 0), (-97, 0), (-109, 0), (-301, 0), (-289, 0),
                 (-73, 0), (-85, 0), (-37, 0), (-25, 0), (-1, 0), (-13, 0),
                 (-133, 0), (-121, 0), (-49, 0), (-61, 0), (-229, 0),
                 (-217, 0), (-193, 0), (-205, 0)]
    img = Image.open(path)
    w, h = img.size
    sw, sh = (10, 58)
    inc = 1
    for (left, up) in positions:
        left = abs(left)
        up = abs(up)
        right = left + sw
        down = up + sh
        region = img.crop((left, up, right, down))
        region.save("./%s_%s.png" % (slice_name, inc))
        inc += 1


def merge_images(slice_name="SLICE", merged_name=uuid4().get_hex().upper()):
    new_img = Image.new('RGBA', (262, 118))

    x_offset = 0
    for i in range(1, 27):
        slice_path = "./%s_%s.png" % (slice_name, i)
        img = Image.open(slice_path)
        new_img.paste(img, (x_offset, 0))
        x_offset += img.size[0]
        os.remove(slice_path)

    x_offset = 0
    for i in range(27, 53):
        slice_path = "./%s_%s.png" % (slice_name, i)
        img = Image.open(slice_path)
        new_img.paste(img, (x_offset, img.size[1]))
        x_offset += img.size[0]
        os.remove(slice_path)

    new_img.save('%s.png' % merged_name)


def main():
    home_page()


if __name__ == "__main__":
    main()
