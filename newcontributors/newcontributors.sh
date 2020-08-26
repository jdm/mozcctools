echo "<ul>"
export LANG=C
cat new.txt | \
# remove all @TLD stems from email addresses
sed -E -e 's/@[A-Za-z\.0-9]+//g' | \
# fix nameless entries like "  <a>: ..."
sed -E -e 's/^   <([a-z0-9_\.\+\-]+)>:/\1:/' | \
# fix nameless entries like "[:foo]  <a>:"
sed -E -e 's/^\[:([A-Za-z0-9_]+)\]   </\1 </' | \
# remove : prefixes
sed -E -e 's/:([A-Za-z0-9])/\1/g' | \
# remove [:name]
sed -E -e 's/\[([A-Za-z0-9_\.\/:;,!?\+ \-]+)\]//g' | \
# remove (:name)
sed -E -e 's/\(([A-Za-z0-9_\.\/:;,!\?\+ \-]+)\)//g' | \
# remove <a>
sed -E -e 's/<([A-Za-z0-9_\.\+\-]+)>//' | \
# remove excess spaces
tr -s ' ' | \
# remove excess spaces 
sed -e 's/ :/:/g' | \
# add list item elements
sed -e 's/^/<li>/g' -e 's/$/<\/li>/g'
echo "</ul>"
