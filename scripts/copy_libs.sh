#!/bin/bash

# Define the source directory relative to the script location
SOURCE_DIR="$(dirname "$0")/../libs"

# Define the target directory relative to the script location
TARGET_DIR="$(dirname "$0")/../compose_containers"

# Define the tests directory relative to the script location
TESTS_DIR="$(dirname "$0")/../tests"

# Check if the source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Source directory $SOURCE_DIR does not exist."
  exit 1
fi

# Iterate over each subdirectory in the target directory
for CONTAINER_DIR in "$TARGET_DIR"/*; do
  if [ -d "$CONTAINER_DIR" ]; then
    # Remove the existing libs directory if it exists
    if [ -d "$CONTAINER_DIR/libs" ]; then
      rm -rf "$CONTAINER_DIR/libs"
    fi
    # Copy the libs directory to the container directory
    cp -r "$SOURCE_DIR" "$CONTAINER_DIR"
    echo "Copied $SOURCE_DIR to $CONTAINER_DIR"
  fi
done

# Copy the libs directory to the tests directory
if [ -d "$TESTS_DIR" ]; then
  if [ -d "$TESTS_DIR/libs" ]; then
    rm -rf "$TESTS_DIR/libs"
  fi
  cp -r "$SOURCE_DIR" "$TESTS_DIR"
  echo "Copied $SOURCE_DIR to $TESTS_DIR"
fi

echo "Done."