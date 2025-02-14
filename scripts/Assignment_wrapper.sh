#!/usr/bin/env bash 
set -e

# Complaints, bugs, praise, requests, cute cat pics, memes etc can be sent to theresa_wacker@mailbox.org or t.wacker2@exeter.ac.uk

die() { echo "$@" ; exit 1; }
diemsg() {
    echo "Usage: $0 -m <.map-file> -p <.ped-file> -a <prefix; default=INCH_> -c <column number; default=0>"
    echo ""
    echo "Arguments -m and -p are mandatory."
    echo ""
    echo "-h for help"
    die ""
}

echo "Welcome! This is the assignment wrapper. This automates running the other two scripts. All results should be found in the folder where the .pep and .map files originate from. "
echo ""
echo "-h for help"
echo ""

if [ "$1" == "-h" ] || [ $# -lt 4 ]; then
    diemsg
fi

# Variable assignment
MAP=
PED=
PREFIX=
COLUMN=

# Initialize variables to track whether mandatory options are provided
a_provided=false
b_provided=false


# Gather input files and settings
while [ $# -gt 0 ]; do
    case "$1" in
    -m) MAP="$2"; shift; a_provided=true;;
    -p) PED="$2"; shift; b_provided=true;;
    -a) PREFIX="$2"; shift;;
    -c) COLUMN="$2"; shift;;
    -*) echo >&2 "Unknown option: $1"; diemsg;;
    *) break;;    # terminate while loop
    esac
    shift
done

##############
### CHECKS ###
##############
echo "Checking if mandatory arguments have been provided..."

# CHECK1: Check if mandatory arguments are provided
if [ "$a_provided" = false ] || [ "$b_provided" = false ]; then
    diemsg "Error: The values -m and -p are mandatory!"
fi

echo "Mandatory arguments have been provided!"

# CHECK2: Function to check if a given Python command exists and print its version
echo "Checking python version..."
if command -v python3 &>/dev/null; then
    default_python="python3"
elif command -v python &>/dev/null; then
    default_python="python"
else
    die "Neither python nor python3 is available."
fi

$default_python --version

############
### MAIN ###
############
# Get the script directory:
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# get the parent of the script directory

PARENT_DIR="$(dirname "$SCRIPT_DIR")"
#check if environment exists or create one

if [ ! -d DataSteward ]; then
    "$default_python" -m venv DataSteward || die "Failed to create virtual environment."
fi

DataSteward/bin/pip install --upgrade pip
DataSteward/bin/pip install -r "$PARENT_DIR"/requirements.txt
source DataSteward/bin/activate

#running manipulate_pep_prefix_and_columns.py

echo "Running manipulate_ped_prefix_and_columns.py to fulfill objective 1 and 2"

if  [[ -n $PREFIX && -n $COLUMN ]]; then
    "$default_python"  "$SCRIPT_DIR"/manipulate_ped_prefix_and_columns.py -t "$PED" -p "$PREFIX" -c "$COLUMN" && true
    EXIT_STATUS="$?"
elif [[ -n $COLUMN ]]; then
    "$default_python"  "$SCRIPT_DIR"/manipulate_ped_prefix_and_columns.py -t "$PED" -c "$COLUMN" && true
    EXIT_STATUS="$?"
elif [[ -n $PREFIX ]]; then
    "$default_python"  "$SCRIPT_DIR"/manipulate_ped_prefix_and_columns.py -t "$PED" -p "$PREFIX" && true
    EXIT_STATUS="$?"
else
    "$default_python"  "$SCRIPT_DIR"/manipulate_ped_prefix_and_columns.py -t "$PED" && true
    EXIT_STATUS="$?"
fi

#check if the command failed with an exit status other than 0
if [[ $EXIT_STATUS -ne 0 ]]; then
    echo "Script failed with error ${EXIT_STATUS}. Check log for details!"
    exit 1
fi
echo "Fulfilled objective 1 and 2!"
#running ped_map_to_tped_tfam_transpose.py
echo "Running ped_map_to_tped_tfam_transpose.py to fulfill objective 3"

"$default_python" "$SCRIPT_DIR"/ped_map_to_tped_tfam_transpose.py -m "$MAP" -p "$PED"&& true
EXIT_STATUS="$?"

#check if the command failed with an exit status other than 0
if [[ $EXIT_STATUS -ne 0 ]]; then
    echo "Script failed with error ${EXIT_STATUS}. Check log for details!"
    exit 1
fi
echo "Fulfilled objective 3!"

