from testbox import Testbox
import sys
import os

if __name__ == "__main__":

    testPath = os.getenv("TEST_PROJECT_FOLDER")

    if(testPath is None):
        print("Error: No Test project folder defined. Set environment variable with name 'TEST_PROJECT_FOLDER'.")
        sys.exit(1)

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

    if not os.path.exists(f"repo/{testPath}/Reports"):
        os.makedirs(f"repo/{testPath}/Reports")

    with open("Reports/Testreport.html", "w", encoding="utf-8") as f:
        f.write(htmlReport)

    if(result == False):
        sys.exit(1)
    else:    
        sys.exit(0)