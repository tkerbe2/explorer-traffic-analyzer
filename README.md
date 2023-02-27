# Explorer Data Analyzer

Explorer Data Analzyer is a Python script that can be used to analyze raw Explorer data from the illumio Core platform.
The purpose of this tool is to help people identify particular traffic patterns for the purpose of building Micro-Segmentation policies.

# Installation

This script can be used as a simple python file or you can utilize the executable as an all-in-one package. Keep in mind there are variables
you will want to change to customize your tool before you make it an executable. 

This tool will look for an list the following illumio explorer data information:
- Highest, lowest, mean, and total flow count
- Traffic with a providing process
- Traffic with a providing user
- Provider port information
- SSH and RDP traffic observed
- F5 Self-IPs for a range you need to specify (by default .5-.10)
- Application Deployment example application with example application labels for Jenkins and uDeploy
- Ports with 1000+ flows seen
- Scan traffic for a presented range of ports (example provided)

The variables and pieces of code you will want to customize are marked with "## CHANGE NEEDED ##"


# Usage

When you first run this script a python UI should open and ask for an Employee ID, App ID, and file from a selector.
When the script executes successfully it will dump the output files into the directory it lives in.

The output files will be nameda accordingly with an example application ID of 123456:

AnalysisReport-123456, HighFlowsReport-123456, ScanDetectReport-123456

# Contributing

Pull requests are welcome. This script can be freely used, distributed, and modified by anyone.
