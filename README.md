# SCF

SCF aims to create a very simple format which is ideal for
config usage. It is separated into "Sections", "Keys" and "Values".

Each SCF file must have at least one section and all extra key->values must be
within a section. 

### An example config

```
# Comment

<test.scf>

{section1}
    database = "hello"
    hello = true
    list = [
        [10, 10],
        "test", "test", "test"
    ]
    test = {"test": 10}
    x = 10
 ```
    
### Defining the SCF dictionary
    
* `#` Comment
* `{x}` Section
* `<file.scf>` Import
* `key = value`


### Some value types:

* `true/false` or `True/False` -> Bool
* `10` -> Integer
* `10.3` -> Float
* `"string"` or `'string'` -> String
* `[1, 2]` -> List
* `{"a": 10}` -> Dictionary
* `(1, 2)` -> Tuple

The config will be returned as a Python dictionary.


## Using SCF


SCF can be parsed from a file or from a string.

### Parsing from a file
test.scf
```
{section1}
    database = "hello"
    hello = true
    list = [
        [10, 10],
        "test", "test", "test"
    ]
    test = {"test": 10}
    x = 10
```
Python
```python
>>> config = SCF.read("test.scf")
>>> config
{'section1': {'database': 'hello', 'hello': True, 'list': [[10, 10], 'test', 'test', 'test'], 'test': {'test': 10}, 'x': 10}}
```
### Parsing from a string
Python
```python
>>> config_string = """
{section1}
    database = "hello"
    hello = true
    list = [
        [10, 10],
        "test", "test", "test"
    ]
    test = {"test": 10}
    x = 10
"""
>>> config = SCF.parse(config_string)
>>> config
{'section1': {'database': 'hello', 'hello': True, 'list': [[10, 10], 'test', 'test', 'test'], 'test': {'test': 10}, 'x': 10}}
```


Both `read` and `parse` have two keyword arguments `error_report` and `strict`. `error_report` will print warnings on duplicate keys whereas `strict` will raise an exception. 


