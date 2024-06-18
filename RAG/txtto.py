import re

def extract_dialogues_from_txt(txt_paths):
    dialogues = []
    for txt_path in txt_paths:
        with open(txt_path, 'r', encoding='utf-8') as file:
            text = file.read()
            dialogues.extend(extract_dialogues_from_text(text))
    return dialogues

def extract_dialogues_from_text(text):
    # Find all content between "Dialogue" and "Vocabulary"
    dialogue_sections = re.findall(r'Dialogue(.*?)Vocabulary', text, re.DOTALL)
    all_dialogues = []

    for section in dialogue_sections:
        # Remove newline characters within the section
        section = re.sub(r'\n+', ' ', section).strip()

        # Split into individual dialogues
        dialogue_lines = re.split(r'\b[A-Z][a-z]*\s*:\s*', section)[1:]
        speakers = ['Sam', 'Kathy']

        for i, line in enumerate(dialogue_lines):
            if line.strip():
                speaker = speakers[i % 2]
                all_dialogues.append(f"{speaker}: {line.strip()}")

    return all_dialogues

def save_dialogues_to_file(dialogues, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for dialogue in dialogues:
            file.write(dialogue + '\n')

# Load and process TXT documents
txt_paths = ['Advanced English Conversations.txt']
dialogues = extract_dialogues_from_txt(txt_paths)

# Save extracted and formatted dialogues to a text file
output_path = 'formatted_dialogues.txt'
save_dialogues_to_file(dialogues, output_path)

print(f"Dialogues have been extracted and saved to {output_path}")
