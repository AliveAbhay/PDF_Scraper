input_file_path = 'output.txt'

with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = [line.strip() if not line.startswith('[') else '\n' + line.strip() for line in file]

formatted_text = ''.join(lines)

with open(input_file_path, 'w', encoding='utf-8') as file:
    file.write(formatted_text)
    print('Text rearrangement Done')