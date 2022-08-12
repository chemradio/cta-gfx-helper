from create_html_gfx import create_html
from animation_extractor import extract_png_sequence
from png_stitcher import stitch_images
from animation_configurator import create_animation_parameters
from html_server import create_server
import os
import glob

# files = glob.glob('/Users/tim/code/ae-to-html/html/html_assemblies/*')
# for f in files:
#     os.remove(f)

def create_video_gfx(order) -> str:
    """Creates a video of multiple files like Background and Foreground images,
    adds audio file if neccessary and returns path to a ready video"""

    # start the server
    create_server()
    
    # create animation parameters object
    animation_parameters = create_animation_parameters(order)

    # build html page with animation
    html_assembly_name = create_html(animation_parameters.to_object())
    html_assembly_path = f'./html/html_assemblies/{html_assembly_name}'

    # extract pngs
    extract_png_sequence(html_assembly_name)

    # stitch pngs to mp4
    png_path = f"{html_assembly_path}/png_sequence"
    ready_video_path = f"{html_assembly_path}/{order['render_filename']}"
    stitch_images(png_path, ready_video_path)

    return ready_video_path











# testing
if __name__ == "__main__":
    order = {
      "status": "success",
      "first_name": "\u0414\u0430\u043a\u0438\u043d",
      "telegram_id": 348887647,
      "chat_id": 348887647,
      "screenshots_ready": True,
      "video_ready": False,
      "start_timestamp": 1660220929.0,
      "request_type": "video_auto",
      "stage": "completed",
      "link": "https://www.gov.kz/memleket/entities/prokuror/press/news/details/410143?lang=ru",
      "animation_type": "facebook",
      "quote_enabled": True,
      "quote_text": "\u0414\u043e\u043a\u0430\u0437\u0430\u043d\u043e \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0430\u043c\u0438 \u043f\u043e\u043b\u0438\u0446\u0438\u0438 \u0441 7 \u043f\u043e 17 \u044f\u043d\u0432\u0430\u0440\u044f 2022 \u0433\u043e\u0434\u0430 \u043f\u044b\u0442\u043e\u043a \u043a 23 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0430\u043c, \u0437\u0430\u0434\u0435\u0440\u0436\u0430\u043d\u043d\u044b\u043c \u0437\u0430 \u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u0435 \u043c\u0430\u0441\u0441\u043e\u0432\u044b\u0445 \u0431\u0435\u0441\u043f\u043e\u0440\u044f\u0434\u043a\u043e\u0432 \u0432 \u0422\u0430\u043b\u0434\u044b\u043a\u043e\u0440\u0433\u0430\u043d\u0435. \u041f\u043e\u0434\u043e\u0437\u0440\u0435\u0432\u0430\u0435\u043c\u044b\u043c\u0438 \u043f\u043e \u0441\u0442\u0430\u0442\u044c\u0435 \"\u041f\u044b\u0442\u043a\u0438\" \u043f\u0440\u0438\u0437\u043d\u0430\u043d\u044b \u043f\u044f\u0442\u044c \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u043e\u0432 \u043f\u043e\u043b\u0438\u0446\u0438\u0438. \u0427\u0435\u0442\u0432\u0435\u0440\u0442\u043e\u0433\u043e \u0430\u0432\u0433\u0443\u0441\u0442\u0430 2022 \u0433\u043e\u0434\u0430 \u0443\u0433\u043e\u043b\u043e\u0432\u043d\u043e\u0435 \u0434\u0435\u043b\u043e \u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e \u0432 \u0441\u0443\u0434 \u0434\u043b\u044f \u0440\u0430\u0441\u0441\u043c\u043e\u0442\u0440\u0435\u043d\u0438\u044f \u043f\u043e \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443.",
      "quote_author_enabled": True,
      "quote_author": "\u0413\u0435\u043d\u0435\u0440\u0430\u043b\u044c\u043d\u0430\u044f \u043f\u0440\u043e\u043a\u0443\u0440\u0430\u0442\u0443\u0440\u0430 \u041a\u0430\u0437\u0430\u0445\u0441\u0442\u0430\u043d\u0430",
      "audio_enabled": True,
      "audio_path": "/Users/tim/code/cta-gfx-telegram-bot/assets/user_files//user_f2dca8685bc84fc0.mp3",
      "results_message_id": 21219,
      "render_filename": "\u0414\u0430\u043a\u0438\u043d-gfx-1660221361.mp4",
      "is_two_layer": True,
      "bg_path": "/Users/tim/code/ae-to-html/01_BG_2fd26050c5df9b57.png",
      "fg_path": "/Users/tim/code/ae-to-html/02_FG_56de5e33650775e4.png",
      "link_type": "scroll",
      "start_render_timestamp": 1660221406.116628
    }
    print(
        create_video_gfx(order)
    )
