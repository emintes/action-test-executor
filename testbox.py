from time import time
import serial.tools.list_ports
import serial
from projectFileReader import *
import subprocess
import time
from testreport import Testreport

class Testbox():

    def __init__(self, testPath):
        self.testPath = testPath
        self.projectFileReader = ProjectFileReader(testPath)
        self.testbox_port = None
        self.testresport = Testreport(self.projectFileReader.getProjectName())

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
        print("Restart Testbox...")
        
        with serial.Serial(self.testbox_port, 115200, timeout=2) as ser:
            ser.write(b'import machine\n')
            ser.write(b'machine.reset()\n')

        time.sleep(3)
        return True
    
    def runTest(self):
        if not self.testbox_port:
            print("Error: No Testbox port set. Please initialize Testbox first.")
            return False

        with serial.Serial(self.testbox_port, 115200, timeout=2) as ser:
            ser.readall()
            ser.write(b'tfc.start()\n')
            
            start_time = time.time()
            print("Empfange Daten von Testbox:")
            while time.time() - start_time < 5:  # 5 Sekunden lang lesen
                line = ser.readline()
                if line:
                    self.testresport.addEntryByString(line.decode(errors='ignore').strip())

            return True