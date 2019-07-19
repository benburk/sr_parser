"""
SR Parser
A shift-reduce parser written in python.
"""
import re
from collections import namedtuple

Token = namedtuple("Token", ("type", "value"))
LexRule = namedtuple("LexRule", ("expression", "handler"))
ParseRule = namedtuple("ParseRule", ("operator", "inputs", "handler"))
OpPrecedence = namedtuple("OpPrecedence", ("associativity", "operators"))


def make_lexer(grammar):
    """create a lexer for a particular grammar"""

    def lex(text):
        """generate a series of tokens from an input string"""
        while text:
            for rule in grammar:
                match = re.match(rule.expression, text)
                if match:
                    match_text = match.group()
                    token = rule.handler(match_text)
                    if token:
                        yield token
                    text = text[len(match_text) :]
                    break
            else:
                exit("could not lex" + text)

    return lex


def make_parser(rules, precedence):
    """create a parser for a set of rules and precedence table"""

    def compare_precedence(op1, op2):
        """compares the precedence of two operators
        returns true if op1 has lower precedence than op2"""
        prec1 = next((x for x in enumerate(precedence) if op1 in x[1].operators), None)
        prec2 = next((x for x in enumerate(precedence) if op2 in x[1].operators), None)
        return (
            prec1
            and prec2
            and (
                (prec1[0] < prec2[0])
                or (prec1[0] == prec2[0])
                and prec2[1].associativity == "right"
            )
        )

    def parse(tokens: iter) -> Token:
        """ implementation of a shift reduce parser
        Args:
            tokens: a token iterator
        Returns:
            the final node left in the tree
        """
        stack = []
        next_tok = next(tokens, None)
        while True:
            for rule in rules:
                n_rules = len(rule.inputs)
                if rule.inputs == [t.type for t in stack[-n_rules:]] and not (
                    rule.operator
                    and next_tok
                    and compare_precedence(rule.operator, next_tok.type)
                ):
                    stack[-n_rules:] = [rule.handler(*stack[-n_rules:])]
                    break

            else:
                if next_tok:
                    stack.append(next_tok)
                    next_tok = next(tokens, None)
                elif len(stack) <= 1:
                    break
                else:
                    exit("error parsing" + str(stack))
        return stack[0]

    return parse
