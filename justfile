set dotenv-load

# List commands, default
default:
  just --list

# Build the site in docker
build:
    -docker run -it --rm \
        -v .:/app \
        -w /app \
        -u "$(id -u):$(id -g)" \
        -p 3000:3000 \
        --name node \
        node:23-bookworm \
        npx observable build

# Start the dev server in docker
dev:
    -docker run -it --rm \
        -v .:/app \
        -w /app \
        -u "$(id -u):$(id -g)" \
        -p 3000:3000 \
        --name node \
        node:23-bookworm \
        npx observable preview --host 0.0.0.0

# Start a shell in the docker container
shell:
    -docker run -it --rm \
        -v .:/app \
        -w /app \
        -u "$(id -u):$(id -g)" \
        -p 3000:3000 \
        --name node \
        node:23-bookworm \
        bash
