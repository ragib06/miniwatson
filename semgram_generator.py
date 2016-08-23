"""
Takes a parse tree as input and generates a grammer which has semantics attached with each node.
"""


def generate_semgram(tree):
    sem_dict = []
    for item in tree:  # item type: nltk.tree.Tree (http://www.nltk.org/_modules/nltk/tree.html)
        for i in item.productions():  # rather than working on trees, we are working on grammers that produced this sentence.
            print i
            sem_dict.append(i)

    f = open('grammars/semgram.fcfg', 'w')  # will write the semantic grammer in this file
    f.write("% start S\n")  # mandatory start line for all semantic grammers

    for item in sem_dict:  # item type: nltk.grammar.Production(http://www.nltk.org/_modules/nltk/grammar.html)
        newrule = ""
        if item.is_nonlexical():  # right hand side only contains nonterminals
            lst_rhs = list(item.rhs())
            lst_rhs_sems = ["?" + str(x).lower() for x in lst_rhs]
            newrule += item.lhs().__str__() + "[sem=("
            for sem in lst_rhs_sems:
                newrule += sem + "+"
            newrule = newrule[:-1]  # remove trailing +
            newrule += ")]"

            newrule += "->"  # continue generating the right hand side

            for item in lst_rhs:
                newrule += str(item)  # concatenate node name
                newrule += "[sem=" + "?" + str(item).lower() + "]"  # concatenate semantics
            newrule += "\n"
            f.write(newrule)
            newrule = ""
        else:  # right hand side contains terminals
            rhs = list(item.rhs())[0]
            if item.lhs().__str__() in ["VB", "V"]:  # special treatment for the verb
                newrule += item.lhs().__str__() + "[sem=("
                newrule += "<\\x \\y." + rhs + "(y,x)>"  # lambda expression according to the verb
                newrule += ")]"
            else:
                newrule += item.lhs().__str__() + "[sem=("
                newrule += "'" + rhs + "'"
                newrule += ")]"
            newrule += "->"
            newrule += "'" + rhs + "'"
            newrule += "\n"
            f.write(newrule)
            newrule = ""

    f.close()
