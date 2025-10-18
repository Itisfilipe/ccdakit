# Builder Pattern

Understanding the builder pattern in ccdakit.

## Builder Architecture

Builders convert protocol-compliant data into XML elements using lxml.

### Basic Builder

```python
from ccdakit.core.base import CDAElement
from lxml import etree

class MyBuilder(CDAElement):
    def __init__(self, data, version):
        super().__init__(version)
        self.data = data

    def build(self) -> etree._Element:
        # Create XML element
        element = etree.Element("myElement")
        element.set("classCode", "OBS")

        # Add child elements
        code = etree.SubElement(element, "code")
        code.set("code", self.data.code)
        code.set("codeSystem", "2.16.840.1.113883.6.96")

        return element
```

## Section Builders

Section builders follow a standard pattern:

```python
class MySection(CDAElement):
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.X",
                extension="2015-08-01"
            )
        ]
    }

    def __init__(self, items, version=CDAVersion.R2_1):
        super().__init__(version)
        self.items = items

    def build(self) -> etree._Element:
        section = etree.Element("section")

        # Add template IDs
        self._add_template_ids(section)

        # Add section code
        code = etree.SubElement(section, "code")
        code.set("code", "12345-6")
        code.set("codeSystem", "2.16.840.1.113883.6.1")

        # Add title
        title = etree.SubElement(section, "title")
        title.text = "My Section"

        # Add narrative
        self._add_narrative(section)

        # Add entries
        for item in self.items:
            self._add_entry(section, item)

        return section
```

## Reusable Components

ccdakit provides reusable builders for common elements:

### Code Builder

```python
from ccdakit.builders.common import Code

code_element = Code(
    code="12345",
    code_system="2.16.840.1.113883.6.96",
    display_name="Example Code"
).build()
```

### EffectiveTime Builder

```python
from ccdakit.builders.common import EffectiveTime
from datetime import datetime

time_element = EffectiveTime(
    value=datetime.now()
).build()
```

## Next Steps

- [Architecture](architecture.md)
- [API Reference](../api/builders.md)
