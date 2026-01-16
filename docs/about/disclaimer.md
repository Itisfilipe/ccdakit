# Disclaimer

## Not an Official HL7 Product

**ccdakit is an independent, community-driven project and is NOT an official product of HL7 International.**

This library is:
- **Not affiliated with** HL7 International
- **Not endorsed by** HL7 International
- **Not officially recognized** by HL7 International
- **Not certified** by any regulatory body

### Trademarks

HL7®, Health Level Seven®, and C-CDA® are registered trademarks of Health Level Seven International. The use of these trademarks does not imply any affiliation with or endorsement by HL7 International.

## AI-Assisted Development

This project was **developed extensively with AI assistance** using Claude Code by Anthropic.

### What This Means

- **Code Generation:** Significant portions of code were generated or assisted by AI
- **Documentation:** Most documentation, including the comprehensive HL7/C-CDA guide, was created with AI assistance
- **Testing:** Test suites were developed with AI support
- **Architecture:** Design patterns and architectural decisions involved AI collaboration

### Quality Assurance

Despite AI assistance, this project includes:
- ✅ Comprehensive test suite (3,825 tests, 28% coverage)
- ✅ Validation against official HL7 specifications
- ✅ Manual review and verification of implementations
- ✅ Verification of Template IDs against official specifications
- ✅ Cross-checking with official C-CDA documentation

## Usage Disclaimer

### For Development and Testing

This library is suitable for:
- Development and testing environments
- Educational purposes
- Prototyping and proof-of-concept projects
- Learning C-CDA standards
- Non-critical applications

### Production Use Warning

**⚠️ Before using in production:**

1. **Thorough Testing Required**
   - Validate all generated documents against official HL7 validators
   - Test with your specific use cases and data
   - Perform security audits as needed

2. **Regulatory Compliance**
   - Consult official HL7 C-CDA specifications
   - Verify compliance with ONC certification requirements if applicable
   - Engage qualified HL7 consultants for regulatory guidance
   - Perform independent validation and testing

3. **Medical/Clinical Use**
   - This software handles healthcare data - treat it with appropriate care
   - Ensure HIPAA compliance in your implementation
   - Follow all applicable healthcare data regulations
   - Have qualified healthcare IT professionals review your implementation

4. **Legal Review**
   - Review the MIT License terms
   - Understand liability limitations
   - Ensure compliance with your organization's policies

## No Warranty

This software is provided "AS IS" without warranty of any kind, express or implied. See the [MIT License](license.md) for full details.

**The authors and contributors:**
- Make no warranties about the suitability of this software for any purpose
- Are not liable for any damages arising from use of this software
- Do not guarantee compliance with any regulations or standards
- Do not guarantee the accuracy or completeness of generated documents

## Validation and Testing

While we strive for correctness:

- **Always validate** generated documents with official tools:
  - [NIST C-CDA Validator](https://sitenv.org/ccda-validator)
  - [HL7 C-CDA Validator](https://www.hl7validator.com/)

- **Always test** with your specific:
  - Data models and workflows
  - Integration points
  - Regulatory requirements
  - Use cases

- **Always consult** official sources:
  - [HL7 C-CDA R2.1 Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
  - [HL7 CDA Release 2](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=7)
  - Official HL7 specifications and errata

## Official HL7 Resources

For authoritative guidance on C-CDA standards:

- **HL7 International:** [https://www.hl7.org/](https://www.hl7.org/)
- **C-CDA Specifications:** [http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- **HL7 Working Groups:** [https://www.hl7.org/special/committees/index.cfm](https://www.hl7.org/special/committees/index.cfm)

## Community Support

This is a community project with community support:

- Issues and bugs: [GitHub Issues](https://github.com/Itisfilipe/ccdakit/issues)
- Questions and discussion: [GitHub Discussions](https://github.com/Itisfilipe/ccdakit/discussions)
- Documentation: This documentation site

**We do not provide:**
- Official HL7 support
- Regulatory compliance consulting
- Legal advice
- Healthcare IT consulting
- Production support guarantees

## Contributions

Contributions are welcome! By contributing, you acknowledge:
- Your contributions may be assisted by AI tools
- You agree to the MIT License terms
- Your contributions do not make this an official HL7 project
- You understand the disclaimer terms

See [Contributing Guide](../development/contributing.md) for details.

## Contact

For questions about HL7 standards themselves, please contact HL7 International directly.

For questions about this library, please use GitHub Issues or Discussions.

---

**Last Updated:** January 2026

**Bottom Line:** This is an independent, AI-assisted tool to help you work with C-CDA. It's not official. Test thoroughly. Validate everything. Use at your own risk. Consult official HL7 resources for authoritative guidance.
