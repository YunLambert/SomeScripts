# 艺术二维码

如果想进一步了解原理，可以参考我的[这一篇博客](https://yunlambert.github.io/2019/01/15/%E6%B7%B1%E5%BA%A6%E6%8E%A2%E7%B4%A2%E4%BA%8C%E7%BB%B4%E7%A0%81%E5%8F%8A%E5%85%B6%E5%BA%94%E7%94%A8/)

## Halftone.py

一些主要的参数如下:

```
-o 输出文件命名
-v 二维码版本[1-40]
-e 纠错方式 L M Q H中的一个
-b 调整亮度
-c 调整对比度
-C 输出有颜色
-r rgba颜色设定
=======不常用or有问题=======
-g 输入文件为gif
-m 将图片放置在正中央
-d 在-g的基础上设置duration
```

举例:

```
python Halftone.py -C -r 100 50 100 199 -o 001_out.gif 001.gif "You Found The Egg!"

python Halftone.py -C -r 65 105 225 199 -o 002_out.png 002.png https://github.com/YunLambert
    
python Halftone.py -o 003_out.gif 001.gif "You Found The Egg!"
```

其中-C 是代表有颜色输出，-r是颜色设定rgba，rgb的值可以通过这个[链接](http://tool.oschina.net/commons?type=3)去查询。
001_out.gif,002_out.png,003.gif如下:

https://github.com/YunLambert/Python_MOOC/blob/master/art_qrcode/001_out.gif

![002_out.png](https://upload-images.jianshu.io/upload_images/7154520-51de40b69443eb30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

https://github.com/YunLambert/Python_MOOC/blob/master/art_qrcode/003_out.gif

## myqr.py

是由sylnsfar大神所写的代码，可以直接跳转至此[MD说明文件](https://github.com/sylnsfar/qrcode/blob/master/README-cn.md)

## pyqart

是由7sDream大神所写的代码，可以直接跳转至此[MD说明文件](https://github.com/7sDream/pyqart/blob/master/README.zh.md)



本文及博客已同步在公众号内:

![wx.jpg](https://upload-images.jianshu.io/upload_images/7154520-531edf907587b9fd.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

