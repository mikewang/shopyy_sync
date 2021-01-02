#!/usr/local/bin/bash

for water in $(ls /scratch/snyder/r/rong10/water*dat); do
 watername=$(basename ${water})
 echo $water
 num=$(echo ${watername} | sed 's/water//' | awk -F'.' '{print $1}')
 new_watername="water.$((num+1)).inp"
 cp water_stardard.inp ${new_watername}
 cat ${water} | sed -n '/\---CLOSED/, /\$END/p'| sed '$d' >> ${new_watername}
done
