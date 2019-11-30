class Parser(object):
    def __init__(self, src: str, index: int):
        self.src = src
        self.index = index

    def parseElem(self):
        while self.src[self.index] in (' ', '\t', '\n'):
            self.index += 1
        if self.src[self.index] == '(':
            self.index += 1
            return self.parseList()
        elif self.src[self.index] == ')':
            self.index += 1
            return ')'
        chars = []
        while self.src[self.index] not in (' ', '\t', '\n', ')'):
            chars.append(self.src[self.index])
            self.index += 1
        return ''.join(chars)

    def parseList(self):
        elem = self.parseElem()
        elems = []
        while elem != ')':
            elems.append(elem)
            elem = self.parseElem()
        return elems

