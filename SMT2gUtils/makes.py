def makeAdd(num1: str, num2: str) -> str:
    return f"(+ {num1} {num2})"

def makeSub(num1: str, num2: str) -> str:
    return f"(- {num1} {num2})"

def makeMulti(num1: str, num2: str) -> str:
    return f"(* {num1} {num2})"

def makeDiv(num1: str, num2: str) -> str:
    return f"(/ {num1} {num2})"

def makePow(num1: str, num2: str) -> str:
    return f"(^ {num1} {num2})"

def makeAnd(bool1: str, *args: str) -> str:
    return f"(and {bool1} {' '.join(args)})"

def makeOr(bool1: str, *args: str) -> str:
    return f"(or {bool1} {' '.join(args)})"

def makeGTE(num1: str, num2: str) -> str:
    return f"(>= {num1} {num2})"

def makeLTE(num1: str, num2: str) -> str:
    return f"(<= {num1} {num2})"

def makeGT(num1: str, num2: str) -> str:
    return f"(> {num1} {num2})"

def makeLT(num1: str, num2: str) -> str:
    return f"(< {num1} {num2})"

def makeEQ(num1: str, num2: str) -> str:
    return f"(= {num1} {num2})"

def makeAssertion(term: str) -> str:
    return f"(assert {term})\n"

def makeByte(index: int) -> str:
    return f"byte{index}"