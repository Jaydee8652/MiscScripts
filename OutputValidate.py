# Imports
import os
import datetime
import sys
import shutil
import subprocess

# Params - can be modified


logs = os.path.join(os.getcwd(), "logs")
if not os.path.exists(logs):
    os.makedirs(logs)

# Functions
# Prints and logs in one, convention I personally like
def printToLog(info):
    time = ""
    if not str(info).startswith(" ---"):
        time = str(datetime.datetime.now().strftime("[%H:%M:%S]"))
    log = str(os.path.basename(sys.argv[0]).split(".")[0] + ".log")

    with open(os.path.join(logs, log), "a") as log:
        print(f"{time} {info}", file=log)
        print(f"{time} {info}")

#Create directory if it doesn't exist. Optionally crash deliberately if doesn't exist
def createDirectory(path, text, exit):
    if not os.path.exists(path):
        printToLog(text + " ["+ path + "]")
        os.makedirs(path)
        if exit:
            quit()

# Main
log = str(os.path.basename(sys.argv[0]).split(".")[0] + ".log")
homeDirectory = os.getcwd()  # Directory where we are
printToLog(" --- \n" + str(datetime.datetime.now().strftime("[%H:%M:%S] ")) + "# INFO - Starting new " + str(
    os.path.basename(sys.argv[0]).split(".")[0]) + " process in [" + homeDirectory + "]")

inputDirectory = os.path.join(homeDirectory, "inputDirectory")
createDirectory(inputDirectory, f"# WARN - No firectory for input files found, created at [{inputDirectory}]", True)

targets = sorted([directory for directory in os.listdir(inputDirectory) if
                  os.path.isdir(os.path.join(inputDirectory, directory)) and not directory.startswith(
                      ".") and os.path.isfile(
                      os.path.join(os.path.join(inputDirectory, directory), directory + ".out"))])

if len(targets) == 0:  # Make sure there are .xyzs in the directory
    printToLog(f"# WARN - No .out files found to process.")
    quit()
else:
    printToLog(f"# INFO - {str(len(targets))} .out files found at [{homeDirectory}]")
    printToLog(f"# INFO - Following .out files are available [{str(list(targets))}]")

for refcode in targets:
    refcodeDirectory = os.path.join(inputDirectory, refcode)
    out = os.path.join(refcodeDirectory, f"{refcode}.out")

    if os.path.isfile(out):
        with open(out) as file:
            lines = file.readlines()
            frequencies = ''.join(lines).split("""-----------------------
VIBRATIONAL FREQUENCIES
-----------------------""")[1].split("""


""")[0].split("\n")

            frequencies = [line for line in frequencies if line.strip()]
            #printToLog(frequencies)
            for number, line in enumerate(frequencies, 0):
                #printToLog(line)
                if(line.__contains__("***imaginary mode***")):
                    printToLog(f"# INFO - Compound [{refcode}] contains an imaginary mode [{line}]")


