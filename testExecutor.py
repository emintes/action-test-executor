from testbox import Testbox
import sys
import subprocess

# Beispielnutzung:
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Error: Parameter missing. Usage: python findTestbox.py <testPath>")
        print("<testPath> is the path to the folder where the testproject is placed")
        sys.exit(1)

    testPath = sys.argv[1]

    testbox = Testbox()
    testboxFound = testbox.init()
    if not testboxFound:
        print("Error: No Testbox found! Please connect the Testbox and try again.")
        sys.exit(1)

    fileList = testbox.getListOfFilesToCopyFromProjectFile()
    
    #result = subprocess.run(["mpremote connect " + pyboard_port + " fs cp entrypoint.sh :entrypoint.sh"], capture_output=True, text=True, shell=True)
    # Rückgabecode
    #print("Return code:", result.returncode)

    # Standardausgabe
    #print("stdout:", result.stdout)

    # Fehlerausgabe
    #print("stderr:", result.stderr)

        
    
    print("FERTIG")
    sys.exit(1)