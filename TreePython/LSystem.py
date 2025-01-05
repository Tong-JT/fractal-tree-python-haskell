class LSystem:

    def __init__(self, axiom="F", rule="F[+F][-F[-F]F]F[+F][-F]"):
        self.axiom = axiom
        self.rule = rule

    def buildLSystemString(self, axiomString, layers):
        for _ in range(layers):
            axiomString = self.applyRule(axiomString)
        return axiomString

    def applyRule(self, axiomString):
        newString = []
        for character in axiomString:
            if character == 'F':
                newString.append(self.rule)
            else:
                newString.append(character)
        return ''.join(newString)