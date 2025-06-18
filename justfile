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

# Push to dev site
push-dev:
    rclone sync dist $RCLONE_DEV_TARGET --progress
    @echo "Deployed to $RCLONE_DEV_TARGET"

# Build the site
[confirm]
push-prod:
    rclone sync dist $RCLONE_PROD_TARGET --progress
    @echo "Deployed to $RCLONE_PROD_TARGET"

# Build and deploy to dev, then ask about prod
deploy: build copy-assets push-dev push-prod

# Re-run loaders, then build and deploy to prod
nightly: inv-all build copy-assets push-dev
