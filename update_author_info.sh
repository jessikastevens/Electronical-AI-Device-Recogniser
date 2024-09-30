git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "144670355+23knightst813@users.noreply.github.com" ];
then
    GIT_AUTHOR_EMAIL="23knightst813@collyers.ac.uk";
fi
if [ "$GIT_COMMITTER_EMAIL" = "144670355+23knightst813@users.noreply.github.com" ];
then
    GIT_COMMITTER_EMAIL="23knightst813@collyers.ac.uk";
fi
' --tag-name-filter cat -- --branches --tags
