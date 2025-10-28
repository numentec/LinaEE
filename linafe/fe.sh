#!/usr/bin/env sh
set -e

: "${HOST:=0.0.0.0}"
: "${PORT:=3001}"

export HOST PORT

if [ "$NODE_ENV" = "production" ]; then
  # To build and start the application in production mode, uncomment the lines below:
  echo "Starting in production on $HOST:$PORT"
  # npm run build
  npm run start
else
  # Start the application in development mode
  echo "Starting in dev on $HOST:$PORT"
  npm run dev
fi