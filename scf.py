import ast

"""
Simple Config Format

SCF aims to create a very simple format which is ideal for
config usage. It is separated into "Sections", "Keys" and "Values".

Each SCF file must have at least one section and all extra key->values must be
within a section. 

An example config

# Comment

{section1}
    database = "hello"
    hello = true
    list = [
        [10, 10],
        "test", "test", "test"
    ]
    test = {"test": 10}
    x = 10
    
Defining the SCF dictionary
    
# Comment
{x} Section
key = value

Some value types:

true/false or True/False -> Bool
10 -> Integer
10.3 -> Float
"string" or 'string' -> String
[1, 2] -> List
{"a": 10} -> Dictionary
(1, 2) -> Tuple

The config will be returned as a Python dictionary.
"""


class InvalidValue(Exception):
    """Value found outside of a section!"""


class OverwriteKey(Exception):
    """A key has been replaced!"""


class SCF:
    @staticmethod
    def parse(string_to_parse, error_report=True, strict=False):
        """
        Parse the SCF file and place values into a python dictionary

        Params:
            file_to_read: String -> File passed to be read
            error_report: Bool -> Report duplicate keys
            strict: Bool -> Raise an exception on duplicate keys
        """

        string_to_parse = SCF.check_imports(string_to_parse)

        return_dictionary = {}
        key = ""

        lines = string_to_parse.splitlines()

        checking_multiline = {"{": 0, "[": 0, "(": 0, "checking": False}
        char_swap = {"}": "{", "]": "[", ")": "("}

        for line in lines:
            line = line.strip()
            comment = False
            if not checking_multiline["checking"]:
                checking_value = False
                creating_key = False
                value_key = ""
                value = ""

            for char in line:
                if comment or char == " ":
                    continue

                if char == "#":
                    comment = True
                    continue

                if char == "{" and not checking_value:
                    key = ""
                    creating_key = True
                    continue

                if char == "}" and not checking_value:
                    return_dictionary[key] = {}
                    creating_key = False
                    continue

                if creating_key:
                    key = "".join((key, char))
                    continue

                if char != "=" and not checking_value:
                    value_key = "".join((value_key, char))
                    continue

                if char == "=":
                    checking_value = True
                    continue

                if char in "{[(":
                    checking_multiline[char] += 1
                    checking_multiline["checking"] = True
                elif char in "}])":
                    char_key = char_swap[char]
                    checking_multiline[char_key] -= 1
                    check = False
                    for mutli_char in "{[(":
                        if checking_multiline[mutli_char] != 0:
                            check = True
                            break
                    checking_multiline["checking"] = check

                value = "".join((value, char))
            if value_key and value and not checking_multiline["checking"]:
                if key == "":
                    raise InvalidValue("Value found outside of a section!")

                if value in ["true", "false"]:
                    value = value.title()

                value = ast.literal_eval(value)

                if strict:
                    if return_dictionary[key].get(value_key, None) is not None:
                        raise OverwriteKey("Key: `{}` has been replaced in section: {}!".format(value_key, key))

                if error_report:
                    if return_dictionary[key].get(value_key, None) is not None:
                        print("Key: `{}` has been replaced in section: {}!".format(value_key, key))

                return_dictionary[key][value_key] = value
        return return_dictionary

    @staticmethod
    def check_imports(string_to_parse):
        """
        Check the SCF file for other SCF file imports

        params:
            string_to_parse: String -> Main config as a string to search for imports
        """
        lines = string_to_parse.splitlines()

        import_files = []
        for line in lines:
            if "<" not in line:
                continue

            import_file = ""
            import_file_check = False

            for char in line:
                if char == "<":
                    import_file_check = True
                    continue

                if char == ">":
                    import_file_check = False
                    continue

                if import_file_check:
                    import_file = "".join((import_file, char))
            if import_file:
                import_files.append(import_file)

        for config_file in import_files:
            with open(config_file) as f:
                contents = f.read()
            string_to_parse = "\n".join((string_to_parse, contents))

        return string_to_parse

    @staticmethod
    def read(file_to_read, error_report=True, strict=False):
        """
        Read the SCF file and get the string to be parsed

        Params:
            file_to_read: String -> File passed to be read
            error_report: Bool -> Report duplicate keys
            strict: Bool -> Raise an exception on duplicate keys
        """
        with open(file_to_read) as f:
            contents = f.read()
        return SCF.parse(contents, error_report, strict)


if __name__ == "__main__":
    config = SCF.read("test.scf")
    print(config)

    config_exception = SCF.read("test.scf", strict=True)  # Exception will be raised if duplicate key is found
