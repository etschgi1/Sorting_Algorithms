from __future__ import print_function, unicode_literals
import glob
from PyInquirer import prompt
from gentestdata import GenData
import os
import sys
import time
from abc import ABC, abstractmethod
from pprint import pprint
from random import randrange


class Sorting():
    algs = {"BubbleSort": "Nice", "BogoSort": "best Sorting Alg"}

    @classmethod
    def getSortList(cls):
        return list(cls.algs.keys())

    @classmethod
    def printSorts(cls, Info=False):
        print("Available sorts: ", end="\n")
        if Info:
            print("Name \t \t Info")
            for k, v in cls.algs.items():
                print("- "+k+": "+v)
        else:
            print("Name")
            for k in cls.algs.keys():
                print("- "+k)

    def __init__(self, input_path, timer=True, peak=False):
        self.path = input_path
        self.timer_status = timer
        self.nums = []
        self.peak = peak

    def loadNums(self):
        with open(self.path, "r") as f:
            self.nums = f.readlines()
            self.nums = self.nums[0].split(", ")
            self.nums = [int(num) for num in self.nums]
        if(self.peak):
            print(self.nums[:10])

    def getNums(self):
        return self.nums


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


def main():
    commands = {"reset all nums": resetallNums,
                "run sort": runSort, "help": None, "quit": None, "sort info": sortInfo}
    while True:
        ui = None
        while ui not in commands:
            ui = input(">").lower()
        if ui == "help":
            print("Commands:")
            for c in commands.keys():
                print("\t- " + c)
            continue
        elif ui == "quit" or ui == "exit":
            break
        commands[ui]()


def sortInfo(verbal=False):
    Sorting.printSorts(verbal)


def runSort():
    #sorting_algs = {"BubbleSort": BubbleSort, "BogoSort": BogoSort}
    sortInfo()
    files = []
    for file in glob.glob("data/*.txt"):
        files.append(file)
    while True:
        questions = [
            {'type': 'list',
             'name': 'alg',
             'message': 'Which Sorting Algorithm should run?',
             'choices': Sorting.getSortList()+['All']},
            {'type': 'list',
             'name': 'files',
             'message': 'On which File?',
             'choices': files+['All']},
            {'type': 'confirm',
             'name': 'runconfirm',
             'message': 'Ready?',
             'default': False}
        ]
        ans = prompt(questions)
        if ans['runconfirm'] == True:
            break
    if ans['alg'] == "All":
        print("Running everything on file(s): {}".format(ans['files']))
        algs = Sorting.getSortList()
    else:
        algs = [ans['alg']]
    if ans['files'] == "All":
        to_sort = files
    else:
        to_sort = [ans['files']]
    times = {}
    for file in to_sort:
        sorter = Sorting(file)
        sorter.loadNums()
        key = file.split("/")[-1].split(".")[0]
        times[key] = {}
        for alg in algs:
            alg = globals()[alg](sorter.getNums())  # create Sorting class
            print("Starting {} with numbers from {}...".format(alg.getName(), file))
            start = time.time()
            alg.sort()  # Alg sorts list
            end = time.time()
            times[key][alg.getName()] = round(
                end-start, 2) if alg.checkSort() else "Not sorted!"
    pprint(times)


def resetallNums():
    Seed = int(input("Seed = "))
    Count = int(input("Count = (Max = 10.000) "))
    Seed, Count = min(0, Seed), min(max(Count, 2), 10000)
    print("Reseting all Files: ")
    dummy = GenData()
    algs = dummy.getGeneratorAlgs()
    for a in algs:
        print("- "+a+": ")
        dummy = GenData(hash=Seed, alg=str(a), entries=Count)
        dummy.getData()


if __name__ == '__main__':
    print("###Tester for different Sorting-Algorithms### \n\t help for Help \t quit to Quit\n")
    main()
