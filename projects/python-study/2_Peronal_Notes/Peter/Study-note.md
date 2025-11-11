## Type -> have method
- F-string
- String
- Integer
- Float
- List
- Tuple
- Dictionary
- Set

## Function
- print()
- type()
- len()
- input()
- range()
- sum()

## Definition
- Squre Bracket [] : 리스트, 인덱싱, 슬라이싱
- Parenthesis () : 함수 호출, 튜플
- Curly braces {} : 딕셔너리, 집합

## Operator (연산자)
- 산술: +, -, *, /, //, %, **
- 비교: ==, !=, >, <, >=, <=
- 논리: and, or, not
- 할당: =, +=, -=, *=, /=

## 조건문
```python
if 조건:
    ...
elif 조건:
    ...
else:
    ...
```

## 반복문
```python
for i in range(5):
    print(i)

while 조건:
    ...
```

## 함수 정의
```python
def 함수이름(매개변수):
    return 결과
```

## 모듈 사용
```python
import math
print(math.sqrt(16))
```

## 예외 처리
```python
try:
    ...
except Exception as e:
    print(e)
```

## dir
Here’s how you can explore methods for some common types:

For a string:

python
코드 복사

print(dir(""))
For an integer:

python
코드 복사

print(dir(0))
For a float:

python
코드 복사

print(dir(0.0))
For a dictionary:

python
코드 복사

print(dir({}))
Using dir() with these will provide you with a list of all methods and attributes related to the specific type of object you’re curious about.

## List에 저장하기
> saving results to a list
promotional_descriptions = []
for flavor in ice_cream_flavors:
    prompt = f"""For the ice cream flavor listed below, 
    provide a captivating description that could be used for promotional purposes.

    Flavor: {flavor}

    """
    description = get_llm_response(prompt)
    promotional_descriptions.append(description)



## List와 method syntax
> In the following code, remove the country 
> that is not in South America

countries_in_south_america = ["Colombia", "Peru", 
                              "Brasil", "Japan",
                              "Argentina"]

### WRITE CODE HERE ###
countries_in_south_america.remove("Japan")
### --------------- ###

## Indentation
In for loops, the block of code that should be repeated for each element must be indented (usually with four spaces or a tab) to show that it is part of the loop.

Here's how you can fix the indentation error in your for loop:

python
코드 복사
for task in list_of_tasks:
    print_llm_response(task)


## magic method (or dunder methods)
In Python, the names surrounded by double underscores (like __add__) are known as "magic methods" or "dunder methods" (short for double underscore methods). These methods are used to implement and customize behavior for operators and built-in functions. They are not typically called directly. Instead, they're called automatically in particular situations.

For example:

__add__: This is used when you add objects together using the + operator. For lists, using list1 + list2 will call list1.__add__(list2).

__len__: This is used with the len() function. When you do len(my_list), it calls my_list.__len__().

__getitem__: This is used when accessing elements using the indexing syntax, such as my_list[0], which calls my_list.__getitem__(0).

These methods allow Python objects to use familiar operations, and they help in making your classes work with standard operations and functions. Generally, you don’t call these methods directly; you use the associated operators or functions.


## Argument vs parameter in fuction
> From week 1 lesson

In programming, the term "argument" refers to the actual data you provide to a function when you call it. The reason we use the word "argument" comes from mathematical terminology, where it describes a value that is used in the calculation of a function.

When you define a function, you specify "parameters," which are like placeholders. When you call the function, you provide "arguments," the actual values that fill in those placeholders and allow the function to perform its operations.

Here's a simple example:

python
코드 복사

def greet(name):
    print("Hello, " + name + "!")

greet("Alice")  # "Alice" is the argument
In this example, name is the parameter in the function definition, and "Alice" is the argument we pass to the function when calling it.

