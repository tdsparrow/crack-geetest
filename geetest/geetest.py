# -*- coding: utf-8 -*-

import time
import uuid
import StringIO

from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains


class BaseGeetestCrack(object):

    """验证码破解基础类"""

    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()

    def input_by_id(self, text=u"中国移动", element_id="keyword"):
        """输入查询关键词

        :text: Unicode, 要输入的文本
        :element_id: 输入框网页元素id

        """
        input_el = self.driver.find_element_by_id(element_id)
        input_el.clear()
        input_el.send_keys(text)
        time.sleep(3.5)

    def click_by_id(self, element_id="btn_query"):
        """点击查询按钮

        :element_id: 查询按钮网页元素id

        """
        search_el = self.driver.find_element_by_id(element_id)
        search_el.click()
        time.sleep(3.5)

    def calculate_slider_offset(self):
        """计算滑块偏移位置，必须在点击查询按钮之后调用

        :returns: Number

        """
        img1 = self.crop_captcha_image()
        self.click_and_hold_slider()
        img2 = self.crop_captcha_image()
        w1, h1 = img1.size
        w2, h2 = img2.size
        if w1 != w2 or h1 != h2:
            return False
        left = 0
        flag = False
        for i in xrange(60, w1):
            for j in xrange(h1):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    flag = True
                    break
            if flag:
                break
        if left == 45:
            left -= 2
        return left-7

    def is_pixel_equal(self, img1, img2, x, y):
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        if (abs(pix1[0] - pix2[0] < 60) and abs(pix1[1] - pix2[1] < 60) and abs(pix1[2] - pix2[2] < 60)):
            return True
        else:
            return False

    def crop_captcha_image(self, element_id="gt_box"):
        """截取验证码图片

        :element_id: 验证码图片网页元素id
        :returns: StringIO, 图片内容

        """
        captcha_el = self.driver.find_element_by_class_name(element_id)
        location = captcha_el.location
        size = captcha_el.size
        left = int(location['x'])
        top = int(location['y'])
#        left = 1010
#        top = 535
        # right = left + int(size['width'])
        # bottom = top + int(size['height'])
        right = left + 523
        bottom = top + 235
        print(left, top, right, bottom)

        screenshot = self.driver.get_screenshot_as_png()

        screenshot = Image.open(StringIO.StringIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save("%s.png" % uuid.uuid4().get_hex())
        return captcha

    def get_browser_name(self):
        """获取当前使用浏览器名称
        :returns: TODO

        """
        return str(self.driver).split('.')[2]

    def click_and_hold_slider(self, element_class="gt_slider_knob"):
        self.move_to_element(element_class)
        action = ActionChains(self.driver)
        action.click_and_hold().perform()

    def drag_and_drop(self, x_offset=0, y_offset=0, element_class="gt_slider_knob"):
        """拖拽滑块

        :x_offset: 相对滑块x坐标偏移
        :y_offset: 相对滑块y坐标偏移
        :element_class: 滑块网页元素CSS类名

        """
        dragger = self.driver.find_element_by_class_name(element_class)
        action = ActionChains(self.driver)

        self.move_to_element(element_class)
        action.click_and_hold().perform()

        import random
        for m in xrange(x_offset):
            action.move_by_offset(1,0)
            time.sleep(random.randint(2,4)/100)

        # action.drag_and_drop_by_offset(dragger, x_offset, y_offset).perform()
        action.release().perform()
        # 这个延时必须有，在滑动后等待回复原状
        time.sleep(8)

    def move_by_offset_and_release(self, x_offset=0):
        import random
        action = ActionChains(self.driver)
        for m in xrange(x_offset):
            action.move_by_offset(1,random.choice([-1,-2,1,2]))
            time.sleep(random.randint(2,2+m*2)/100)

        action.release().perform()

    def move_to_element(self, element_class="gt_slider_knob"):
        """鼠标移动到网页元素上

        :element: 目标网页元素

        """
        time.sleep(3)
        element = self.driver.find_element_by_class_name(element_class)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        time.sleep(4.5)

    def crack(self):
        """执行破解程序

        """
        raise NotImplementedError
