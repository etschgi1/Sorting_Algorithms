from __future__ import print_function, unicode_literals
import glob
from PyInquirer import prompt
from gentestdata import GenData
import os
import sys
import time
from pprint import pprint
from sorts import *


class Sorting():
    algs = {"BubbleSort": "Nice", "BogoSort": "best Sorting Alg",
            "SelectionSort": "Takes the min of every pass and moves it to front",
            "OptimizedSelectionSort": "Sorts using min and max of each pass twice as fast as original"}

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
        self.length = 0

    def loadNums(self):
        with open(self.path, "r") as f:
            self.nums = f.readlines()
            self.nums = self.nums[0].split(", ")
            self.nums = [int(num) for num in self.nums]
            self.length = len(self.nums)
        if(self.peak):
            print(self.nums[:10])

    def getNums(self):
        return self.nums

    def getLenght(self):
        return self.length


def main():
    commands = {"reset all nums": resetallNums, "reset nums": resetNums,
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
             'choices': Sorting.getSortList()+['All']+['All without BogoSort']},
            {'type': 'list',
             'name': 'files',
             'message': 'On which File?',
             'choices': files+['All']},
            {'type': 'list',
             'name': 'loglevel',
             'message': 'Loglevel',
             'choices': ['minimal (default)', 'all']},
            {'type': 'confirm',
             'name': 'runconfirm',
             'message': 'Ready?',
             'default': False}
        ]
        ans = prompt(questions)
        loglevel = 1 if ans['loglevel'] == 'all' else 0
        if ans['runconfirm'] == True:
            break
    if ans['alg'] == "All":
        print("Running everything on file(s): {}".format(ans['files']))
        algs = Sorting.getSortList()
    elif ans['alg'] == 'All without BogoSort':
        print("Running everything, except BogoSort on file(s): {}".format(
            ans['files']))
        algs = Sorting.getSortList()
        algs.remove("BogoSort")
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
            if loglevel:
                print(f"Numbers to sort {sorter.getLenght()}")
            start = time.time()
            alg.sort()  # Alg sorts list
            end = time.time()
            times[key][alg.getName()] = {'time (s)': round(
                end-start, 2) if alg.checkSort() else "Not sorted!",
                'total_swaps': alg.getTotalSwaps() if alg.getTotalSwaps() != 0 else "Not supported"}
    if loglevel:
        pprint(times)


def resetNums():
    Seed = int(input("Seed = "))
    Count = int(input("Count = (Max = 10.000.000) "))
    Seed, Count = min(0, Seed), min(max(Count, 2), 10000000)
    dummy = GenData()
    algs = dummy.getGeneratorAlgs()
    question = [
        {'type': 'list',
         'name': 'files',
         'message': 'Select files to reset:',
         'choices': algs}
    ]
    ans = prompt(question)
    print("- "+ans['files']+": ")
    dummy = GenData(hash=Seed, alg=str(ans['files']), entries=Count)
    dummy.getData()


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
