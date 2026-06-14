#!/bin/bash

UserID=$(id -u)
GroupID=$(id -g)
MOUNT_DIR=/tmp
BKP_DIR="${MOUNT_DIR}/org_main-org/dashboards"
TARGET_DIR=./grafana/
set -x
#tool is gdg> 0.5
sudo docker run --rm -v ./grafana_importer.yml:/app/config/importer.yml \
	-v $MOUNT_DIR:/app/exports -it ghcr.io/esnet/gdg backup dash list
sudo docker run --rm -v ./grafana_importer.yml:/app/config/importer.yml \
	-v $MOUNT_DIR:/app/exports -it ghcr.io/esnet/gdg backup dash download 
sudo cp -r $BKP_DIR $TARGET_DIR 
sudo chown -R $UserID:$GroupID $TARGET_DIR

#./restart_grafana.sh
#rm -rf $BKP_DIR
