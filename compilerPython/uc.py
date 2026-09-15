import re

dataTypes = {  
	#plain
	'I64', 'I32', 'I16', 'I8', 
	'U64', 'U32', 'U16', 'U8', 
	'F64', 'F32', 'F16', 'F8', 
	'C64', 'C32', 'C16', 'C8',
	'B1',
	#array
	'@I64', '@I32', '@I16', '@I8', 
	'@U64', '@U32', '@U16', '@U8', 
	'@F64', '@F32', '@F16', '@F8',
	'@C64', '@C32', '@C16', '@C8',
	'@B1',
	#pointers
	'*I64', '*I32', '*I16', '*I8', 
	'*U64', '*U32', '*U16', '*U8', 
	'*F64', '*F32', '*F16', '*F8',
	'*C64', '*C32', '*C16', '*C8',
	'*B1',
	#pointer to an array
	'*@I64', '*@I32', '*@I16', '*@I8', 
	'*@U64', '*@U32', '*@U16', '*@U8', 
	'*@F64', '*@F32', '*@F16', '*@F8',
	'*@C64', '*@C32', '*@C16', '*@C8',
	'*@B1',
	#array of pointers
	'@*I64', '@*I32', '@*I16', '@*I8', 
	'@*U64', '@*U32', '@*U16', '@*U8', 
	'@*F64', '@*F32', '@*F16', '@*F8',
	'@*C64', '@*C32', '@*C16', '@*C8',
	'@*B1'
}

registerTypes = { 'R' + dataType for dataType in dataTypes }
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
	'switch',
	'case',
	'default'
}
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
		# Pre-process line endings safely without losing spacing logic
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

			# Combined regex string literal flags and corrected regex pattern order
			words = re.findall(
				r'"[^"]*"|'                       # String literals
				r'#include|'                       # Preprocessor
				r'==|!=|<=|>=|<<=|>>=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|&&|\|\||\+\+|--|' # Multi-character operators
				r'[@*]*[A-Za-z_][A-Za-z0-9_.]*|'   # Identifiers / Types
				r'\d+\.\d+|'                       # Floats
				r'\d+|'                            # Integers
				r'[@#;{}()[\]<>:=,+\-*/!&|^]',    # Single character symbols
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
		# Parser stub
		ast_str = "".join(ast)
		print(ast_str)
