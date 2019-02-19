#!/bin/sh


EXEC_FILES=(photo_upload.py tags.py gen_sponsor.py gen_exchanges.py gen_projects.py gen_markets.py gen_banner.py)

for f in $EXEC_FILES
do
	python ./$f
	if [ $? != 0 ]; then
		echo "run $f falied!"
		exit -1
	fi
done

