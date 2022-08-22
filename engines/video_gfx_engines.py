import interlinks
import os
import json
import time
import threading
import PIL
# from engines.telegram_bot import bot
from database.db import db_handler
from engines.sender_engine import send_ready_orders, send_video_order
from engines.video_gfx_html.video_wizard import create_video_gfx
from os_scripts.os_script_handler import os_script


import logging
logger_gfx = logging.getLogger(__name__)
logger_gfx.setLevel(logging.DEBUG)
logging_gfx_formatter = logging.Formatter('%(asctime)s: %(name)s: %(message)s')
logging_gfx_file_handler = logging.FileHandler(f'./logs/{__name__}.log', mode='w+')
logging_gfx_file_handler.setLevel(logging.DEBUG)
logging_gfx_file_handler.setFormatter(logging_gfx_formatter)
logging_gfx_stream_handler = logging.StreamHandler()
logging_gfx_stream_handler.setFormatter(logging_gfx_formatter)
logger_gfx.addHandler(logging_gfx_file_handler)
logger_gfx.addHandler(logging_gfx_stream_handler)




def render_video_orders():
    logger_gfx.debug("THREAD: render_video_orders accessed")
    def renderer():
        # time.sleep(30)  # initial startup to allow screenshots to be captured
        while db_handler.get_unrendered_orders():
            logger_gfx.debug("GFX Renderer started")
            time.sleep(1)
            order = db_handler.get_unrendered_orders()[0]

            # launch html-based animation creator
            create_video_gfx(order=order)

            db_handler.update_doc_db_parameters(doc_id=order.doc_id, parameters={'stage':'sending', 'start_render_timestamp': time.time()})
            logger_gfx.debug("GFX Renderer accessed SENDER Engine")
            send_video_order(order)
            
            time.sleep(10)
        return

    for thread in threading.enumerate():
        if 'render_video_orders_thread' in thread.name:
            logger_gfx.debug("THREAD: render_video_orders already runnung")
            return False

    render_video_orders_thread = threading.Thread(target=renderer, args=(), name='render_video_orders_thread')
    render_video_orders_thread.start()
    logger_gfx.debug("THREAD: render_video_orders started")
    return True


def create_uber_parameters(query):
    logger_gfx.debug("UBERPARAMETERS: Creation started")
    bg_path = query['bg_path']
    fg_path = query.get('fg_path', False)
    isTwoLayer = query.get('is_two_layer', False)
    
    if query['request_type'] == 'video_auto':
        if isTwoLayer:
            fg_image = PIL.Image.open(fg_path)
            width, height = fg_image.size
            if width/height < .7:
                animationType = 'facebook'
            else:
                animationType = query['link_type']
        else:
            animationType = query['link_type']

    elif query['request_type'] == 'video_files':
        if fg_path:
            animationType = query['fg_animation_type']
        else:
            animationType = query['bg_animation_type']

    

    quoteEnabled = query["quote_enabled"]
    quoteText = query["quote_text"] if quoteEnabled else ''
    quoteAuthorEnabled = query["quote_author_enabled"] if quoteEnabled else False
    quoteAuthor = query["quote_author"] if quoteAuthorEnabled else ''

    hasAudio = True if query['audio_enabled'] else False
    audio_path = query['audio_path'] if hasAudio else ''
    
    backgroundAnimationType = "scroll" if query['request_type'] == 'video_auto' else query['bg_animation_type']
    roundCorners = True if query['request_type'] == 'video_auto' else query.get('round_corners_enabled', False)
    
    biggerPost = False
    staticPost = True if quoteEnabled else False
    compSlideIn = False
    motionBlur = True

    resolution = [1920, 1080]
    descriptor = query['render_filename']
    outputPath = interlinks.render_output_path
    fontFamily = "Roboto Condensed"

    ccVersion = 2020
    isAutoDoable = True
    saveProject = False

    logger_gfx.debug("UBERPARAMETERS: Dumping json")
    python_parameters = f"""
        backGroundImage:new File ({json.dumps(bg_path)}),
        foregroundImage:new File ({json.dumps(fg_path)}),
        isTwoLayer:{json.dumps(isTwoLayer)},
        audioFile:new File ({json.dumps(audio_path)}),
        hasAudio:{json.dumps(hasAudio)},
        animationType:{json.dumps(animationType)},
        backgroundAnimationType:{json.dumps(backgroundAnimationType)},
        roundCorners:{json.dumps(roundCorners)},
        biggerPost:{json.dumps(biggerPost)},
        staticPost:{json.dumps(staticPost)},
        compSlideIn:{json.dumps(compSlideIn)},
        motionBlur:{json.dumps(motionBlur)},
        quoteEnabled:{json.dumps(quoteEnabled)},
        quoteAuthor:{json.dumps(quoteAuthor)},
        quoteText:{json.dumps(quoteText)},
        resolution: {resolution},
        descriptor:{json.dumps(descriptor)},
        outputPath:{json.dumps(outputPath)},
        fontFamily:{json.dumps(fontFamily)},
        ccVersion:{ccVersion},
        isAutoDoable:{json.dumps(isAutoDoable)},
        saveProject:{json.dumps(saveProject)},
    """

    with open(interlinks.path_to_uber_parameters, 'w') as parameters_file:
        parameters_file.write('uberParameters = {')
        parameters_file.write(python_parameters)
        parameters_file.write('}')

    logger_gfx.debug("UBERPARAMETERS: Done writing. Runnung CT_QUOTER script")

    os_script.launcher()

    # revert parameters.jsx to empty state
    time.sleep(10)

    python_parameters = f"""
        backGroundImage: '',
        foregroundImage: '',
        isTwoLayer: '',
        audioFile: '',
        hasAudio: '',
        animationType: '',
        backgroundAnimationType: '',
        roundCorners: '',
        biggerPost: '',
        staticPost: '',
        compSlideIn: '',
        motionBlur: '',
        quoteEnabled: '',
        quoteAuthor: '',
        quoteText: '',
        resolution: '',
        descriptor: '',
        outputPath: '',
        fontFamily: '',
        ccVersion: '',
        isAutoDoable: '',
        saveProject: '',
    """

    with open(interlinks.path_to_uber_parameters, 'w') as parameters_file:
        parameters_file.write('uberParameters = {')
        parameters_file.write(python_parameters)
        parameters_file.write('}')