#!/usr/bin/env python

"""
Script that add a prefix (by default INCH_) to a column of choice (by default: 0) and changes phenotype status to be affected (2) for even numbered IDs
and unaffected (1) for odd numbered IDs, except for ID 27. 

This fullfills objective 1 and 2 of the assignment.

Input:
    - a tfam file

Output:
    - a modified tfam file

License: 
    MIT
"""
# Generic/ Build-ins
import argparse

# other libs
import pandas as pd
from pathlib import Path

# module-level metadata
__author__ = "Theresa Wacker"
__copyright__ = "Copyright, 2025, Data Steward Assignment"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Theresa Wacker"
__email__ = "t.wacker2@exeter.ac.uk"
__status__ = "Dev"

###############
#  FUNCTIONS  #
###############
def change_prefix(df_tfam: pd.DataFrame, prefix: str, column: int) -> pd.DataFrame:
    """
    Changes the entry of a column in a dataframe to have a prefix. The default is column 0 and the INCH_ as a prefix.

    Args:
        dt_tfam (pd.DataFrame): the dataframe from the tfam file generated with the ped_map_to_tped_transpose.py script
        prefix (str): a prefix. Default: INCH_
        column (int): which column to manipulate the entry in

    Returns:
        dt_tfam (pd.DataFrame): a modified dataframe

    Raises:
        TypeError
        RuntimeError
        Exception
    """
    try:
        df_tfam[column] = str(prefix) + df_tfam[column].astype(str)
        return df_tfam
    except TypeError as err:
        print(f"A TypeError occurred in the change_prefix function. Is the column number an integer and the prefix typecast-able to a string?: {err}")
        raise
    except RuntimeError as err:
        print(f"Oh no, a runtimeerror occurred in the change_prefix function: {err}")
        raise
    except Exception as err: #hovers up any other exceptions that might be thrown
        print(f"An exception occurred in change_prefix: {err}")
        raise
def manipulate_phenotype_status(df_tfam: pd.DataFrame)-> pd.DataFrame:
    """
    This is hardcoded and should definitely be made more flexible, but for the sake of this exercise, we will leave it like that for now.
    Any ID (of an individual) in the .tfam file that is even has the phenotype status in column 5 changed to affected (2).
    Any ID (of an individual) in the .tfam file that is odd has the phenotype status in column 5 changed to unaffected(1).
    Individual 27 is skipped.

    Args:
        dt_tfam (pd.DataFrame): the pandas dataframe of the .tfam file

    Returns:
        dt_tfam (pd.DataFrame): the pandas dataframe of the .tfam file with the changed phenotype status
    
    Raises:
        Nothing at the moment. This should have a try-except block in the future.
    """
    # iterrows() would be easiest, but is really slow. I therefore try vectorization with boolean indexing, which is new to me, but speeds things up
    # this way I try to future-proof this script for actual real-life usage with big data frames
    
    # deal with uneven family IDs first
    #Create boolean mask for rows where integer in column 0 is even
    mask = (df_tfam[0].str.extract(r'(\d+)')[0].astype(int) % 2 == 0)

    # Update column 5 to 2 if true
    df_tfam.iloc[mask.values, 5] = 2

    #do the same for uneven without 27
    # Extract numbers from column 0 as integers
    extracted_ints = df_tfam[0].str.extract(r'(\d+)')[0].astype(int)

    # Create mask for odd integers (uneven) EXCEPT for 27
    mask = (extracted_ints % 2 != 0) & (extracted_ints != 27)

    # Set column 5 to 1 if true
    df_tfam.iloc[mask.values, 5] = 1
    
    #all done, df_tfam gets returned
    return df_tfam

###############
#    MAIN     #
###############
def main():
    '''Change column values to contain a prefix. Change phenotype status according to whether patient has a uneven or even ID, yielding 1 or 2 respectively. Skip patient ID 27.'''
    #parse the args
    parser = argparse.ArgumentParser(prog="Data Steward Assignment",description='Manipulates tfam file to have a change in the column value prefix of one column (default 0) and change phenotype status.', epilog="t.wacker2@exeter.ac.uk")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument('-t', '--tfam', type=Path, required=True, help="The tfam file to be manipulated")
    parser.add_argument('-p', '--prefix', type=str, default="INCH_", help="The prefix to add to the column of choice. Default: INCH_")
    parser.add_argument('-c', '--col', type=int, default=0, help="Number of the column (caution: 0 indexed) to have the prefix added to the values. Default: 0")
 
    args = parser.parse_args()

    #find the folder of the map and ped files
    folder_path=Path(args.tfam).parent

    #GET THE DATAFRAME 
    try:
        #use read_csv to read in the data from the tfam file
        df_tfam=pd.read_csv(args.tfam, sep="\t", header=None)
    except FileNotFoundError as err:
        print(f"File was not found{err}")
        raise
    except pd.errors.EmptyDataError as err:
        print(f"No data: {err}")
        raise
    except pd.errors.ParserError as err:
        print(f"Parse error: {err}")
        raise
    except Exception as err:
        print(f"Undefined exception: {err}")
        raise

    # ADD THE PREFIX
    try:
        df_tfam=change_prefix(df_tfam, args.prefix, args.col)
    except Exception as err:
        print(f"An Error occured: {err}")#one error to rule them all (generic)
        raise
    
    # CHANGE PHENOTYPE STATUS
    try:
        df_tfam=manipulate_phenotype_status(df_tfam)
    except Exception as err:
        print(f"An Error occured: {err}")
        raise
    # SAVE TFAM file
    #new file
    file_tfam = Path(args.tfam.stem + "_modified.tfam")
    outfile_tfam= folder_path / file_tfam

    # try to save it to the file using pandas .to_csv
    try:
        df_tfam.to_csv(outfile_tfam, sep="\t", header=False,index=False)
    except RuntimeError as err:
        print(f"An Error occured: {err}")#generic error
        raise
    except FileNotFoundError as err:
        print(f"The file could not be found: {err}")
        raise
    except IOError as err:
        print(f" Some kind of issue occured with file access: {err}")
        raise
    
    # HORRAY, WE HAVE A TFAM AND TPEP FILE
    print("Finished! All objectives have been fulfilled.")


if __name__ == '__main__':
    main()