# Null Flavors in C-CDA

This guide explains how to use null flavors correctly in ccdakit when building C-CDA documents.

## What are Null Flavors?

Null flavors are standardized codes used in HL7 C-CDA documents to indicate why data is missing or not available for SHALL (required) elements. According to the HL7 specification, when a required element has no data, you must either provide a value OR use an appropriate null flavor.

## When to Use Null Flavors

### SHALL Elements (Required)

When a SHALL element has no data available, you **MUST** use a null flavor. Omitting the element entirely will cause validation errors.

**Example**: If a patient cannot remember when their allergy started, the `effectiveTime/low` element must still be present with `nullFlavor="UNK"`.

### MAY/SHOULD Elements (Optional)

For MAY or SHOULD elements, if no data is available, you can simply omit the entire element. Null flavors are not required.

## Standard Null Flavor Values

ccdakit provides the `NullFlavor` class with all standard HL7 null flavor values:

| Code  | Name | Usage |
|-------|------|-------|
| `NI`  | No Information | The value was not sought or is not available |
| `UNK` | Unknown | A proper value is applicable but is not known |
| `NA`  | Not Applicable | No proper value is applicable in this context |
| `ASKU` | Asked but Unknown | Information was sought but not found |
| `OTH` | Other | The actual value is not a member of the permitted value set |
| `NASK` | Not Asked | This information has not been sought |
| `MSK` | Masked | Information exists but has been masked for security/privacy |
| `NP` | Not Present | Value is exceptional (e.g., reference element points elsewhere) |
| `NINF` | Negative Infinity | Negative infinity value |
| `PINF` | Positive Infinity | Positive infinity value |

## Using the Null Flavor Utility

### Import the Module

```python
from ccdakit.utils.null_flavors import (
    NullFlavor,
    create_null_code,
    create_null_value,
    create_null_id,
    create_null_time,
    create_null_time_low,
    create_null_time_high,
    add_null_flavor,
    should_use_null_flavor,
    get_default_null_flavor_for_element,
)
```

### Common Patterns

#### 1. Code Not in Value Set

When a code is required but the actual value is not in the permitted value set:

```python
# Instead of manually creating:
code_elem = etree.SubElement(obs, f"{{{NS}}}code")
code_elem.set("nullFlavor", "OTH")
text_elem = etree.SubElement(code_elem, f"{{{NS}}}originalText")
text_elem.text = "Custom medication"

# Use the utility:
code_elem = create_null_code("OTH", "Custom medication")
obs.append(code_elem)
```

#### 2. Unknown Date/Time

When a date or time is required but unknown:

```python
# For unknown onset date:
low_elem = create_null_time_low("UNK")
time_elem.append(low_elem)

# For ongoing condition (no end date):
high_elem = create_null_time_high("UNK")
time_elem.append(high_elem)

# For not applicable (advance directive with no end):
high_elem = create_null_time_high("NA")
time_elem.append(high_elem)
```

#### 3. Unknown Identifier

When an ID is required but not available:

```python
id_elem = create_null_id("UNK")
participant_role.append(id_elem)
```

#### 4. Value Not in Permitted Set

When an observation value is required but not in the permitted value set:

```python
value_elem = create_null_value("CD", "OTH", "Patient reported severity")
obs.append(value_elem)
```

#### 5. Section with No Information

When a section may have `nullFlavor="NI"` to indicate no information available:

```python
section = etree.Element(f"{{{NS}}}section")
if null_flavor:
    add_null_flavor(section, "NI")
```

### Helper Functions

#### Check if Null Flavor Should Be Used

```python
# Determine if you should use a null flavor
if should_use_null_flavor(patient_data.onset_date, required=True):
    low_elem = create_null_time_low("UNK")
else:
    low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
    low_elem.set("value", format_date(patient_data.onset_date))
```

#### Get Default Null Flavor for Element Type

```python
# Get recommended null flavor for an element type
null_flavor = get_default_null_flavor_for_element("code")  # Returns "OTH"
null_flavor = get_default_null_flavor_for_element("id")    # Returns "UNK"
null_flavor = get_default_null_flavor_for_element("time")  # Returns "UNK"
```

## Best Practices

### 1. Use Most Specific Null Flavor

Choose the null flavor that best describes why data is missing:

- **UNK** when data exists but is not known (patient doesn't remember)
- **NI** when data was not sought or collected
- **ASKU** when you explicitly asked but couldn't determine
- **OTH** when value doesn't fit permitted value set
- **NA** when not applicable (e.g., end date for ongoing condition)

### 2. Include originalText When Using OTH

When using `nullFlavor="OTH"` for codes or values, always include `originalText` to provide the actual value:

```python
code_elem = create_null_code("OTH", "Patient's home remedy tea")
```

### 3. Document Null Flavor Decisions

Add comments explaining why null flavors are used:

```python
# CONF:1198-32449: If no ending time, high SHALL have nullFlavor="NA"
if not self.directive.end_date:
    high_elem = create_null_time_high("NA")
```

### 4. Validate Against C-CDA Rules

Different null flavors are permitted in different contexts. Check the C-CDA specification for your specific template to ensure the null flavor is allowed.

## Common Scenarios

### Allergy with Unknown Onset

```python
def _add_effective_time(self, obs: etree._Element) -> None:
    """Add effectiveTime with onset date or null flavor if unknown."""
    time_elem = etree.SubElement(obs, f"{{{NS}}}effectiveTime")

    if self.allergy.onset_date:
        time_elem.set("value", self.allergy.onset_date.strftime("%Y%m%d"))
    else:
        # Patient doesn't remember onset date
        add_null_flavor(time_elem, "UNK")
```

### Medication with Unknown Route

```python
def _add_route(self, sub_admin: etree._Element) -> None:
    """Add route code or null flavor if not specified."""
    route_elem = etree.SubElement(sub_admin, f"{{{NS}}}routeCode")

    if self.medication.route_code:
        route_elem.set("code", self.medication.route_code)
        route_elem.set("codeSystem", self.ROUTE_OID)
    else:
        # Route not specified
        add_null_flavor(route_elem, "UNK")
```

### Advance Directive with No End Date

```python
def _add_effective_time(self, obs: etree._Element) -> None:
    """Add effectiveTime with low and high elements."""
    time_elem = etree.SubElement(obs, f"{{{NS}}}effectiveTime")

    # Start date (required)
    low_elem = create_null_time_low("UNK" if not self.directive.start_date else None)
    if self.directive.start_date:
        low_elem.set("value", self.directive.start_date.strftime("%Y%m%d"))
    time_elem.append(low_elem)

    # End date - use NA if directive has no specified ending
    if self.directive.end_date:
        high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
        high_elem.set("value", self.directive.end_date.strftime("%Y%m%d"))
    else:
        # CONF:1198-32449: No specified ending time
        high_elem = create_null_time_high("NA")
        time_elem.append(high_elem)
```

### Section with No Information Available

```python
def build(self) -> etree.Element:
    """Build section with optional null flavor."""
    section = etree.Element(f"{{{NS}}}section")

    # Add null flavor if no information available (CONF:1198-32802)
    if self.null_flavor:
        add_null_flavor(section, self.null_flavor)

    # ... rest of section building

    # If nullFlavor is not present, SHALL contain at least one entry
    if not self.null_flavor:
        for item in self.items:
            self._add_entry(section, item)

    return section
```

## Migration Guide for Existing Builders

If you have existing builders that manually set null flavors, consider migrating to the standardized utilities:

### Before (Manual)

```python
code_elem = etree.SubElement(obs, f"{{{NS}}}code")
code_elem.set("nullFlavor", "OTH")
text_elem = etree.SubElement(code_elem, f"{{{NS}}}originalText")
text_elem.text = medication.name
```

### After (Using Utility)

```python
from ccdakit.utils.null_flavors import create_null_code

code_elem = create_null_code("OTH", medication.name)
obs.append(code_elem)
```

### Before (Manual effectiveTime)

```python
if not problem.onset_date:
    low_elem.set("nullFlavor", "UNK")
```

### After (Using Utility)

```python
from ccdakit.utils.null_flavors import create_null_time_low

if not problem.onset_date:
    low_elem = create_null_time_low("UNK")
else:
    low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
    low_elem.set("value", format_date(problem.onset_date))
time_elem.append(low_elem)
```

## Testing Null Flavors

When testing builders that use null flavors:

```python
def test_allergy_with_unknown_onset():
    """Test allergy with unknown onset date uses correct null flavor."""
    # Create allergy with no onset date
    allergy_data = SimpleNamespace(
        allergen="Penicillin",
        onset_date=None,  # Unknown
        # ... other fields
    )

    builder = AllergyObservation(allergy_data)
    elem = builder.to_element()

    # Verify null flavor is present
    time_elem = elem.find(f"{{{NS}}}effectiveTime")
    assert time_elem is not None
    assert time_elem.get("nullFlavor") == "UNK"
```

## Validation

The null flavor utilities include validation:

```python
from ccdakit.utils.null_flavors import add_null_flavor

# This will raise ValueError - invalid null flavor
try:
    add_null_flavor(elem, "INVALID")
except ValueError as e:
    print(f"Error: {e}")
    # Error: Invalid null flavor: INVALID. Must be one of: NI, UNK, NA, ...
```

## References

- [HL7 V3 Data Types - Null Flavors](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=264)
- [C-CDA Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- [Null Flavor Utility API Documentation](../api/utilities.md#null-flavors)

## See Also

- [Builder Pattern](builders.md) - Overview of builder architecture
- [C-CDA Conformance](../guides/hl7-guide/03-templates-and-conformance.md) - Understanding SHALL/SHOULD/MAY
- [Testing Guide](testing.md) - How to test builders with null flavors
