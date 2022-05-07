import random


class SieveOfEratosthenes:
    def __init__(self, limit: int) -> None:
        self.limit = limit  # exclusive
        self.is_prime = [True] * self.limit
        self.run_sieve()

    def run_sieve(self):
        self.is_prime[0] = False
        self.is_prime[1] = False

        num1 = 2
        while num1 * num1 < self.limit:
            if not self.is_prime[num1]:
                num1 += 1
                continue

            num2 = num1
            while num1 * num2 < self.limit:
                self.is_prime[num1 * num2] = False
                num2 += 1
            
            num1 += 1

    def closest_prime(self, num: int) -> int:
        i = 0
        while num + i < self.limit or num - i >  1:
            if num + i < self.limit and self.is_prime[num + i]:
                return num + i

            if num - i > 0 and self.is_prime[num - i]:
                return num - i

            i += 1
        else:
            raise ValueError("No prime")


if __name__ == "__main__":
    limit = 10000
    sieve = SieveOfEratosthenes(limit)

    for i in range(100):
        randomint = random.randint(0, limit-1)
        print(f"Closest prime to {randomint} is {sieve.closest_prime(randomint)}")
