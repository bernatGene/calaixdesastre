import asyncio
import time
import re
from playsound import playsound


async def set_timer(dt):
    t0 = time.time()
    te = t0 + dt
    while (rem := (te - time.time())) > 0:
        rem = int(round(rem))
        h = rem // (60**2)
        m = (rem % (60**2)) // 60
        s = rem - (h * 60**2 + m * 60)
        print(f"Time left: {h:02d}:{m:02d}:{s:02d}", end="\r")
        await asyncio.sleep(1)
    playsound("./mixkit-classic-alarm-995.wav")
    return


async def caffeinate(finished):
    proc = await asyncio.create_subprocess_shell("caffeinate")
    try:
        await proc.wait()
    except asyncio.CancelledError:
        proc.terminate()
        finished.set()


async def main():
    while True:
        timer = input("Presets [1]: 20min, [2]: 1h, or Timer duration hh:mm:ss : ")
        match timer:
            case "1":
                h, m, s = 0, 20, 0
                seconds = 20 *60
            case "2":
                seconds = 60 * 60
                h, m, s = 1, 0, 0
            case _:
                time_format = re.compile("\d\d:\d\d:\d\d")
                if time_format.match(timer) is None:
                    print("Bad format")
                    continue
                dd = re.compile("\d\d")
                h, m, s = [int(d) for d in dd.findall(timer)]
                seconds = h * 60 * 60 + m * 60 + s
        print(
            f"setting timer for {h} h, {m} m, {s} s (total {seconds} seconds)"
        )
        finished = asyncio.Event()
        await asyncio.gather(
            asyncio.wait_for(caffeinate(finished), timeout=seconds),
            set_timer(seconds)
        )
        await finished.wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
