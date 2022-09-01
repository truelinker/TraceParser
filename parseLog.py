import re
import os
import tqdm
import csv
import enumTrans
print (tqdm.__version__)


class ParseETL:

    _analyLines = []
    _subsearchList = []
    _rexSubSearchList = []

    def __init__(self, inputfile, outputfile):
        self._inputfile = inputfile
        self._outputfile = open(outputfile, "w")
        self._fileSize = os.path.getsize(self._inputfile)
        self._progress = 0

    def readProfile(self,profile):        
        with open(profile) as fp:
            search   = re.compile(r"(.*)SearchList(.*)")  
            skip     = re.compile(r"(.*)SkipList(.*)")
            searchList = []
            skipList = []
            searchindex = 0
            for line in fp:
                if(search.match(line)):
                    for line in fp:
                        if line == '\n':
                            break
                        elif re.match(r"#", line):
                            continue
                        line = line.strip()
                        inner_list  = line.split(',') 
                        n = len(inner_list)
                        if(n > 1):
                            condition = []                         
                            searchList.append("^(?=(.*?" + inner_list[0] + "))\\" + str(searchindex * 2 + 1) + "(.*)")
                            for index in range(0, n):
                                condition.append("(.*)" + inner_list[index] + "(.*)")
                            self._subsearchList.append(condition)
                        else:
                            searchList.append("^(?=(.*?" + inner_list[0] + "))\\" + str(searchindex * 2 + 1) + "(.*)")
                        searchindex = searchindex + 1

                if(skip.match(line)):
                    for line in fp:
                        if line == '\n':
                            break
                        line = line.strip()
                        inner_list  = line.split(',') 
                        n = len(inner_list)
                        for index in range(0, n):
                            skipList.append("^(?=(.*?" + inner_list[index] + "))\\" + str(index * 2 + 1) + "(.*)")
                
            self._rexSearchList = re.compile('|'.join(searchList))
            self._rexSkipList = re.compile('|'.join(skipList))
                 
    def examLines(self):
        found = False
        searchNum = len(self._subsearchList)
        for index in range (0, searchNum):
            searchItem = re.compile(self._subsearchList[index][0])
            if(searchItem.match(self._analyLines)):
                found = TRUE
                subSearchNum = len(self._subsearchList[index])
                for index2 in range (1, subSearchNum):
                    searchItem = re.compile(self._subsearchList[index][index2], re.MULTILINE|re.DOTALL)
                    if(searchItem.match(self._analyLines)):
                        if index2 == (subSearchNum - 1):
                            print(self._analyLines, end="", file=self._outputfile)
                    else:
                        break
        if found == False:
            print(self._analyLines, end="", file=self._outputfile)
    
    def writeFileClose(self):
        self._outputfile.close()

    def findLine(self):  
            num_lines = sum(1 for line in open(self._inputfile,'r'))
            with open(self._inputfile) as fp:
                outer = tqdm.tqdm(total=num_lines, desc='Analysing', position=0)
                for line in fp:
                    outer.update(1)
                    if(self._rexSearchList.match(line)):
                            self._analyLines = line
                            for line in fp:
                                outer.update(1)
                                if(self._rexSkipList.match(line)):
                                    self.examLines()
                                    self._analyLines = []
                                    if(self._rexSearchList.match(line)):
                                        self._analyLines = line
                                    else:
                                        break
                                else:
                                    self._analyLines = self._analyLines + line

                    else:
                        continue
                if(len(self._analyLines) == 0):
                    return
                if(self._rexSearchList.match(self._analyLines)):
                    self.examLines()

MyFile = 'LogExample.txt'  # Input file
GeneratedFile = MyFile + 'Filter.txt'  # Output file
GeneratedMsgIDFile = MyFile + 'FilterEnumID.txt'  # Output file


Profile = 'profile_a.txt'

parse = ParseETL(MyFile, GeneratedFile)
parse.readProfile(Profile)
parse.findLine()
parse.writeFileClose()

Enum = enumTrans.EnumParseClass()
Enum.coreEnumParse()
Enum.msgIdEnumParse()
Enum.ConvertEnumIdToMsgStr(GeneratedFile, GeneratedMsgIDFile)

