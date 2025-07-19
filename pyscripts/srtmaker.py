from pathlib import Path
import asyncio
import sys
from mediaplayer import MediaPlayer


async def ainput(string: str) -> str:
    await asyncio.to_thread(sys.stdout.write, f"{string} ")
    return await asyncio.to_thread(sys.stdin.readline)


class SubBlock:
    def __init__(self, index, start, end, text) -> None:
        self.index = index
        self.start = start
        self.end = end
        self.text = text

    def __repr__(self) -> str:
        return f"""{self.index}
{self.start} --> {self.end}
{self.text}

"""


async def interact():
    file = Path("./audiovideo.mp3")
    broken = Path("./broken.txt").read_text().splitlines()
    player = MediaPlayer(file)
    player.play()
    blocks = []
    is_open = False
    start = None
    end = None
    for i, (line, next_line) in enumerate(zip(broken, broken[1:]+["end"])):
        while True:
            if is_open:
                print("Open:", line)
            else:
                print("Closed:", next_line)
            char = await ainput("")
            str_time = "0" + player.get_str_time().replace(".", ",")[0:-3]

            if not is_open and player.is_playing():
                is_open = True
                start = str_time
                player.pause()

            elif is_open and not player.is_playing():
                player.play()

            elif is_open and player.is_playing():
                is_open = False
                end = str_time
                block = SubBlock(i+1, start, end, line)
                blocks.append(block)
                print(block)
                player.pause()

            elif char == "s" and not is_open and not player.is_playing():
                player.play()
                break

            if not is_open and not player.is_playing():
                is_open = True
                start = str_time
                player.play()
                break
    
    text = ""
    for block in blocks:
        text += str(block)
    print(text)
    Path("./output.strt").write_text(text)

def main():
    try:
        asyncio.run(interact())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
