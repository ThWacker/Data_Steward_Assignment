#!/usr/bin/env python

"""
Script that transposes a plink ped and a plink map file to a tped and tfam format. 
Tped are files containing SNP and genotype information where one row is a SNP.

This fullfills objective 3 of the assignment 

Input:
    - a pep file from Plink
    - a corresponding map file from Plink

Output:
    - a tpep file 
    - a tfam file

License: 
    MIT
"""
# Generic/ Build-ins
import argparse

# other libs
import pandas as pd
from pathlib import Path
from typing import Tuple

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
def combine_allele_columns(df_alleles: pd.DataFrame)-> pd.DataFrame:
    """
    Combine every second column of the allele columns. Headers are ignored.

    Args:
        df_alleles (pd.dataframe): the split off part of the pep file dataframe that contains only the alleles

    Returns:
        merged_df (pd.DataFrame): A pandas dataframe with combines columns
    
    Raises:
        Exception
    """
    # merge every second column without caring about the headers (column 0 and 1, 2 and 3 etc.). Give the columns a new header that is the iterator divided by 2
    try:
        merged_df = pd.DataFrame({
            i // 2: df_alleles.iloc[:, i].astype(str) + ' ' + df_alleles.iloc[:, i + 1].astype(str)
            for i in range(0, df_alleles.shape[1], 2)
        }
        )
        return merged_df
    except Exception as err:
        print(f"Oh no! An error occured in the combine_allele_columns function: {err}")
        raise

def split_dataframe(df_ped: pd.DataFrame)->Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the pep file dataframe into the Patient ID part (column 0-6) and the alleles.

    Args:
        df_ped (pd.DataFrame): the dataframe of the ped file

    Returns:
        df_fam (pd.DataFrame): the first 7 columns (0-6) from the ped file
        df_alleles (pd.DataFrame): the alleles columns of the ped file dataframe

    Raises:
        Exception
    """
    #subset the dataframe into two subdataframes, with one containing the patient ID columns (0-6), and the rest the alleles
    try:
        df_fam= df_ped.iloc[:,:6]# first half is columns 0-6 -> separate dataframe
        df_alleles = df_ped.iloc[:,6:]# second half is all the alleles -> separate dataframe 
        return df_fam, df_alleles
    except Exception as err:
        print(f"Booo, there was an error in the split_dataframe function: {err}"
              )
        raise

def transpose_dataframe(df_alleles_cb: pd.DataFrame)-> pd.DataFrame:
    """
    Transposes the alleles data frame. Columns to rows.

    Args:
        df_alleles_cb (pd.DataFrame): the alleles dataframe split of the ped dataframe with combined alleles columns

    Returns:
        t_df_alleles_cb (pd.DataFrame): the transposed dataframe
    
    Raises:
        Exception
    """
    # the actual magic happens here: columns become rows. We can use pandas transpose function for that
    try:
        t_df_alleles_cb = df_alleles_cb.transpose()
        return t_df_alleles_cb
    except Exception as err:
        print(f"The dataframe was not transposed because the following error happened: {err}\n Meh!\n")
        raise


def combine_dataframes(df_map: pd.DataFrame, t_df_alleles_cb: pd.DataFrame)->pd.DataFrame:
    """
    Combines the map file with the transposed pep file to yield a tpep file. 
    
    Args:
        df_map (pd.DataFrame): a pandas dataframe from the map file
        t_df_alleles_cb (pd.DataFrame): a pandas dataframe of the transposed alleles column
    
    Returns
        tpep_df (pd.DataFrame): a pandas dataframe in tpep format

    Raises:
        Exception
    """
    #combine the dataframes
    try:
        tpep_df=pd.concat([df_map, t_df_alleles_cb], axis=1, ignore_index=True)
        return tpep_df
    except Exception as err:
        print(f"Could not combine dataframes, an error occured: {err}")
        raise

###############
#    MAIN     #
###############
def main():
    '''Transpose ped to tped. Main is run when script is run directly, when __name__= __main__ evaluates to true. '''
    #parse the args
    parser = argparse.ArgumentParser(prog="Data Steward Assignment",description='Takes ped and map output files from Plink, transposes them to tped and tfam.', epilog="t.wacker2@exeter.ac.uk")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument('-p', '--ped', type=Path, required=True, help="The ped file to be transformed")
    parser.add_argument('-m', '--map', type=Path, required=True, help="The map file to be transformed")
 
    args = parser.parse_args()

    #find the folder of the map and ped files
    folder_path=Path(args.ped).parent

    #GET THE DATAFRAMES 
    try:
        #use read_csv to read in the data from the ped file
        df_ped=pd.read_csv(args.ped, sep=" ", header=None)
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

    try:
        #use read_csv to read in the data from the map file
        df_map=pd.read_csv(args.map, sep="\t", header=None)
    except FileNotFoundError as err:
        print("File was not found")
        raise
    except pd.errors.EmptyDataError as err:
        print(f"No data: {err}")
        raise
    except pd.errors.ParserError as err:
        print(f"Parse error: {err}")
        raise
    except Exception as err:
        print(f"Undefined exception: {err}") #None of the above happened, this catches all other exceptions
        raise
    
    # SPLIT PED DATAFRAME
    # split the ped file into family information (column 0-5) and allele information
    try:
        df_fam, df_alleles=split_dataframe(df_ped)
    except Exception as err:
        print(f"An Error occured: {err}")#one error to rule them all (generic)
        raise

    # SAVE TFAM file
    #new file
    file_tfam = Path(args.ped.stem + ".tfam")
    outfile_tfam= folder_path / file_tfam

    # try to save it to the file using pandas .to_csv
    try:
        df_fam.to_csv(outfile_tfam, sep="\t", header=False, index=False)
    except RuntimeError as err:
        print(f"An Error occured: {err}")#generic error
        raise
    except FileNotFoundError as err:
        print(f"The file could not be found: {err}")
        raise
    except IOError as err:
        print(f" Some kind of issue occured with file access: {err}")
        raise
    
    # TRANSPOSE DF_ALLELES ALLELES

    #first we have to make sure that each two alleles remain together
    try:
        df_alleles_cb=combine_allele_columns(df_alleles)
    except Exception as err:
        print(f"An Error occured: {err}")
        raise

    #then we transpose
    try: 
        t_df_alleles_cb=transpose_dataframe(df_alleles_cb)
    except Exception as err:
        print(f"An Error occured: {err}")
        raise

    #COMBINE MAP DATAFRAME WITH TRANSPOSED ALLELES & SAVE
    try:
        tpep_df=combine_dataframes(df_map, t_df_alleles_cb)
    except Exception as err:
        print(f"An Error occured: {err}")
        raise
    # try to save it to the file using pandas .to_csv
     #new file
    file_tpep = Path(args.ped.stem + ".tped")
    outfile_tpep = folder_path / file_tpep

    # try to save it to the file using pandas .to_csv
    try:
        tpep_df.to_csv(outfile_tpep, sep="\t", header=False, index= False)
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
    print("Heureka, all done!")


if __name__ == '__main__':
    main()
 