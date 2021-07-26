from __future__ import print_function, unicode_literals
import glob
from PyInquirer import prompt
from gentestdata import GenData
import os
import sys
import time


class Sorting():
    algs = {"Bubble-Sort": "Nice", "Bogosort": "best Sorting Alg"}

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
        self.algnamemap = {"bubble-sort": bubbleSort, "Bogosort": bogoSort}
        self.path = input_path
        self.startime = 0
        self.endtime = 0
        self.timer_status = timer
        self.nums = []
        self.peak = peak

    def startTimer(self):
        self.startime = time.time()

    def stopTimer(self):
        self.endtime = time.time()

    def getTime(self):
        self.endtime - self.starttime

    def loadNums(self):
        with open(self.path, "r") as f:
            self.nums = f.readlines()
        if(self.peak):
            print(self.nums[0].split()[:10])


class bubbleSort(Sorting):
    def __init__(self):
        pass


class bogoSort(Sorting):
    def __init__(self):
        pass


def main():
    commands = {"reset nums": resetNums,
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
        elif ui == "quit":
            break
        commands[ui]()


def sortInfo(verbal=False):
    Sorting.printSorts(verbal)


def runSort():
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

    for file in to_sort:  # create sorter
        sorter = Sorting(file, peak=False)
        sorter.loadNums()
        for alg in algs:
            pass


def resetNums():
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
