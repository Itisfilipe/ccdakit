# Protocol System

Deep dive into the protocol system.

## What Are Protocols?

Protocols are Python's way of defining structural types (also called "duck typing"). Unlike interfaces in other languages, protocols don't require explicit inheritance.

## How It Works

```python
from typing import Protocol

# Define the contract
class ProblemProtocol(Protocol):
    @property
    def name(self) -> str:
        """Problem name."""
        ...

    @property
    def code(self) -> str:
        """Diagnostic code."""
        ...

# Any class with these properties satisfies the protocol
class MyProblem:
    def __init__(self, name: str, code: str):
        self._name = name
        self._code = code

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> str:
        return self._code

# Type checker understands this works
def process_problem(problem: ProblemProtocol):
    print(problem.name, problem.code)

# This is valid!
process_problem(MyProblem("Diabetes", "73211009"))
```

## Benefits

1. **No Inheritance**: Your classes stay independent
2. **Type Safety**: IDEs and type checkers understand the contracts
3. **Flexibility**: Works with any Python class structure
4. **Testability**: Easy to mock and stub

## Protocol Design Principles

### Required vs Optional

```python
class PatientProtocol(Protocol):
    # Required properties
    @property
    def first_name(self) -> str: ...

    @property
    def last_name(self) -> str: ...

    # Optional property (returns Optional type)
    @property
    def middle_name(self) -> Optional[str]: ...
```

### Runtime Checking

Protocols are primarily for static type checking, but you can check at runtime:

```python
from typing import runtime_checkable

@runtime_checkable
class PatientProtocol(Protocol):
    @property
    def first_name(self) -> str: ...

# Runtime check
if isinstance(obj, PatientProtocol):
    print("It's a patient!")
```

## Next Steps

- [Protocols API Reference](../api/protocols.md)
- [Custom Models](../examples/custom-models.md)
