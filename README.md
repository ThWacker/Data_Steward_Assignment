#  Data Steward Assignment
Repository accompanying the task given for the Data Steward position interview

# Overview

Scripts are found in the scripts folder and can be run individually or through the ```Assignment_wrapper.sh``` bash script. 
These script manipulate [PLINK](https://www.cog-genomics.org/plink/) .map and .ped files, manipulate them and produce tranposed .tped and .tfam files.

```manipulate_ped_prefix_and_columns.py``` will manipulate the pep file in place to change the prefix of a column of choice, by default column 0 and the prefix "INCH_". It will also change the phenotype status in column 5 from not recorded (-9) to affected (2) in the case of even family IDs and unaffected (1) in the case of odd family IDs. This is currently not flexibly changeable. 

```ped_map_to_tped_tfam_transpose.py``` transposes the .ped file and .map file to a .tped and .tfam file. Note that .tped can also be generated by ```PLINK``` itself using the ```--recode transpose``` command. This does not generate a .tfam file though

# Features

- manipulates a column of choice in the .ped file to add a prefix to its values. __*NOTE: it does that in place, no new .pep file is generated*__
- manipulates column 5 of the .ped file to have an altered phenotype status: 2 (affected) for even family IDs, 1 (unaffected) for uneven family IDs. It ignores any ID that is 27. __*NOTE: it does that in place, no new .pep file is generated*__
- generates a .tped file from a .map and .ped file
- generates a .tfam file from a .ped file and a .map file

# Folder structure
All scripts are found in 'scripts'. 
The .ped and .map files are found in the 'Data_steward_interview_task' folder.
You can see example output .tped and .tfam files in 'Data_steward_interview_task/example_output'

# Usage

> This is a work in progress. Currently it assumes you are running the scripts from the repo folder (the base folder) and that the scripts are in scripts. It makes no assumptions per se about where the .map and .ped files are.

Git clone the repo

``` 
git clone https://github.com/ThWacker/Data_Steward_Assignment.git
```

Change into the repo

``` 
cd ~/your_path_to_the_repo/Data_Steward_Assignment
```

Run the wrapper script like so (example):

``` 
./scripts/Assignment_wrapper.sh -m ./Data_steward_interview_task/My_SNPS.map -p ./Data_steward_interview_task/My_SNPS.ped
```

# THANK YOU FOR CONSIDERING ME AS AN APPLICANT!

