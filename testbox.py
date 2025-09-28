from time import time
import serial.tools.list_ports
import serial
from projectFileReader import *
import subprocess
import time
from testreport import Testreport
import hashlib

class Testbox():

    def __init__(self, testPath, projectFile):
        self.testPath = testPath
        self.projectFile = projectFile
        self.projectFileReader = ProjectFileReader(testPath, projectFile)
        self.testbox_port = None
        self.testresport = Testreport(self.projectFileReader.projectName)
        

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
            
            command = f"mpremote connect {self.testbox_port} fs cp {self.testPath}/{file} :Tests/{file}"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            if result.returncode == 0:
                print("    OK")
            else:
                print(f"    Error {result.stderr}")
                return False

        # now the project - config file:
        print(f"  Copying project config file...")
        config_string = self.projectFileReader.getCheckboxConfigString()
        with open("testconfig.conf", "w", encoding="utf-8") as f:
            f.write(config_string)
        
        command = f"mpremote connect {self.testbox_port} fs cp testconfig.conf :Tests/testconfig.conf"
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

        with serial.Serial(self.testbox_port, 115200, timeout=5) as ser:
            ser.readall()
            ser.write(b'tfc.start()\n')
            
            print("Empfange Daten von Testbox:")
            while True:  # 5 Sekunden lang lesen
                line = ser.readline()
                if line:
                    line = line.decode(errors='ignore').strip()

                    if("[EXECUTE COMMAND]" in line):
                        parts = line.split(";")
                        cmdNumber = int(parts[1])-1     #array index is 0-based, command 1, 2, 3 --> array index 0, 1, 2
                        userArgs = parts[2]
                        command = self.projectFileReader.commands[cmdNumber]
                        args = self.projectFileReader.commandArgs[cmdNumber]
                        self.testresport.consoleOutputs.append(" ".join(["Executing command:", command, "with args:", args, userArgs]))

                        cmd = command + " " + args + " " + userArgs
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                        if(self.projectFileReader.showConsoleOutput[cmdNumber]==True):
                            self.testresport.consoleOutputs.append(result.stdout)
                            self.testresport.consoleOutputs.append(result.stderr)

                        ser.write(("tfc.setCommandExecutionResult(" + str(result.returncode) + ")\n").encode())
                    else:
                        self.testresport.addEntryByString(line)

                else:
                    break

            return (self.testresport.failedCnt == 0)
    
    def combine(a: str | None, b: str | None) -> str | None:
        parts = [x for x in (a, b) if x is not None]
        return " ".join(parts) if parts else None