from abc import ABC, abstractmethod


class AbstractSort(ABC):
    def __init__(self, to_sort):
        self.to_sort = to_sort
        self.length = len(to_sort)

    @abstractmethod
    def sort(self):
        pass

    def swap(self, i1, i2):
        temp = self.to_sort[i1]
        self.to_sort[i1] = self.to_sort[i2]
        self.to_sort[i2] = temp

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
