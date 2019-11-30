
class Lambda(dict):
    def __init__(self, args, statement, env):
        self.args = args
        self.statement = statement
        self.env = env

    def __repr__(self):
        return '''lambda<{args},{statement},{env}>''' \
            .format(args=self.args, statement=self.statement, env=self.env)


class Number(object):
    @staticmethod
    def isNumber(literal: str):
        return literal.isdigit() or (literal[0] == '-' and literal[1:].isdigit())


class Boolean(object):
    @staticmethod
    def isBoolean(literal: str):
        return literal in ('true', 'false')

    @staticmethod
    def getBoolean(literal: str):
        return {
            'false': False,
            'true': True
        }[literal]


class Symbol(object):
    @staticmethod
    def isSymbol(literal: str):
        if not literal[0] in '+-*/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            return False
        for c in literal[1:0]:
            if c not in '+-*/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
                return False
        return True

