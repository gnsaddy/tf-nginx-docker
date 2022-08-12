#!/bin/bash

# this script is used to rollback the state of the repository to the specified commit hash

echo "********** Rollback to commit **********"

read -p "Enter commit hash: " commit_hash

echo "********** current branch name **********"

git branch | grep \* | cut -d ' ' -f2

git reset --hard $commit_hash

echo "********** Rollback complete **********"

