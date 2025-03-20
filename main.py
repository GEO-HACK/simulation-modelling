import random

def dice_generator():

    while True:
        rand_num = random.random()  # Generate random numbers between 0 and 1
        
        
        if 0 <= rand_num < 1/6:
            yield 1
        elif 1/6 <= rand_num < 2/6:
            yield 2
        elif 2/6 <= rand_num < 3/6:
            yield 3
        elif 3/6 <= rand_num < 4/6:
            yield 4
        elif 4/6 <= rand_num < 5/6:
            yield 5
        else:
            yield 6 # 5/6 <= rand_num < 1

rolls = 1000
dice_gen = dice_generator()
frequency = {i: 0 for i in range(1, 7)}  # Dictionary to store faces


for _ in range(rolls):
    face = next(dice_gen)
    frequency[face] += 1

# Display results in a table
print(f"{'Face':<5}  {'Frequency':<10}  {'Percent':<10}")
print("-" * 30)
for face, count in frequency.items():
    percent = (count / rolls) * 100
    print(f"{face:<5}{count:<10}{percent:.2f}%")
