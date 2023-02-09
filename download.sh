rm -rf ./src/data
export FILEID=1WE1lWdCd9goa7cRnOgeQq_2qHEdjxrSQ
export FILENAME=incognia-cin-data.zip
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$FILEID" -O $FILENAME && rm -rf /tmp/cookies.txt
unzip -P $INCOGNIA_CASE_PASSWORD incognia-cin-data.zip -d ./src
mv ./src/incognia-cin-data ./src/data
rm -rf ./src/incognia-cin-data.zip
rm -rf ./incognia-cin-data.zip