#!/bin/bash -e

file=food_data_idx3828.txt
newfile=new_food_data_3828_4435.txt
#，
CHAR1=$(python -c 'print u"\uff0c".encode("utf8")')
#。
CHAR2=$(python -c 'print u"\u3002".encode("utf8")')
#！
CHAR3=$(python -c 'print u"\uff01".encode("utf8")')
#～
CHAR4=$(python -c 'print u"\uff5e".encode("utf8")')
#…
CHAR5=$(python -c 'print u"\u2026".encode("utf8")')

cat $file | \
sed "/^\s*$/d" \
| tr '\n' ' ' \
| sed "s/\t/ /g" \
| sed "s/(\([^()]*\))/\n\1\n/g" \
| sed "s/\[\([^]]*\)\]/\n\1\n/g" \
| sed "s/["$CHAR1"]/\n/g" \
| sed "s/["$CHAR2"]/\n/g" \
| sed "s/[!?,][!?,]*/\n/g" \
| sed "s/["$CHAR3"]["$CHAR3"]*/\n/g" \
| sed "s/[~][~]*/\n/g" \
| sed "s/["$CHAR4"]["$CHAR4"]*/\n/g" \
| sed "s/["$CHAR5"]["$CHAR5"]*/\n/g" \
| sed "s/^[ \t]*//g" \
| sed "s/[ \t][ \t]*/ /g" \
| sed "s/[ ][ ]*//g" \
| sed "/^\s*$/d" \
| sed "s/"===Thisistheseparator.==="/\n===This is the separator.===\n/g"> $newfile

#| sed "s/\"\([^\"]*\)\"/\n\1\n/g" \
#| sed "s/\'\([^\']*\)\'/\n\1\n/g" \
#| sed "/^[^ ]*$/d" \
#| sed "s/^ //g" \
#| sed "/^\s*$/d" \
#| sed "s/[^[:print:]]//g" \
#| sed "s/\(\$[0-9][0-9]*\)/\1\n/g" \
