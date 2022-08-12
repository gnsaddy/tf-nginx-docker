#!/bin/bash
echo "********** New git commit **********"

echo "********** Commit message **********"

read -p "Enter commit message: " commit_message

git add .

git commit -m "$commit_message"

echo "********** Branch name **********"

# check current branch name

git branch | grep \* | cut -d ' ' -f2

read -p "Enter branch name: " branch_name

git push origin $branch_name