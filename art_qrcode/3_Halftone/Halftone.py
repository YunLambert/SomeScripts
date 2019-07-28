from PIL import Image
from PIL import ImageEnhance
from PIL import ImageSequence
# from images2gif import writeGif, readGif
import qrcode
from qrcode import util
import argparse


def produce(text, img, ver=5, err_crt=qrcode.constants.ERROR_CORRECT_H, bri=1.0, cont=1.0, \
            colourful=False, rgba=(0, 0, 0, 255), pixelate=False):
    if type(img) is Image.Image:  # 如果已经是图片了，直接pass；如果是字符串，则打开相应的图片；如果为空，则返回[]
        pass
    elif type(img) is str:
        img = Image.open(img)
    else:
        return []

    frames = []
    for frame in ImageSequence.Iterator(img):  # 一帧一帧处理动图
        frames.append(produce_helper(text, frame.copy(), ver, err_crt, bri, cont, colourful, rgba, pixelate))
    return frames


def produce_helper(text, img, ver=5, err_crt=qrcode.constants.ERROR_CORRECT_H, bri=1.0, cont=1.0, \
                   colourful=False, rgba=(0, 0, 0, 255), pixelate=False):
    qr = qrcode.QRCode(
        version=ver,
        error_correction=err_crt,
        box_size=3,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    # 根据参数进行颜色处理:
    img_qr = qr.make_image().convert().convert('RGBA')
    if colourful and (rgba != (0, 0, 0, 255)):
        color_picture(img_qr, rgba)

    # 修减本地图片，去宽和高短的一边作为size
    local_img = img.convert('RGBA')
    local_img_size = None
    img_size = img_qr.size[0] - 24
    if local_img.size[0] < local_img.size[1]:
        local_img_size = local_img.size[0]
    else:
        local_img_size = local_img.size[1]
    img_enh = local_img.crop((0, 0, local_img_size, local_img_size))
    # 调节亮度与对比度
    enh = ImageEnhance.Contrast(img_enh)
    img_enh = enh.enhance(cont)
    enh = ImageEnhance.Brightness(img_enh)
    img_enh = enh.enhance(bri)

    if not colourful:
        if pixelate:
            img_enh = img_enh.convert('1').convert('RGBA')
        else:
            img_enh = img_enh.convert('L').convert('RGBA')
    """
        1 ------------------（1位像素，黑白，每字节一个像素存储）
        L ------------------（8位像素，黑白）
        P ------------------（8位像素，使用调色板映射到任何其他模式）
        RGB-----------------（3x8位像素，真彩色）
        RGBA----------------（4x8位像素，带透明度掩模的真彩色）
        CMYK----------------（4x8位像素，分色）
        YCbCr---------------（3x8位像素，彩色视频格式）
        I-------------------（32位有符号整数像素）
        F-------------------（32位浮点像素）
     """

    img_frame = img_qr
    img_enh = img_enh.resize((img_size * 10, img_size * 10))
    img_enh_l = img_enh.convert("L").resize((img_size, img_size))
    img_frame_l = img_frame.convert("L")

    for x in range(0, img_size):  # 二维码三个角落不作处理
        for y in range(0, img_size):
            if x < 24 and (y < 24 or y > img_size - 25):
                continue
            if x > img_size - 25 and y < 24:
                continue
            if (x % 3 == 1 and y % 3 == 1):
                if (img_frame_l.getpixel((x + 12, y + 12)) > 70 and img_enh_l.getpixel((x, y)) < 185) or (
                        img_frame_l.getpixel((x + 12, y + 12)) < 185 and img_enh_l.getpixel((x, y)) > 70):
                    continue
            img_frame.putpixel((x + 12, y + 12), (0, 0, 0, 0))  # 放黑色

    pos = qrcode.util.pattern_position(qr.version)
    img_qr2 = qr.make_image().convert("RGBA")
    if colourful and (rgba != (0, 0, 0, 0)):
        color_picture(img_qr2, rgba)
    for i in pos:
        for j in pos:
            if (i == 6 and j == pos[-1]) or (j == 6 and i == pos[-1]) or (i == 6 and j == 6):
                continue
            else:
                rect = (3 * (i - 2) + 12, 3 * (j - 2) + 12, 3 * (i + 3) + 12, 3 * (j + 3) + 12)
                img_tmp = img_qr2.crop(rect)
                img_frame.paste(img_tmp, rect)  # 把img_qr2的非pattern部分剪切到img_tmp上

    # 结合
    img_res = Image.new("RGBA", (img_frame.size[0] * 10, img_frame.size[1] * 10), (255, 255, 255, 255))
    img_res.paste(img_enh, (120, 120), img_enh)
    img_frame = img_frame.resize((img_frame.size[0] * 10, img_frame.size[1] * 10))
    img_res.paste(img_frame, (0, 0), img_frame)
    img_res = img_res.convert('RGB')
    if pixelate:
        return img_res.resize(img_qr.size).resize((local_img_size, local_img_size))
    return img_res


def color_picture(image, color):
    pixels = image.load()
    size = image.size[0]
    for width in range(size):
        for height in range(size):
            r, g, b, a = pixels[width, height]
            if (r, g, b, a) == (0, 0, 0, 255):
                pixels[width, height] = color
            else:
                pixels[width, height] = (r, g, b, color[3])


def main():
    # 参数设置
    """args meaning:
       :txt: QR text
       :img: Image path / Image object
       :ver: QR version
       :err_crt: QR error correct
       :bri: Brightness enhance
       :cont: Contrast enhance
       :colourful: If colourful mode
       :rgba: color to replace black
       :pixelate: pixelate
       """
    parser = argparse.ArgumentParser(description="Combine your QR code with custom picture")
    parser.add_argument("image")
    parser.add_argument("text", help="QRcode Text.")
    parser.add_argument("-o", "--output", help="Name of output file.")
    parser.add_argument("-v", "--version", type=int, help="QR version.In range of [1-40]")
    parser.add_argument("-e", "--errorcorrect", choices={"L", "M", "Q", "H"}, help="Error correct")
    parser.add_argument("-b", "--brightness", type=float, help="Brightness enhance")
    parser.add_argument("-c", "--contrast", type=float, help="Contrast enhance")
    parser.add_argument("-C", "--colourful", action="store_true", help="colourful mode")
    parser.add_argument("-r", "--rgba", nargs=4, metavar=('R', 'G', 'B', 'A'), type=int, help="color to replace black")
    parser.add_argument("-p", "--pixelate", action="store_true", help="pixelate")
    parser.add_argument("-g", "--gif", type=bool, help="if the image is gif")
    parser.add_argument("-m", "--modify", type=bool, help="resize the image in the middle")
    parser.add_argument("-d", "--duration", type=float, help="duration of gif")
    args = parser.parse_args()

    # 赋值参数
    # -image
    img = args.image

    # -text
    text = args.text

    # -o
    if args.output is not None:
        output = args.output
    else:
        output = "result_artqrcode.png"

    # -v
    ver = 5
    if args.version:
        if args.version >= 1 and args.version <= 40:
            ver = args.version
    # -e
    ec = qrcode.constants.ERROR_CORRECT_H
    if args.errorcorrect:
        if args.errorcorrect == 'L':
            ec = qrcode.constants.ERROR_CORRECT_L
        if args.errorcorrect == 'M':
            ec = qrcode.constants.ERROR_CORRECT_M
        if args.errorcorrect == 'Q':
            ec = qrcode.constants.ERROR_CORRECT_Q
    # -b
    if args.brightness:
        bri = args.brightness
    else:
        bri = 1.0

    # -c
    if args.contrast:
        cont = args.contrast
    else:
        cont = 1.0

    # -C
    if args.colourful:
        colr = True
    else:
        colr = False

    # -p
    if args.pixelate:
        pixelate = True
    else:
        pixelate = False

    # -d
    if args.duration:
        duration = args.duration
    else:
        if args.gif is not None:
            print("GIF without a duration! Count it as 0.1s!")
        duration = 0.1

    if colr:
        if args.rgba:
            rgba = tuple(args.rgba)
        else:
            rgba = (0, 0, 0, 255)
    else:
        rgba = (0, 0, 0, 255)

    # 以下是使用了images2gif的部分，如果想研究可以取消注释
    # if args.gif:
    #     if args.output:
    #         output=args.output
    #     else:
    #         output="result_artqrcode.gif"
    #     images=readGif(img,False)
    #     if args.modify:
    #         width,height=images[0].size
    #         rect=((width-height)/2,0,(width+height)/2,height)
    #         for frame in images:
    #             frame=frame.crop(rect)
    #     qr_img=[]
    #     for frame in images:
    #         qr_img.append(produce(text, frame, ec, bri, cont, colourful=colr, rgba=rgba, pixelate=pixelate)[0])
    #     writeGif(output,qr_img,duration=duration,repeat=True,subRectangles=False)
    # else:
    #     result = produce(text, img, ec, bri, cont, colourful=colr, rgba=rgba, pixelate=pixelate)
    #     if len(result) == 1 or output.upper()[-3:] != "GIF":  # 如果成功生成1张图片或者文件后缀不为GIF的多张图片
    #         result[0].save(output)
    #     elif len(result) > 1:  # 如果是动图
    #         result[0].save(output, save_all=True, append_images=result[1:],loop=1,duration=0.1, optimize=True)


    result = produce(text, img, ec, bri, cont, colourful=colr, rgba=rgba, pixelate=pixelate)
    if len(result) == 1 or output.upper()[-3:] != "GIF":  # 如果成功生成1张图片或者文件后缀不为GIF的多张图片
        result[0].save(output)
    elif len(result) > 1:  # 如果是动图
        result[0].save(output, save_all=True, append_images=result[1:], loop=1, duration=0.1, optimize=True)

main()
