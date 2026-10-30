# Imports
import os
import datetime
import sys
import shutil
import subprocess

# Params - can be modified
calculation = "Opt"

functional = "wB97X-D4"
basisSet = "def2-SVP"

nprocs = "1"

charge = "0"
spinMultiplicity = "1"


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

xyzs = {os.path.splitext(file)[0].replace(".xyz", ""): file for file in sorted(os.listdir(homeDirectory)) if
        file.endswith('.xyz') and os.path.isfile(os.path.join(homeDirectory, file))}

if len(xyzs) == 0:  # Make sure there are .xyzs in the directory
    printToLog(f"# WARN - No .xyz files found to process. Place .xyz files in [{homeDirectory}]")
    quit()
else:
    printToLog(f"# INFO - {str(len(xyzs))} .xyz files found at [{homeDirectory}]")
    printToLog("# INFO - Following .cif files are available [" + str(list(xyzs.values())) + "]")

for refcode, filename in xyzs.items():
    refcodeDirectory = os.path.join(homeDirectory, refcode)
    createDirectory(refcodeDirectory, f"# INFO - Directory for [{refcode}] created at [{refcodeDirectory}]", False)
    shutil.move(os.path.join(homeDirectory, filename), os.path.join(refcodeDirectory, filename))

    input = os.path.join(refcodeDirectory, f"{refcode}.inp")
    content = f"""
! {functional} {basisSet}
! {calculation}
! NormalPrint

% pal
nprocs {nprocs}
end

* xyzfile {charge} {spinMultiplicity} {refcode}.xyz

"""
    with open(input, "w") as file:
        print(content.lstrip("\n"), file=file)
        printToLog(f"# INFO - Created .inp file for [{refcode}] file at [{input}]")
    subprocess.call(f"cd {refcodeDirectory}; orca_rungen-1 -n {nprocs} -i {refcode}.inp", shell=True)
