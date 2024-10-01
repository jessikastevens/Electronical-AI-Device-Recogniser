#!/bin/bash

builder_checker() {
    output=$(docker buildx inspect my-builder-hbt-heuristiq-cp-whole 2>&1)

    if [[ "$output" == "ERROR: no builder \" my-builder-hbt-heuristiq-cp-whole\" found" ]]; then
        echo "Builder not found"
        docker buildx create --use --name "my-builder-hbt-heuristiq-cp-whole"
    else
        echo "Builder found"
        docker buildx use my-builder-hbt-heuristiq-cp-whole
    fi
}

version_increase() {
    if [ -f "$VERSION_FILE" ]; then
        VERSION=$(cat $VERSION_FILE)
        VERSION=$(echo $VERSION | awk -F. -v OFS=. '{$NF++;print}')
    else
        VERSION="1.0.0"
    fi
    echo $VERSION >$VERSION_FILE
}