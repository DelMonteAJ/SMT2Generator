def SMT2preamble() -> str:
    return '''\
;; Preamble
(set-info :smt-lib-version 2.6)
(set-logic QF_LRA)\n'''

def SMTclosing(returnModel: bool=True) -> str:
    if returnModel:
        return '''\
;; Closing
(check-sat)

(get-model)\n'''

    else:
        return '''\
;; Closing
(check-sat)\n'''

def fileToDecimalList(filepath: str) -> list[int]:
    finalList = []
    with open(filepath, 'rb') as f:
        for letter in f.read():   
            finalList.append(letter)
    return finalList

def fileBytesToVariables(fileContents: list[int]) -> str:
    string = ";; Setting up variables\n"
    for byteIndex, byte in enumerate(fileContents):
        string += f"(declare-fun byte{byteIndex} () Real)\n"
    return string