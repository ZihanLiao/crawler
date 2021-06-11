#!/bin/bash


target_dir=$1

for f in `ls $target_dir`; do
    if [[ ${file##.*} -eq 'm4a' ]]
    then
        rm -f $target_dir'/'$f
    fi
done

luoli=`ls $target_dir | grep luoli- | wc -w`
shaonv=`ls $target_dir | grep shaomv- | wc -w`
yujie=`ls $target_dir | grep yujie- | wc -w`
shaonian=`ls $target_dir | grep shaonian- | wc -w`
dashu=`ls $target_dir | grep dashu- | wc -w`

echo "$luoli $shaonv $yujie $shaonian $dashu"

count=($luoli, $shaonv, $yujie, $shaonian, $dashu)

min=${count[0]}
for i in ${count[@]}; do
    if [[ ${min} -gt $i ]]; then
        min=$i
    fi
done

echo $min