#########################################
############## TEST - PROJECT 6 ###############
#########################################
#
# HOW TO RUN
# 0) Make sure you have python 3.7 installed
# 1) Run on school computer, extract the zip to the folder of your
# assembler(including make and run file).
# 2) Run in terminal using 'python3 tests.py'
# 3) Results will be shown in terminal
#
# The files in cmp are from the provided assembler
#########################################
import difflib
import os
import subprocess

import sys

PYTHON_VER = f"If you see this error message, you are using python 2.x instead of 3.7"

PROGRAM_NAME_1 = "Assembler"

#########################################
def cmp_files(cmp_file, out_file):
    with open(cmp_file, 'r') as fCmp:
        with open(out_file, 'r') as fOut:
            diff = difflib.ndiff(fOut.readlines(), fCmp.readlines())

            for i, line in enumerate(diff):
                if line.startswith("- ") or line.startswith("+ ") or line.startswith("? "):
                    print("\tOutput test - FAIL")
                    print("\tDifference found in '" + out_file + "' at line " + str(i))
                    return

            print("\tOutput test - PASS")


def t_file(test_name, file_name):
    print(test_name)
    in_file = f"test/{file_name}"
    out_file = "cmp/" + os.path.splitext(file_name)[0] + ".hack"
    cmp_file = "cmp/" + os.path.splitext(file_name)[0] + ".hack"

    with open(out_file, 'w') as fOut:
        try:
            program = in_file

            subprocess.run(program, stdout=fOut, stderr=subprocess.STDOUT, shell=True, timeout=10)

        except subprocess.TimeoutExpired:
            print(test_name + "\tTest - FAIL")
            print("\tTIMEOUT Reached")
            return

    cmp_files(cmp_file, out_file)


#########################################
if __name__ == "__main__":
    # if "--no-valgrind" in sys.argv:
    #    USE_VALGRIND = False

    print("\n------- MAKE START -------")

    # if subprocess.run("make", text=True, shell=True).returncode != 0:
    #     print("\nProgram failed making")
    #     exit(1)


    print("------- MAKE END - The section above should have no warnings nor "
          "errors -------")
    print("\nProgram compiled successfully")

    print("\n------- TEST START -------")
    print("\nRunning your Assembler:\n")
    if subprocess.run("Assembler test", text=True, shell=True).returncode != 0:
        print("\nProgram failed running")
        exit(1)

    for file in os.listdir("test"):
        if file.endswith(".asm"):
            t_file(file, file)
            print()
    print()

    print("------- TEST END -------")
