import re

abcs = ""
lexed = []

dataTypes = {
    "I64", "I32", "I16", "I8",
    "R64", "R32", "R16", "R8",
    "U64", "U32", "U16", "U8",
    "F64", "F32", "F16", "B1",
    "V0",

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
    "@*U64", "@*U32", "@*U16", "@*U8",
    "@*F64", "@*F32", "@*B1",

    "I64_", "I32_", "I16_", "I8_",
    "R64_", "R32_", "R16_", "R8_",
    "U64_", "U32_", "U16_", "U8_",
    "F64_", "F32_", "F16_", "B1_",
    "V0_",

    "@I64_", "@I32_", "@I16_", "@I8_",
    "@U64_", "@U32_", "@U16_", "@U8_",
    "@F64_", "@F32_", "@B1_",

    "*I64_", "*I32_", "*I16_", "*I8_",
    "*U64_", "*U32_", "*U16_", "*U8_",
    "*F64_", "*F32_", "*F16_", "*B1_",

    "*@I64_", "*@I32_", "*@I16_", "*@I8_",
    "*@U64_", "*@U32_", "*@U16_", "*@U8_",
    "*@F64_", "*@F32_", "*@B1_",

    "@*I64_", "@*I32_", "@*I16_", "@*I8_",
    "@*U64_", "@*U32_", "@*U16_", "@*U8_",
    "@*F64_", "@*F32_", "@*B1_",
}


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
    "_", "#", ",", ".",

    '"', "\n"
}

keywords = {
    "return",
    "#include",

    "add",
    "sub",
    "xor",
    "or",
    "and",
    "not",

    "shift<",
    "shift>",
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
				r'"[^"]*"|#include|shift<|shift>|==|!=|<=|>=|&&|\|\||\+\+|--|[A-Za-z_][A-Za-z0-9_]*|\d+|[@#._;{}()[\]<>:=,+\-*/!]',
				line
			)
			for word in words:
				if word in dataTypes:
					lexed.append(f"dataType: " + word + "\n")
				elif word in symbols:
					lexed.append(f"symbol: " + word + "\n")
				elif word in keywords:
					lexed.append(f"keyword: " + word + "\n")
				else:
					lexed.append(f"identifier: " + word + "\n")
		print("".join(lexed))

