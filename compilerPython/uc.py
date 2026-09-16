import re
#stuff & things
dataTypes = {  
	#plain
	'I64', 'I32', 'I16', 'I8', 
	'U64', 'U32', 'U16', 'U8', 
	'F64', 'F32', 'F16', 'F8', 
	'C64', 'C32', 'C16', 'C8',
	'$C8',
	'B1',
	#array
	'@I64', '@I32', '@I16', '@I8', 
	'@U64', '@U32', '@U16', '@U8', 
	'@F64', '@F32', '@F16', '@F8',
	'@C64', '@C32', '@C16', '@C8',
	'@$C8',
	'@B1',
	#pointers
	'*I64', '*I32', '*I16', '*I8', 
	'*U64', '*U32', '*U16', '*U8', 
	'*F64', '*F32', '*F16', '*F8',
	'*C64', '*C32', '*C16', '*C8',
	'*$C8',
	'*B1',
	#array of pointers
	'@*I64', '@*I32', '@*I16', '@*I8', 
	'@*U64', '@*U32', '@*U16', '@*U8', 
	'@*F64', '@*F32', '@*F16', '@*F8',
	'@*C64', '@*C32', '@*C16', '@*C8',
	'@*$C8',
	'@*B1'
}
#add shit 
registerTypes = { 'R.' + dataType for dataType in dataTypes }
funcTypes = { dataType + '_' for dataType in dataTypes }
funcTypes.add('V0_')

symbols = {
	';', '{', '}', '(', ')', '[', ']',

	# Comparison
	'==', '!=', '<', '>', '<=', '>=',

	# Assignment
	'=', '+=', '-=', '*=', '/=', '%=',
	'<<=', '>>=', '&=', '|=', '^=', '!=',

	# Arithmetic
	'+', '-', '*', '/', '%',
	'++', '--',

	# Logical
	'&&', '||', '!',

	# Bitwise
	'&', '|', '^', '~',
	'<<', '>>',

	# Other
	'_', '#', ',', '\n',
	'?', ':'
}

keywords = {
	'return',
	'#include',
	'if',
	'elif',
	'else',
	'true',
	'false',
	'while',
	'for',
	'break',
	'continue',
	'struct',
	'main',
	'dat'
}
#EASTER EGG(language used to be called abacus)
abcs = ""

while True:
	cmd = input("$~ ")
	found = False
	file = ""

	if cmd.strip() in [ 'exit', 'quit' ]:
		break

	if cmd.startswith(abcs):
		filename = cmd[len(abcs) :].strip()
		try:
			with open(filename, 'r') as f:
				file = f.read()
			found = True
		except FileNotFoundError:
			print(f"error: file {filename} not found")
	else:
		print("error: use uc prefix to compile")
		
	# Lexer
	lexed = []
	ast = []
	tokens = []
	
	if found:
		new_file = ""
		in_string = False
		for char in file:
			if char == '"':
				in_string = not in_string
				new_file += char
			elif char in [';', '{', '}'] and not in_string:
				new_file += char + '\n'
			else:
				new_file += char

		lines = new_file.splitlines()

		for line in lines:
			if '//' in line:
				line = line[:line.index('//')]

			# regex i tottaly didnt google
			words = re.findall(
                r'"[^"]*"|'                       # Strings
                r'#include|'                      # Include keyword
                r'R\.[@*]*[A-Z0-9$]+(?:_)?|'       # Register types (e.g. R.I64, R.@*U32)
                r'[@*]*[A-Z0-9$]+(?:_)?|'         # Data types and Function types 
                r'==|!=|<=|>=|<<=|>>=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|&&|\|\||\+\+|--|' # Multi-char operators
                r'[A-Za-z_][A-Za-z0-9_.]*|'        # Identifiers
                r'\d+\.\d+|'                      # Floats
                r'\d+|'                           # Integers
                r'[@;{}()[\]<>:=,+\-*/!&|^~?_#]', # Single fallback symbols
                line
            )


			for word in words:
				if word in registerTypes:
					lexed.append(f"registerType, {word}")
				elif word in dataTypes:
					lexed.append(f"dataType, {word}")
				elif word in funcTypes:
					lexed.append(f"functype, {word}")
				elif word in symbols:
					lexed.append(f"symbol, {word}")
				elif word in keywords:
					lexed.append(f"keyword, {word}")
				elif re.fullmatch(r'\d+\.\d+', word):
					lexed.append(f"float, {word}")
				elif re.fullmatch(r'\d+', word):
					lexed.append(f"integer, {word}")
				elif re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*', word):
					lexed.append(f"identifier, {word}")
				elif re.fullmatch(r'"[^"]*"', word):
					lexed.append(f"string, {word}")
				else:
					print(f"error: unidentified or malformed token: {word}")
					break
		for token in lexed:
			print(token)

        # Parser
		ast = []

		for index, token in enumerate(lexed):

			if token.startswith("functype"):
				func_type = token.replace("functype,", "").replace("_", "")
				name = lexed[index + 1]

				for prefix in ("keyword,", "identifier,"):
					name = name.replace(prefix, "")

				ast.append(
					f"function:\n"
					f"\tname: {name}\n"
					f"\ttype: {func_type}\n"
				)

			elif token.startswith("dataType"):
				data_type = token.replace("dataType,", "")

				if index + 4 < len(lexed):
					name = lexed[index + 2].replace("identifier,", "")
					value = ""

					if lexed[index + 4] == "symbol, ;":
						value = ""

					elif lexed[index + 4] == "symbol, =":
						if index + 5 < len(lexed):
							value = lexed[index + 5]

							for prefix in ("string, ", "integer, ", "float, "):
								value = value.replace(prefix, "")

					ast.append(
						f"\tdecl:\n"
						f"\t\tdatType: {data_type}\n"
						f"\t\tname: {name}\n"
						f"\t\tvalue: {value}\n"
					)

			elif token == "symbol, (":
				if index + 4 < len(lexed):
					name = lexed[index + 1]

					if name.startswith("identifier,"):
						name = name.replace("identifier,", "")

						if lexed[index + 2] == "symbol, )" and lexed[index + 3] == "symbol, =":
							value = lexed[index + 4]

							for prefix in ("string, ", "integer, ", "float, "):
								value = value.replace(prefix, "")

							ast.append(
								f"\tassign:\n"
								f"\t\tname: {name}\n"
								f"\t\tvalue: {value}\n"
							)

		ast_str = "".join(ast)
		print(ast_str)
