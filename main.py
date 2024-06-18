import os
import time
import shutil
import logging
import numpy as np
import soundfile as sf
import whisper
from PIL import Image, ExifTags
from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from modules.stt import transcribe_audio
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from modules.stt import start_recording
from RAG.rag_ollama import correct_text
from modules.tts import text_to_speech
from modules.video_generation import generate_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="Z:/PyCharmFire/webui/static"), name="static")
app.mount("/video", StaticFiles(directory="Z:/PyCharmFire/webui/video"), name="video")
app.mount("/system_tts", StaticFiles(directory="Z:/PyCharmFire/webui/system_tts"), name="system_tts")


templates = Jinja2Templates(directory="templates")


# 先进入哪里？
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("language.html", {"request": request})


@app.post("/api/process-text/")
async def process_text(text: str = Form(...)):
    processed_text = text[::-1]
    return {"message": "文本已处理", "original_text": text, "processed_text": processed_text}


class TextModel(BaseModel):
    text: str


@app.post("/api/process-user-text/")
async def process_user_text(text_model: TextModel):
    corrected_text = correct_text(text_model.text)
    return {"original_text": text_model.text, "corrected_text": corrected_text}


@app.post("/api/start-recording/")
async def api_start_recording():
    try:
        stream = start_recording()
        stream.start()
        return JSONResponse(content={"message": "录音已开始"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def save_file(file, directory='uploads'):
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    filepath = os.path.join(directory, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        logging.info(f"Saved file {file.filename} to {filepath}")
    return filepath


logging.basicConfig(level=logging.INFO)


# 详细打印错误信息
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


# index_en_1.html
@app.get("/index_en_1", response_class=HTMLResponse)
async def index_en_1():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_1.html"
    return FileResponse(file_path)

# index_en_2.html
@app.get("/index_en_2", response_class=HTMLResponse)
async def index_en_2():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_2.html"
    return FileResponse(file_path)

# index_en_3.html
@app.get("/index_en_3", response_class=HTMLResponse)
async def index_en_3():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_3.html"
    return FileResponse(file_path)

# index_en_4.html
@app.get("/index_en_4", response_class=HTMLResponse)
async def index_en_4():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_4.html"
    return FileResponse(file_path)

# index_en_5.html
@app.get("/index_en_5", response_class=HTMLResponse)
async def index_en_5():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_5.html"
    return FileResponse(file_path)

# index_en_6.html
@app.get("/index_en_6", response_class=HTMLResponse)
async def index_en_6():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_6.html"
    return FileResponse(file_path)

# index_en_7.html
@app.get("/index_en_7", response_class=HTMLResponse)
async def index_en_7():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_7.html"
    return FileResponse(file_path)

# index_en_8.html
@app.get("/index_en_8", response_class=HTMLResponse)
async def index_en_8():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_8.html"
    return FileResponse(file_path)

# index_en_9.html
@app.get("/index_en_9", response_class=HTMLResponse)
async def index_en_9():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_9.html"
    return FileResponse(file_path)

# index_en_10.html
@app.get("/index_en_10", response_class=HTMLResponse)
async def index_en_10():
    file_path = "Z:/PyCharmFire/webui/templates/index_en_10.html"
    return FileResponse(file_path)

# language.html界面
@app.get("/language", response_class=HTMLResponse)
async def serve_language():
    file_path = "Z:/PyCharmFire/webui/templates/language.html"
    return FileResponse(file_path)


# language_chinese.html界面
@app.get("/language_chinese", response_class=HTMLResponse)
async def serve_language_chinese():
    file_path = "Z:/PyCharmFire/webui/templates/language_chinese.html"
    return FileResponse(file_path)


# language_korean.html界面
@app.get("/language_korean", response_class=HTMLResponse)
async def serve_language_korean():
    file_path = "Z:/PyCharmFire/webui/templates/language_korean.html"
    return FileResponse(file_path)


# language_english.html界面
@app.get("/language_english", response_class=HTMLResponse)
async def serve_language_english():
    file_path = "Z:/PyCharmFire/webui/templates/language_english.html"
    return FileResponse(file_path)


# 添加路由来服务 HTML 页面
@app.get("/photo-upload.html")
async def serve_photo_upload():
    # 使用绝对路径来确保文件可以被正确找到
    file_path = "Z:/PyCharmFire/webui/templates/photo-upload.html"
    return FileResponse(file_path)


# 添加路由来服务 HTML 页面
@app.get("/talker.html")
async def serve_talker():
    # 使用绝对路径来确保文件可以被正确找到
    file_path = "Z:/PyCharmFire/webui/templates/talker.html"
    return FileResponse(file_path)


# 选择引擎
user_engine_selection = {}  # 全局变量存储用户选择


@app.post("/api/select-engine")
async def select_engine(request: Request):
    data = await request.json()
    engine = data.get("engine")

    if engine not in ["sadtalker", "dreamtalker","voice"]:
        raise HTTPException(status_code=400, detail="Invalid engine selection")

    # 保存用户选择到全局变量，或者其他持久化的地方
    user_engine_selection['selected'] = engine
    return JSONResponse({"message": f"Engine {engine} selected successfully"})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
# 网页音频
@app.post("/api/process-audio/")
async def process_audio(request: Request):
    # 此处省略实际的音频处理逻辑
    # 假设处理后的音频文件名是 ollama_audio.wav
    audio_filename = "ollama_audio.wav"
    return JSONResponse(status_code=200, content={"audio_url": f"/system_tts/{audio_filename}"})


# upload-photo接收文件
@app.post("/api/upload-photo")
async def upload_photo(photo: UploadFile = File(...)):
    new_filename = "image.png"  # 新文件名固定为 image.png
    file_location = os.path.join('Z:/PyCharmFire/webui/image', new_filename)  # 设置文件完整路径

    try:
        # 确保目标目录存在，如果不存在则创建
        os.makedirs(os.path.dirname(file_location), exist_ok=True)

        # 检查文件类型是否符合预期，假设只接受图片文件
        if not photo.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Invalid file type. Only image files are accepted.")

        # 将上传的文件转换为图片
        image = Image.open(photo.file)

        # 处理EXIF旋转信息
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image._getexif().items())
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass

        # 保存图片为 PNG
        image.save(file_location, 'PNG')

        # 返回上传成功的消息
        return JSONResponse(status_code=200,
                            content={"message": "Photo uploaded successfully", "filename": new_filename})

    except Exception as e:
        # 记录异常到你的日志系统（如果有）
        return JSONResponse(status_code=500, content={"detail": str(e)})


@app.post("/api/stop-recording/")
async def api_stop_recording(request: Request):
    logging.info("Received stop recording request")
    try:
        form_data = await request.form()
        file = form_data.get('file')
        if not file or file.filename == '':
            logging.error("No file uploaded(99)")
            return JSONResponse(status_code=118, content={"message": "No file uploaded"})
        # 保存文件
        audio_filename = save_file(file)
        logging.info(f"File saved: {audio_filename}")

        # 进行音频转录
        stt_start_time = time.time()
        transcribed_text, saved_path = transcribe_audio(os.path.basename(audio_filename))
        logging.info(f"Transcription successful: {saved_path}")
        stt_end_time = time.time()
        stt_processing_time = stt_end_time - stt_start_time

        # 对转录后的文本进行处理
        llm_start_time = time.time()
        corrected_text = correct_text(transcribed_text)
        logging.info(f"Text correction completed: {corrected_text}")
        llm_end_time = time.time()
        llm_processing_time = llm_end_time - llm_start_time

        # 生成TTS音频
        # tts_start_time = time.time()
        tts_audio_path = text_to_speech(corrected_text)
        logging.info(f"TTS audio generated: {tts_audio_path}")
        # tts_end_time = time.time()
        # tts_processing_time = tts_end_time - tts_start_time

        # 如果选择的是"voice"引擎，直接返回音频路径，不生成视频
        engine = user_engine_selection.get('selected', 'voice')  # 使用全局变量的用户选择
        if engine == "voice":
            relative_audio_path = tts_audio_path.replace("Z:/PyCharmFire/webui/", "")
            return JSONResponse(status_code=200, content={
                "message": "Audio processed successfully",
                "audio_url": f"/{relative_audio_path}",
                "transcribed_text": transcribed_text,  # 原始文本
                "corrected_text": corrected_text

            })

        # 生成视频
        video_output_directory = "Z:\\PyCharmFire\\webui\\video"
        video_filename = "output_video.mp4"
        video_file_path = os.path.join(video_output_directory, video_filename)

        # 检查并删除已存在的旧文件
        if os.path.exists(video_file_path):
            os.remove(video_file_path)
            logging.info("Old video file removed.")

        # 确认文件已删除
        if not os.path.exists(video_file_path):
            logging.info("Confirmed: Old video file successfully deleted.")
        else:
            logging.error("Error: Old video file still exists.")

        # 生成新视频文件的逻辑
        video_start_time = time.time()
        engine = user_engine_selection.get('selected', 'voice')  # 使用全局变量的用户选择
        result = generate_video(engine, "Z:/PyCharmFire/webui")
        logging.info(f"Video generation result: {result['message']}")
        video_end_time = time.time()
        video_processing_time = video_end_time - video_start_time
        logging.info("Video generated successfully")

        # 检查视频文件是否存在
        if os.path.exists(video_file_path):
            logging.info("Video file is ready and exists.")
            video_url = f"/video/output_video.mp4"
            response_content = {
                "message": "File processed successfully",
                "stt_processing_time": stt_processing_time,
                "llm_processing_time": llm_processing_time,
                # "tts_processing_time": tts_processing_time,
                "video_processing_time": video_processing_time,
                "filename": audio_filename,
                "transcribed_text": transcribed_text,
                "transcript_file": saved_path,
                "corrected_text": corrected_text,
                "tts_audio_path": tts_audio_path,
                "video_path": video_file_path,
                "video_url": video_url

            }

            logging.info(f"Returning JSON response: {response_content}")
            return JSONResponse(content=response_content)

        else:
            logging.error("Video file does not exist.")
            return JSONResponse(status_code=404, content={"message": "Video file not found"})
    except Exception as e:
        logging.error(f"Error processing the audio file: {str(e)}")
        return JSONResponse(status_code=502, content={"message": f"Error processing the audio file: {str(e)}"})


# Ensure the directory for saving audio exists
os.makedirs('uploads', exist_ok=True)

# Global variable for storing audio data
audio_data = np.empty((0, 2), dtype='float64')


def stop_recording_and_transcribe(filename, model_name="base", sample_rate=44100):
    global audio_data
    sf.write(filename, audio_data, samplerate=sample_rate)
    audio_data = np.empty((0, 2), dtype='float64')
    model = whisper.load_model(model_name)
    result = model.transcribe(filename)
    text_dir = "text"
    os.makedirs(text_dir, exist_ok=True)
    text_filename = os.path.splitext(filename)[0] + ".txt"
    text_filepath = os.path.join(text_dir, text_filename)
    with open(text_filepath, "w") as f:
        f.write(result['text'])
    return result['text'], text_filepath



