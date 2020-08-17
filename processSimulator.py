from tkinter import *
import tkinter.ttk as tkrttk
import platform
import copy
import math

processArray = []


class Process:

    def __init__(self, processNumber, arrivalTime, burstTime, priority):
        self.name = "P" + str(processNumber)
        self.burstTime = burstTime
        self.decBurstTime = burstTime
        self.arrivalTime = arrivalTime
        self.startTime = []
        self.endTime = []
        self.turnAroundTime = 0
        self.waitingTime = 0
        self.priority = priority


class MainWindow(Tk):
    def __init__(self):
        super(MainWindow, self).__init__()
        if platform.system() == "Windows":
            self.geometry("1270x620")  # TODO: Platform support
        else:
            self.geometry("1300x710")
        self.numberOfProcess = 0
        self.resizable(False, False)
        self.var = StringVar()
        self.var2 = StringVar()
        self.var3 = StringVar()
        self.var4 = StringVar()
        self.varArrival = StringVar()
        self.varBurst = StringVar()
        self.varPriority = StringVar()

        self.lvl1 = Frame(self)
        self.lvl2 = Frame(self)
        self.lvl3 = Frame(self)

        self.label = Label(self.lvl2, textvariable=self.var, relief=SOLID)
        self.label2 = Label(self.lvl2, textvariable=self.var2, relief=SOLID, width=33)  # TODO: Platform support
        if platform.system() == "Windows":
            self.label3 = Label(self.lvl2, textvariable=self.var3, relief=SOLID, width=115)  # TODO: Platform support
        else:
            self.label3 = Label(self.lvl2, textvariable=self.var3, relief=SOLID, width=86)
        self.label4 = Label(self.lvl3, textvariable=self.var4, relief=SOLID)
        self.arrivalLabel = Label(self.lvl2, textvariable=self.varArrival)
        self.burstLabel = Label(self.lvl2, textvariable=self.varBurst)
        self.priorityLabel = Label(self.lvl2, textvariable=self.varPriority)

        self.treeview = tkrttk.Treeview(self.lvl1, height=5)  # TODO: Platform support
        self.calctreeview = tkrttk.Treeview(self.lvl2, height=9)  # TODO: Platform support

        self.listBox = Listbox(self.lvl2)

        self.arrivalEntry = Entry(self.lvl2, bd=5)
        self.burstEntry = Entry(self.lvl2, bd=5)
        self.priorityEntry = Entry(self.lvl2, bd=5)

        self.addBtn = Button(self.lvl2, text="Create process", command=self.add)
        self.removeBtn = Button(self.lvl2, text="Remove process", command=self.remove)
        self.clearAllBtn = Button(self.lvl2, text="Clear all process", command=self.clear)
        self.startBtn = Button(self.lvl3, text="Start Simulation", command=self.start)
        if platform.system() == "Windows":
            self.display = Text(self.lvl3, height=10, bd=2, relief=SOLID)  # TODO: Platform support
        else:
            self.display = Text(self.lvl3, height=15, bd=2, relief=SOLID)  # TODO: Platform support
        self.display2 = Text(self.lvl2, height=13, width=55, bd=2, relief=SOLID)  # TODO: Platform support

        self.initUI()

    def initUI(self):
        self.title("CPU Process Scheduling Simulator")
        self.var.set("Select scheduling algorithm")
        self.var2.set("Add Process")
        self.var3.set("Calculation Output")
        self.var4.set("Gantt Chart")
        self.varArrival.set("Arrival Time")
        self.varBurst.set("Burst Time")
        self.varPriority.set("Priority")
        self.listBox.insert(1, "Preemptive SJF")
        self.listBox.insert(2, "Non Preemptive SJF")
        self.listBox.insert(3, "Preemptive Priority")
        self.listBox.insert(4, "Non Preemptive Priority")
        self.listBox.insert(5, "Round Robin")
        self.treeview["column"] = ("Process", "Burst Time", "Arrival Time", "Priority")
        self.calctreeview["column"] = ("Process", "Waiting Time", "Turnaround Time")

        self.treeview.column("#0", width=50, minwidth=25, stretch=NO, anchor=CENTER)
        self.treeview.column("Process", width=100, minwidth=50, anchor=CENTER)
        self.treeview.column("Burst Time", width=100, minwidth=50, anchor=CENTER)
        self.treeview.column("Arrival Time", width=100, minwidth=50, anchor=CENTER)
        self.treeview.column("Priority", width=100, minwidth=50, anchor=CENTER)

        self.treeview.heading("#0", text="#")
        self.treeview.heading("Process", text="Process")
        self.treeview.heading("Burst Time", text="Burst Time")
        self.treeview.heading("Arrival Time", text="Arrival Time")
        self.treeview.heading("Priority", text="Priority")

        self.calctreeview.column("#0", width=50, anchor=CENTER)
        self.calctreeview.column("Process", width=100, anchor=CENTER)
        self.calctreeview.column("Waiting Time", width=100, anchor=CENTER)
        self.calctreeview.column("Turnaround Time", width=100, anchor=CENTER)

        self.calctreeview.heading("#0", text="#")
        self.calctreeview.heading("Process", text="Process")
        self.calctreeview.heading("Waiting Time", text="Waiting Time")
        self.calctreeview.heading("Turnaround Time", text="Turnaround Time")

        self.lvl1.pack(fill=X)
        self.treeview.pack(fill=X)

        self.lvl2.pack(fill=X)

        # TODO: Platform support
        self.label.grid(row=0, column=0, padx=6, pady=5)
        self.label2.grid(row=0, column=1, padx=8, pady=5, columnspan=3)
        self.label3.grid(row=0, column=6, padx=5, pady=5, columnspan=2)
        self.burstLabel.grid(row=1, column=1)
        self.arrivalLabel.grid(row=2, column=1)
        self.priorityLabel.grid(row=3, column=1)

        self.burstEntry.grid(row=1, column=2, columnspan=2)
        self.arrivalEntry.grid(row=2, column=2, columnspan=2)
        self.priorityEntry.grid(row=3, column=2, columnspan=2)

        self.listBox.grid(row=1, column=0, padx=5, pady=5, rowspan=10)

        self.addBtn.grid(row=5, column=3)
        self.removeBtn.grid(row=5, column=2)
        self.clearAllBtn.grid(row=5, column=1)

        self.calctreeview.grid(row=1, column=4, rowspan=6, columnspan=3)

        self.display2.grid(row=1, column=7, rowspan=6, columnspan=2, padx=5)

        self.lvl3.pack(fill=X)
        self.label4.pack(fill=X, padx=5, pady=5)
        self.display.pack(fill=X, padx=5, pady=5)
        self.startBtn.pack(fill=X, padx=5)

    def insertTreeview(self, process, burstTime, arrivalTime, priority):
        self.treeview.insert("", 'end', text="-", values=(process, burstTime, arrivalTime, priority))

    def insertCalcTreeView(self, process, avgWaiting, avgTurnaround):
        self.calctreeview.insert("", 'end', text="-", values=(process, avgWaiting, avgTurnaround))

    def add(self):
        self.numberOfProcess = self.numberOfProcess + 1
        processArray.append(
            Process(self.numberOfProcess, int(self.arrivalEntry.get()), int(self.burstEntry.get()),
                    int(self.priorityEntry.get())))

        if len(processArray) != 0:
            process = processArray[len(processArray) - 1]
            self.insertTreeview(process.name, process.burstTime, process.arrivalTime
                                , process.priority)

    def remove(self):
        curItem = self.treeview.focus()
        if len(curItem) != 0:
            values = self.treeview.item(curItem)
            datas = values['values']

            for process in processArray:
                if datas[0] == process.name:
                    processArray.remove(process)
                    self.treeview.delete(curItem)

    def clear(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        self.numberOfProcess = 0
        processArray.clear()

    def resetOutput(self):
        self.display.delete(1.0, END)
        self.display2.delete(1.0, END)
        for i in self.calctreeview.get_children():
            self.calctreeview.delete(i)

    def calcEndResult(self, avgturnaround, avgwaiting):  # Show total avg turnAround and waiting time
        self.display2.insert(INSERT, "Average Turnaround time : " + avgturnaround)
        self.display2.insert(INSERT, "\nAverage Waiting Time : " + avgwaiting)

    def gantChartOut(self, processName, processTime, end=False):

        charLength = 0
        if platform.system() == "Windows":
            charLength += 168  # TODO: platform check
        else:
            charLength += 192  # TODO: platform check
        totalLine = 1000
        border = "------------"
        tempstring = "|" + '{:^10}'.format(processName) + "|"
        if len(self.display.get(1.0, "1.end")) == 0:
            for x in range(totalLine):
                self.display.insert(INSERT, "\n")
            self.display.insert("1.end", border)
            self.display.insert("2.end", tempstring)
            self.display.insert("3.end", border)
            self.display.insert("4.end", "0")
            for x in range(len(border) - len(str(processTime)) - 1):
                self.display.insert("4.end", " ")
            self.display.insert("4.end", processTime)

        else:
            for lineNumber in range(totalLine):
                if (len(self.display.get(str(lineNumber + 1) + ".0", str(lineNumber + 1) + ".end")) + 12) < charLength:
                    self.display.insert(str(lineNumber + 1) + ".end", border)
                    self.display.insert(str(lineNumber + 2) + ".end", tempstring)
                    self.display.insert(str(lineNumber + 3) + ".end", border)
                    for x in range(len(border) - len(str(processTime))):
                        self.display.insert(str(lineNumber + 4) + ".end", " ")
                    self.display.insert(str(lineNumber + 4) + ".end", processTime)
                    break

    def start(self):

        self.resetOutput()
        if str(self.listBox.curselection()) == "(0,)":
            self.preSJF()
        elif str(self.listBox.curselection()) == "(1,)":
            self.nonPreSJF()
        elif str(self.listBox.curselection()) == "(2,)":
            self.prePrio()
        elif str(self.listBox.curselection()) == "(4,)":
            self.RR()
        elif str(self.listBox.curselection()) == "(3,)":
            self.nonPrePrio()
        else:
            self.display.insert(INSERT, "PLEASE SELECT A SCHEDULING ALGORITHM...")

    def preSJF(self):

        processArray.sort(key=lambda x: (x.arrivalTime, x.burstTime))

        time = 0
        copyProcessList = processArray.copy()  # change to deep copy
        processQueue = []
        process = Process(0, 0, copyProcessList[0].arrivalTime, math.inf)
        while True:
            restart = True
            while restart:
                if len(copyProcessList) == 0:
                    restart = False
                else:
                    restart = True

                for i in range(len(copyProcessList)):
                    if copyProcessList[i].arrivalTime == time:
                        processQueue.append(copyProcessList.pop(i))
                        break
                    else:
                        restart = False
            processQueue.sort(key=lambda x: (x.decBurstTime, x.arrivalTime))
            if len(processQueue) > 0 and process.name != processQueue[0].name:
                process.endTime.append(time)
                if (process.name != "P0" and process.name != "P100") and process.decBurstTime > 1:
                    self.gantChartOut(process.name, time)
                for e in processQueue:  #
                    if "P100" in e.name:  #
                        # put gant chart ("IDLE", time)
                        self.gantChartOut("IDLE", time)
                        processQueue.pop(processQueue.index(e))  #
                process = processQueue[0]
                process.startTime.append(time)
            elif len(processQueue) == 0 and process.name == "P0":
                processQueue.append(process)
            time = time + 1
            process.decBurstTime = process.decBurstTime - 1
            if process.decBurstTime <= 0:
                process.endTime.append(time)
                if process.name == "P0":
                    self.gantChartOut("IDLE", time)
                else:
                    # put gant chart (process.name, time)
                    self.gantChartOut(process.name, time)
                if len(processQueue) != 0:
                    processQueue.pop(0)
            if len(processQueue) == 0:
                if len(copyProcessList) == 0:
                    break
                elif copyProcessList[0].arrivalTime == time:
                    continue
                else:
                    processQueue.append(Process(100, time, math.inf, math.inf))  #
                    process = processQueue[0]  #

        for i in range(len(processArray)):
            for st in range(len(processArray[i].startTime)):
                if st == 0:
                    processArray[i].waitingTime = processArray[i].startTime[st] - processArray[i].arrivalTime
                else:
                    processArray[i].waitingTime = processArray[i].waitingTime + (
                            processArray[i].startTime[st] - processArray[i].endTime[st - 1])
            processArray[i].turnAroundTime = processArray[i].waitingTime + processArray[i].burstTime

        for i in range(len(processArray)):
            self.insertCalcTreeView(processArray[i].name, processArray[i].waitingTime,
                                    processArray[i].turnAroundTime)

        sumWT = 0
        sumTT = 0
        for i in range(len(processArray)):
            sumWT = sumWT + processArray[i].waitingTime
            sumTT = sumTT + processArray[i].turnAroundTime
        averageWT = sumWT / len(processArray)
        averageTT = sumTT / len(processArray)
        print("Average WT:  %.2f" % averageWT)
        print("Average TT:  %.2f" % averageTT)
        self.calcEndResult(str(averageTT), str(averageWT))

        # debug
        for i in range(len(processArray)):
            print("\n" + processArray[i].name)
            print(processArray[i].startTime)
            print(processArray[i].endTime)

        # reset all the values
        for i in range(len(processArray)):
            processArray[i].decBurstTime = processArray[i].burstTime
            processArray[i].startTime = []
            processArray[i].endTime = []
            processArray[i].waitingTime = 0
            processArray[i].turnAroundTime = 0
        # reset the position
        processArray.sort(key=lambda x: x.name)

    def nonPreSJF(self):
        processArray.sort(key=lambda x: (x.arrivalTime, x.burstTime))

        time = 0
        copyProcessList = processArray.copy()
        processQueue = []
        process = Process(0, 0, copyProcessList[0].arrivalTime, math.inf)
        while True:
            restart = True
            while restart:
                if len(copyProcessList) == 0:
                    restart = False
                else:
                    restart = True

                for i in range(len(copyProcessList)):
                    if copyProcessList[i].arrivalTime == time:
                        processQueue.append(copyProcessList.pop(i))
                        break
                    else:
                        restart = False
            processQueue.sort(key=lambda x: x.decBurstTime)
            if process.name == "P0":
                if len(processQueue) > 0:
                    process = processQueue[0]
                    process.startTime.append(time)
                else:
                    processQueue.append(process)
            elif len(processQueue) > 1 and "P100" in process.name:
                for e in processQueue:
                    if "P100" in e.name:
                        # add print gantt chart here ("IDLE", time)
                        self.gantChartOut("IDLE", time)
                        processQueue.remove(e)
                        process = processQueue[0]
                        process.startTime.append(time)
            time = time + 1
            process.decBurstTime = process.decBurstTime - 1
            if process.decBurstTime <= 0:
                process.endTime.append(time)
                if process.name == "P0":
                    # put print gantchart here ("IDLE", time)
                    self.gantChartOut("IDLE", time)
                else:
                    self.gantChartOut(process.name, time)
                processQueue.pop(processQueue.index(process))
                if len(processQueue) == 0:
                    if len(copyProcessList) == 0:
                        break
                    elif copyProcessList[0].arrivalTime == time:
                        continue
                    else:
                        processQueue.append(Process(100, time, math.inf, math.inf))
                        process = processQueue[0]
                        process.startTime.append(time)
                else:
                    process = processQueue[0]
                    process.startTime.append(time)

        for i in range(len(processArray)):
            for st in range(len(processArray[i].startTime)):
                if st == 0:
                    processArray[i].waitingTime = processArray[i].startTime[st] - processArray[i].arrivalTime
                else:
                    processArray[i].waitingTime = processArray[i].waitingTime + (
                            processArray[i].startTime[st] - processArray[i].endTime[st - 1])
            processArray[i].turnAroundTime = processArray[i].waitingTime + processArray[i].burstTime

        for i in range(len(processArray)):
            self.insertCalcTreeView(processArray[i].name, processArray[i].waitingTime,
                                    processArray[i].turnAroundTime)

        sumWT = 0
        sumTT = 0
        for i in range(len(processArray)):
            sumWT = sumWT + processArray[i].waitingTime
            sumTT = sumTT + processArray[i].turnAroundTime
        averageWT = sumWT / len(processArray)
        averageTT = sumTT / len(processArray)
        print("Average WT:  %.2f" % averageWT)
        print("Average TT:  %.2f" % averageTT)
        self.calcEndResult(str(averageTT), str(averageWT))

        # debug
        for i in range(len(processArray)):
            print("\n" + processArray[i].name)
            print(processArray[i].startTime)
            print(processArray[i].endTime)

        # reset all the values
        for i in range(len(processArray)):
            processArray[i].decBurstTime = processArray[i].burstTime
            processArray[i].startTime = []
            processArray[i].endTime = []
            processArray[i].waitingTime = 0
            processArray[i].turnAroundTime = 0
        # reset the position
        processArray.sort(key=lambda x: x.name)

    def prePrio(self):
        processArray.sort(key=lambda x: (x.arrivalTime, x.burstTime))

        time = 0
        copyProcessList = processArray.copy()
        processQueue = []
        process = Process(0, 0, copyProcessList[0].arrivalTime, math.inf)
        while True:
            restart = True
            while restart:
                if len(copyProcessList) == 0:
                    restart = False
                else:
                    restart = True

                for i in range(len(copyProcessList)):
                    if copyProcessList[i].arrivalTime == time:
                        processQueue.append(copyProcessList.pop(i))
                        break
                    else:
                        restart = False
            processQueue.sort(key=lambda x: (x.priority, x.decBurstTime))

            if len(processQueue) > 0 and process.name != processQueue[0].name:
                process.endTime.append(time)
                if (process.name != "P0" and process.name != "P100") and process.decBurstTime > 1:
                    self.gantChartOut(process.name, time)
                for e in processQueue:  #
                    if "P100" in e.name:  #
                        # add print gantt chart here
                        self.gantChartOut("IDLE", time)
                        processQueue.pop(processQueue.index(e))  #
                process = processQueue[0]
                process.startTime.append(time)
            elif len(processQueue) == 0 and process.name == "P0":
                processQueue.append(process)
            time = time + 1
            process.decBurstTime = process.decBurstTime - 1
            if process.decBurstTime == 0:
                process.endTime.append(time)
                if process.name == "P0":
                    self.gantChartOut("IDLE", time)
                else:
                    # put gant chart (process.name, time)
                    self.gantChartOut(process.name, time)
                processQueue.pop(0)
            if len(processQueue) == 0:
                if len(copyProcessList) == 0:
                    break
                elif copyProcessList[0].arrivalTime == time:
                    continue
                else:
                    processQueue.append(Process(100, time, math.inf, math.inf))  #
                    process = processQueue[0]  #

        for i in range(len(processArray)):
            for st in range(len(processArray[i].startTime)):
                if st == 0:
                    processArray[i].waitingTime = processArray[i].startTime[st] - processArray[i].arrivalTime
                else:
                    processArray[i].waitingTime = processArray[i].waitingTime + (
                            processArray[i].startTime[st] - processArray[i].endTime[st - 1])
            processArray[i].turnAroundTime = processArray[i].waitingTime + processArray[i].burstTime

        for i in range(len(processArray)):
            self.insertCalcTreeView(processArray[i].name, processArray[i].waitingTime,
                                    processArray[i].turnAroundTime)

        sumWT = 0
        sumTT = 0
        for i in range(len(processArray)):
            sumWT = sumWT + processArray[i].waitingTime
            sumTT = sumTT + processArray[i].turnAroundTime
        averageWT = sumWT / len(processArray)
        averageTT = sumTT / len(processArray)
        print("Average WT:  %.2f" % averageWT)
        print("Average TT:  %.2f" % averageTT)
        self.calcEndResult(str(averageTT), str(averageWT))

        # debug
        for i in range(len(processArray)):
            print("\n" + processArray[i].name)
            print(processArray[i].startTime)
            print(processArray[i].endTime)

        # reset all the values
        for i in range(len(processArray)):
            processArray[i].decBurstTime = processArray[i].burstTime
            processArray[i].startTime = []
            processArray[i].endTime = []
            processArray[i].waitingTime = 0
            processArray[i].turnAroundTime = 0
        # reset the position
        processArray.sort(key=lambda x: x.name)

    def nonPrePrio(self):

        processArray.sort(key=lambda x: (x.arrivalTime, x.burstTime))

        time = 0
        copyProcessList = processArray.copy()
        processQueue = []
        process = Process(0, 0, copyProcessList[0].arrivalTime, math.inf)
        while True:
            restart = True
            while restart:
                if len(copyProcessList) == 0:
                    restart = False
                else:
                    restart = True

                for i in range(len(copyProcessList)):
                    if copyProcessList[i].arrivalTime == time:
                        processQueue.append(copyProcessList.pop(i))
                        break
                    else:
                        restart = False
            processQueue.sort(key=lambda x: (x.priority, x.decBurstTime))
            if process.name == "P0":
                if len(processQueue) > 0:
                    process = processQueue[0]
                    process.startTime.append(time)
                else:
                    processQueue.append(process)
            elif len(processQueue) > 1 and "P100" in process.name:
                for e in processQueue:
                    if "P100" in e.name:
                        # add print gantt chart here
                        self.gantChartOut("IDLE", time)
                        processQueue.remove(e)
                        process = processQueue[0]
                        process.startTime.append(time)
            time = time + 1
            process.decBurstTime = process.decBurstTime - 1
            if process.decBurstTime <= 0:
                process.endTime.append(time)
                if process.name == "P0":
                    # put print gantchart here ("IDLE", time)
                    self.gantChartOut("IDLE", time)
                else:
                    self.gantChartOut(process.name, time)
                processQueue.pop(processQueue.index(process))
                if len(processQueue) == 0:
                    if len(copyProcessList) == 0:
                        break
                    elif copyProcessList[0].arrivalTime == time:
                        continue
                    else:
                        processQueue.append(Process(100, time, math.inf, math.inf))
                        process = processQueue[0]
                else:
                    process = processQueue[0]
                    process.startTime.append(time)

        for i in range(len(processArray)):
            for st in range(len(processArray[i].startTime)):
                if st == 0:
                    processArray[i].waitingTime = processArray[i].startTime[st] - processArray[i].arrivalTime
                else:
                    processArray[i].waitingTime = processArray[i].waitingTime + (
                            processArray[i].startTime[st] - processArray[i].endTime[st - 1])
            processArray[i].turnAroundTime = processArray[i].waitingTime + processArray[i].burstTime

        for i in range(len(processArray)):
            self.insertCalcTreeView(processArray[i].name, processArray[i].waitingTime,
                                    processArray[i].turnAroundTime)

        sumWT = 0
        sumTT = 0
        for i in range(len(processArray)):
            sumWT = sumWT + processArray[i].waitingTime
            sumTT = sumTT + processArray[i].turnAroundTime
        averageWT = sumWT / len(processArray)
        averageTT = sumTT / len(processArray)
        print("Average WT:  %.2f" % averageWT)
        print("Average TT:  %.2f" % averageTT)
        self.calcEndResult(str(averageTT), str(averageWT))

        # debug
        for i in range(len(processArray)):
            print("\n" + processArray[i].name)
            print(processArray[i].startTime)
            print(processArray[i].endTime)

        # reset all the values
        for i in range(len(processArray)):
            processArray[i].decBurstTime = processArray[i].burstTime
            processArray[i].startTime = []
            processArray[i].endTime = []
            processArray[i].waitingTime = 0
            processArray[i].turnAroundTime = 0
        # reset the position
        processArray.sort(key=lambda x: x.name)

    def RR(self):
        quantum = DialogPrompt().quantum
        print(quantum)
        processArray.sort(key=lambda x: x.arrivalTime)

        time = 0
        currentQuantum = 0
        copyProcessList = processArray.copy()
        processQueue = []
        process = Process(0, 0, copyProcessList[0].arrivalTime, math.inf)  # need 4 args
        moveProcess = None
        while True:
            restart = True
            while restart:
                if len(copyProcessList) == 0:
                    restart = False
                else:
                    restart = True

                for i in range(len(copyProcessList)):
                    if copyProcessList[i].arrivalTime == time:
                        processQueue.append(copyProcessList.pop(i))
                        break
                    else:
                        restart = False
            if moveProcess is not None:
                processQueue.append(moveProcess)
                moveProcess = None
            if process.name == "P0":
                if len(processQueue) > 0:
                    process = processQueue[0]
                    process.startTime.append(time)
                else:
                    processQueue.append(process)
                    currentQuantum = math.inf
            elif len(processQueue) > 1 and "P100" in process.name:
                for e in processQueue:
                    if "P100" in e.name:
                        # add print gantt chart here
                        self.gantChartOut("IDLE", time)
                        processQueue.remove(e)
                        process = processQueue[0]
                        process.startTime.append(time)
            time = time + 1
            currentQuantum = currentQuantum + 1
            process.decBurstTime = process.decBurstTime - 1
            print("Check", process.name, currentQuantum, quantum, time, process.decBurstTime)
            if process.decBurstTime == 0:
                process.endTime.append(time)
                if process.name == "P0":
                    # put print gantchart here ("IDLE", time)
                    self.gantChartOut("IDLE", time)
                else:
                    self.gantChartOut(process.name, time)
                processQueue.remove(process)
                if len(processQueue) == 0:
                    if len(copyProcessList) == 0:
                        break
                    elif copyProcessList[0].arrivalTime == time:
                        continue
                    else:
                        processQueue.append(Process(100, time, math.inf, math.inf))
                        process = processQueue[0]
                        currentQuantum = math.inf
                else:
                    process = processQueue[0]
                    process.startTime.append(time)
                    currentQuantum = 0
            elif currentQuantum == quantum:
                print("Enter", process.name, time)
                process.endTime.append(time)
                # add print gantt chart here
                self.gantChartOut(process.name, time)
                moveProcess = processQueue.pop(0)
                process = processQueue[0]
                process.startTime.append(time)
                currentQuantum = 0

        for i in range(len(processArray)):
            for st in range(len(processArray[i].startTime)):
                if st == 0:
                    processArray[i].waitingTime = processArray[i].startTime[st] - processArray[i].arrivalTime
                else:
                    processArray[i].waitingTime = processArray[i].waitingTime + (
                            processArray[i].startTime[st] - processArray[i].endTime[st - 1])
            processArray[i].turnAroundTime = processArray[i].waitingTime + processArray[i].burstTime

        for i in range(len(processArray)):
            self.insertCalcTreeView(processArray[i].name, processArray[i].waitingTime,
                                    processArray[i].turnAroundTime)

        sumWT = 0
        sumTT = 0
        for i in range(len(processArray)):
            sumWT = sumWT + processArray[i].waitingTime
            sumTT = sumTT + processArray[i].turnAroundTime
        averageWT = sumWT / len(processArray)
        averageTT = sumTT / len(processArray)
        print("Average WT:  %.2f" % averageWT)
        print("Average TT:  %.2f" % averageTT)
        self.calcEndResult(str(averageTT), str(averageWT))

        # debug
        for i in range(len(processArray)):
            print("\n" + processArray[i].name)
            print(processArray[i].startTime)
            print(processArray[i].endTime)
        # reset all the values
        for i in range(len(processArray)):
            processArray[i].decBurstTime = processArray[i].burstTime
            processArray[i].startTime = []
            processArray[i].endTime = []
            processArray[i].waitingTime = 0
            processArray[i].turnAroundTime = 0
        # reset the position
        processArray.sort(key=lambda x: x.name)


class DialogPrompt(Tk):
    def __init__(self):
        super(DialogPrompt, self).__init__()
        self.quantum = 0
        self.geometry("500x200")
        self.title("Quantum time dialog")
        self.entry = Entry(self, bd=5)
        self.button = Button(self, text="OK", command=self.on_button)
        self.label = Label(self, text="Input quantum time")
        self.label.pack(fill=X)
        self.entry.pack(fill=X)
        self.button.pack(fill=X)
        self.wait_window(self)

    def on_button(self):
        self.quantum = int(self.entry.get())
        self.destroy()


if __name__ == "__main__":
    mainController = MainWindow()
