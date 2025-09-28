from logging import root
import os
import sys
import xml.etree.ElementTree as ET

class Teststep:
    def __init__(self, active, name, numberOfRuns=1):
        self.active = active
        self.name = name
        self.numberOfRuns = numberOfRuns

class ProjectFileReader:
    def __init__(self, projectPath, projectFile):
        self.projectPath = projectPath
        self.projectFile = projectFile
        self.teststeps = []
        self.fileList = []
        self.commands = ["", "", ""]
        self.commandArgs = ["", "", ""]
        self.showConsoleOutput = [True, True, True]
        self.readProjectFile()

    def readProjectFile(self):

        if not os.path.isfile(self.projectPath + '/' + self.projectFile):
            print(f"Error: No project-file found in {self.projectPath}/{self.projectFile}")
            sys.exit(1)

        tree = ET.parse(self.projectPath + '/' + self.projectFile)
        root = tree.getroot()

        self.projectName = root.find('ProjectName').text or ""
        self.commands[0] = root.find('CmdExeCommand1').text or ""
        self.commands[1] = root.find('CmdExeCommand2').text or ""
        self.commands[2] = root.find('CmdExeCommand3').text or ""
        self.commandArgs[0] = root.find('CmdExeParameter1').text or ""
        self.commandArgs[1] = root.find('CmdExeParameter2').text or ""
        self.commandArgs[2] = root.find('CmdExeParameter3').text or ""
        self.showConsoleOutput[0] = root.find('CmdShowConsole1').text=="true"
        self.showConsoleOutput[1] = root.find('CmdShowConsole2').text=="true"
        self.showConsoleOutput[2] = root.find('CmdShowConsole3').text=="true"   

        for teststep in root.iter('Teststep'):
            teststep_active = teststep.find('Active').text.lower() == 'true'
            teststep_name = teststep.find('Name').text
            teststep_number_of_runs = int(teststep.find('NumberOfRuns').text)
            print(str(teststep_active) + " - " + teststep_name + " - " + str(teststep_number_of_runs))
            
            self.teststeps.append(Teststep(teststep_active, teststep_name, teststep_number_of_runs))

    def getListOfFilesToCopy(self):
        self.fileList = []
        for file in os.listdir(self.projectPath):
            if file.endswith(".py"):
                self.fileList.append(file)

        return self.fileList
    
    def getCheckboxConfigString(self):
        result = self.projectName + "\r\n"
        for step in self.teststeps:
            result += f"{step.active};{step.numberOfRuns};{step.name}\r\n"
        
        return result