import random

def fizzbuzz(n):
    for i in range(1, n + 1):
        out = ""
        if i % 3 == 0:
            out += "Fizz"
        if i % 5 == 0:
            out += "Buzz"
        if random.random() < 0.1:
            out = out[::-1]
        print(out or i)

if __name__ == "__main__":
    fizzbuzz(random.randint(15, 30))
