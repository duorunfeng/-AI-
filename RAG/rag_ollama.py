import os
import subprocess
from ollama import chat

def correct_text(input_text, target_directory="system_text", result_filename='ollama_result.txt'):
    try:
        result = subprocess.run(
            ['X:\\anaconda\\envs\\rag\\python', 'Z:\\PyCharmFire\\webui\\RAG\\rag.py', input_text],
            check=True,
            capture_output=True,
            text=True
        )
        corrected_text = result.stdout.strip()

        if not corrected_text:  # 如果 corrected_text 为空，执行备用的文本处理逻辑
            corrected_text = backup_correct_text(input_text, target_directory, result_filename)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while calling rag.py: {e.stderr}")
        corrected_text = backup_correct_text(input_text, target_directory, result_filename)

    # 确保目标文件夹存在
    os.makedirs(target_directory, exist_ok=True)
    # 定义完整的文件路径
    full_path = os.path.join(target_directory, result_filename)
    # 保存文本到文件
    with open(full_path, "w") as file:
        file.write(corrected_text)

    return corrected_text

def backup_correct_text(input_text, target_directory="system_text", result_filename='ollama_result.txt'):
    messages = [
        {
            'role': 'user',
            'content': "Correct only this sentence's grammatical errors and return(Parentheses cannot be added): " + input_text,
        },
    ]
    corrected_text = ""
    for part in chat('llama3_for:latest', messages=messages, stream=True):
        corrected_text += part['message']['content']

    # 确保目标文件夹存在
    os.makedirs(target_directory, exist_ok=True)
    # 定义完整的文件路径
    full_path = os.path.join(target_directory, result_filename)
    # 保存文本到文件
    with open(full_path, "w") as file:
        file.write(corrected_text)
    return corrected_text
