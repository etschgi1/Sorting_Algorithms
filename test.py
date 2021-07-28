from __future__ import print_function, unicode_literals
import glob
from PyInquirer import prompt
from gentestdata import GenData
import os
import sys
import time
from pprint import pprint
from random import randrange
from sorts import *


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
