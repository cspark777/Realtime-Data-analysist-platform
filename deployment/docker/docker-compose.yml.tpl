version: '3.7'

networks:
  frontend:
    driver: overlay
  backend:
    driver: overlay

services:

  admin-gui-proxy:
    image: dockercloud/haproxy
    depends_on:
      - admin-gui
    environment:
      - BALANCE=leastconn
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 80:80
    networks:
      - frontend
    deploy:
      placement:
        constraints: [node.role == manager]

  admin-gui:
    image: REPOSITORY_URI/data-admin-gui:stable
    ports:
      - "8000:8000"
      - "8888"
    deploy:
      resources:
        limits:
          cpus: '0.60'
          memory: 500M
        reservations:
          cpus: '0.20'
          memory: 200M
      replicas: 4
      restart_policy:
        condition: on-failure
    volumes:
      - static:/data-admin-gui/static
    environment:
      - ALLOWED_HOSTS=*
      - DB_NAME=%DATA_DB_NAME%
      - DB_HOST=%DATA_DB_HOST%
      - DB_USER=%DATA_DB_USER%
      - DB_PASSWORD=%DATA_DB_PASSWORD%
      - DB_PORT=%DATA_DB_PORT%
      - AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%
      - AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%
      - DATA_SERVER=http://%DATA_SERVER%:81/
      - SERVICE_PORTS=8000
      - KAFKA_URL="%DATA_SERVER%:9092,%DATA_WORKER_1%:9092,%DATA_WORKER_2%:9092,%DATA_WORKER_3%:9092"
      - KAFKA_URL_PUBLIC="%DATA_SERVER%:9094,%DATA_WORKER_1%:9094,%DATA_WORKER_2%:9094,%DATA_WORKER_3%:9094"
      - DRUID_URL=%DRUID_QUERY_SERVER%:8888
      - PIVOT_URL=%DRUID_QUERY_SERVER%:9095
      - ELK_URL=%ELK_URL%
      - WEBSOCKET_SERVER=%DATA_WEBSOCKET_SERVER%:8888
      - SENDER_EMAIL=tech@gmail.com
    depends_on:
      - kafka
    networks:
      - frontend
    # logging:
    #   driver: "fluentd"
    #   options:
    #     fluentd-async-connect: "true"
    #     tag: docker.admin-gui
    #     fluentd-address: %DATA_SERVER%:24224

volumes:
  static:



