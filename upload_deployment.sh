#!/usr/bin/env bash


cd lambda
zip -r alexa-pugs-adventures.zip ./*
mv alexa-pugs-adventures.zip ../
cd ../


aws s3 cp ./alexa-pugs-adventures.zip s3://crossfade-alexa-deployment/pugs-adventures/  --profile=crossfade

aws lambda update-function-code --function-name AlexaPugsAdventures --s3-bucket crossfade-alexa-deployment --s3-key pugs-adventures/alexa-pugs-adventures.zip --publish --profile=crossfade --region us-east-1
# final location
# s3://crossfade-alexa-deployment/pugs-adventures/alexa-pugs-adventures.zip