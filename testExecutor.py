from testbox import Testbox
import sys
import os
import stat

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

    testreportPath = f"repo/{testPath}/Reports"

    if not os.path.exists(testreportPath):
        os.makedirs(testreportPath)
        os.chmod(testreportPath, 0o777)

    with open(testreportPath+"/Testreport.html", "w", encoding="utf-8") as f:
        f.write(htmlReport)

    # Setze Rechte so, dass der Datei-Besitzer lesen & schreiben darf
    os.chmod(testreportPath+"/Testreport.html", 
        stat.S_IRUSR | stat.S_IWUSR |  # Besitzer lesen + schreiben
        stat.S_IRGRP | stat.S_IWGRP |  # Gruppe lesen + schreiben
        stat.S_IROTH | stat.S_IWOTH)   # Andere lesen + schreiben

    if(result == False):
        sys.exit(1)
    else:    
        sys.exit(0)