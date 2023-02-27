# Explorer Data Analyzer

Explorer Data Analzyer is a Python script that can be used to analyze raw Explorer data from the illumio Core platform.
The purpose of this tool is to help people identify particular traffic patterns for the purpose of building Micro-Segmentation policies.

# Installation

This script can be used as a simple python file or you can utilize the executable as an all-in-one package. Keep in mind there are variables
You will want to change to customize your tool before you make it an executable.  


# Usage

When you first run this script a python UI should open and ask for an Employee ID, App ID, and file from a selector.
When the script executes successfully it will dump the output files into the directory it lives in.
The output files will be nameda accordingly:
	- AnalysisReport-<application id>
	- HighFlowsReport-<application id>
	- ScanDetectReport-<application id>

# Contributing

Pull requests are welcome. This script can be freely used, distributed, and modified by anyone.
