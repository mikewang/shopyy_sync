#!/bin/sh -l
##Load GAMESS (ALREADY DONE)
module load gamess
arg=$1

#Copy rungms to current folder
cp /apps/cent7/gamess/18.Aug.2016/rungms .
cp /apps/cent7/gamess/18.Aug.2016/gms-files.csh .

IFS='.' read -ra separated <<< $arg

path="/scratch/snyder/r/rong10/"
rm "${path}${separated[0]}.${separated[1]}."*
fn="$arg.out"
./rungms $arg 02 > $fn
