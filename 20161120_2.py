from __future__ import division
import csv, sys

fop = open('20161120_2.txt','w')

class Recovery:

    def __init__(self):
        self.variables = {}
        self.activeTrans = []
        self.startedTrans = []
        self.logs = []
        self.transNames = []
        self.commitedTrans = []

    def processLog(self,log):
        logComm = ""
        # print(log)
        if log.lower().startswith('<start ckpt'):
            # print(log)
            tg = log.find('>')
            tmp = log[log.find('<start ckpt')+12:tg].split(',')
            # print(tmp)
            tmp = [x.strip('( )') for x in tmp]
            # print(tmp)
            logComm = 'start ckpt'
            tmp.reverse()
            return(logComm,tmp)

        if log.lower().startswith('<start'):
            tmp = log.strip().split(' ')
            tmp[0] = tmp[0][tmp[0].find('<')+1:].strip()
            tmp = [i.strip('>') for i in tmp]
            tmp.reverse()
            logComm = 'start'
            return(logComm,tmp)

        if log.lower().startswith('<commit'):
            tmp = log.strip().split(' ')
            tmp[0] = tmp[0][tmp[0].find('<')+1:].strip('')
            tmp = [i.strip('>') for i in tmp]
            tmp.reverse()
            logComm = 'commit'
            return(logComm,tmp)

        if log.lower().startswith('<end ckpt>'):
            log.reverse()
            logComm = 'end ckpt'
            return(logComm,log)

        logComm = 'change'
        tg = log.find('>')
        tmp = log[log.find('<')+1:tg].split(',')
        tmp = [x.strip() for x in tmp]
        return(logComm,tmp)

    def readLogs(self,filename):
        f = open(filename,'r')
        for line in f:
            if len(line.strip()) > 0:
                self.logs.append(line.strip())

        tp = self.logs[0]
        cnt = 0
        self.processVariables(tp)
        ind = self.pass1()
        self.pass2(ind)
        # self.updatedVariableNames.sort()
        for i in sorted(self.variables):
            if cnt < len(self.variables) - 1:
                fop.write(i + " " + str(self.variables[i]) + " ")
            else:
                fop.write(i + " " + str(self.variables[i]))
            cnt += 1
        fop.write('\n')

    def pass1(self):
        isStartCkpt = False
        isEndCkpt = not(True)

        for ind,log in enumerate(reversed(self.logs[1:])):
            logComm, tokens = self.processLog(log)
            # print(log,logComm,tokens)

            if logComm == 'start ckpt':
                isStartCkpt = True
                self.activeTrans.extend(tokens)
                tp = []
                for i in self.activeTrans:
                    if i not in self.commitedTrans:
                        tp.append(i)
                self.activeTrans = tp
                if int(isEndCkpt) == 1:
                    break
            elif logComm == 'start':
                self.startedTrans.append(tokens[0])
                if int(isStartCkpt) == 1:
                    if tokens[0] in self.activeTrans:
                        self.activeTrans.remove(tokens[0])
                    if len(self.activeTrans) == 0:
                        break
            elif logComm == 'end ckpt':
                isEndCkpt = True

            elif logComm == 'commit':
                self.commitedTrans.append(tokens[0])


        self.activeTrans = [i for i in self.startedTrans if i not in self.commitedTrans]
        # print(self.activeTrans)
        # print(self.commitedTrans)
        return ind

    def processVariables(self,vars):
        vars = vars.split(' ')
        i=0
        for i in range(0,len(vars),2):
            self.variables[vars[i]] = int(vars[i+1])

    def pass2(self,ind):
        t = ind + 1
        for i in range(t):
            n = i + 1
            logComm, tokens = self.processLog(self.logs[len(self.logs) - n])
            if logComm == 'change':
                num = int(tokens[2])
                var = tokens[1]
                trans = tokens[0]
                if trans not in self.activeTrans:
                    pass
                elif trans in self.activeTrans:
                    self.variables[var] = num


if __name__ == '__main__':
    recov = Recovery()
    recov.readLogs(sys.argv[1])