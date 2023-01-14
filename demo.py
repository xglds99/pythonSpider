import os
import numpy as np
import tkinter as tk
from tqdm import tqdm
from time import sleep
from shutil import rmtree
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

SAMPLE_RATE = 0.4
OUT_FILE_NAME = "out"

# 获取当前路径
now_path = os.getcwd()


def main():
    """主函数"""
    input("*** 注意：过程中会创建许多图片或文件夹，请不要乱动或删除！*** （回车继续...） ")

    # 打开视屏路径
    try:
        filepath = get_video()
    except FileExistsError as k:
        print(k)
        sleep(2)
        return

    print("开始转换。。。")

    # 视频转换为图片
    video_to_photos(filepath)

    # 如果文件夹中含有其他音乐则删除
    now_music = [f for f in os.listdir(now_path) if f.split(".")[-1] == "mp3"]
    for m in now_music:
        os.remove(now_path + "/" + m)

    # 获取视频中的音乐
    get_music(filepath)

    # 获取当前文件夹下的所有图片文件
    photos = [f for f in os.listdir(now_path) if f.split(".")[-1] == "jpg"]

    # 获取当前文件夹下的音乐
    music_list = [f for f in os.listdir(now_path) if f.split(".")[-1] == "mp3"]
    if music_list:
        music = music_list[0]
    else:
        music = None

    # 如果没有out文件夹，则创建文件夹
    if not os.path.exists(OUT_FILE_NAME):
        os.mkdir(OUT_FILE_NAME)

    # 图片转字符图像
    print("\n转换中，过程中请勿关闭，请稍等...")
    for p in tqdm(photos):
        ascii_art(now_path + "/" + p, p.split(".")[0])

    # # 字符图像转视屏
    photos_to_video()

    # 如果当前文件夹中含有提取的音乐则将视频、音乐合并
    # 然后删除音乐
    if music:
        music_join_video()
        os.remove(now_path + "/" + music)

    # 删除所有图片保留视屏
    print("\n正在清理缓存，请稍等...")
    for p in photos:
        os.remove(now_path + "/" + p)
    os.remove(now_path + "/" + OUT_FILE_NAME + ".mp4")
    rmtree("./%s" % OUT_FILE_NAME, True)

    print("转换完成，请在output.mp4中查看转换的视屏！")
    sleep(2.3)


def ascii_art(file, save_name):
    """图片转字符图"""

    # 打开图片
    im = Image.open(file)

    # 调整图片亮度
    brightness = 2  # 增强亮度的值
    enh_bri = ImageEnhance.Brightness(im)
    im = enh_bri.enhance(brightness)

    # 保存的路径
    save_path = "%s/%s/%s%s" % (now_path, OUT_FILE_NAME, save_name, ".png")

    # 计算字母长宽比
    font = ImageFont.load_default()
    # font = ImageFont.truetype("SourceCodePro-Bold.ttf", size=12)
    aspect_ratio = font.getsize("x")[0] / font.getsize("x")[1]
    new_im_size = np.array(
        [im.size[0] * SAMPLE_RATE, im.size[1] * SAMPLE_RATE * aspect_ratio]
    ).astype(int)

    # 调整图像
    im = im.resize(new_im_size)

    # 判断是否为纯色图片，如果为纯色图片调整图像大小不进行字符处理
    r, g, b = im.getextrema()
    if r[0] == r[1] and g[0] == g[1] and b[0] == b[1]:
        letter_size = font.getsize("x")
        im_out_size = new_im_size * letter_size
        im_out = Image.new("RGB", tuple(im_out_size), im.getcolors()[0][1])
        im_out.save(save_path)
        return

    # 保留一个图像的副本以进行颜色采样
    im_color = np.array(im)

    # 转换为灰度的图像
    im = im.convert("L")

    # 转换为numpy数组以进行图像处理
    im = np.array(im)

    # 以升序定义将形成最终ascii的所有符号
    symbols = np.array(list(" .-vM"))

    # 规范化的最小值和最大值到 [0, max_symbol_index)
    im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

    # 生成ascii样品
    ascii = symbols[im.astype(int)]

    # 创建一个用于绘制ascii文本的输出图像
    letter_size = font.getsize("x")
    im_out_size = new_im_size * letter_size
    bg_color = "black"
    im_out = Image.new("RGB", tuple(im_out_size), bg_color)
    draw = ImageDraw.Draw(im_out)

    # 绘制文本
    y = 0
    for i, line in enumerate(ascii):
        for j, ch in enumerate(line):
            color = tuple(im_color[i, j])  # 来自原始图像的样本颜色
            draw.text((letter_size[0] * j, y), ch[0], fill=color, font=font)
        y += letter_size[1]  # 按字母的高度增加y

    # 保存成图像文件
    im_out.save(save_path)


def get_video():
    """打开视屏路径"""
    print("请您选择要转换的视屏")

    # 打开选择文件对话框
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()  # 获得选择好的文件

    file_extension = os.path.splitext(filepath)[1]

    # 如果不在格式内则报错
    if file_extension not in [".mp4", ".flv", ".avi", ".mpg", ".wmv"]:
        raise FileExistsError("目前只支持mp4, flv, avi, mpg, wmv视频格式")

    return filepath


def video_to_photos(filepath):
    """视频转换为图片"""
    # 调用ffmpeg命令实现视屏转为图片 fps=25
    command = "{}/tool/ffmpeg -i {} -r 25 -f image2 image-%1d.jpg".format(now_path, filepath)
    os.system(command)


def photos_to_video():
    """图像转视屏"""
    # 调用ffmpeg命令实现图片转为视屏
    command = "{0}/tool/ffmpeg -i {0}/{1}/image-%1d.png out.mp4".format(now_path, OUT_FILE_NAME)
    os.system(command)


def get_music(filepath):
    """获取视频中的音乐"""
    # 调用ffmpeg命令获取视频中的音乐
    command = "{}/tool/ffmpeg -i {} -f mp3 {}.mp3".format(now_path, filepath, OUT_FILE_NAME)
    os.system(command)


def music_join_video():
    """视频、音乐合并"""
    # 调用ffmpeg命令获取视频中的音乐
    command = "{0}/tool/ffmpeg -i {1}.mp3 -i {0}/out.mp4 {1}put.mp4".format(now_path, OUT_FILE_NAME)
    os.system(command)


if __name__ == "__main__":
    main()
