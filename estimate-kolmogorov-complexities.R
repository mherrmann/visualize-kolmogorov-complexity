# Usage:
#     Rscript estimate-kolmogorov-complexities.R SIZE OUTPUT_FILE
# Writes the estimated Kolmogorov complexity of the bit representations of
# 0 ... 2 ^ SIZE to OUTPUT_FILE.

require(acss)
library(parallel)

args = commandArgs(trailingOnly=TRUE)

SIZE <- strtoi(args[1])
OUTPUT_FILE <- args[2]

asBinary <- function(x, nBits = 8) {
    paste(tail(rev(as.numeric(intToBits(x))), nBits), collapse='')
}

# Clear the file
close(file(OUTPUT_FILE, open="w"))

getKCs <- function() {
    return(mclapply(0:(2**SIZE - 1), getKC, mc.cores=detectCores()))
}

getKC <- function(i) {
    return(acss(string = asBinary(i), alphabet = 2)[1])
}

for (value in getKCs()) {
    write(
        toString(value),
        file=OUTPUT_FILE, append=TRUE
    )
}