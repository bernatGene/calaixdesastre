from pathlib import Path
import argparse
import glob


def add_white_space(path: Path):
    text = path.read_text()
    new_text = []
    for line in text.splitlines():
        line = line.rstrip() + '  '
        new_text.append(line)
    path.write_text("\n".join(new_text))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input files")
    parser.add_argument("input", type=str, help="File or glob")
    args = parser.parse_args()
    input_files = glob.glob(args.input)
    for file in input_files:
        print("Reading file", file)
        add_white_space(Path(file))

   


