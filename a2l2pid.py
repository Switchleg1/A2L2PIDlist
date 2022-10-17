import sys
import csv

pidList = []

def findPID(name):
    index = 0
    for pid in pidList:
        if pid["Address"] == name:
            return index

        index += 1

    return -1
        

with open(sys.argv[2], "r", encoding="utf-8-sig", errors="surrogateescape") as templateFile:
    templateList = csv.DictReader(templateFile)
    for pid in templateList:
        pidList.append(pid)
        
with open(sys.argv[1], "r", encoding="utf-8-sig", errors="surrogateescape") as a2lFile:
    currentState = 0
    variablePos = -1
    variableName = ""
    a2lLines = a2lFile.readlines()
    for currentLine in a2lLines:
            
        if currentState == 0:
            currentLine = currentLine.strip()
            beginPos = currentLine.find("/begin")
            measurePos = currentLine.find("MEASUREMENT")
            charPos = currentLine.find("CHARACTERISTIC")
            if beginPos == 0:
                if measurePos >= 0:
                    variableName = currentLine[measurePos + 12:]
                elif charPos >= 0:
                    variableName = currentLine[charPos + 15:]

                variablePos = findPID(variableName)
                if variablePos >= 0:
                    currentState = 1
                else:
                    variablePos = 0
                    variableName = ""

        elif currentState == 1:
            currentLine = currentLine.strip()
            beginPos = currentLine.find("/begin")
            if beginPos == 0:
                currentState = 2

        elif currentState == 2:
            currentLine = currentLine.strip()
            addPos = currentLine.find("0x")
            if addPos == 0:
                pidList[variablePos]["Address"] = currentLine
                currentState = 0

with open(sys.argv[3], "w", newline='') as outputFile:
    outputHeader = ["Name", "Unit", "Equation", "Format", "Address", "Length", "Signed", "ProgMin", "ProgMax", "WarnMin", "WarnMax", "Smoothing", "Enabled", "Tabs", "Assign To"]
    outputCSV = csv.DictWriter(outputFile, fieldnames=outputHeader)
    outputCSV.writeheader()
    for pidTemp in pidList:
        outputCSV.writerow(pidTemp)
        
              
            
            
