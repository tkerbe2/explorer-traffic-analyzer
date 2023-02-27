import pandas as pd
import re
import PySimpleGUI as sg


# This script was created by tkerbe2 / Taylor Kerber.
# This script can be modified, used, and distributed by anyone freely.
# Taylor Kerber does not offer any support or warranty for this script.
# Taylor Kerber is not responsible for any monetary or non-monetary damages that usage or misusage of this script may cause
# The user of this script acknowledges and accepts all risks and responsibilities
# Last updated 01/24/2023
# Main version tool number increment is for large feature sets
# Minor version tool number increment is for large updates or additional functions




# Change this variable to change tool version
## CHANGE NEEDED ##
toolVer = "1.6"


# Main function below
def explorerAnalysis():
    #df_csv = pd.read_csv('trafficdata.csv')
    pd.options.display.max_rows = 9999
    sg.theme('DarkTeal5')

    # This builds the very basic structure of the UI using the PySimpleGUI

    explorerAnalysisGUI = [
        [sg.Text('Please enter the following information...')],
        [sg.Text("Choose a file: "), sg.InputText(), sg.FileBrowse()],
        # [sg.Text('Enter your filename', size=(15, 1)), sg.InputText()],
        [sg.Text('Enter your application ID', size=(15, 1)), sg.InputText()],
        [sg.Text('Enter your employee ID or #', size=(18, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]

    # This reads values from input

    window = sg.Window('Explorer Data Analysis Helper', explorerAnalysisGUI)
    event, values = window.read()

    # This is the CSV file you are importing into the tool
    csvFile = values[0]

    # This is an application ID - some organizations label internal applications with ID numbers
    appID = values[1]

    # This is for employee ID or employee number
    empID = values[2]

    window.close()



    # Pandas opens the CSV to read

    df_csv = pd.read_csv(csvFile)

    ## CHANGE NEEDED ##
    # Regex patterns for IPs defined below
    # Keep in mind that these most likely need to be changed for specifc network architecture
    # For example some networks use .5 - .9 IP addresses on their network for load balancer Self-IPs
    # Other networks may use totally random IP addresses that cannot be handled with regex

    IDpattern = re.compile(('''\d{1,8}'''))
    F5IPpattern = re.compile('''((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}([4-7]\Z)''')
    nonF5IP = []
    F5IP = []

    # You can create IP lists for known network load balancer IPs and then let the script search for them as consumers
    # Below are just two example IP list names for illumio

    ## CHANGE NEEDED ##
    F5ipList = ["IL:US-MAIN", "IL:APAC-MAIN"]


    # Gathering data from the csv file


    # Below is the if statement that checks for a valid application ID and employee ID and uses pandas to create lists of values from traffic data

    if empID != "" and IDpattern.match(empID) and appID != "" and IDpattern.match(appID):
        maxFlow = df_csv['Num Flows'].max()
        minFlow = df_csv['Num Flows'].min()
        sumFlow = df_csv['Num Flows'].sum()
        meanFlow = int(df_csv['Num Flows'].mean())
        providerProcess = df_csv['Providing Process'].unique()
        providerUser = df_csv['Providing Username'].unique()
        providerIP = df_csv['Provider IP'].unique()
        consumerIP = df_csv['Consumer IP'].unique()
        consumerIPlist = df_csv['Consumer IPList'].unique()
        providerIPcount = len(providerIP)
        providerProcesscount = len(providerProcess)
        providerUsercount = len(providerUser)
        ports = df_csv['Port']


        # This opens and creates the output file

        outputFile = open("AnalysisReport-" + appID + ".txt", "w")
        outputFileHighFlow = open("HighFlowsReport-" + appID + ".txt", "w")
        outputFileScanDetect = open("ScanDetectReport-" + appID + ".txt", "w")

        # This writes header info for the main output file

        outputFile.write("_____________________________________________________________________________________________\r\n")
        outputFile.write("Analysis for AppID: " + str(appID) + "\r\n")
        outputFile.write("Prepared for Employee: " + str(empID) + "\r\n")
        outputFile.write("Tool version: " + toolVer + "\r\n" + "\r\n")
        outputFile.write("_____________________________________________________________________________________________\r\n")

        # This writes header info for the scan detection output file

        outputFileScanDetect.write("_____________________________________________________________________________________________\r\n")
        outputFileScanDetect.write("Analysis for AppID: " + str(appID) + "\r\n")
        outputFileScanDetect.write("Prepared for Employee: " + str(empID) + "\r\n")
        outputFileScanDetect.write("Tool version: " + toolVer + "\r\n")
        outputFileScanDetect.write("_____________________________________________________________________________________________\r\n")

        # This writes header info for the high flow count output file

        outputFileHighFlow.write("_____________________________________________________________________________________________\r\n")
        outputFileHighFlow.write("Analysis for AppID: " + str(appID) + "\r\n")
        outputFileHighFlow.write("Prepared for Employee: " + str(empID) + "\r\n")
        outputFileHighFlow.write("Tool version: " + toolVer + "\r\n")
        outputFileHighFlow.write("_____________________________________________________________________________________________\r\n")

        outputFile.write("Flows Seen __________________________________________________________________________________\r\n")
        outputFile.write("_____________________________________________________________________________________________\r\n" + "\r\n")
        outputFile.write("Highest flow count seen was " + str(maxFlow) + " flows\r\n")
        outputFile.write("Lowest flow count seen was " + str(minFlow) + " flows\r\n")
        outputFile.write("Mean flow count for this capture was " + str(meanFlow) + " flows\r\n")
        outputFile.write("There are a total of " + str(sumFlow) + " flows\r\n" + "\r\n")

        # This writes process info on the main output file

        outputFile.write("_____________________________________________________________________________________________\r\n")
        outputFile.write("Providing Processes Seen ____________________________________________________________________\r\n")
        outputFile.write("_____________________________________________________________________________________________\r\n" + "\r\n")
        outputFile.write("There are (" + str(providerUsercount) + ") unique provider processes seen in this capture:\r\n" + "\r\n")

        # The loop below looks for users and writes to the main output file

        for user in providerUser:
            if user != None:
                outputFile.write(str(user) + "\r\n")
            else:
                outputFile.write("Other non valid user found")

        # This is the providing users section of the main output file

        outputFile.write("_____________________________________________________________________________________________\r\n")
        outputFile.write("Providing Users Seen ________________________________________________________________________\r\n")
        outputFile.write("_____________________________________________________________________________________________\r\n" + "\r\n")
        # print("There are " + str(providerUsercount) + " unique provider processes seen in this Explorer data:")
        outputFile.write("There are (" + str(providerProcesscount) + ") unique provider users seen in this capture:\r\n" + "\r\n")
        for process in providerProcess:
            if process != None:
                # print(process)
                outputFile.write(str(process) + "\r\n")
            else:
                # print("Other non valid process found")
                outputFile.write("Other non valid process found" + "\r\n")

        # Values below are common ports used by Tanium peer-to-peer scanning tools

        portSummary = df_csv.loc[(df_csv['Providing Process'].notnull()) & (df_csv['Port'] != 0), ['Port', 'Providing Process']]
        highFlowSummary = df_csv.loc[(df_csv['Num Flows'].notnull()) & (df_csv['Num Flows'] > 1000) & (df_csv['Port'] != 0), ['Port', 'Num Flows', 'Providing Process']]
        userSSHSummary = df_csv.loc[(df_csv['Consuming Userrname'].notnull()) & (df_csv['Port'] == 22), ['Port', 'Consuming Userrname', 'Consumer IPList' ]]
        userRDPSummary = df_csv.loc[(df_csv['Consuming Userrname'].notnull()) & (df_csv['Port'] == 3389), ['Port', 'Consuming Userrname', 'Consumer IPList']]

        ## CHANGE NEEDED ##
        # Jenkins and uDeploy are commonly used in environments and can be used as an example of traffic pattern to search for
        # App label names will most likely need to be changed below to work in your environment

        uDeploySummary = df_csv.loc[(df_csv['Consumer App'].notnull()) & (df_csv['Consumer App'] == "A:uDeploy"),
                                   ['Consumer App', 'Port', 'Provider IP' ]]
        jenkinsSummary = df_csv.loc[(df_csv['Consumer App'].notnull()) & (df_csv['Consumer App'] ==
                                    "A:Jenkins"),['Consumer App', 'Port', 'Provider IP' ]]

        # These are some common scan ports that can be used in Tanium
        # You will want to change the values in this list or simply create an external list and import it

        ## CHANGE NEEDED ##
        knownScanPorts = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 443, 445, 1173, 17472, 3306, 3389, 5060, 5061, 8080, 9100]

        # This is the providing port information that writes to the main output file

        outputFile.write("_____________________________________________________________________________________________\r\n")
        outputFile.write("Provider Port Information ___________________________________________________________________\r\n")
        outputFile.write("_____________________________________________________________________________________________\r\n" + "\r\n")
        outputFile.write("The following ports with listening processes were found and the app owner should be made aware of them:\r\n" + "\r\n")

        summaryPortvalues = portSummary.value_counts()
        summaryUserSSHvalues = userSSHSummary.value_counts()
        summaryUserRDPvalues = userRDPSummary.value_counts()
        summaryhighFlowvalues = highFlowSummary.value_counts()
        summaryUdeployvalues = uDeploySummary.value_counts()
        summaryJenkinsvalues = jenkinsSummary.value_counts()

        outputFile.write(str(summaryPortvalues) + "\r\n")
        outputFile.write("! For both Windows and Linux workloads you may see some system processes !\r\n")
        outputFile.write("! For Linux workloads you want to look for things like the app name or for example Java - which is commonly used !\r\n")
        outputFile.write("! You can ignore nan and root !\r\n")

        # This is writing the high flow port summary data to the high flow output file

        outputFileHighFlow.write("_____________________________________________________________________________________________\r\n")
        outputFileHighFlow.write("Ports with 1000+ Flows ______________________________________________________________________\r\n")
        outputFileHighFlow.write("_____________________________________________________________________________________________\r\n")
        outputFileHighFlow.write("The following ports have a flow count of over 1000 in this capture:\r\n" + "\r\n")
        outputFileHighFlow.write("! These port flows should be further investigated !\r\n" + "\r\n")
        outputFileHighFlow.write(str(summaryhighFlowvalues) + "\r\n")

        # If SSH or RDP ports were seen they will be written to the main output file under this section

        outputFile.write("_____________________________________________________________________________________________\r\n")
        outputFile.write("User SSH & RDP Information___________________________________________________________________\r\n")
        outputFile.write("_____________________________________________________________________________________________\r\n" + "\r\n")

        if len(summaryUserRDPvalues) == 0:
            outputFile.write("No RDP traffic observed in this capture" + "\r\n")
        else:
            outputFile.write(str(summaryUserRDPvalues) + "\r\n")

        if len(summaryUserSSHvalues) == 0:
            outputFile.write("No SSH traffic observed in this capture" + "\r\n")
        else:
            outputFile.write(str(summaryUserSSHvalues) + "\r\n")

        # This will write scan detection header info to the scan detection output file

        outputFileScanDetect.write("_____________________________________________________________________________________________\r\n")
        outputFileScanDetect.write("Scan Detection ______________________________________________________________________________\r\n")
        outputFileScanDetect.write("_____________________________________________________________________________________________\r\n")
        outputFileScanDetect.write("! Scan traffic should always be further investigated !\r\n" + "\r\n")

        # If you have load balancers on your network and are looking for the backend load balancer IPs in traffic data you can see that here

        outputFile.write("_____________________________________________________________________________________________\r\n")
        outputFile.write("Load Balancing Information___________________________________________________________________\r\n")
        outputFile.write("_____________________________________________________________________________________________\r\n" + "\r\n")

        for IP in consumerIP:
            if F5IPpattern.match(str(IP)) or F5IPpattern2.match(str(IP)) and str(IP) != "":
                F5IP.append(str(IP))
            else:
                nonF5IP.append(str(IP))

        if len(F5IP) == 0:
            outputFile.write("No Self-IPs observed in this capture" + "\r\n")
        else:
            outputFile.write("The following potential load balancer F5 Self-IPs were identified as sources:\r\n" + "\r\n")
            for IP in F5IP:
                outputFile.write(str(IP) + "\r\n")



        outputFile.write("_____________________________________________________________________________________________\r\n")
        outputFile.write("Application Deployment_______________________________________________________________________\r\n")
        outputFile.write("_____________________________________________________________________________________________\r\n" + "\r\n")

        ## CHANGE NEEDED ##

        if len(summaryJenkinsvalues) == 0:
            outputFile.write("No Jenkins traffic observed in this capture" + "\r\n")
        else:
            outputFile.write(str(summaryJenkinsvalues) + "\r\n")

        if len(summaryUdeployvalues) == 0:
            outputFile.write("No uDeploy traffic observed in this capture" + "\r\n")
        else:
            outputFile.write(str(summaryUdeployvalues) + "\r\n")




      # Below is the scan check feature that looks for all ports matching in knownscanPorts and compares against what is seen

        scancheck = all(port in ports for port in knownScanPorts)

        if scancheck is True:
            outputFileScanDetect.write("Known Tanium scan ports: " + str(knownScanPorts) + "\r\n")
            outputFileScanDetect.write("All of the following scan ports have been seen indicating that scan traffic is highly likely " + "\r\n")
        else:
            outputFileScanDetect.write("Known scan ports: " + str(knownScanPorts) + "\r\n")
            outputFileScanDetect.write("No strong indication of a scan was seen as none or too few scan ports were identified" + "\r\n")



        outputFile.close()
        outputFileHighFlow.close()
        outputFileScanDetect.close()

    else:
        print("Invalid input")


explorerAnalysis()
