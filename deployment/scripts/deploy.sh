#!/usr/bin/env bash

set -e

function check_swarm_connection(){
    echo "Check Data Server Swarm Connection.."
    export DATA_SERVER=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA services manager'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
    if [ -z "$DATA_SERVER" ]; then
        echo -e "There is no Data Service Manager in $AWS_REGION.\n"
        echo -e "Skip deployment in $AWS_REGION.\n"
        exit 0
    else
        nc -z -v $DATA_SERVER 2375
        if [ "$?" != 0 ]; then
            echo -e "Swarm Service is not running...\n"
            echo -e "Failed deployment to $AWS_REGION \n"
            exit 1
        fi
    fi
}

function login_ecr(){
    echo "Login ECR."
    eval $(aws ecr get-login --no-include-email --region us-west-1)
    if [ "$?" -ne 0 ]; then
        echo "Cannot login ECR."
        exit 1
    fi
}

function prepare_deploy(){
    echo "Start to deploy on $AWS_REGION.."

    export DATA_SERVER=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA services manager'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
    export DATA_WORKER_1=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA services worker 1'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
    export DATA_WORKER_2=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA services worker 2'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
    export DATA_WORKER_3=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA services worker 3'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
    
    export DRUID_QUERY_SERVER=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA druid query server'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
    export ELK_URL=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='elk'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
    export DATA_WEBSOCKET_SERVER=$(aws ec2 --region $AWS_REGION describe-instances --filters "Name=tag:Name,Values='DATA services manager'" --query "Reservations[*].Instances[*].PublicIpAddress" --output=text)
    export DATA_DB_HOST=$(aws rds --region $AWS_REGION describe-db-instances --db-instance-identifier="DATA-admin-gui-db" | jq -r '.DBInstances[] | .Endpoint.Address')
    export DATA_DB_NAME=DATA
    export DATA_DB_USER=DATA
    export DATA_DB_PASSWORD=DATA
    export DATA_DB_PORT=5432
    export AWS_ACCESS_KEY_ID=AAAAAAAAAAAAAAAAAAAAAAA
    export AWS_SECRET_ACCESS_KEY=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

    sed -e "s|REPOSITORY_URI|$REPOSITORY_URI|g" \
        -e "s|%DATA_DB_NAME%|$DATA_DB_NAME|g" \
        -e "s|%DATA_DB_HOST%|$DATA_DB_HOST|g" \
        -e "s|%DATA_DB_USER%|$DATA_DB_USER|g" \
        -e "s|%DATA_DB_PASSWORD%|$DATA_DB_PASSWORD|g" \
        -e "s|%DATA_DB_PORT%|$DATA_DB_PORT|g" \
        -e "s|%AWS_ACCESS_KEY_ID%|$AWS_ACCESS_KEY_ID|g" \
        -e "s|%AWS_SECRET_ACCESS_KEY%|$AWS_SECRET_ACCESS_KEY|g" \
        -e "s|%DATA_SERVER%|$DATA_SERVER|g" \
        -e "s|%DATA_WORKER_1%|$DATA_WORKER_1|g" \
        -e "s|%DATA_WORKER_2%|$DATA_WORKER_2|g" \
        -e "s|%DATA_WORKER_3%|$DATA_WORKER_3|g" \
        -e "s|%DRUID_QUERY_SERVER%|$DRUID_QUERY_SERVER|g" \
        -e "s|%ELK_URL%|$ELK_URL|g" \
        -e "s|%DATA_WEBSOCKET_SERVER%|$DATA_WEBSOCKET_SERVER|g" \
        deployment/docker/docker-compose.yml.tpl > deployment/docker/docker-compose.yml
}

function deploy(){
    DOCKER_COMPOSE_FILE="./deployment/docker/docker-compose.yml"
    echo "Deploying DATA Admin GUI Service..."
    docker -H tcp://${DATA_SERVER}:2375 stack deploy -c $DOCKER_COMPOSE_FILE --with-registry-auth --resolve-image=always DATA
    echo "Finished deploying DATA Admin GUI Service..."
}

AWS_REGION=$1
if [ -z "$AWS_REGION" ]; then 
    echo "\$AWS_REGION is null"
    exit 1
else
    check_swarm_connection
    login_ecr
    prepare_deploy
    deploy
fi
