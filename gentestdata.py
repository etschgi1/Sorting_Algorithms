import sys
import os
import random
import sympy
# Globals:


def main():
    valid_algs = ['numbers', 'primes', 'randnums', 'fib']
    args = {'hash': 0, 'alg': valid_algs[0], 'entries': 100}
    count = 0
    for key in args.keys():
        count += 1
        try:
            if(key == 'alg' and sys.argv[count] not in valid_algs):
                continue
            if(key == 'entries' and int(sys.argv[count]) < 2):
                print("entries must be >=2, entries set to 2!")
                args['entries'] = 2
                continue
            args[key] = sys.argv[count]
        except IndexError:
            pass
    hash, alg, entries = args.values()
    # print(os.path.dirname(sys.argv[0]))
    Generator = GenData(os.path.dirname(sys.argv[0]), hash, alg, entries)
    Generator.getData()


class GenData():
    def __init__(self, path=os.path.dirname(sys.argv[0]), hash=0, alg='dummy', entries=100):
        self.algmap = {"fib": self.fib, "primes": self.primes,
                       "numbers": self.numbers, "randnums": self.randnums, "dummy": self.dummy}
        self.path = path
        self.hash = int(hash)
        self.algname = alg
        self.alg = self.algmap[alg]
        self.entries = int(entries)
        self.nums = []
        random.seed()

    def getGeneratorAlgs(self):
        return list(self.algmap.keys())

    def getData(self):
        self.alg()  # run Alg
        # shuffel
        random.shuffle(self.nums)
        # print(self.nums)
        self.writeToFile()

    def randnums(self):
        """Draws from a random range which is 1 to 10 Time larger than items drawn"""
        factor = int(random.randint(1, 10))
        rand_range = random.randint(self.entries, self.entries*factor)
        self.nums = list(random.sample(range(rand_range), self.entries))

    def numbers(self):
        self.nums = [i for i in range(self.entries)]

    def dummy(self):
        return()

    def fib(self):
        """Fine for n < 10.000"""
        self.nums = [1, 1]
        for i in range(self.entries-1):
            self.nums.append(self.nums[-1] + self.nums[-2])
        self.nums.remove(1)

    def primes(self):
        cur = 3
        self.nums = [2]
        while len(self.nums) < self.entries:
            if all(cur % i != 0 for i in self.nums):
                self.nums.append(cur)
            cur += 1
        for p in self.nums:  # Checks validity
            if not sympy.isprime(p):
                print("Sieve false!")

    def writeToFile(self):
        if self.entries < 1 or self.algname == "dummy":
            print("---")
            return()
        filename = self.path + "/data/"+self.algname+".txt"
        print(filename)
        with open(filename, 'w') as f:
            n = 1
            while n < len(self.nums):
                f.write(str(self.nums[n-1])+", ")
                n += 1
            f.write(str(self.nums[-1]))


if __name__ == '__main__':
    main()
