#!/bin/bash 
INKSCAPE=`which inkscape`
MAGICK=`which magick`

if [ "${1##*.}" = "svg" ]; then
# svg format

	BASENAME=`basename ${1} .svg`
	DIRNAME=`dirname ${1}`
	W=`${INKSCAPE} -W ${1}`
	W=${W/.*} # to integer
	H=`${INKSCAPE} -H ${1}`
	H=${H/.*} # to integer
	echo "Dimensions " ${W} "x" ${H}
	

	if [ ${W} -gt 500 ]; then
		${INKSCAPE} ${1} --export-width=1000 --export-area-drawing --export-filename=${DIRNAME}/${BASENAME}.png --export-type="png"
		${INKSCAPE} ${1} --export-width=500 --export-area-drawing --export-filename=${DIRNAME}/${BASENAME}.pdf --export-type="pdf"
		${MAGICK} ${DIRNAME}/${BASENAME}.png -resize '500x' ${DIRNAME}/${BASENAME}.png
#       sips --resampleWidth 500 ${DIRNAME}/${BASENAME}.png
#       sips --resampleWidth 1000 ${DIRNAME}/${BASENAME}.pdf
	else
		#echo "Dimensions " ${W} "x" ${H}
		${INKSCAPE} ${1} --export-area-drawing --export-filename=${DIRNAME}/${BASENAME}.png --export-type="png"
		${INKSCAPE} ${1} --export-area-drawing --export-filename=${DIRNAME}/${BASENAME}.pdf --export-type="pdf"
#       ${INKSCAPE} ${1} --export-area-drawing --export-png=${DIRNAME}/${BASENAME}.png
	fi
else
    echo Not a svg file
fi
