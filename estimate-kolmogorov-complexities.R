# Usage:
#     Rscript estimate-kolmogorov-complexities.R SIZE OUTPUT_FILE
# Writes the estimated Kolmogorov complexity of the bit representations of
# 0 ... 2 ^ SIZE to OUTPUT_FILE.

require(acss)

args = commandArgs(trailingOnly=TRUE)

SIZE <- strtoi(args[1])
OUTPUT_FILE <- args[2]

asBinary <- function(x, nBits = 8) {
    paste(tail(rev(as.numeric(intToBits(x))), nBits), collapse='')
}

# Clear the file
close(file(OUTPUT_FILE, open="w"))

getKCs <- function() {
    result <- vector(length=2**SIZE)
    i <- 1
    while (i <= 2 ** SIZE) {
        result[i] = acss(string = asBinary(i), alphabet = 2)[1]
        i = i + 1
    }
    return(result)
}

for (value in getKCs()) {
    write(
        toString(value),
        file=OUTPUT_FILE, append=TRUE
    )
}