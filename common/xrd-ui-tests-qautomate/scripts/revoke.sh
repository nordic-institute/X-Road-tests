echo Start revoke cert
cat scripts/sign-cert_automation.$1 | $2 ca-revoke
echo End revoke cert

