#!/bin/bash

source_file=$1
output_file=$2
 
sed_regex_of_matrix_slice='/EIGENVECTORS/, /END OF RHF CALCULATION/'
 
sed_regex_of_matrix_rows='/^ \{1,\}[0-9]\{1,2\} \{1,\}[OH] \{1,\}[123]/'
 
rows_of_matrix=$(cat ${source_file} | sed -n "${sed_regex_of_matrix_slice}p" | sed -n "${sed_regex_of_matrix_rows}p" | awk '{print $1}' | sort -unr | head -n 1)

cols_of_matrix=${rows_of_matrix}

rows_of_all=$(cat ${source_file} | sed -n "${sed_regex_of_matrix_slice}p" | sed -n "${sed_regex_of_matrix_rows}p" | wc -l)

wraps_of_matrix=$(expr ${rows_of_all} / ${rows_of_matrix})


cat ${source_file} | sed -n "${sed_regex_of_matrix_slice}p" | sed -n "${sed_regex_of_matrix_rows}p" | \
	awk -v order_of_matrix=${rows_of_matrix} -v wraps_of_matrix=${wraps_of_matrix} -v output_file="${output_file}"  ' 
		BEGIN{
			row=0;
			col=0;
		}

		{
			row = $1 - 1;

			base = int(NR / order_of_matrix);

			if(NR % order_of_matrix == 0) {
				base = int((NR - 1) / order_of_matrix)
			}

			for(i = 0; i < 5; i++) {
				k = i + 5;
				m[row, (i + (5 * base))] = $k;
			};
		}

		END {
			#
			# printj
			#
			#
			for (i = 0; i < order_of_matrix; i++) {
				for (j = 0; j < order_of_matrix; j++) {
					# printf("m[%d, %d] = %f ", i, j, m[i, j]);
					printf("%f\t", m[i, j]) >> output_file
				}
				print "" >> output_file
			}
		}
	'

