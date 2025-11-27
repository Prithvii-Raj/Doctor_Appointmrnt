#✅ Conclusion
# Packing looks similar to creating a collection because both hold multiple values.
#But conceptually, packing is about combining values for assignment or function passing, not about storing  manipulating a dataset.

# 1️⃣ Definitions

# Packing:
# Packing is the process of combining multiple values into a single variable. In Python, this is usually done using tuples, but lists and dictionaries can also be used.

# Unpacking:
# Unpacking is the process of extracting values from a packed structure into separate variables.

# 2️⃣ Types of Packing
# a) Tuple Packing (most common)
# Packing values into a tuple
numbers = 1, 2, 3
print(numbers)  # Output: (1, 2, 3)

# *b) List Packing (using )
values = [1, 2, 3, 4, 5]
*start, end = values
print(start)  # [1, 2, 3, 4]
print(end)    # 5

# **c) Dictionary Packing (using )

# Packing keyword arguments into a dictionary when passing to functions:

def display_info(**kwargs):
    print(kwargs)

display_info(name="Alice", age=25)
# Output: {'name': 'Alice', 'age': 25}

# 3️⃣ Types of Unpacking
# a) Tuple Unpacking
numbers = (1, 2, 3)
a, b, c = numbers
print(a, b, c)  # Output: 1 2 3

# b) List Unpacking with * operator
values = [1, 2, 3, 4, 5]
first, *middle, last = values
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5

# c) Dictionary Unpacking in Function Calls
def greet(name, age):
    print(f"Hello {name}, you are {age} years old")

info = {"name": "Alice", "age": 25}
greet(**info)

# 4️⃣ Nested Packing and Unpacking
# Nested Packing
nested = 1, 2, (3, 4)
print(nested)  # (1, 2, (3, 4))

# Nested Unpacking
nested = (1, 2, (3, 4))
a, b, (c, d) = nested
print(a, b, c, d)  # Output: 1 2 3 4

# Nested Unpacking with *
nested = [1, 2, [3, 4, 5], 6]
a, b, [*c], d = nested
print(a, b, c, d)  # Output: 1 2 [3, 4, 5] 6