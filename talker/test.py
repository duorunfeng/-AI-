import argparse
import os
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script for running different models.")
    parser.add_argument("--image", type=str, help="Path to the image.")
    parser.add_argument("--audio", type=str, help="Path to the audio.")
    parser.add_argument("--model", type=str, choices=["sadtalker", "dreamtalk"], help="Choose model: sadtalk or dreamtalk")
    args = parser.parse_args()

    base_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录的绝对路径

    if args.model == "sadtalker":
        os.chdir(os.path.join(base_path, 'SadTalker'))
        # 运行sadtalk模型的命令
        command = f"python {os.path.join(base_path, 'SadTalker', 'inference.py')} --driven_audio {args.audio} --source_image {args.image} --result_dir ./examples/animation --still --preprocess resize --enhancer gfpgan" #
    elif args.model == "dreamtalk":
        os.chdir(os.path.join(base_path, 'dreamtalk'))
        # 运行dreamtalk模型的命令
        command = f"python {os.path.join(base_path, 'dreamtalk', 'inference_for_demo_video.py')} --wav_path {args.audio} --style_clip_path data/style_clip/3DMM/M030_front_neutral_level1_001.mat --pose_path data/pose/RichardShelby_front_neutral_level1_001.mat --image_path {args.image} --cfg_scale 1.0 --max_gen_len 30 --output_name dream1"
    else:
        print("Invalid model choice. Choose either sadtalk or dreamtalk.")
        exit(1)

    # 运行命令
    import subprocess
    start_time = time.time()
    subprocess.run(command.split())
    end_time = time.time()
    print(end_time - start_time)
