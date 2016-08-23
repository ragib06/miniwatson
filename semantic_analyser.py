__author__ = 'ragib'

import nltk
from nltk.sem.logic import Expression, LambdaExpression
from nltk import grammar, parse
import logging


class SemUtil:

    def __init__(self):
        pass

    @staticmethod
    def quote(str):
        return '\'' + str + '\''

    @staticmethod
    def clearNonterminal(N):
        if len(N.symbol().split('+')) > 1:
            return ''.join(N.symbol().split('+'))
        else:
            return N.symbol()


class SemanticAnalyser:

    def __init__(self):
        pass

    def treeCallback(self, tree, height):
        prod = tree.productions()[0]
        lhs = prod.lhs().symbol()

        if tree.height() == 2:

            rhs = prod.rhs()[0]

            if lhs in ['.', '?', ':']:
                return ''

            if len(lhs.split('+')) > 1:
                lhs = ''.join(lhs.split('+'))

            if lhs in ['VB', 'VBN', 'VBZ', 'VBD'] and (not rhs[0].isupper()):
                sem = lhs + '[SEM=(<\\x \\y.' + rhs + '(y,x)>)] -> ' + SemUtil.quote(rhs)
            elif (lhs in ['DT', 'IN', 'JJS']) and (rhs not in ['highest', 'higher', 'deepest', 'deeper']):
                sem = lhs + '[SEM=()]' + '->' + SemUtil.quote(rhs)
            else:
                sem = lhs + '[SEM=(' + SemUtil.quote(rhs) + ')]' + ' -> ' + SemUtil.quote(rhs)

        else:
            rhs = prod.rhs()
            rhs = map(SemUtil.clearNonterminal, rhs)

            if tree.height() == height:
                lhs = 'SS'

            if len(lhs.split('+')) > 1:
                lhs = ''.join(lhs.split('+'))

            cnt = 0
            sem = lhs + '[SEM=(' + ' + '.join(['?' + rhs[i].lower() + str(i) for i in range(len(rhs))]) + ')]' + ' -> ' + ' '.join(
                [rhs[i] + '[SEM=?' + rhs[i].lower() + str(i) + ']' for i in range(len(rhs))])

        return sem + '\n'

    def traverseTree(self, tree, height):
        semgram = self.treeCallback(tree, height)
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                subsemgram = self.traverseTree(subtree, height)
                if subsemgram is not None:
                    semgram = semgram + subsemgram
        return semgram

    def lambdaReducer(self, tree):
        read_expr = Expression.fromstring # logical expression reader
        answer = tree[0].label()['SEM'] # generated string would be at the root of the tree

        lst_arguments = []
        lst_funcs = []
        for item in list(answer):
            if isinstance(item, LambdaExpression):
                lst_funcs.append(item)
            else:
                if isinstance(item, nltk.featstruct.FeatureValueTuple):
                    if item.__repr__() in ['(which)', '(who)', '(where)', '(when)']:
                        lst_arguments.append('(wh)')
                    elif len(item.__repr__().split('.')) > 1: #actually lambda
                        lst_funcs.append(item.__repr__()[1:-1])
                    else:
                        lst_arguments.append(item.__repr__()) # __repr__() for string representation
                elif item in ['which', 'who', 'where', 'when']:
                    lst_arguments.append('(wh)')
                elif item not in ['oscar']:
                    lst_arguments.append('('+item+')')

        if len(lst_funcs) > 1:
            lst_funcs = [func for func in lst_funcs if str(func).split('.')[1].split('(')[0] not in ['is', 'was', 'did', 'has']]

        fs = ""
        fs += str(lst_funcs[0])
        for item in lst_arguments:
            fs += item

        fexp = read_expr(fs)
        return fexp.simplify()

    def getSemanticFromParseTree(self, question, parse_tree):
        try:
            semgram = '% start SS\n' + self.traverseTree(parse_tree, parse_tree.height())
            logging.debug('Semantic Grammar: %s', semgram)

            semgrammar = grammar.FeatureGrammar.fromstring(semgram)
            semparser = parse.FeatureEarleyChartParser(semgrammar)
            tree = list(semparser.parse(question.split()))

            return self.lambdaReducer(tree)
        except Exception as exp:
            logging.error('Domain: %s', exp)

