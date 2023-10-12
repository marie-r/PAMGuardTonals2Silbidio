library(PamBinaries)
library(jsonlite)
library(magrittr)

# The first command-line argument is the source directory
# in which all of the Pamguard DataFiles lie.
# The second command-line argument is the output file name
args = commandArgs(trailingOnly=TRUE)

if (length(args) != 2) {
  print("Error: Must be called with exactly two arguments.")
  print("[call script] /folder/with/pamguard/binaries /output/file.json")
  quit()
}

# function to take a single Pamguard annotation file and
# convert it into a "human-readable" data structure
readFile <- function(filename) {
  
  binaryFile = loadPamguardBinaryFile(filename)
  
  data = contourToFreq(binaryFile)$data
  
  parsedData <- list()
  for (d in data){
    time <- d$time
    freq <- d$freq
    timeFreq <- list(time = time, freq = freq)
    parsedData <- append(parsedData, list(timeFreq))
  }
  parsedData
}

# Get all PAMGuard annotations
files = Sys.glob(paste(args[1],"/*.pgdf", sep = ""))

parsedFiles <- list()
for (file in files){
  
  parsedFiles <- append(parsedFiles, list(list(filename = file, data=readFile(file))))
}


sink(args[2])
jsonlite::toJSON(parsedFiles) %>% jsonlite::prettify()
sink()
