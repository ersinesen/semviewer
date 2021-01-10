#
# Docker for semviwer
# 
# - inner port: 8080 
# - Google Cloud Run expects containers to serve things on port 8080
#
# EE Jan '21

FROM node

RUN apt update

COPY index.js index.js
COPY semviewer.html semviewer.html
COPY output.nrrd output.nrrd

# Install node dependencies.
RUN npm i express
RUN npm install --only=production


# gcloud 
CMD [ "node", "index.js" ]