echo Start revoke cert
cat scripts/auth-cert_automation.$1 | $2 ca-revoke
echo End revoke cert

