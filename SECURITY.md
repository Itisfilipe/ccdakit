# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in ccdakit, please report it responsibly:

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Send a detailed report to: [filipeamarals@gmail.com](mailto:filipeamarals@gmail.com)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Initial Response**: Within 48 hours
- **Updates**: Every 72 hours until resolved
- **Resolution Timeline**: Critical issues within 7 days, others within 30 days
- **Credit**: Security researchers will be credited (unless they prefer to remain anonymous)

## Security Considerations for Healthcare Data

ccdakit generates HL7 C-CDA documents that may contain Protected Health Information (PHI). Organizations using this library must implement appropriate security measures.

### PHI/HIPAA Compliance

**Important**: ccdakit is a document generation library. HIPAA compliance is the responsibility of the implementing organization, not the library itself.

#### Your Responsibilities

When using ccdakit in a healthcare environment:

1. **Data Protection**
   - Encrypt PHI at rest and in transit
   - Implement access controls per HIPAA Security Rule
   - Maintain audit logs of document generation
   - Use secure channels for document transmission

2. **Minimum Necessary**
   - Only include required data elements
   - Apply appropriate confidentiality codes
   - Implement role-based access controls

3. **Business Associate Agreements**
   - Ensure proper BAAs are in place
   - Document data flows
   - Maintain chain of trust

4. **Data Retention**
   - Follow applicable retention policies
   - Implement secure deletion procedures
   - Document destruction procedures

### XML Security Best Practices

ccdakit generates XML documents. Follow these security practices when processing them:

#### XXE (XML External Entity) Prevention

**Risk**: XML parsers can be exploited to access local files, perform SSRF attacks, or cause denial of service.

**Mitigation**:

```python
from lxml import etree

# SECURE: Disable external entities when parsing user-provided XML
parser = etree.XMLParser(
    resolve_entities=False,  # Disable entity resolution
    no_network=True,         # Disable network access
    dtd_validation=False,    # Disable DTD validation
    load_dtd=False,          # Don't load DTD
)

# Parse with secure parser
tree = etree.parse(xml_file, parser)
```

**Note**: ccdakit's XML generation is safe from XXE attacks. This applies when you're *parsing* C-CDA documents from external sources.

#### XSD Validation Security

When validating documents with XSD schemas:

```python
from ccdakit.validators import XSDValidator

# SECURE: XSDValidator uses secure parser settings by default
validator = XSDValidator()
result = validator.validate(xml_string)

# The validator automatically:
# - Disables external entity resolution
# - Blocks network access
# - Prevents DTD processing
```

#### Input Validation

Always validate data before document generation:

```python
from ccdakit.validators import validate_patient_data

# Validate all input data
if not validate_patient_data(patient):
    raise ValueError("Invalid patient data")

# Sanitize text fields
def sanitize_text(text: str) -> str:
    """Remove potentially dangerous characters."""
    # Remove XML special characters that aren't escaped
    # Remove control characters
    # Limit length
    return text.strip()[:1000]

patient.name = sanitize_text(patient.name)
```

#### Code Injection Prevention

**Risk**: Malicious code system values or codes could be injected.

**Mitigation**:

```python
from ccdakit.validators import CodeSystemValidator

# Validate codes against known code systems
validator = CodeSystemValidator()

# Only allow codes from approved code systems
if not validator.validate_code(code, code_system):
    raise ValueError(f"Invalid code: {code} for system: {code_system}")
```

### Document Generation Security

#### Template Injection Prevention

ccdakit uses builders, not string templates, preventing template injection attacks:

```python
# SECURE: Builders escape all values automatically
from ccdakit.builders.sections import ProblemsSection

# This is safe - builder handles escaping
problem.name = "Test <script>alert('xss')</script>"
section = ProblemsSection(problems=[problem])

# Generated XML will have escaped characters:
# &lt;script&gt;alert('xss')&lt;/script&gt;
```

#### ID Generation Security

Document and element IDs should be cryptographically random:

```python
import uuid

# SECURE: Use UUID4 for document IDs
document_id = str(uuid.uuid4())

# INSECURE: Don't use predictable IDs
# document_id = f"DOC-{counter}"  # Predictable

# INSECURE: Don't expose internal IDs
# document_id = str(patient.database_id)  # Information disclosure
```

### Schematron Validation Security

When using Schematron validation:

```python
from ccdakit.validators import SchematronValidator

# SECURE: SchematronValidator uses secure XSLT processor
validator = SchematronValidator()

# Automatically:
# - Downloads official HL7 schemas
# - Verifies integrity
# - Uses secure XSLT transformation
# - Disables external document access
```

### Cryptographic Considerations

#### Digital Signatures

If you need to sign C-CDA documents:

```python
from lxml import etree
from signxml import XMLSigner

def sign_ccda_document(xml_string: str, private_key_path: str) -> str:
    """
    Sign C-CDA document with digital signature.

    NOTE: This is a conceptual example. Consult cryptography experts
    for production implementations.
    """
    root = etree.fromstring(xml_string.encode())

    # Sign the document
    signer = XMLSigner(
        method=XMLSigner.Method.enveloped,
        digest_algorithm='sha256',
        signature_algorithm='rsa-sha256',
    )

    with open(private_key_path, 'rb') as f:
        key = f.read()

    signed_root = signer.sign(root, key=key)
    return etree.tostring(signed_root, encoding='unicode')
```

#### Encryption

For encrypting C-CDA documents in transit or at rest:

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

def encrypt_ccda(xml_string: str, password: str) -> bytes:
    """
    Encrypt C-CDA document with password.

    NOTE: This is a conceptual example. Use established
    healthcare encryption standards (e.g., Direct Protocol).
    """
    # Derive key from password
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt_should_be_random',  # Use random salt
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    # Encrypt
    f = Fernet(key)
    return f.encrypt(xml_string.encode())
```

### Audit Logging

Maintain security audit logs for document generation:

```python
import logging
from datetime import datetime

# Configure security audit logger
audit_logger = logging.getLogger('ccda_audit')
audit_logger.setLevel(logging.INFO)

def log_document_generation(
    user_id: str,
    patient_id: str,
    document_id: str,
    sections: list[str],
):
    """Log document generation for audit trail."""
    audit_logger.info(
        "CCDA_GENERATED",
        extra={
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "patient_id": patient_id,  # Hashed or anonymized
            "document_id": document_id,
            "sections": sections,
            "action": "generate",
        }
    )
```

### Dependency Security

ccdakit has minimal dependencies to reduce attack surface:

```bash
# Check for known vulnerabilities in dependencies
pip install safety
safety check

# Keep dependencies updated
pip install --upgrade ccdakit
```

### Security Checklist

Before using ccdakit in production:

- [ ] Implement HIPAA-compliant access controls
- [ ] Enable audit logging
- [ ] Use secure XML parsers when reading C-CDA documents
- [ ] Validate all input data
- [ ] Implement encryption for PHI at rest and in transit
- [ ] Use cryptographically random document IDs
- [ ] Review and test error handling (no PHI in error messages)
- [ ] Implement rate limiting for document generation
- [ ] Configure proper authentication and authorization
- [ ] Establish incident response procedures
- [ ] Conduct security testing (penetration testing, code review)
- [ ] Document security architecture
- [ ] Train staff on security procedures

### Known Security Limitations

1. **No Built-in Encryption**: ccdakit generates unencrypted XML. Encryption must be implemented separately.

2. **No Access Controls**: The library doesn't enforce access controls. Implement authorization in your application.

3. **No Digital Signatures**: Document signing must be implemented separately if required.

4. **No Data Masking**: The library doesn't mask or redact PHI. Implement data minimization in your application.

5. **No Network Security**: Document transmission security must be implemented separately (e.g., TLS, Direct Protocol).

### Third-Party Security Assessments

This library has not undergone:
- Penetration testing
- Security audit by third-party firm
- HIPAA compliance certification

**Organizations should conduct their own security assessments before production use.**

### Security Updates

Security patches will be released promptly:
- **Critical**: Within 24-48 hours
- **High**: Within 1 week
- **Medium**: Within 30 days
- **Low**: Next minor release

Subscribe to security advisories:
- Watch the GitHub repository
- Enable GitHub security alerts
- Join the mailing list (when available)

## Secure Coding Practices in ccdakit

The library follows these security practices:

### Input Validation

```python
# All user input is validated
def validate_code(code: str, code_system: str) -> bool:
    """Validate codes against known systems."""
    if not code or not code_system:
        return False

    # Check format
    if not re.match(r'^[A-Za-z0-9\-\.]+$', code):
        return False

    # Validate against code system
    return CodeSystemRegistry.validate(code, code_system)
```

### Output Encoding

```python
# All XML output is properly escaped
from lxml import etree

# Text is automatically escaped
element.text = user_input  # Safe - lxml escapes automatically

# Attribute values are escaped
element.set("value", user_input)  # Safe - lxml escapes automatically
```

### Type Safety

```python
# Strong typing prevents many bugs
from typing import Protocol

class PatientProtocol(Protocol):
    @property
    def name(self) -> str: ...  # Must be string

    @property
    def date_of_birth(self) -> date: ...  # Must be date object
```

### Safe Defaults

```python
# Secure defaults for all configuration
class CDAConfig:
    def __init__(self):
        self.validate_codes = True  # Enabled by default
        self.require_template_ids = True  # Enabled by default
        self.allow_null_flavors = False  # Disabled by default
```

## Contact

For security concerns:
- **Email**: filipeamarals@gmail.com
- **GitHub**: [@Itisfilipe](https://github.com/Itisfilipe)

For general questions:
- **GitHub Issues**: [https://github.com/Itisfilipe/ccdakit/issues](https://github.com/Itisfilipe/ccdakit/issues)
- **GitHub Discussions**: [https://github.com/Itisfilipe/ccdakit/discussions](https://github.com/Itisfilipe/ccdakit/discussions)

---

**Disclaimer**: This security policy provides guidance but does not constitute legal or compliance advice. Organizations must consult with qualified healthcare IT security and compliance professionals to ensure their specific implementation meets all applicable regulations and standards.
