import ply.yacc as yacc
from python_lexer import PythonLexer

class PythonParser:
    tokens = PythonLexer.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    def p_statement_assign(self, p):
        'statement : NAME EQUALS expression'
        p[0] = ('=', p[1], p[3])

    def p_statement_expr(self, p):
        'statement : expression'
        p[0] = p[1]

    def p_expression_binop(self, p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression'''
        p[0] = (p[2], p[1], p[3])

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = ('-', p[2])

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_expression_name(self, p):
        'expression : NAME'
        p[0] = ('name', p[1])

    def p_error(self, p):
        print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        return self.parser.parse(data)
