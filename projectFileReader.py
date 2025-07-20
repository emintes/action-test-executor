from logging import root
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
        self.readProjectFile()

    def readProjectFile(self):
        # Hier könnte der Code zum Lesen der Projektdatei stehen
        # Zum Beispiel:
        tree = ET.parse(self.projectPath + '/project.etp')
        root = tree.getroot()

        insideTeststepList = False

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