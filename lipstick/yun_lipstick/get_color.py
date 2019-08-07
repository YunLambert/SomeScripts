"""
get lipstick's color
@input: image(with lipstick's color)
@output: lipstick type
author: YunLambert
date:20190807
"""
import os
import colorsys
import PIL.Image as Image
import json


def get_color(image):
    # to get dominant color
    max_score = 0.0001
    result_color = None
    for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)

        if y > 0.9:
            continue
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            result_color = (r, g, b)
        return result_color


def my_hex2rgb(color):
    h = color.lstrip("#")
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return rgb


def comp_color(image_dir):
    try:
        image = Image.open(image_dir)
        image = image.convert("RGB")
    except Exception as e:
        print(e)
        return
    des_color = get_color(image)
    with open('lipstick.json', 'r', encoding="utf-8") as f:
        dic = json.load(f)
        num = len(dic["brands"])
        s_list = []
        for i in range(num):
            s_num = len(dic["brands"][i]["series"])
            s_list.append(s_num)

        m = {}
        for j in range(num):
            for s in range(s_list[j]):
                brand_name = dic["brands"][j]["name"]
                lip_name = dic["brands"][j]["series"][s]["name"]
                lipsticks_num = len(dic["brands"][j]["series"][s]["lipsticks"])
                for r in range(lipsticks_num):
                    color = dic["brands"][j]["series"][s]["lipsticks"][r]["color"]
                    desc = dic["brands"][j]["series"][s]["lipsticks"][r]["name"]
                    m[color] = brand_name + " " + lip_name + " " + desc

        judge = 0
        for key,value in m.items():
            (r,g,b) = my_hex2rgb(key)
            (r1,g1,b1) = des_color
            # print(r,g,b)
            # print(r1,g1,b1)

            if abs(r-r1)<10 and abs(g-g1)<10 and (b-b1)<10:
                print("与 " + image_dir + "图片中 相近的口红可能为：" + value)
                judge = 1
        if judge == 0:
            print("暂无口红匹配色号！")




if __name__ == "__main__":
    comp_color("./test.jpg")