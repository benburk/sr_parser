"""
defines the grammar to be interpreted by a shift reduce
parser to parse arithmetic expressions
"""
from sr_parser.sr_parser import LexRule
from sr_parser.sr_parser import make_lexer
from sr_parser.sr_parser import make_parser
from sr_parser.sr_parser import OpPrecedence
from sr_parser.sr_parser import ParseRule
from sr_parser.sr_parser import Token


GRAMMAR = (
    LexRule(r"\s+", lambda match: None),
    LexRule(r"\d+\.?\d*", lambda match: Token("number", float(match))),
    LexRule(r"\+", lambda match: Token("add", None)),
    LexRule(r"-", lambda match: Token("sub", None)),
    LexRule(r"\*", lambda match: Token("mul", None)),
    LexRule(r"/", lambda match: Token("div", None)),
    LexRule(r"\^", lambda match: Token("pow", None)),
    LexRule(r"\(", lambda match: Token("(", None)),
    LexRule(r"\)", lambda match: Token(")", None)),
)
PRECEDENCE = (
    OpPrecedence("left", {"add", "sub"}),
    OpPrecedence("left", {"mul", "div"}),
    OpPrecedence("right", {"pow"}),
)
RULES = (
    ParseRule(None, ["number"], lambda n: Token("E", n.value)),
    ParseRule(None, ["(", "E", ")"], lambda l, ex, r: ex),
    ParseRule("add", ["E", "add", "E"], lambda l, op, r: Token("E", l.value + r.value)),
    ParseRule("sub", ["E", "sub", "E"], lambda l, op, r: Token("E", l.value - r.value)),
    ParseRule("mul", ["E", "mul", "E"], lambda l, op, r: Token("E", l.value * r.value)),
    ParseRule("div", ["E", "div", "E"], lambda l, op, r: Token("E", l.value / r.value)),
    ParseRule(
        "pow", ["E", "pow", "E"], lambda l, op, r: Token("E", pow(l.value, r.value))
    ),
)


def main():
    """ example usage """
    lex = make_lexer(GRAMMAR)
    parse = make_parser(RULES, PRECEDENCE)
    while True:
        text = input(">")
        if not text:
            exit("Exiting...")
        tokens = lex(text)
        result = parse(tokens)
        print(result.value)
