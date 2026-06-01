import timeit
import random
from collections import Counter

random_numbers = [random.randint(0, 100) for _ in range(1000000)]

def function():
    counts = {}
    for num in random_numbers:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1
    return counts

def top():
    counts = function()
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

def counter_function():
    return Counter(random_numbers)

def counter_top():
    return Counter(random_numbers).most_common(10)


if __name__ == '__main__':
    time_func = timeit.timeit(function, number=1)
    time_counter = timeit.timeit(counter_function, number=1)
    time_top = timeit.timeit(top, number=1)
    time_counter_top = timeit.timeit(counter_top, number=1)

    print(f"my function: {time_func}")
    print(f"Counter: {time_counter}")
    print(f"my top: {time_top}")
    print(f"Counter's top: {time_counter_top}")
