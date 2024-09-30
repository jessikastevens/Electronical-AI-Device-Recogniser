git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_NAME" = "23knightst813" ];
then
    GIT_AUTHOR_EMAIL="144670355+23knightst813@users.noreply.github.com";
fi
if [ "$GIT_COMMITTER_NAME" = "23knightst813" ];
then
    GIT_COMMITTER_EMAIL="144670355+23knightst813@users.noreply.github.com";
fi
' --tag-name-filter cat -- --branches --tags
