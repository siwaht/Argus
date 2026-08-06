---
name: skill-addition
description: Use when the user asks to add or multiply two numbers. Documents the add and multiply operations, their input format, and expected results.
---

# Addition and Multiplication Skill

## Description
This skill can add or multiply two numbers as input and returns the result.

## Usage
Use the command `add(a: number, b: number)` to add two numbers together or `multiply(a: number, b: number)` to multiply two numbers.

## Example
- Input for Addition: `{ "a": 5, "b": 3 }` -> Output: `8`  
- Input for Multiplication: `{ "a": 5, "b": 3 }` -> Output: `15`

## Function Signatures
```python
add(a: int, b: int) -> int
multiply(a: int, b: int) -> int
```