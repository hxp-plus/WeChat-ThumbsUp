import os
import time
from random import randint

from PIL import Image

SCREEN_RESOLUTION_X = 1080  # 屏幕分辨率X
SCREEN_RESOLUTION_Y = 2244  # 屏幕分辨率Y
SWIPE_UP_BOTTOM = 2000  # 向上滑动时的起始坐标，如果从太地下开始向上滑，手势操作会退出微信
SWIPE_UP_TOP = 150  # 微信“朋友圈”标题的最底下的位置
LIKE_BUTTON_X = 759  # 点赞前先要点的那个两个点图标中第一个点的位置
LIKE_BUTTON_RGB = [141, 141, 147]  # 点赞前先要点的那个两个点图标中第一个点的RGB值


def is_pixel_same(pixel_a, pixel_b):
    for i in range(3):
        if not pixel_a[i] == pixel_b[i]:
            return False
    return True


def get_current_screen():
    time.sleep(1)
    os.system("adb shell screencap -p /sdcard/qzone-thumbsup.png")
    os.system("adb pull /sdcard/qzone-thumbsup.png ./qzone-thumbsup.png")


def get_like_button_y():
    get_current_screen()
    img = Image.open("./qzone-thumbsup.png")
    px = img.convert('RGB')
    for y in range(0, SCREEN_RESOLUTION_Y):
        current_pixel = px.getpixel((LIKE_BUTTON_X, y))
        if is_pixel_same(current_pixel, LIKE_BUTTON_RGB):
            return y
    swipe_up(int(SCREEN_RESOLUTION_Y / 2))
    return get_like_button_y()


def click_like(y):
    for i in range(100):
        os.system("adb shell input tap {0} {1}".format(LIKE_BUTTON_X, y))
    print("Clicked the like button 99 times, y={0}".format(y))
    time.sleep(1)
    get_current_screen()


def swipe_up(y):
    print("Swipe up by {0}".format(y))
    os.system("adb shell input swipe {0} {1} {2} {3} {4}".format(SCREEN_RESOLUTION_X / 2, SWIPE_UP_BOTTOM,
                                                                 SCREEN_RESOLUTION_X / 2,
                                                                 SWIPE_UP_BOTTOM - y + SWIPE_UP_TOP,
                                                                 (y - SWIPE_UP_TOP) * 2))


def main():
    while True:
        y = get_like_button_y()
        click_like(y)
        swipe_up(y)


if __name__ == "__main__":
    main()
