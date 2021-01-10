#
# Docker for semviwer
# 
# - inner port: 8080 
# - Google Cloud Run expects containers to serve things on port 8080
#
# EE Jan '21

FROM node

RUN apt update

# Dont use / as working directory since gcloud gives error for npm install
WORKDIR /home/node

COPY index.js /home/node/index.js
COPY semviewer.html /home/node/semviewer.html
COPY output2.nrrd /home/node/output.nrrd

# Install node dependencies.
RUN npm i express
RUN npm install --only=production


# gcloud 
CMD [ "node", "index.js" ]