#set -x
basepath=~/Documents/releasecontributors
if [ "$1" == "--clean" ]
then
  shift
  rm $basepath/*
fi
for (( i=10; i<=$1; i++ ))
do
  file="$basepath/$i"
  if [ ! -f $file ]
  then
    echo Getting info for $i
    python releasecontributors.py $i $file
    if [[ "$?" != "0" ]]
    then
      exit 1
    fi
    #until python releasecontributors.py $i $file;
    #do
    #  echo Retrying...
    #done
  fi
done
python bgznewcontributors.py 10 $1 $basepath
