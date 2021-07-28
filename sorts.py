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

    @staticmethod
    def getName(info_list=False):
        name = "Bubble Sort"
        info = """Bubble sort, sometimes referred to as sinking sort, is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. The algorithm, which is a comparison sort, is named for the way smaller or larger elements "bubble" to the top of the list."""
        info_link = "https://en.wikipedia.org/wiki/Bubble_sort"
        if info_list:
            return [name, info, info_link]
        return name

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
    @staticmethod
    def getName(info_list=False):
        name = "Bogo Sort"
        info = """In computer science, bogosort (also known as permutation sort, stupid sort, or slowsort) is a highly inefficient sorting algorithm based on the generate and test paradigm. The function successively generates permutations of its input until it finds one that is sorted. It is not useful for sorting, but may be used for educational purposes, to contrast it with more efficient algorithms."""
        info_link = "https://en.wikipedia.org/wiki/Bogosort"
        if info_list:
            return [name, info, info_link]
        return name

    def sort(self):
        while not super().checkSort():
            r1 = randrange(0, self.length)
            r2 = randrange(0, self.length)
            super().swap(r1, r2)


class SelectionSort(AbstractSort):
    """Implementation of Selection Sort
    Space Complexity: O(1)
    Time Complexity: O(n^2)"""

    @staticmethod
    def getName(info_list=False):
        name = "Selection Sort"
        info = """In computer science, selection sort is an in-place comparison sorting algorithm. It has an O(n^2) time complexity, which makes it inefficient on large lists, and generally performs worse than the similar insertion sort. Selection sort is noted for its simplicity and has performance advantages over more complicated algorithms in certain situations, particularly where auxiliary memory is limited."""
        info_link = "https://en.wikipedia.org/wiki/Selection_sort"
        if info_list:
            return [name, info, info_link]
        return name

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

    @staticmethod
    def getName(info_list=False):
        name = "Optimized Selection Sort"
        info = """In computer science, selection sort is an in-place comparison sorting algorithm. It has an O(n^2) time complexity, which makes it inefficient on large lists, and generally performs worse than the similar insertion sort. Selection sort is noted for its simplicity and has performance advantages over more complicated algorithms in certain situations, particularly where auxiliary memory is limited."""
        info_link = "https://en.wikipedia.org/wiki/Selection_sort"
        if info_list:
            return [name, info, info_link]
        return name

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


class TimeSort(AbstractSort):
    """Hybrid Algorithm using Mergesort and/or Insertionsort depending on array size
    Space Complexity: worst: O(n)
    Time Complexity: best: O(n), avg: O(n*log(n)) (but often better)"""
    @staticmethod
    def getName(info_list=False):
        name = "Time Sort (Python internal)"
        info = """Timsort ist ein hybrider Sortieralgorithmus, der von Mergesort und Insertionsort abgeleitet ist. Er wurde entwickelt, um auf verschiedenen realen Daten schnell zu arbeiten. Er wurde 2002 von Tim Peters für die Nutzung in Python entwickelt und ist ab der Version 2.3 der Standard-Sortieralgorithmus in Python. Mittlerweile wird er auch in Java SE 7 und auf der Android-Plattform genutzt."""
        info_link = "https://de.wikipedia.org/wiki/Timsort"
        if info_list:
            return [name, info, info_link]
        return name

    def sort(self):
        self.to_sort = sorted(self.to_sort)
