# SMT2Generator

## A Proof-of-Concept of SMT2-based File Validation and Reconstruction

## Prerequisites Installation
```
pip install -r requirements.txt
```


## How to Run
### SMT2 Generation
#### The following command will print the SMT2 problem to stdout using the input as hex bytes as a model. 
> If the problem should be written to a file, provide an output file path.
> To validate and test the input against the newly created problem, use the generate-validate mode instead
```
python3 smt2generator.py generate -i "{Input File Path}" [-o "{Output File Path (.smt2)}"]
```
### SMT2 Reconstruction
#### The following command will use an SMT2 file input to recreate a file that satisfies it.
> If the data should be written to a file, provide an output file path.
```
python3 smt2generator.py reconstruct -i "{Input File Path (.smt2)}" [-o "{Output File Path}"]
```
