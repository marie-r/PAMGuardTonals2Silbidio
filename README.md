# PAMGuardTonals2Silbido

This utility is **NOT** secure and could execute arbitrary code if not handled safely.

A basic utility that transfers binary tonal-annotation files from the PAMGuard .pgdf format to the *silbido* binary tonal-annotation format.

## Dependencies
The utility has been tested with Python 3.11.6 and R 4.3.1. For the utility to work, R must have the [PamBinaries](https://github.com/cran/PamBinaries) (tested 1.8.1), jsonlite, and magrittr (tested 2.0.3) libraries installed. 

## Use
To call the utility, use

python3 PamguardToSilbidoBinaries.py source/binaries/directory destination/directory path/to/Rscript

The utility will execute "path/to/Rscript" under the presumption that R will be called. This is **INSECURE** because a user of this program could input an arbitrary command to be run. On windows, The file will likely be "Program Files\R\R-{*R-version*}\bin\Rscript.exe".

To get the full list of legal ways to call the utility, use

python3 PamguardToSilbidoBinaries.py -h

There are two PAMGuard binary files included for testing. To verify that the utility is working, use

.\PamguardToSilbidoBinaries.py ./test-pamguard-binaries ./ */path/to/Rscript*


## Contains
The following files are included.
- filterMoans.py: Code to filter silbido annotations, that poor annotations be removed.
- PamguardBinariesToJson.R: An R script to read multiple PAMGuard binary tonal-annotation files and to generate a corresponding JSON file.
- PamguardToBinaryFiles.py: The main program.
- README.md: The readme.
- readRJSON.py: Code to parse the JSON format resulting from PamguardBinariesToJson.R into a desireable data structure.
- test-pamguard-binaries: Contains two PAMGuard binary files with which to test this utility.
- silbidopy: A basic package to read and to write *silbido* binary annotation files.
