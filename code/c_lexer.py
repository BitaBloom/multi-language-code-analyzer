import ply.lex as lex

class CLexer:
    tokens = (
        'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'NAME', 'EQUALS',
        'SEMICOLON', 'LBRACE', 'RBRACE'
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_EQUALS = r'='
    t_SEMICOLON = r';'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_ignore = ' \t'

    @staticmethod
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    @staticmethod
    def t_NAME(t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t

    @staticmethod
    def t_error(t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()
