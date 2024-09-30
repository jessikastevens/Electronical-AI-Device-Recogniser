git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_NAME" = "23kngightst813" ];
then
    GIT_AUTHOR_NAME="23knightst813";
    GIT_AUTHOR_EMAIL="23knightst813@collyers.ac.uk";
fi
if [ "$GIT_COMMITTER_NAME" = "23kngightst813" ];
then
    GIT_COMMITTER_NAME="23knightst813";
    GIT_COMMITTER_EMAIL="23knightst813@collyers.ac.uk";
fi
' --tag-name-filter cat -- --branches --tags
