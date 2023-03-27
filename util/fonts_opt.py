import os
import sys
from pathlib import Path

import wget
from rich.console import Console

ROOT_PATH = sys.path[0]  

fonts_list = ["SimSun.ttf", "TimesNewRoman.ttf", "malgun.ttf"]  
fonts_suffix = ["ttc", "ttf", "otf"]  

data_url_dict = {
    "SimSun.ttf": "https://gitee.com/CV_Lab/gradio_yolov5_det/attach_files/1053539/download/SimSun.ttf",
    "TimesNewRoman.ttf": "https://gitee.com/CV_Lab/gradio_yolov5_det/attach_files/1053537/download/TimesNewRoman.ttf",
    "malgun.ttf": "https://gitee.com/CV_Lab/gradio_yolov5_det/attach_files/1053538/download/malgun.ttf",}

console = Console()


# 创建字体库
def add_fronts(font_diff):

    global font_name

    for k, v in data_url_dict.items():
        if k in font_diff:
            font_name = v.split("/")[-1] 
            Path(f"{ROOT_PATH}/fonts").mkdir(parents=True, exist_ok=True) 

            file_path = f"{ROOT_PATH}/fonts/{font_name}"

            try:
                wget.download(v, file_path)
            except Exception as e:
                print(e)
                sys.exit()
            else:
                print()



def is_fonts(fonts_dir):
    if os.path.isdir(fonts_dir):

        f_list = os.listdir(fonts_dir)  

        font_diff = list(set(fonts_list).difference(set(f_list)))

        if font_diff != []:
            add_fronts(font_diff)
    else:
        add_fronts(fonts_list)
