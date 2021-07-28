from abc import ABC, abstractmethod
from random import randrange
from math import inf


class AbstractSort(ABC):
    """Abstract sort Baseclass"""

    def __init__(self, to_sort, log_swaps=True):
        self.to_sort = to_sort
        self.length = len(to_sort)
        self.log_swaps = log_swaps
        self.totalswaps = 0

    @abstractmethod
    def sort(self):
        pass

    def swap(self, i1, i2):
        temp = self.to_sort[i1]
        self.to_sort[i1] = self.to_sort[i2]
        self.to_sort[i2] = temp
        if self.log_swaps:
            self.totalswaps += 1

    def getTotalSwaps(self):
        return self.totalswaps

    def checkSort(self):
        for n in range(len(self.to_sort)-1):
            if self.to_sort[n+1] < self.to_sort[n]:
                return False
        return True


class BubbleSort(AbstractSort):
    """Original Bubble Sort implementation
    Space Complexity: O(1)
    Time Complexity: O(n^2) best and avg case"""

    def getName(self):
        return "Bubble Sort"

    def sort(self):
        n = self.length
        while n > 0:
            swap = False
            for i in range(n-1):
                if self.to_sort[i] > self.to_sort[i+1]:
                    super().swap(i, i+1)
                    swap = True
            if not swap:  # if in one rotation no swap happens it's sorted!
                break
            n -= 1


class BogoSort(AbstractSort):
    """The best Sorting Algorithm. Don't try to sort lists with more than 10 entries
    Space Complexity: O(1)
    Time Complexity: best: O(1), worst: O(∞)"""

    def getName(self):
        return "Bogo Sort"

    def sort(self):
        while not super().checkSort():
            r1 = randrange(0, self.length)
            r2 = randrange(0, self.length)
            super().swap(r1, r2)


class SelectionSort(AbstractSort):
    """Implementation of Selection Sort
    Space Complexity: O(1)
    Time Complexity: O(n^2)"""

    def getName(self):
        return "Selection Sort"

    def sort(self):
        smallestpos = 0
        for start in range(self.length):
            smallest = inf
            for count in range(start, self.length):
                val = self.to_sort[count]
                if val < smallest:
                    smallestpos, smallest = count, val
            super().swap(start, smallestpos)


class OptimizedSelectionSort(AbstractSort):
    """Implementation of an optimized Selection Sort
    Space Complexity: O(1)
    Time Complexity: O(n^2) (best case twice as fast as ordinary Selection Sort)"""

    def getName(self):
        return "Optimized Selection Sort"

    def sort(self):
        smallestpos = 0
        biggestpos = 0
        for start in range(self.length//2):  # Only have length
            smallest = inf
            biggest = -inf
            for count in range(start, self.length-start):
                val = self.to_sort[count]
                if val < smallest:
                    smallestpos, smallest = count, val
                if val > biggest:
                    biggestpos, biggest = count, val
            super().swap(start, smallestpos)
            # change if biggest was switched!
            biggestpos = smallestpos if biggestpos == start else biggestpos
            super().swap(self.length-start-1, biggestpos)
