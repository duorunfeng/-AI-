# rag.py
import sys
from text_processor import process_input

def main(input_text):
    try:
        # 调用 text_processor 处理输入
        corrected_text = process_input(input_text)
        if not corrected_text:  # 找不到匹配内容
            print("")
        else:
            print(corrected_text)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    input_text = sys.argv[1]
    main(input_text)
