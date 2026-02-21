#!/usr/bin/env sh

set -e

: "${HOST:=0.0.0.0}"
: "${PORT:=3001}"
: "${NODE_ENV:=development}"

export HOST PORT NODE_ENV

echo "Starting in $NODE_ENV on $HOST:$PORT"

if [ "$NODE_ENV" = "production" ]; then
  # To build the application in production mode, uncomment the line below:
  # npm run build
  npm run start
else
  # Start the application in development mode
  npm run dev
fi

