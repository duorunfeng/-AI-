import torch
import os
from TTS.api import TTS

# 文本到语音的转换函数
def text_to_speech(text_content, output_directory="system_tts", output_filename='ollama_audio.wav'):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False).to(device)
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, output_filename)
    tts.tts_to_file(text=text_content, file_path=output_file_path)
    print(f"TTS处理结果已保存到: {output_file_path}")
    return output_file_path

# 文本文件转语音文件的函数
def convert_text_to_speech(text_path='system_text/ollama_result.txt', audio_dir='system_tts'):
    # 确保音频输出目录存在
    os.makedirs(audio_dir, exist_ok=True)

    # 读取文本内容
    with open(text_path, 'r') as file:
        text_content = file.read()

    # 转换文本为音频
    audio_output_path = text_to_speech(text_content, output_directory=audio_dir, output_filename='ollama_audio.wav')

    print(f"Generated audio file: {audio_output_path}")

# 调用函数进行转换
convert_text_to_speech()
