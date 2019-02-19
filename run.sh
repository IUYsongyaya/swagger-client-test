# !/bin/sh

SCENARIOS=(main staff tenant venture sponsor otc)
ROOT_DIR=`pwd`
NONSTOP=0

#$ROOT_DIR/bigbang 1

#if [ $? -ne 0 ]; then
#	echo "Bigbang failed!"
#	exit 1
#fi

if [ $# -gt 0 ]; then
	SCENARIOS=$1
fi

if [ $# -eq 2 ]; then
	NONSTOP=$2	
fi

echo "Check scenarios: $SCENARIOS"

function check_ignore()
{
	file_check=$1
	dir_check=$2
	file_list=$3
	for i in ${file_list[*]}
	do
		echo "$file_check vs $dir_check/$i"
		if [ $file_check == $dir_check/$i ]; then
			echo "ignore it!"
			return 1
		fi
	done
	return 0
}

for dir in $SCENARIOS
do
	scenario_dir=$ROOT_DIR/test/$dir/scenario
	if [ -f $scenario_dir/.pytestignore ]; then
		ignore_files=`cat $scenario_dir/.pytestignore|cut -f1`
	else
		ignore_files=()
	fi
	
	echo "ignore files: $ignore_files"

	test_files=`find $scenario_dir/ -name '*.py'|grep -v '__init__.py'|cut -f1`
	total_count=0
	fails_count=0
	for f in $test_files
	do
		let total_count+=1
		check_ignore $f $scenario_dir ${ignore_files[*]}
		if [ $? -eq 0 ]; then
	    		echo "try file: $f"
			pytest $f
			if [ $? -eq 1 ]; then
				if [ $NONSTOP -eq 1 ]; then
					let fails_count+=1
				else
					echo "====>Pytest $f failed with exit: $?"
					exit 1
				fi
			fi
		else
			echo "ignore $f"
		fi
	done
	echo "Total $total_count test files, $fails_count fails"	
done

