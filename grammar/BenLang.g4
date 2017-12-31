grammar BenLang;		
statement: 	expr SEMICOLON
		  | ifOnly
		  | ifElse
		  | whileLoop
		  | declaration SEMICOLON
		  | assignment SEMICOLON;

expression: expr | STRING;

statementBlock: statement*;
prog:		statementBlock;

declaration: TYPE IDENTIFIER EQUALS expression;
assignment: IDENTIFIER EQUALS expression;

whileLoop: 		WHILE LBRACKET expr RBRACKET LMOUSTACHE statementBlock RMOUSTACHE;
ifElse:     	IF LBRACKET expr RBRACKET LMOUSTACHE statementBlock RMOUSTACHE ELSE LMOUSTACHE statementBlock RMOUSTACHE;
ifOnly:			IF LBRACKET expr RBRACKET LMOUSTACHE statementBlock RMOUSTACHE;

expr: TRUE | FALSE | IDENTIFIER | application | INTEGER  | STRING
      |<assoc=right> OP_NOT expr
      | PLUS expr
      | MINUS expr
      | LBRACKET expr RBRACKET
	  | expr '*' expr
      | expr '/' expr
      | expr PLUS expr
      | expr '-' expr
      | expr OP_LT expr
      | expr OP_EQ expr
      | expr OP_AND expr
      | expr OP_OR expr;


application: IDENTIFIER params;
params: LBRACKET expression? paramsRest;
paramsRest: COMMA expression paramsRest | RBRACKET;

EQUALS: '=';
STRING:  QUOT STRING_CHAR* QUOT;
ESCAPE_CHAR: '\n' | '\r';
QUOT:		 '"';
BACKSLASH:   '\\';
TYPE: 		BOOL_TYPE | STRING_TYPE | INT_TYPE;
BOOL_TYPE: 		 'bool';
INT_TYPE: 		 'int';
STRING_TYPE: 'string';
WHILE: 		 'while';
RMOUSTACHE:  '}';
LMOUSTACHE:  '{';
ELSE:		'else';
IF: 		'if';
OP_LT:      '<';
OP_EQ:		'==';
OP_NOT:		'!';
OP_OR:		'||';
OP_AND:		'&&';
FALSE:		'false';
TRUE: 		'true';
IDENTIFIER:  NON_NUMBER ALTHNUM*;
fragment ALTHNUM:    [a-zA-Z0-9]+;
fragment NON_NUMBER:  [a-zA-Z];
LBRACKET:	'(';
RBRACKET:	')';
INTEGER:	DIGIT | DIGIT_NO_0 DIGIT*;
PLUS:		'+';
MINUS:		'-';
DIV:		'/';
MULT:		'*';
COMMA: 		',';
SEMICOLON: 	';';
PLUSMINUS: 			PLUS | MINUS;
fragment DIGIT:		 ('0'..'9');
fragment DIGIT_NO_0: ('1'..'9');
WS:			[ \n\t\r]+ -> channel(HIDDEN);
STRING_CHAR: UNICODE | ESCAPE | ESCAPE_CHAR;
UNICODE:     '\u0000'..'\u0021' | '\u0023' ..'\u00FF';
ESCAPE: 	BACKSLASH BACKSLASH BACKSLASH*;
