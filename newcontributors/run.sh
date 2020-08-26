basepath=/tmp
for (( i=10; i<=$1; i++ ))
do
  file="$basepath/$i"
  echo Getting info for $i
  python releasecontributors.py $i $file
  if [[ "$?" != "0" ]]
  then
    exit 1
  fi
done
python bgznewcontributors.py 10 $1 $basepath
