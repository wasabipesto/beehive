set dotenv-load

# List commands, default
default:
  just --list

# Start the dev server
dev:
  npx observable preview

# Clean the dist
clean:
    rm -rf dist

# Build the site
build:
    npx observable build

# Copy in static assets (eventually we won't need this)
copy-assets:
    mkdir dist/assets
    cp -r src/assets/* dist/assets/

# Base invalidation function (private recipe)
_invalidate pattern="":
    find src/.observablehq/cache -type f \( -name "*.json" -o -name "*.csv" \) \
    {{ if pattern != "" { "-path \"*" + pattern + "*\"" } else { "" } }} \
    -exec sh -c 'for file; do mv "$file" "$file.bak" && echo "Moved: $file"; done' sh '{}' \;

# Invalidate all data files
inv-all:
    @just _invalidate

# Invalidate specific data files
inv arg:
    @just _invalidate "{{arg}}"

# Build the site
deploy-dev: build copy-assets
    rclone sync dist $RCLONE_DEV_TARGET --progress
    @echo "Deployed to $RCLONE_DEV_TARGET"

# Build the site
deploy-prod: build copy-assets
    rclone sync dist $RCLONE_PROD_TARGET --progress
    @echo "Deployed to $RCLONE_PROD_TARGET"

# Run nightly build and deploy
nightly: inv-all deploy-dev
