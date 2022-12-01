#!/bin/bash
chk=1
while read LINE; do
	echo
	echo "----------------------------------------------------------------------------------------"
	echo [searching : $LINE]
	echo
	if [ "${chk}" -eq 1 ];
	then
		grep -rn "$LINE" ./txts;
		chk=0
	else
		grep -rni "$LINE" ./txts
	fi
done < $1
