import re

abcs = ""


dataTypes = {
    "I64", "I32", "I16", "I8",
    "U64", "U32", "U16", "U8",
    "F64", "F32", "F16", "F8",
    "B1",

    "@I64", "@I32", "@I16", "@I8",
    "@U64", "@U32", "@U16", "@U8",
    "@F64", "@F32", "@B1",

    "*I64", "*I32", "*I16", "*I8",
    "*U64", "*U32", "*U16", "*U8",
    "*F64", "*F32", "*F16", "*B1",

    "*@I64", "*@I32", "*@I16", "*@I8",
    "*@U64", "*@U32", "*@U16", "*@U8",
    "*@F64", "*@F32", "*@B1",

    "@*I64", "@*I32", "@*I16", "@*I8",
    "@*U64", "@*U32", "@*U8",
    "@*F64", "@*F32", "@*B1"
}

registerTypes = {
    "R" + dataType
    for dataType in dataTypes
}

funcTypes = {
    dataType + "_"
    for dataType in dataTypes
}

funcTypes.add("V0_")

symbols = {
    ";", "{", "}", "(", ")", "[", "]",

    # Comparison
    "==", "!=", "<", ">", "<=", ">=",

    # Assignment
    "=", "+=", "-=", "*=", "/=",
    "<<=", ">>=", "&=", "|=", "^=",

    # Arithmetic
    "+", "-", "*", "/",
    "++", "--",

    # Logical
    "&&", "||", "!",

    # Syntax
    "_", "#", ",",

    '"', "\n"
}

keywords = {
    "return",
    "#include",
    "if",
    "elif",
    "else",
        "true",
        "false"
}
while True:
        cmd = input("$~ ")
        found = False
        file = ""

        if cmd.strip() in ["exit", "quit"]:
                break

        if cmd.startswith(abcs):
                filename = cmd[len(abcs) :].strip()
                try:
                        with open(filename, "r") as f:
                                file = f.read()
                                found = True
                except FileNotFoundError:
                        print(f"error: file '{filename}' not found")
        else:
                print("error: use uc prefix to compile")
        # Lexer
        lexed = []
        ast = []
        if found:
                cleaned = ""
                in_string = False

                for char in file:
                        if char == '"':
                                in_string = not in_string
                                cleaned += char

                        elif char.isspace() and not in_string:
                                continue

                        else:
                                cleaned += char

                file = cleaned
                new_file = ""
                in_string = False

                for char in file:
                        if char == '"':
                                in_string = not in_string
                                new_file += char
                        elif char == ";" and not in_string:
                                new_file += ";\n"

                        elif char == "{" and not in_string:
                                new_file += "{\n"
                        elif char == "}" and not in_string:
                                new_file += "}\n"
                        elif char == ">" and not in_string:
                                new_file += ">\n"
                        else:
                                new_file += char
                lines = new_file.splitlines()
                for line in lines:
                        if "//" in line:
                                line = line[:line.index("//")]
                        words = re.findall(
                                r'"[^"]*"|'
                                r'#include|'
                                r'==|!=|<=|>=|<<=|>>=|\+=|-=|\*=|/=|&&|\|\||\+\+|--|'
                                r'[@*]*[A-Za-z_][A-Za-z0-9_.]*|'
                                r'\d+\.\d+|'
                                r'\d+|'
                                r'[@#;{}()[\]<>:=,+\-*/!&|^]',
                                line
                                )
                        for word in words:
                            if word in registerTypes:
                                lexed.append(f"registerType: '{word}'\n")

                            elif word in dataTypes:
                                lexed.append(f"dataType: '{word}'\n")

                            elif word in funcTypes:
                                lexed.append(f"functype: '{word}'\n")

                            elif word in symbols:
                                lexed.append(f"symbol: '{word}'\n")

                            elif word in keywords:
                                lexed.append(f"keyword: '{word}'\n")

                            elif re.fullmatch(r"\d+\.\d+", word):
                                lexed.append(f"float: '{word}'\n")

                            elif re.fullmatch(r"\d+", word):
                                lexed.append(f"integer: '{word}'\n")

                            elif re.fullmatch(r'"[^"]*"', word):
                                lexed.append(f"string: {word}\n")

                            elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", word):
                                lexed.append(f"identifier: '{word}'\n")

                            else:
                                print(f"error: unidentified or malformed token: '{word}'")
                lexed = "".join(lexed)
                print(lexed)
                #parser
                ast = "".join(ast)

                print(ast)
