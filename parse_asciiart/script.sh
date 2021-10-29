# BEGIN

find \( -name 000.txt -or \( -name 001.txt -not -path "*other*" \) \) -delete

echo 'remove \r...'
dos2unix `find -type f -name "*.txt"` &> /dev/null

echo 'remove signs...'
sed -e 's/\r/\n/g;s/jgs/   /g;s/Max/   /g;s/hjw/   /g;s/ejm/   /g;s/snd/   /g;s/mrf/   /g;s/-Row/    /g;s/Targon/      /g;s/ctr/   /g' \
	-i `find -type f -name "*.txt"`

echo 'remove tailling spaces...'
sed -e 's/\s\+$//g' -i `find -type f -name "*.txt"`

recursive()
{
	echo "recursive $1"
	if [[ -z "`find $1 -maxdepth 1 -type f -name "*.txt"`" ]]
	then
		for dir in `find $1 -maxdepth 1 -type d`
		do
			if [[ "$dir" == "$1" ]]
			then
				continue
			fi
			recursive $dir
		done
		return 0
	fi

	rm -f $1/0.txt
	for file in `find $1 -maxdepth 1 -type f -name "*.txt" | sort -V`
	do
		cat $file >> $1/0.txt
		echo      >> $1/0.txt
		echo      >> $1/0.txt
		echo      >> $1/0.txt
	done
}

recursive .


# END
