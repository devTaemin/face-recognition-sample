# Face Recognition Hub
# author: Zeng Yifu（曾逸夫） 감사하무니다
# creation time: 2022-07-28
# email: zyfiy1314@163.com
# project homepage: https://gitee.com/CV_Lab/face-recognition-hub

########################### Modules ###########################
import os
import sys
from pathlib import Path

import face_recognition
import gradio as gr
from PIL import Image, ImageDraw, ImageFont

from util.fonts_opt import is_fonts
###############################################################

##### sys.path
##### 모듈을 import할 때 찾아야할 경로들을 저장해둔 list
ROOT_PATH = sys.path[0]

IMG_PATH_Test = "./img_examples/unknown"

FONTSIZE = 15

OCR_TR_DESCRIPTION = '''
# Face Recognition
<div id="content_align">https://github.com/ageitgey/face_recognition demo</div>
'''

def str_intercept(img_path):
    img_path_ = img_path[::-1]
    point_index = 0  
    slash_index = 0  

    flag_pi = 0
    flag_si = 0

    for i in range(len(img_path_)):
        if (img_path_[i] == "." and flag_pi == 0):
            point_index = i
            flag_pi = 1

        if (img_path_[i] == "/" and flag_si == 0):
            slash_index = i
            flag_si = 1

    point_index = len(img_path) - 1 - point_index
    slash_index = len(img_path) - 1 - slash_index

    return point_index, slash_index



def face_entry(img_path, name_text):
    if img_path == "" or name_text == "" or img_path is None or name_text is None:
        return None, None, None

    point_index, slash_index = str_intercept(img_path)
    img_renamePath = f"{img_path[:slash_index+1]}{name_text}{img_path[point_index:]}"
    os.rename(img_path, img_renamePath)
    img_ = Image.open(img_renamePath)
    print(img_renamePath)

    return img_, img_renamePath, name_text


def set_example_image(example: list):
    return gr.Image.update(value=example[0])


def face_recognition_(img_srcPath, img_tagPath, img_personName):
    print("face_recognition_ start....\n")
    print("img_srcPath: " + img_srcPath +"\n")
    print("image_tagPath: " + img_tagPath + "\n")
    print("img_personName: " + img_personName + "\n")
    
    if img_tagPath == "" or img_tagPath is None:
        return None

    # 얼굴 DB
    image_of_person = face_recognition.load_image_file(img_srcPath)
    person_face_encoding = face_recognition.face_encodings(image_of_person)[0]

    known_face_encodings = [person_face_encoding,]

    known_face_names = [img_personName,]

    test_image = face_recognition.load_image_file(img_tagPath)
    


    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    pil_image = Image.fromarray(test_image)
    img_pil = ImageDraw.Draw(pil_image)
    textFont = ImageFont.truetype(str(f"{ROOT_PATH}/fonts/SimSun.ttf"), size=FONTSIZE)
    
    #     ymin, xmax, ymax, xmin
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown Person"

        if True in matches:
            first_matches_index = matches.index(True)
            name = known_face_names[first_matches_index]

        img_pil.rectangle([left, top, right, bottom], fill=None, outline=(255, 228, 181), width=2)  
        text_w, text_h = textFont.getsize(name)  

        img_pil.rectangle(
            (left, top, left + text_w, top + text_h),
            fill=(255, 255, 255),
            outline=(255, 255, 255),
        )

        img_pil.multiline_text(
            (left, top),
            name,
            fill=(0, 0, 0),
            font=textFont,
            align="center",
        )

    del img_pil
    return pil_image


def main():
    # 폰트 설정
    is_fonts(f"{ROOT_PATH}/fonts") 

    with gr.Blocks(css='style.css') as demo:
        gr.Markdown(OCR_TR_DESCRIPTION)

        with gr.Row():
            gr.Markdown("### Step 01: Face Entry")
            
            
        with gr.Row():
            ##### 입력 부분 ###########################################
            with gr.Column():
                with gr.Row():
                    # 학습을 위해 입력하는 이미지
                    input_img = gr.Image(image_mode="RGB", source="upload", type="filepath", label="face entry")
                with gr.Row():
                    # 학습을 위해 입력하는 이미지의 이름
                    input_name = gr.Textbox(label="Name")
                with gr.Row():
                    # inputs = [ input_img, input_name ]
                    btn = gr.Button(value="Entry")
            ##########################################################

            # 보여주는 코드 ###########################################
            with gr.Column():
                with gr.Row():
                    output_ = gr.Image(image_mode="RGB", source="upload", type="pil", label="entry image")
                    input_srcImg = gr.Variable(value="")
                    input_srcName = gr.Variable(value="")
            ##########################################################        
            
                    
                    
        with gr.Row():
            ##### 테스트 목록 #########################################
            example_list = [["./img_examples/known/ChengLong.jpg", "成龙"],
                            ["./img_examples/known/VinDiesel.jpg", "VinDiesel"],
                            ["./img_examples/known/JasonStatham.jpg", "JasonStatham"],
                            ["./img_examples/known/ZhenZidan.jpg", "甄子丹"]]
            gr.Examples(example_list,
                        [input_img, input_name],
                        output_,
                        set_example_image,
                        cache_examples=False)
            ##########################################################


        with gr.Row():
                gr.Markdown("### Step 02: Face Test")
                
                
        with gr.Row():
            
            ##### 테스트 입력 ###############################################
            with gr.Column():
                with gr.Row():
                    input_img_test = gr.Image(image_mode="RGB", source="upload", type="filepath", label="test image")
                with gr.Row():
                    btn_test = gr.Button(value="Test")
                with gr.Row():
                    paths = sorted(Path(IMG_PATH_Test).rglob('*.jpg'))
                    example_images_test = gr.Dataset(components=[input_img],
                                                     samples=[[path.as_posix()] for path in paths])
            ################################################################


            ##### 결과 #####################################################
            with gr.Column():
                with gr.Row():
                    output_test = gr.Image(image_mode="RGB", source="upload", type="pil", label="identify image")
            ################################################################

        btn.click(fn=face_entry, inputs=[input_img, input_name], outputs=[output_, input_srcImg, input_srcName])

        btn_test.click(fn=face_recognition_,
                       inputs=[input_srcImg, input_img_test, input_srcName],
                       outputs=[output_test])
        
        example_images_test.click(fn=set_example_image, 
                                  inputs=[example_images_test,], 
                                  outputs=[input_img_test,])

        return demo


if __name__ == "__main__":
    demo = main()
    demo.launch(inbrowser=True)