from basic_types import Number, Boolean, Symbol, Lambda
from parser import Parser


class Eval(object):
    def __init__(self, elem, env: dict):
        self.elem = elem
        self.env = env

    def __call__(self, *args, **kwargs):
        if isinstance(self.elem, list):
            if self.elem[0] == 'define':
                if not isinstance(self.elem[1], list):
                    self.env[self.elem[1]] = Eval(self.elem[2], self.env)()
                else:
                    # (define (A a b c..) (...) )  (define A (lambda a b c..) (...))
                    name = self.elem[1][0]
                    lbd = ['lambda']
                    lbd.append(self.elem[1][1:])
                    lbd.append(self.elem[2])
                    self.elem[1] = lbd
                    self.elem.insert(1, name)
                    self.elem.pop()
                    return self()
                return None
            elif self.elem[0] == 'lambda':
                return self.parseLambda()
            elif self.elem[0] == 'cond':
                branches = self.elem[1:]
                for branch in branches:
                    if Apply(branch[0], self.env)():
                        return Eval(branch[1], self.env)()
                return None
            else:
                return Apply(self.elem, self.env)()
        if Number.isNumber(self.elem):
            return int(self.elem)
        if Boolean.isBoolean(self.elem):
            return Boolean.getBoolean(self.elem)
        if Symbol.isSymbol(self.elem):
            v = self.env.get(self.elem, None)
            if not v == None:
                return self.env.get(self.elem)
            print('''no symbol '{symbol}' in env'''.format(symbol=self.elem))
            exit(1)

    def parseLambda(self):
        args = self.elem[1]
        statement = self.elem[2]
        env = {}

        # TODO: save all (key,value) in new Environment
        # for key, value in self.env.items():
        #     env[key] = value
        flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
        needed = flatten(self.elem)
        for key in needed:
            value = self.env.get(key, None)
            if value != None:
                env[key] = value
        return Lambda(args, statement, env)


class sum(object):
    def __init__(self, args):
        self.args = args

    def __call__(self, *args, **kwargs):
        value = 0
        for arg in self.args:
            value += arg
        return value


class And(object):
    def __init__(self, args):
        self.args = args

    def __call__(self, *args, **kwargs):
        value = True
        for arg in self.args:
            value &= arg
        return value


class equal(object):
    def __init__(self, args):
        self.args = args

    def __call__(self, *args, **kwargs):
        return self.args[0] == self.args[1]


class less(object):
    def __init__(self, args):
        self.args = args

    def __call__(self, *args, **kwargs):
        return self.args[0] < self.args[1]


class more(object):
    def __init__(self, args):
        self.args = args

    def __call__(self, *args, **kwargs):
        return self.args[0] > self.args[1]


Environment = {
    'sum': sum,
    '+': sum,
    'and': And,
    '&': And,
    'equal': equal,
    'more': more,
    'less': less,
}


class Apply(object):
    def __init__(self, elems, env):
        self.elems = elems
        self.env = env

    def __call__(self, *args, **kwargs):
        operator = Eval(self.elems[0], self.env)()
        args = [Eval(elem, self.env)() for elem in self.elems[1:]]
        if isinstance(operator, Lambda):
            for index in range(len(operator.args)):
                operator.env[operator.args[index]] = args[index]
            return Eval(operator.statement, operator.env)()
        else:
            return operator(args)()


def lisp(src: str):
    elem = Parser(src, 0).parseElem()
    value = Eval(elem, Environment)()
    if not value == None:
        print(value)


if __name__ == '__main__':
    lisp('''(define cons  (lambda (x y) (   lambda (z) (cond    ((equal z 0) x)
                                                                ((equal z 1) y)
                                                        )
                                        )
                            )
            )''')

    lisp('''(define car (lambda (pair) (pair 0)
                        )
            )''')
    lisp('''(define cdr (lambda (pair) (pair 1)))''')

    lisp('(car (cons 1 2))')
    lisp('(cdr (cons 1 2))')

    lisp('(define pair (cons 7 -3) ))')
    lisp('(car pair)')
    lisp('(cdr pair)')

    lisp('(define (triple x y z) (cons x (cons y z))))')
    lisp('(define (mid tri) (car (cdr tri)) )')
    lisp('(define (left tri) (car tri) )')
    lisp('(define (right tri) (cdr (cdr tri)) )')
    lisp('(define leaf (triple 7 2 1))')
    lisp('(left leaf)')
    lisp('(mid leaf)')
    lisp('(right leaf)')

    lisp('(define (inc x) (+ x 1))')
    lisp('(inc 2)')
    lisp('(inc 4)')
    lisp('(and true false)')
