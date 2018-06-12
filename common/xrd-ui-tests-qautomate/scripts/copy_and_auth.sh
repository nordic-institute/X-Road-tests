whoami
echo Start cert copy
echo $1
ls -la /home/jenkins/Downloads/
cp -f $1auth_csr*.$2 scripts/temp_auth.$2
rm -f $1auth_csr*.$2
ls -la scripts
echo End cert copy
echo Start cert sign-auth
echo $2
cat scripts/temp_auth.$2 | $3 > scripts/auth-cert_automation.$2
echo End cert sign-auth
