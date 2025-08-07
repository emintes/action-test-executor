import os
from datetime import datetime
from tracedrawer import TraceDrawer

class Teststep():
    def __init__(self, name):
        self.name = name
        self.result = ""
        self.testresults = []


class Testresult():
    def __init__(self, description):
        self.description = description
        self.result = ""
        self.expected = ""
        self.value = ""

    def __str__(self):
        color = ""
        resetColor = "\033[0m"
        if self.result.upper() == "PASSED":
            color = "\033[92m"  # Grün
        elif self.result.upper() == "FAILED":
            color = "\033[91m"  # Rot
        return f"{self.description[:40]:<40} | {self.value[:13]:<13} | {self.expected[:25]:<25} | {color}{self.result}{resetColor}"

def printTableHeader():
    print(f"{'Description':<40} | {'Value':<13} | {'Expected':<25} | {'Result':<10}")
    print("-" * 97)

class Testreport:
    def __init__(self, title):
        self.title = title
        self.teststeps = []
        self.testresult = "Not Started"
        self.boxSerialNumber = ""
        self.boxHWVersion = ""
        self.boxSWVersion = ""
        self.passedCnt = 0
        self.failedCnt = 0
        self.currentTeststep = None
        self.consoleOutputs = []
        self.traceDrawer = TraceDrawer()
        self.testresultPictures = []

    def __str__(self):
        return f"{self.title} - Serial: {self.boxSerialNumber}, HW: {self.boxHWVersion}, SW: {self.boxSWVersion}, Result: {self.testresult}"
    
    def updateTestresult(self, result):
        if result == "PASSED":
            self.passedCnt += 1
        elif result == "FAILED":
            self.failedCnt += 1
        
        if self.passedCnt + self.failedCnt > 0:
            if self.failedCnt > 0:
                self.testresult = "FAILED"
            else:
                self.testresult = "PASSED"
        else:
            self.testresult = "Not Started"

    def addEntryByString(self, entry):
        parts = entry.split(";")
        if len(parts) == 0:
            print(f"Error: Invalid entry format: {entry}")
            return
        
        if(parts[0].strip() == ""):
            #ignore empty lines
            return
        
        if "[START TEST]" in parts[0]:
            print(f"Starting Test: {self.title}")
            self.teststeps = []
            self.currentTeststep = None
            self.passedCnt = 0
            self.failedCnt = 0
            self.testresult = "Running"

        elif "[RUN STEP]" in parts[0]:
            teststep = Teststep(name=parts[1].strip())
            self.teststeps.append(teststep)
            self.currentTeststep = teststep
            print("")
            print("=================================================================================================")
            print(f"Running Teststep: {teststep.name}")
            print("=================================================================================================")
            printTableHeader()

        elif "[END STEP]" in parts[0].strip():
            print("-------------------------------------------------------------------------------------------------")
            self.currentTeststep.result = parts[2].strip()
            color = ""
            resetColor = "\033[0m"
            if self.currentTeststep.result.upper() == "PASSED":
                color = "\033[92m"  # Grün
            elif self.currentTeststep.result.upper() == "FAILED":
                color = "\033[91m"  # Rot
            print(f"Result of Teststep: {color}{self.currentTeststep.result}{resetColor}")
            print("")

        elif "[BOX INFO]" in parts[0]:
            print("Testbox Infos:")
            self.boxSerialNumber = parts[1].strip()
            self.boxHWVersion = parts[2].strip()
            self.boxSWVersion = parts[3].strip()
            print(f"  Serialnumber:     {self.boxSerialNumber}")
            print(f"  Hardware Version: {self.boxHWVersion}")
            print(f"  Software Version: {self.boxSWVersion}")

        elif "[RESULT MINMAX]" in parts[0]:
            result = Testresult(description=parts[1].strip())
            if (parts[2] == ""):    #only max value is given
                result.expected = "<= " + parts[3] + " " + parts[5]
            elif (parts[3] == ""):    #only min value is given
                result.expected = ">= " + parts[2] + " " + parts[5]
            else:
                #min and max value is given
                result.expected = parts[2] + " - " + parts[3] + " " + parts[5]
            
            result.value = parts[4].strip() + " " + parts[5].strip()
            result.result = parts[6].strip()

            self.currentTeststep.testresults.append(result)
            self.updateTestresult(result.result)
            print(result)

        elif "[RESULT VALUE]" in parts[0]:
            result = Testresult(description=parts[1].strip())
            result.expected = parts[2].strip() + " " + parts[4].strip()
            result.value = parts[3].strip() + " " + parts[4].strip()
            result.result = parts[5].strip()

            self.currentTeststep.testresults.append(result)
            self.updateTestresult(result.result)
            print(result)         

        elif "[RESULT STRING]" in parts[0] or "[RESULT BOOL]" in parts[0]:
            result = Testresult(description=parts[1].strip())
            result.expected = parts[2].strip()
            result.value = parts[3].strip()
            result.result = parts[4].strip()

            self.currentTeststep.testresults.append(result)
            self.updateTestresult(result.result)
            print(result)

        elif "[INFO VALUE]" in parts[0]:
            result = Testresult(description=parts[1].strip())
            result.expected = "-"
            result.value = parts[2].strip()
            result.result = "INFO ONLY"

            self.currentTeststep.testresults.append(result)
            self.updateTestresult(result.result)
            print(result)

        elif "[APPEND TRACE]" in parts[0]:
            description = parts[1]

            self.traceDrawer.create_new_chart(description)

            for i in range(0, len(parts) - 2, 3):
                timestep_ms = float(parts[i + 3]) / 1000.0
                self.traceDrawer.add_data(parts[i + 2], timestep_ms, parts[i + 4])

            picture = self.traceDrawer.get_chart_bitmap()

            self.testresultPictures.append(picture)

        elif "[TEST FINISHED]" in parts[0]:

            print(f"Test finished (duration: {float(parts[2])/1000.0} sec)")

            self.printConsoleOutput()

            color = ""
            resetColor = "\033[0m"
            if self.testresult.upper() == "PASSED":
                color = "\033[92m"  # Grün
            elif self.testresult.upper() == "FAILED":
                color = "\033[91m"  # Rot
            print("=================================================================================================")
            print(f"Test finished with result: {color}{self.testresult}{resetColor}")
            print(f"Passed: {self.passedCnt}, Failed: {self.failedCnt}")
            print("=================================================================================================")

        elif "[TEST ABORTED]" in parts[0]:
            print(f"Test aborted")

            self.printConsoleOutput()

            color = ""
            resetColor = "\033[0m"
            color = "\033[91m"  # Rot
            print("=================================================================================================")
            print(f"Testresult: {color}{self.testresult}{resetColor}")
            print(f"Passed: {self.passedCnt}, Failed: {self.failedCnt}")
            print("=================================================================================================")

        else:
            if self.currentTeststep:
                self.consoleOutputs.append(entry)


    def version_info_to_html(self, serialNumber, hwVersion, swVersion):
        result = ""
        result += "<table>\n"
        result += f"<tr><td><b>Serial Number</b></td><td>{serialNumber}</td></tr>\n"
        result += f"<tr><td><b>Hardware Version</b></td><td>{hwVersion}</td></tr>\n"
        result += f"<tr><td><b>Software Version</b></td><td>{swVersion}</td></tr>\n"
        result += "</table>\n"
        return result

    def convert_bitmap_to_base64(self, png_bytes: bytes):
        import base64
        return base64.b64encode(png_bytes).decode('utf-8')
    
    def createHtmlReport(self, template):
        if not os.path.exists(template):
            print("Error: Template file for testreport not found.")
            return ""

        with open(template, "r", encoding="utf-8") as f:
            html = f.read()

        # Test Infos (header)
        html = html.replace("###TEST_TITLE###", self.title)
        html = html.replace("###TESTER_NAME###", "Automated Test")
        testdateTime = getattr(self, "testdateTime", datetime.now())
        html = html.replace(
            "###TEST_DATETIME###",
            testdateTime.strftime("%Y-%m-%d %H:%M")
        )

        # Used Devices
        used_devices = ""
        used_devices += '<div class="contentbox">'
        used_devices += '<div class="contentbox_headline">Checkbox</div>'
        used_devices += '<div class="contentbox_content">'
        used_devices += self.version_info_to_html(self.boxSerialNumber, self.boxHWVersion, self.boxSWVersion)
        used_devices += '</div></div>\n'

        #for i, info in enumerate(getattr(self, "rs485Infos", [])):
        #    used_devices += '<div class="contentbox">'
        #    used_devices += f'<div class="contentbox_headline">RS485 Module {i+1}</div>'
        #    used_devices += '<div class="contentbox_content">'
        #    used_devices += self.version_info_to_html(info)
        #    used_devices += '</div></div>\n'

        #for i, info in enumerate(getattr(self, "powerIOInfos", [])):
        #    used_devices += '<div class="contentbox">'
        #    used_devices += f'<div class="contentbox_headline">Power IO Module {i+1}</div>'
        #    used_devices += '<div class="contentbox_content">'
        #    used_devices += self.version_info_to_html(info)
        #    used_devices += '</div></div>\n'

        html = html.replace("###USED_DEVICES###", used_devices)

        # Testresults
        result_rows = ""
        passed_teststeps = 0
        failed_teststeps = 0
        passed_checks = 0
        failed_checks = 0

        for teststep in self.teststeps:
            result_rows += "<tr>"
            result_rows += f'<td colspan=3 class="StepDescription">{teststep.name}</td>'
            if teststep.result == "PASSED":
                result_rows += '<td class="PassedStep">PASSED</td>'
                passed_teststeps += 1
            elif teststep.result == "FAILED":
                result_rows += '<td class="FailedStep">FAILED</td>'
                failed_teststeps += 1
            else:
                result_rows += f'<td>{teststep.result}</td>'
            result_rows += "</tr>"

            for testresult in teststep.testresults:
                result_rows += "<tr>"
                result_rows += f'<td class="ResultDescription">{testresult.description}</td>'
                result_rows += f'<td class="ResultExpected">{testresult.expected}</td>'
                result_rows += f'<td class="ResultValue">{testresult.value}</td>'
                if testresult.result == "PASSED":
                    result_rows += '<td class="PassedCheck">PASSED</td>'
                    passed_checks += 1
                elif testresult.result == "FAILED":
                    result_rows += '<td class="FailedCheck">FAILED</td>'
                    failed_checks += 1
                else:
                    result_rows += '<td class="PassedCheck"></td>'
                result_rows += "</tr>"

        html = html.replace("###RESULT_TABLE_ROWS###", result_rows)

        # Result Summary
        summary = ""
        if passed_checks + failed_checks == 0:
            result_quote = 1.0
        else:
            result_quote = passed_checks / (passed_checks + failed_checks)
        if failed_teststeps == 0:
            summary += '<div class="PassedLabel">Passed</div>'
        else:
            summary += '<div class="FailedLabel">Failed</div>'
        summary += f"<b>{result_quote * 100:.0f}% passed</b><br/>"
        summary += f"{passed_teststeps} of {passed_teststeps + failed_teststeps} Teststeps were passed<br>"
        summary += f"{passed_checks} of {passed_checks + failed_checks} Value Checks were passed<br>"

        html = html.replace("###RESULT_SUMMARY###", summary)

        result_quote_int = int(round(result_quote * 100.0, 0))
        html = html.replace("###PASSED_PERCENT###", f"{result_quote_int:0}")
        html = html.replace("###FAILED_PERCENT###", f"{100 - result_quote_int:0}")

        appendix = ""
        for pic in getattr(self, "testresultPictures", []):
            b64_pic = self.convert_bitmap_to_base64(pic)
            appendix += f'<img alt="Appendix Image" src="data:image/png;base64,{b64_pic}" /><br>'

        html = html.replace("###APPENDIX###", appendix)

        return html

    def printConsoleOutput(self):
        if len(self.consoleOutputs) > 0:
            print("Console Outputs:")
            for output in self.consoleOutputs:
                print(f"    {output}")