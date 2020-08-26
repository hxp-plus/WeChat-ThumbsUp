import os
import time

from PIL import Image

SCREEN_RESOLUTION_X = 1080  # 屏幕分辨率X
SCREEN_RESOLUTION_Y = 2244  # 屏幕分辨率Y
SWIPE_UP_BOTTOM = 2000  # 向上滑动时的起始坐标，如果从太地下开始向上滑，手势操作会退出微信
SWIPE_UP_TOP = 150  # 微信“朋友圈”标题的最底下的位置
TWO_DOTS_BUTTON_X = 1005  # 点赞前先要点的那个两个点图标中第一个点的位置
TWO_DOTS_BUTTON_RGB = [95, 116, 158]  # 点赞前先要点的那个两个点图标中第一个点的RGB值
HEART_POSITION_UNLIKED_X = 550  # “赞”左边那个心形图标的最左边的和两个点图标中点相同Y坐标的点的X坐标
HEART_POSITION_UNLIKED_RGB = [64, 64, 64]  # 没有被赞时上面那个点的RGB值


def is_pixel_same(pixel_a, pixel_b):
    for i in range(3):
        if not pixel_a[i] == pixel_b[i]:
            return False
    return True


def get_current_screen():
    time.sleep(1)
    os.system("adb shell screencap -p /sdcard/wechat-thumbsup.png")
    os.system("adb pull /sdcard/wechat-thumbsup.png ./wechat-thumbsup.png")


def get_two_dots_button_y():
    get_current_screen()
    img = Image.open("./wechat-thumbsup.png")
    px = img.convert('RGB')
    for y in range(0, SCREEN_RESOLUTION_Y):
        current_pixel = px.getpixel((TWO_DOTS_BUTTON_X, y))
        if is_pixel_same(current_pixel, TWO_DOTS_BUTTON_RGB):
            return y
    return -1


def click_like(y):
    os.system("adb shell input tap {0} {1}".format(TWO_DOTS_BUTTON_X, y))
    print("Clicked the two dots button, y={0}".format(y))
    time.sleep(2)
    get_current_screen()
    img = Image.open("./wechat-thumbsup.png")
    px = img.convert('RGB')
    like_pixel = px.getpixel((HEART_POSITION_UNLIKED_X, y))
    print(like_pixel)
    if is_pixel_same(like_pixel, HEART_POSITION_UNLIKED_RGB):
        os.system("adb shell input tap {0} {1}".format(HEART_POSITION_UNLIKED_X, y))
        print("Thumbed Up")
    else:
        os.system("adb shell input tap {0} {1}".format(TWO_DOTS_BUTTON_X, y))
        print("This moment is liked")


def swipe_up(y):
    print("Swipe up by {0}".format(y))
    os.system("adb shell input swipe {0} {1} {2} {3} 5000".format(SCREEN_RESOLUTION_X / 2, SWIPE_UP_BOTTOM,
                                                                  SCREEN_RESOLUTION_X / 2,
                                                                  SWIPE_UP_BOTTOM - y + SWIPE_UP_TOP))


def main():
    while True:
        y = get_two_dots_button_y()
        click_like(y)
        swipe_up(y)


if __name__ == "__main__":
    main()
