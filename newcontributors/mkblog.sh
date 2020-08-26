set -o errexit
set -o nounset
set -o pipefail

./run.sh $1
numdevs=`wc -l new.txt | cut -d ' ' -f 7`
numnonmoz=`grep -v mozilla.com new.txt | wc -l | cut -d ' ' -f 7`
echo
echo
echo "With the release of Firefox $1, we are pleased to welcome the <strong>${numdevs} developers</strong> who contributed their first code change to Firefox in this release, <strong>${numnonmoz}</strong> of whom were brand new volunteers! Please join us in thanking each of these diligent and enthusiastic individuals, and take a look at their contributions:"
./newcontributors.sh
