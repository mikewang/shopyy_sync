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
## 生成了 dat文件， 输出到.out保存日志。

# water.py -agent0 water0.inp  -agent1 paper0.inp
# 换配置文件。

# 输入 两个 0,1 inp 文件。
# 转换成 .inp.q 文件。
# 处理成q ,生成 gradient。 -- (原来的逻辑不变。)
# 返回如果flase ,继续 使用rungms ，1.inp 生成一个新的 1.dat ，转成 加1 的就是2.inp文件。
# 继续使用 1.inp 和 2.inp 循环。
# 直到200超 ，或者达到 true.