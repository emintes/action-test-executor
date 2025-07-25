from testbox import Testbox
import sys
import os

# Beispielnutzung:
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Error: Parameter missing. Usage: python findTestbox.py <testPath>")
        print("<testPath> is the path to the folder where the testproject is placed")
        sys.exit(1)

    testPath = sys.argv[1]

    testbox = Testbox(f"repo/{testPath}")
    testboxFound = testbox.init()
    if not testboxFound:
        print("Error: No Testbox found! Please connect the Testbox and try again.")
        sys.exit(1)

    result = testbox.copyTestFiles()
    if(result == False):
        sys.exit(1)

    result = testbox.runTest()
    htmlReport = testbox.testresport.createHtmlReport("testreportTemplate.html")

    with open("Testreport.html", "w", encoding="utf-8") as f:
        f.write(htmlReport)

    if(result == False):
        sys.exit(1)
    else:    
        sys.exit(0)