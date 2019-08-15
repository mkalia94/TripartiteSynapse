# The Tripartite Synapse

## Dependencies
Runs on Python 3.x
Dependencies: scipy, numpy, assimulo, matplotlib, argparse, timeit

## Sample Run
An example of running multiple experiments in a bash script is done in `Code/RunExp`

## Example
Running 
`python -i fm_class.py --pumpScaleAst 2 --pumpScaleNeuron 2 --tstart 20 --tend 25 --solve --write -s --name 'HyperNKA2' --plot '{"Pot":["KCi","KCe","KCg"],"MemPot":["Vi","Vg"]}' --titles ' '{"Pot":"[$K^+$] (mM)","MemPot":"Membrane potential (mV)"}''`
will simulate the tripartite synapse under 5 minutes of metabolic stress, when the baseline pump strength is set to twice its initial strength. The name of the experiment is `HyperNKA2` and the result is written to `Code/Experiments.txt`. After the simulation plots of potassium concentrations and membrane potentials are stored in separate figures.

## File structure
1. `fm_model.py`: contains model in a function model(struct,t,y,kwargs)
2. `fm_params.py`: contains parameters estimated as a function of baseline rest and test parameters in a function parameters(struct,testparams,initvals)
3. `fm_class.py`: **Main file**: Performs all argument parsing, generates a class such that any class instance defined by classinstance = fmclass(initvals,testparams) can refer to the model and parameters from `fm_model.py` and `fm_params.py`. Then solves the system and performs plotting of results.

