import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

def generate_self_signed_cert():
    print("Starting certificate generation...")

    os.makedirs('certs', exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    subject = x509.Name([
        x509.NameAttribute(x509.NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(x509.NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, u"My Organization"),
        x509.NameAttribute(x509.NameOID.COMMON_NAME, u"localhost"),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False)
        .sign(private_key, hashes.SHA256(), default_backend())
    )

    # Check sizes and write to files
    cert_bytes = cert.public_bytes(encoding=serialization.Encoding.PEM)
    print(f"Certificate size: {len(cert_bytes)}")
    
    with open("certs/cert.pem", "wb") as f:
        f.write(cert_bytes)
        print("cert.pem written successfully.")

    key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    print(f"Private key size: {len(key_bytes)}")
    
    with open("certs/key.pem", "wb") as f:
        f.write(key_bytes)
        print("key.pem written successfully.")

    print("Certificate generation completed.")

if __name__ == "__main__":
    generate_self_signed_cert()
