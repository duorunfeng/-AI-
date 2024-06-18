import traceback
import sounddevice as sd
import numpy as np
import soundfile as sf
import whisper
import os
import logging  # 确保引入日志库

# 全局变量用于存储音频数据
audio_data = None

def start_recording(sample_rate=44100, channels=2):
    global audio_data
    audio_data = np.empty((0, channels), dtype='float64')
    def callback(indata, frames, time, status):
        global audio_data
        audio_data = np.append(audio_data, indata.copy(), axis=0)

    stream = sd.InputStream(callback=callback, samplerate=sample_rate, channels=channels)
    stream.start()
    return stream

def stop_recording(stream):
    global audio_data
    stream.stop()
    return audio_data

def stop_recording_and_transcribe(audio_filename, model_name="base", sample_rate=44100):
    global audio_data
    uploads_dir = 'uploads'
    os.makedirs(uploads_dir, exist_ok=True)
    audio_path = os.path.join(uploads_dir, audio_filename)
    sf.write(audio_path, audio_data, samplerate=sample_rate)
    audio_data = np.empty((0, 2), dtype='float64')
    return transcribe_audio(audio_path, text_dir='text')

def transcribe_audio(audio_filename, text_dir='text'):
    uploads_dir = 'uploads'
    audio_path = os.path.join(uploads_dir, audio_filename)
    os.makedirs(text_dir, exist_ok=True)
    text_filename = os.path.splitext(os.path.basename(audio_filename))[0] + '.txt'
    text_path = os.path.join(text_dir, text_filename)
    try:
        logging.info("Loading Whisper model...")
        model = whisper.load_model("medium")
        logging.info("Model loaded, transcribing audio...")
        result = model.transcribe(audio_path)
        with open(text_path, 'w') as file:
            file.write(result['text'])
        logging.info(f"Transcription successful: {text_path}")
        return result['text'], text_path
    except FileNotFoundError as e:
        logging.error(f"File not found: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {str(e)}")
        raise

def handle_transcription(audio_filename='audio.wav'):
    transcribed_text, path = stop_recording_and_transcribe(audio_filename)
    logging.info(f"Transcription saved to {path}: {transcribed_text}")
