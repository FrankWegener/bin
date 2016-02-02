#!/bin/bash

## *** created by puppet ***
## *************************

#  /usr/local/bin/scan.bash
#


TEMP="/tmp/scanimage"
OUTPATH="/mnt/_g/__offen/__scans"

clear_screen()
{
	clear
}

scan_page2()
{
	local ret

	echo "Scanning ..."

	clear_screen
	
	scanadf  -v \
		-d "fujitsu:ScanSnap S1500:18239"  \
		--page-height=305 -y 305 \
		--output-file ${TEMP}/scan0 \
		--mode color \
		--resolution 150

	ret=$?
	convert ${TEMP}/scan0 ${TEMP}/scan0.tiff


	[[ $ret == 0 ]] && return 0
	[[ $ret == 7 ]] && return 1

	echo "scan_page: error occured"

}

scan_page()
{
	local ret=1

        while [[ $ret == 1 ]] ; do
		clear_screen
		echo "Insert document !"
		read -n 1 key
		clear_screen

		case $key in
			q) 
				exit 0
				;;
					# close document
			w) 
				return 2
				;;
		esac

		scan_page2
		ret=$?
	done

	if [[ $key == r ]] ; then
		convert ${TEMP}/scan0.tiff  -rotate 90 ${TEMP}/scan1.tiff
		mv ${TEMP}/scan1.tiff ${TEMP}/scan0.tiff
	fi

	return 0
}

scan_doc()
{
	local ret=0

        while [[ $ret == 0 ]] ; do
		scan_page
		ret=$?

			# close document

		if [[ $ret == 2 ]] ; then
			return
		fi

			# crop 

#		convert ${TEMP}/scan0.tiff \
#			-fuzz 16% -trim \
#			-depth 8 \
#			${TEMP}/scan2.tiff

#		rm ${TEMP}/scan0.tiff

			# convert to jpeg,pdf

		convert ${TEMP}/scan0.tiff  -quality 75 ${TEMP}/scan2.jpg
		convert ${TEMP}/scan2.jpg ${TEMP}/scan2.pdf

		if [ ! -e ${TEMP}/out.pdf ] ; then			
			mv ${TEMP}/scan2.pdf ${TEMP}/out.pdf
		else
			pdftk ${TEMP}/out.pdf ${TEMP}/scan2.pdf cat output ${TEMP}/scan3.pdf
			mv ${TEMP}/scan3.pdf ${TEMP}/out.pdf
		fi
	done
}

print_date()
{
        date=`date "+%Y%m%d"`
        year=`echo $date | awk '{print substr($1,1,4); }'`
        month=`echo $date | awk '{print substr($1,5,2); }'`
        day=`echo $date | awk '{print substr($1,7,2); }'`

        echo ${year}-${month}-${day}
}

OUTPATH2="${OUTPATH}/`print_date`"

while [[ 0 == 0 ]] ; do
	OUTFILE="${OUTPATH2}/`print_date`__`date "+%H%M%S"`.pdf"

	rm -rf ${TEMP}
	mkdir ${TEMP}

	scan_doc

		# delete title

	pdftk ${TEMP}/out.pdf dump_data | grep -vh xxx | grep -vh Title > ${TEMP}/metadata
	echo "InfoKey: Title" >> ${TEMP}/metadata
	echo "InfoValue:" >> ${TEMP}/metadata
	pdftk ${TEMP}/out.pdf update_info ${TEMP}/metadata output ${TEMP}/out2.pdf

		# create output

	if [ ! -e ${OUTPATH2} ] ; then
		mkdir ${OUTPATH2}
		chown fwe:fwe ${OUTPATH2}
	fi

	cp ${TEMP}/out2.pdf ${OUTFILE}
	chown fwe:fwe ${OUTFILE}
	atril ${OUTFILE} 2>/dev/null &
done
