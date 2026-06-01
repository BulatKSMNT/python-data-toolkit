import sys
import psutil
import os

def read_file(filename):
    with open(filename) as f:
        for line in f:
            yield line


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()
    process = psutil.Process(os.getpid())
    data = read_file(sys.argv[1])
    for line in data:
        pass

    mem = process.memory_info().rss

    print(f"Peak Memory Usage = {mem / 1024 / 1024:.3f} MB")  # В мегабайтах
    print(f"User Mode Time + System Mode Time = {process.cpu_times().user + process.cpu_times().system:.2f}s")