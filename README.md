# Tavern Hands-on

## REQUIREMENTS

- docker
- docker-compose

## SETUP & RUN TESTS

### docker compose command

1. Get source code

    ```shell
    % git clone git@github.com:aYukiYoshida/tavern_handson.git # via SSH
    ```

1. Build docker images

    ```shell
    % docker compose build
    ```

1. Start docker compose service

    ```shell
    % docker compose up
    ```

1. Run tests

    ```shell
    % tavern.compose.sh [ARGS]
    ```

1. Stop docker compose service

    ```shell
    % docker compose down
    ```

If you run shell prompt in container of Tavern, run the following command.  

```shell
% docker compose exec tavern bash -p
```

### docker command

If you want to only use Tavern, run the following commands.  

- Build docker image

    ```shell
    % docker build -t tavern -f docker/tavern.dockerfile .
    ```

- Run tests

    ```shell
    % tavern.sh [ARGS]
    ```

---
