whoami
echo Start cert copy
echo $1
echo $1sign_csr*.$2 scripts/temp.$2
ls -la /home/jenkins/Downloads/
cp -v -f $1sign_csr*.$2 scripts/temp.$2
rm -f $1sign_csr*.$2
ls -la scripts
echo End cert copy
echo Start cert sign-sign
echo $3
cat scripts/temp.der | $3 > scripts/sign-cert_automation.der
echo End cert sign-sign