echo Using Openssl to Generate a Private Key and Certificate in PEM and DER formats
echo Configure the certificate in requests.txt 

echo delete existing request.csr, key and cert files
del request.csr
del key.pem
del key.der
del cert.pem
del cert.der

rem create a private_key and a certificate signing request
openssl.exe req -newkey rsa:2048 -keyout key.pem -nodes -out request.csr -config request.txt

rem sign the certificate signing request, and produce a certificate
openssl.exe x509 -req -sha256 -days 365 -in request.csr -signkey key.pem -out cert.pem

rem convert the certifivate from pem format to der format
openssl x509 -in cert.pem -out cert.der -outform DER

rem convert the private key from pem format to der format
openssl.exe rsa -in key.pem -out key.der -outform DER

rem copying the .der files to the src folder
copy *.der ..\src /Y
