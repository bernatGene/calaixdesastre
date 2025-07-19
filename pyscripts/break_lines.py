from pathlib import Path

text = Path("./text.txt").read_text()

text = text.replace("\n", " ")

lines = []

char_count = 0
line = ""
for char in text:
    char_count += 1
    line += char
    if char_count > 35 and char == " ":
        lines.append(line)
        line = ""
        char_count = 0
    
for line in lines:
    print(len(line), line)

Path("./broken.txt").write_text("\n".join(lines))

    

