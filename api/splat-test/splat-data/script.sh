#!/bin/bash  
shopt -s nullglob  
for f in ./K10/*.hgt; do  
    echo "Converting $f"  
    srtm2sdf $f 
done 
