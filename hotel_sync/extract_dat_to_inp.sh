#!/usr/local/bin/bash

for water in $(ls /scratch/snyder/r/rong10/water*); do
 water=$(basename ${water})
 num=$(echo ${water} | sed 's/water//' | awk -F'.' '{print $1}')
 new_water="water.$((num+1)).inp"
 cp water_stardard.inp ${new_water}
 cat ${water} | sed -n '/\---CLOSED/, /\$END/p'| sed '$d' >> ${new_water}
done
