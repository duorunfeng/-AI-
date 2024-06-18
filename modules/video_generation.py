import subprocess
import os

def generate_video(engine, base_path):
    # 确定dreamtalk虚拟环境的Python解释器路径
    python_env_path = "X:\\anaconda\\envs\\dreamtalk\\python.exe"  # 适用于Windows系统

    if engine == "sadtalker":
        inference_script = os.path.join(base_path, "talker", "SadTalker", "inference.py")
        audio_file = os.path.join(base_path, "system_tts", "ollama_audio.wav")
        source_image = os.path.join(base_path, "image", "image.png")
        result_dir = os.path.join(base_path, "video")

        # 更改工作目录到 SadTalker 所在目录
        os.chdir(os.path.join(base_path, "talker", "SadTalker"))

        command = f"{python_env_path} {inference_script} --driven_audio {audio_file} --source_image {source_image} --result_dir {result_dir} --still --enhancer gfpgan --preprocess resize"
    elif engine == "dreamtalker":
        inference_script = os.path.join(base_path, "talker", "dreamtalk", "inference_for_demo_video.py")
        audio_file = os.path.join(base_path, "system_tts", "ollama_audio.wav")
        style_clip_path = os.path.join(base_path, "talker", "dreamtalk", "data", "style_clip", "3DMM", "M030_front_neutral_level1_001.mat")
        pose_path = os.path.join(base_path, "talker", "dreamtalk", "data", "pose", "RichardShelby_front_neutral_level1_001.mat")
        source_image = os.path.join(base_path, "image", "image.png")

        # 更改工作目录到 dreamtalk 所在目录
        os.chdir(os.path.join(base_path, "talker", "dreamtalk"))

        command = (
            f"{python_env_path} {inference_script} --wav_path {audio_file} --style_clip_path {style_clip_path} "
            f"--pose_path {pose_path} --image_path {source_image} --cfg_scale 1.0 --max_gen_len 30 --output_name dream1"
        )
    else:
        raise ValueError("Invalid engine name provided")

    try:
        # 运行命令
        subprocess.run(command, shell=True, check=True)
        return {"message": f"{engine} model executed successfully"}
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error executing {engine} model: {str(e)}")
