import serial.tools.list_ports
import xml.etree.ElementTree as ET

class Testbox():
    def __init__(self):
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
                print(f"Testbox found at {pyboard_port}")
                return True
        return False

    def getListOfFilesToCopyFromProjectFile(self, testPath):
        try:
            tree = ET.parse(testPath + '/project.etp')
            root = tree.getroot()
            print("Project file read successfully.")
        except ET.ParseError as e:
            print(f"Error parsing project file: {e}")
            return None
        
                # Beispiel: Alle Elemente und deren Tag ausgeben
        for elem in root.iter():
            print(elem.tag, elem.text)

        return None

    def copyTestFiles(self, fileList):
        if not self.testbox_port:
            print("Error: No Testbox port set. Please initialize Testbox first.")
            return False
        
        print(f"Copying test files from {testPath} to Testbox...")



        # Hier könnte der Code zum Kopieren der Testdateien auf die Testbox stehen
        # Zum Beispiel:
        result = subprocess.run(["mpremote connect " + self.testbox_port + " fs cp " + testPath + " :"], capture_output=True, text=True, shell=True)
        
        if result.returncode != 0:
            print("Error copying files:", result.stderr)
            return False
        
        print("Test files copied successfully.")
        return True