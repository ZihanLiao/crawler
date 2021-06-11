#!/bin/bash

if [ $# -le 1 ];then
echo "Please enter input file path and output file path."	
fi

input_dir=$1
output_dir=$2

if [ ! -d $output_dir ];then
	mkdir $output_dir
else
	echo "Direction already existed"
fi

# Extract 10 pieces from all catagories

catagories=("shaonv" "luoli" "yujie" "dashu" "shaonian")

for catagory in ${catagories[@]};do
	echo $catagory
	count=0
	# echo `ls $input_dir | grep $catagory'-'`
	for file in `ls $input_dir | grep $catagory'-'`;do
		if [[ $count -le 9 ]]; then
			in_file_name=$input_dir'/'${file%.*}
			echo "Input file name is:"$in_file_name
			out_file_name=$output_dir'/'${file%.*}
			echo "Output file name is:"$out_file_name
			file_size=`ls -la $input_dir'/'$in_file_name'.m4a' | awk '{ print $5 }'`
			echo "File size is:"$file_size
				
			if [ -f $in_file_name'.m4a' ] || [ ! $file_size -eq 0 ];then
				ffmpeg -i $in_file_name.m4a -acodec pcm_s16le -y -ac 2 -ar 44100 $out_file_name.wav
				count=${count}+1
			fi
			
			out_file_size=`ls -la $out_file_name'.wav' | awk '{ print $5 }'`
			if [ out_file_size -eq 0 ];then
				rm -f $output_dir'/'$out_file_name'.wav'
			fi
		fi
	done
done




