from logging import root
import os
import sys
import xml.etree.ElementTree as ET

class Teststep:
    def __init__(self, active, name):
        self.active = active
        self.name = name

class ProjectFileReader:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.teststeps = []
        self.fileList = []
        self.commands = ["", "", ""]
        self.commandArgs = ["", "", ""]
        self.showConsoleOutput = [True, True, True]
        self.readProjectFile()

    def getProjectName(self):
        tree = ET.parse(self.projectPath + '/project.etp')
        root = tree.getroot()

        return root.find('ProjectName').text

    def readProjectFile(self):
        if not os.path.isfile(self.projectPath + '/project.etp'):
            print(f"Error: No project-file found in the test-project-folder ({self.projectPath}).")
            sys.exit(1)

        tree = ET.parse(self.projectPath + '/project.etp')
        root = tree.getroot()

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
            
            teststep_active = teststep.find('Active').text == 'true'
            teststep_name = teststep.find('Name').text
            teststep_name_parts = teststep_name.split(' ')

            self.teststeps.append(Teststep(teststep_active, teststep_name_parts[1]))

            if teststep_active:
                fileName = teststep_name_parts[0] + ".py"
                if fileName not in self.fileList:
                    self.fileList.append(fileName)

    def getListOfFilesToCopy(self):
        return self.fileList