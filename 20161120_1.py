from __future__ import division
import csv, sys

fop = open('20161120_1.txt','w')

class Logging():

	def __init__(self,x):
		self.trans = []
		self.transNames = []
		self.transPts = []
		self.tmpVariables = []
		self.variables = {}
		self.variableNames = []
		self.memoryVariableNames = []
		self.memoryVariables = {}
		self.updateVariablesNames = []
		self.transOutVar = {}
		self.x = x

	def printVariables(self):
		for i in range(len(self.variableNames)):
			if i < len(self.variableNames) - 1:
				# sys.stdout.write(self.variableNames[i] + " " + str(self.variables[self.variableNames[i]]) + " ")
				fop.write(self.variableNames[i] + " " + str(self.variables[self.variableNames[i]]) + " ")
			else:
				# sys.stdout.write(self.variableNames[i] + " " + str(self.variables[self.variableNames[i]]))
				fop.write(self.variableNames[i] + " " + str(self.variables[self.variableNames[i]]))
		# print()
		fop.write('\n')

	def printMemVariables(self):
		k = 0
		j = len(self.memoryVariableNames) - 1
		for i in sorted(self.memoryVariableNames):
			if k < j:
				# sys.stdout.write(i + " " + str(self.memoryVariables[i]) + " ")
				fop.write(i + " " + str(self.memoryVariables[i]) + " ")
			else:
				# sys.stdout.write(i + " " + str(self.memoryVariables[i]))
				fop.write(i + " " + str(self.memoryVariables[i]))
			k += 1
		# print()
		fop.write('\n')

	def processVariables(self,var):
		var = var.split(" ")
		for i in range(0,len(var),2):
			self.variables[var[i]] = int(var[i+1])
			self.variableNames.append(var[i])

	def calc(self,rhs,opr,i):
		val2 = rhs.split(opr)[1].strip()
		if val2.isdigit():
			val2 = int(val2)
		else:
			val2 = self.tmpVariables[i][val2]
		val1 = rhs.split(opr)[0].strip()
		val1 = self.tmpVariables[i][val1]
		result = 0
		if opr == '+':
			result = val1+val2
		elif opr == '-':
			result = val1-val2
		elif opr == '*':
			result = val1*val2
		elif opr == '/':
			result = val1/val2

		return result

	def reportLog(self,i,var_write):
		# print('<'+self.transNames[i] + ", " + var_write + ", " + str(self.memoryVariables[var_write]) + ">")
		fop.write('<'+self.transNames[i] + ", " + var_write + ", " + str(self.memoryVariables[var_write]) + ">" + '\n')

	def seperateTrans(self,trans):
		tmp = []
		itr = 0
		for i in range(len(trans)):
			if itr == 0:
				y = trans[i].split(" ")
				num_trans = int(y[1])
				self.transNames.append(y[0])
				self.tmpVariables.append({})
				itr += 1
			elif num_trans == itr:
				tmp.append(trans[i])
				self.trans.append(tmp)
				tmp = []
				itr = 0
			else:
				tmp.append(trans[i])
				itr += 1

	def processQuery(self,query,i):
		if query.startswith('READ'):
			zend = query.find(")")
			ins = query[query.find("(") + 1 : zend]
			var_from_read = ins.split(',')[0]
			var_to_read = ins.split(',')[1]
			# self.tmpVariables[i][var_to_read] = self.variables[var_from_read]
			if var_from_read not in self.memoryVariableNames:
				self.memoryVariableNames.append(var_from_read)
				self.memoryVariables[var_from_read] = self.variables[var_from_read]
				self.tmpVariables[i][var_to_read] = self.memoryVariables[var_from_read]	
			else:
				self.tmpVariables[i][var_to_read] = self.memoryVariables[var_from_read]	
				# print("#read1",self.memoryVariables)
				# print("#read2",self.memoryVariableNames)

		elif query.startswith('WRITE'):
			zend = query.find(")")
			ins = query[query.find("(") + 1 : zend]
			var_to_write = ins.split(',')[0]
			var_from_write = ins.split(',')[1]
			self.reportLog(i,var_to_write)
			# self.variables[var_to_write] = self.tmpVariables[i][var_from_write]
			if var_to_write not in self.memoryVariableNames:
				self.memoryVariableNames.append(var_to_write)
				self.memoryVariables[var_to_write] = self.tmpVariables[i][var_from_write]
				# print(self.memoryVariables)
				self.printMemVariables()
				# print("#write2",self.memoryVariableNames)
			else:
				self.memoryVariables[var_to_write] = self.tmpVariables[i][var_from_write]
				# print(self.memoryVariables)
				self.printMemVariables()
				# print("#write2",self.memoryVariableNames)	
			self.printVariables()


		elif query.startswith('OUTPUT'):
			if self.transPts[i] < len(self.trans[i])-1:
				trans_get = query[7]
				# if trans_get not in self.updateVariablesNames:
				# 	self.updateVariablesNames.append(trans_get)
				# if trans_get in self.updateVariablesNames:
				self.variables[trans_get] = self.memoryVariables[trans_get]
				# self.updateVariablesNames.remove(trans_get)
				pass
			else:
				fop.write("<COMMIT " + self.transNames[i] + ">" + '\n')
				# print("<COMMIT " + self.transNames[i] + ">")
				trans_get = query[7]
				# if trans_get not in self.updateVariablesNames:
				# 	self.updateVariablesNames.append(trans_get)
				# if trans_get in self.updateVariablesNames:
				self.variables[trans_get] = self.memoryVariables[trans_get]
				# self.updateVariablesNames.remove(trans_get)
				# print(self.memoryVariables)
				# if self.memoryVariables != {}:
				self.printMemVariables()
				# for i in range(len(self.variables)):
				# 	self.variables[self.variableNames[i]] = self.memoryVariables[self.variableNames[i]]
				self.printVariables()

		else:
			lhs = query.split("=")[0]
			ch = lhs[-1]
			rhs = query.split("=")[1].strip()
			if ch == ':':
				lhs = lhs[:-1]
			lhs = lhs.strip()
			for opr in ['+','*','/','-']:
				if opr in rhs:
					break

			rhs = self.calc(rhs,opr,i)
			self.tmpVariables[i][lhs] = rhs	

	def roundRobin(self):
		self.transPts = [0] * len(self.trans)
		i = 0
		g = True
		flag = True
		rr_iter = 0
		while (g):
			if rr_iter == 0:
				fop.write("<START " + str(self.transNames[i]) + ">" + '\n')
				# print("<START " + self.transNames[i]+">")
				# print(self.memoryVariables)
				self.printMemVariables()
				self.printVariables()

			for j in range(self.x):
				if self.transPts[i] < len(self.trans[i]):
					self.processQuery(self.trans[i][self.transPts[i]],i)
					# print(self.tmpVariables)
					self.transPts[i] += 1

			tot = len(self.transNames)
			i = (i+1)%tot
			flag = True
			if i == 0:
				rr_iter += 1
				lt = len(self.transPts)
				for j in range(lt):
					lt1 = len(self.trans[j])
					if self.transPts[j] < lt1:
						flag = False
						break
					else:
						continue

				if flag:
					break

	def readTrans(self,filename):
		trans = []
		f = open(filename,'r')
		for line in f:
			if len(line.strip()) != 0:
				trans.append(line.strip())

		self.processVariables(trans[0])
		trans = trans[1:]
		self.seperateTrans(trans)

if __name__ == '__main__':
	log = Logging((int(sys.argv[2])))
	log.readTrans(sys.argv[1])
	# print(log.tmpVariables)
	# print(log.variables)
	# print(log.transPts)
	# print(log.transNames)
	log.roundRobin()