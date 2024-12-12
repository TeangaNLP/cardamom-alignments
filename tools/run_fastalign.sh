FASTALIGN_BIN=./fast_align/build/fast_align
ATOOLS_BIN=./fast_align/build/atools
FILENAME=example
FORWARD_OUTFNAME=forward.alig
REVERSE_OUTFNAME=reverse.alig
SYMMETRIC_OUTFNAME=symmetric.alig
$FASTALIGN_BIN -i $FILENAME -d -o -v > $FORWARD_OUTFNAME 
$FASTALIGN_BIN -i $FILENAME -d -o -v -r > $REVERSE_OUTFNAME
$ATOOLS_BIN -i $FORWARD_OUTFNAME -j $REVERSE_OUTFNAME -c grow-diag-final-and 
