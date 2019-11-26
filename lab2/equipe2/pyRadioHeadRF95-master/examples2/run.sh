# !/bin/bash

#cd /home/pi/pyRadioHeadRF95-master/examples2 
echo "NOVA MEDICAO" >> pegapls.txt
./waterQuality_gateway.py >> pegapls.txt &
