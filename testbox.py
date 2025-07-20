import serial.tools.list_ports
from projectFileReader import *
import subprocess

class Testbox():

    def __init__(self, testPath):
        self.testPath = testPath
        self.projectFileReader = ProjectFileReader(testPath)
        self.testbox_port = None

    # Funktion zum Finden des Testbox-Ports
    # Diese Funktion durchsucht alle seriellen Ports und gibt den Port zurück, der das Pyboard enthält.
    def init(self):
        print("Suche nach Testbox...")
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(f"Port {port.device} - {port.description}")
            if "Pyboard" in port.description:
                self.testbox_port = port.device
                print(f"Testbox found at {self.testbox_port}")
                return True
        return False

    def copyTestFiles(self):
        if not self.testbox_port:
            print("Error: No Testbox port set. Please initialize Testbox first.")
            return False
        
        fileList = self.projectFileReader.getListOfFilesToCopy()
        print(f"Copying {len(fileList)} test files from {self.testPath} to Testbox...")

        for file in fileList:
            print(f"  Copying {file}...")
            
            command = f"mpremote connect {self.testbox_port} fs cp {self.testPath}/{file} :{file}"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            if result.returncode == 0:
                print("    OK")
            else:
                print(f"    Error {result.stderr}")
                return False

        print("All testfiles copied successfully.")
        return True