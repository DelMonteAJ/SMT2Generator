from SMT2gUtils.makes import *
from SMT2gUtils.setup import *
from SMT2gUtils.condensers import *
import argparse
from math import ceil

def generate(source:str, destination:str=None, validate:bool=False):
    '''
    Generates a SMT2 file that has a 
    solvable model that is equal to the
    value of the hex bytes in order
    '''

    contents = fileToDecimalList(source)
    if validate:
        assert destination != None
        from cvc5.pythonic import Solver, Int, sat#, solve_using
        s = Solver()
        variables = [Int(f'byte{i}') for i in range(len(contents))]

    if destination != None:
        with open(destination, "w+") as f:
            f.write(SMT2preamble())
            f.write(fileBytesToVariables(contents))

            for index1, byteValue1 in enumerate(contents):
                print(f"File Written {int(ceil(index1/len(contents) * 100))}%\r", end="")
                for index2, byteValue2 in enumerate(contents):
                    if index1 == index2:
                        continue
                    
                    if (byteValue1 > byteValue2):
                        if validate: s.add(variables[index1] > variables[index2])
                        relation = (makeGT(makeByte(index1), makeByte(index2)))
                    elif (byteValue1 < byteValue2):
                        if validate: s.add(variables[index1] < variables[index2])
                        relation = (makeLT(makeByte(index1), makeByte(index2)))
                    elif (byteValue1 == byteValue2):
                        if validate: s.add(variables[index1] == variables[index2])
                        relation = (makeEQ(makeByte(index1), makeByte(index2)))

                    f.write(makeAssertion(makeAnd(
                                                relation,
                                                makeEQ(makeAdd(makeByte(index1),makeByte(index2)), byteValue1+byteValue2),
                                                makeEQ(makeMulti(makeByte(index1),makeByte(index2)), byteValue1*byteValue2),
                                                makeEQ(makeSub(makeByte(index1),makeByte(index2)), byteValue1-byteValue2) if byteValue1-byteValue2 >= 0 else makeEQ(makeSub(makeByte(index2),makeByte(index1)), byteValue2-byteValue1)
                                                # Generates Unsat when division is used makeEQ(makeDiv(makeByte(index1),makeByte(index2)), byteValue1/byteValue2)
                                                )))
                    
                    if validate:
                        s.add(variables[index1] + variables[index2] == (byteValue1+byteValue2),
                                variables[index1] * variables[index2] == (byteValue1*byteValue2),
                                variables[index1] - variables[index2] == (byteValue1-byteValue2) if byteValue1-byteValue2 >= 0 else variables[index2] - variables[index1] == (byteValue2-byteValue1))

            f.write(SMTclosing())
        print(f"File Written 100%\r")
        print(f"Output file created at {destination}")
    else:
        print(SMT2preamble())
        print(fileBytesToVariables(contents))

        for index1, byteValue1 in enumerate(contents):
            # print(f"File Written {int(ceil(index1/len(contents) * 100))}%\r", end="")
            for index2, byteValue2 in enumerate(contents):
                if index1 == index2:
                    continue
                
                if (byteValue1 > byteValue2):
                    if validate: s.add(variables[index1] > variables[index2])
                    relation = (makeGT(makeByte(index1), makeByte(index2)))
                elif (byteValue1 < byteValue2):
                    if validate: s.add(variables[index1] < variables[index2])
                    relation = (makeLT(makeByte(index1), makeByte(index2)))
                elif (byteValue1 == byteValue2):
                    if validate: s.add(variables[index1] == variables[index2])
                    relation = (makeEQ(makeByte(index1), makeByte(index2)))

                print(makeAssertion(makeAnd(
                                            relation,
                                            makeEQ(makeAdd(makeByte(index1),makeByte(index2)), byteValue1+byteValue2),
                                            makeEQ(makeMulti(makeByte(index1),makeByte(index2)), byteValue1*byteValue2),
                                            makeEQ(makeSub(makeByte(index1),makeByte(index2)), byteValue1-byteValue2) if byteValue1-byteValue2 >= 0 else makeEQ(makeSub(makeByte(index2),makeByte(index1)), byteValue2-byteValue1)
                                            # Generates Unsat when division is used makeEQ(makeDiv(makeByte(index1),makeByte(index2)), byteValue1/byteValue2)
                                            )), end="")
        print(SMTclosing())

    if validate:
        status = s.check()
        print(f"SAT Status: {status}")
        if status == sat:
            # solve_using(s, [variables[i] == contents[i] for i in range(len(contents))])
            print("SAT Problem Validated" if [s.model().eval(variables[i]) for i in range(len(contents))] == contents else "SAT Problem Invalidated")


def reconstruct(source: str, destination: str):
    from cvc5.pythonic import Solver, Int, sat#, solve_using
    import re
    s = Solver()
    counter = 0
    with open(source) as f:
        initializeVariables = True
        c = 0
        lines = f.readlines()
        variables = []
        for line in lines:
            if line.startswith("(declare-fun byte"):
                counter += 1
            elif line.startswith("(assert"):
                if initializeVariables:
                    initializeVariables = False
                    variables = [Int(f'byte{i}') for i in range(counter)]
                # print(line)
                # line = '(assert (and (< byte0 byte10) (= (+ byte0 byte10) 177) (= (* byte0 byte10) 7452) (= (- byte10 byte0) 39)))'
                c += 1


                operations = [int(token.strip(')')) for token in line.split() if token.strip(')').isdigit()]
                line=line[13:-3]
                subProblem = re.findall(r'\(([^)]+)\)', line)[-1][5:].split(" ")
                first = int(subProblem[0][4:])
                second = int(subProblem[1][4:])
                
                # Equality problem 
                # print(f"Operations: {operations}")
                # while line.find("-)")
                s.add(variables[first] + variables[second] == operations[0],
                      variables[first] * variables[second] == operations[1],
                      variables[first] - variables[second] == operations[2])
                # print(line.find(')'))
                # print(line)
                # break
        # print(s)
    s.check()
    if destination != None:
        with open(destination, "w") as f:
            f.write("".join([chr(s.model().eval(variables[i]).as_long()) for i in range(counter)]))
    else:
        print("".join([chr(s.model().eval(variables[i]).as_long()) for i in range(counter)]))

            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Hex SAT Generator",
        description="Generate or Validate Hex-Formulated SMT2 Files.")
    parser.add_argument("mode", choices=["generate", "generate-validate", "reconstruct"], help="Selects which action to take with the given input")
    parser.add_argument("-i", "--input", required=True, help="The file that will have its bytes read")
    parser.add_argument("-o", "--output", help="The path of where the newly made SMT2 file will be written")
    
    args = parser.parse_args()
    print(args.mode)
    if args.mode == "reconstruct":
        reconstruct(args.input, args.output)
    else:
        generate(args.input, args.output, True if args.mode == "generate-validate" else False)
    

