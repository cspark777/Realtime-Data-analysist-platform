#!/bin/bash

FAIL_CODE=6
LRED="\033[1;31m" # Light Red
LGREEN="\033[1;32m" # Light Green
NC='\033[0m' # No Color

function check_status(){
    SERVER=$1
    PORT=$2
    curl -v http://$SERVER:$PORT > /dev/null

    if [ ! $? = ${FAIL_CODE} ];then
        echo -e "${LGREEN}$SERVER is online on $PORT${NC}"
    else
        echo -e "${LRED}$SERVER is down on$PORT${NC}"
    fi
}

AWS_REGION=$1

DATA_SERVER=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA services manager'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
DRUID_QUERY_SERVER=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA druid query server'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
ELK_URL=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='elk'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)


if [ -z "$AWS_REGION" ]; then 
    echo "\$AWS_REGION is null"
    exit 1
elif [ -z "$DATA_SERVER" ] || [ -z "$DRUID_QUERY_SERVER" ] || [ -z "$ELK_URL" ]; then
    echo "Skip validate in $AWS_REGION"
    exit 0
else
    echo -e "${LGREEN}Checking DATA Admin GUI.."
    check_status ${DATA_SERVER} 80      # DATA
    echo -e "${LGREEN}Checking DATA Server"
    check_status ${DATA_SERVER} 81      # DATA
    echo -e "${LGREEN}Checking Swarm Visualizer"
    check_status ${DATA_SERVER} 9000    # SWARM VISUALIZER
    echo -e "${LGREEN}Checking Druid Query Server"
    check_status ${DRUID_QUERY_SERVER} 8888 # DRUID
    echo -e "${LGREEN}Checking Pivot Service"
    check_status ${DRUID_QUERY_SERVER} 9095 # PIVOT
    echo -e "${LGREEN}Checking ELK Service"
    check_status ${ELK_URL} 80              # ELK
fi



