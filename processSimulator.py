from tkinter import *
import tkinter.ttk as tkrttk
import platform
import copy

processArray = []


class Process:
    __numberOfProcess = 0
    __quantumTime = 3

    def __init__(self, arrival, burst, priority, quantum=3):

        Process.__numberOfProcess += 1
        Process.__quantumTime = quantum
        self.__processName = "P" + str(Process.__numberOfProcess)
        self.__arrivalTime = arrival
        self.__burstTime = burst
        self.__priority = priority
        self.__startTime = []
        self.__endTime = []
        self.__turnAroundTime = 0
        self.__waitingTime = 0

    def getStartTime(self):
        return self.__startTime

    def getEndTime(self):
        return self.__endTime

    def getTurnAroundTime(self):
        return int(self.__turnAroundTime)

    def setTurnAroundTime(self, turnAroundTime):
        self.__turnAroundTime = int(turnAroundTime)

    def getWaitingTime(self):
        return int(self.__waitingTime)

    def setWaitingTime(self, waitingTime):
        self.__waitingTime = int(waitingTime)

    def getProcessName(self):
        return self.__processName

    def getArrivalTime(self):
        return int(self.__arrivalTime)

    def getBurstTime(self):
        return int(self.__burstTime)

    def setBurstTime(self, burstTime):
        self.__burstTime = int(burstTime)

    @staticmethod
    def getQuantumTime():
        return int(Process.__quantumTime)

    def getPriority(self):
        return int(self.__priority)

    @staticmethod
    def deleteProcess():
        Process.__numberOfProcess = 0

    @staticmethod
    def setQuantumTime(quantum):
        Process.__quantumTime = int(quantum)


class MainWindow(Tk):
    def __init__(self):
        super(MainWindow, self).__init__()
        if platform.system() == "Windows":
            self.geometry("1270x620")  # TODO: Platform support
        else:
            self.geometry("1300x710")
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
        self.listBox.insert(4, "Round Robin")
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
        self.arrivalLabel.grid(row=1, column=1)
        self.burstLabel.grid(row=2, column=1)
        self.priorityLabel.grid(row=3, column=1)

        self.arrivalEntry.grid(row=1, column=2, columnspan=2)
        self.burstEntry.grid(row=2, column=2, columnspan=2)
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
        processArray.append(
            Process(int(self.arrivalEntry.get()), int(self.burstEntry.get()), int(self.priorityEntry.get())))

        if len(processArray) != 0:
            process = processArray[len(processArray) - 1]
            self.insertTreeview(process.getProcessName(), process.getBurstTime(), process.getArrivalTime()
                                , process.getPriority())

    def remove(self):
        curItem = self.treeview.focus()
        if len(curItem) != 0:
            values = self.treeview.item(curItem)
            datas = values['values']

            for process in processArray:
                if datas[0] == process.getProcessName():
                    processArray.remove(process)
                    self.treeview.delete(curItem)

    def clear(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)

        for process in processArray:
            process.deleteProcess()
        processArray.clear()

    def resetOutput(self):
        self.display.delete(1.0, END)
        self.display2.delete(1.0, END)
        for i in self.calctreeview.get_children():
            self.calctreeview.delete(i)

    def calcEndResult(self, avgturnaround, avgwaiting):  # Show total avg turnAround and waiting time
        self.display2.insert(INSERT, "Total and Average Turnaround time : " + avgturnaround)
        self.display2.insert(INSERT, "\nTotal and Average Waiting time : " + avgwaiting)

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
            self.display.insert("4.end", processTime)
            for x in range(len(border) - len(str(processTime))):
                self.display.insert("4.end", " ")

        else:
            for lineNumber in range(totalLine):
                if end is not True:
                    if (len(self.display.get(str(lineNumber + 1) + ".0", str(lineNumber + 1) + ".end")) + 12) < charLength:
                        self.display.insert(str(lineNumber + 1) + ".end", border)
                        self.display.insert(str(lineNumber + 2) + ".end", tempstring)
                        self.display.insert(str(lineNumber + 3) + ".end", border)
                        self.display.insert(str(lineNumber + 4) + ".end", processTime)
                        for x in range(len(border) - len(str(processTime))):
                            self.display.insert(str(lineNumber + 4) + ".end", " ")
                        break
                else:
                    deleteline = str(lineNumber + 4) + "." + str(len(self.display.get(4.0, "4.end"))-1)
                    self.display.delete(deleteline)
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
        elif str(self.listBox.curselection()) == "(3,)":
            DialogPrompt()
            self.RR()
        else:
            self.display.insert(INSERT, "PLEASE SELECT A SCHEDULING ALGORITHM...")

    def preSJF(self):

        processArray.sort(key=lambda x: (x.getArrivalTime(), x.getBurstTime()))

        time = 0
        copyprocessArray = copy.deepcopy(processArray)
        processQueue = []
        process = Process(0, 0, 0)
        while True:  # this loop keep running if there are process's arrival time reached the current time, stop if there's no more
            restart = True
            while restart:
                if len(copyprocessArray) == 0:
                    restart = False
                else:
                    restart = True

                for i in range(len(copyprocessArray)):
                    if copyprocessArray[i].getArrivalTime() == time:
                        processQueue.append(copyprocessArray.pop(i))
                        break
                    else:
                        restart = False

            processQueue.sort(key=lambda x: x.getBurstTime())
            if len(processQueue) > 0 and process.getProcessName() != processQueue[0].getProcessName():
                process.getEndTime().append(time)
                process = processQueue[0]
                process.getStartTime().append(time)
                self.gantChartOut(process.getProcessName(), time)
                print("GOUT2")
            time = time + 1
            process.setBurstTime(process.getBurstTime() - 1)
            print("Burst", process.getBurstTime())
            if process.getBurstTime() == 0:
                process.getEndTime().append(time)
                processQueue.pop(0)
            if len(processQueue) == 0:
                self.gantChartOut(process.getProcessName(), time, True)
                print("GOUT")
                break

        for i in range(len(processArray)):
            for st in range(len(processArray[i].getStartTime())):
                if st == 0:
                    processArray[i].setWaitingTime(
                        processArray[i].getStartTime()[st] - processArray[i].getArrivalTime())
                else:
                    processArray[i].setWaitingTime(processArray[i].getWaitingTime() + (
                            processArray[i].getStartTime()[st] - processArray[i].getEndTime()[st - 1]))
            processArray[i].setTurnAroundTime(processArray[i].getWaitingTime() + processArray[i].getBurstTime())

        print("\n    BT    AT    WT    TT")
        for i in range(len(processArray)):
            print(processArray[i].getProcessName() + ": %2d    %2d    %2d    %2d"
                  % (processArray[i].getBurstTime(), processArray[i].getArrivalTime(), processArray[i].getWaitingTime(),
                     processArray[i].getTurnAroundTime()))

        sumWT = 0
        sumTT = 0
        for i in range(len(processArray)):
            sumWT = sumWT + processArray[i].getWaitingTime()
            sumTT = sumTT + processArray[i].getTurnAroundTime()
        averageWT = sumWT / len(processArray)
        averageTT = sumTT / len(processArray)
        print("Average WT:  %.2f" % averageWT)
        print("Average TT:  %.2f" % averageTT)

    def nonPreSJF(self):
        print("Non Premptive SJF")

    def prePrio(self):
        print("Premptive Priority")

    def RR(self):
        print(Process.getQuantumTime())
        print("RR")


class DialogPrompt(Tk):
    def __init__(self):
        super(DialogPrompt, self).__init__()
        self.geometry("500x200")
        self.title("Quantum time dialog")
        self.entry = Entry(self, bd=5)
        self.button = Button(self, text="OK", command=self.on_button)
        self.label = Label(self, text="Input quantum time")
        self.label.pack(fill=X)
        self.entry.pack(fill=X)
        self.button.pack(fill=X)
        self.wait_window()

    def on_button(self):
        Process.setQuantumTime(self.entry.get())
        self.destroy()


if __name__ == "__main__":
    mainController = MainWindow()
