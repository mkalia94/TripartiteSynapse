# The Tripartite Synapse

## Dependencies
Runs on Python 3.x
Dependencies: scipy, numpy, assimulo, matplotlib, argparse

## Sample Run
An example of running multiple experiments in a bash script is done in `Code/Example_Run`. Run:
`chmod +x ./Example_Run`
`Example_Run`

## Example
Running 
`python -i fm_class.py --pumpScaleAst 2 --pumpScaleNeuron 2 --tstart 20 --tend 25 --solve --write -s --name 'HyperNKA2' --plot '{"Pot":["KCi","KCe","KCg"],"MemPot":["Vi","Vg"]}' --titles '{"Pot":"[$K^+$] (mM)","MemPot":"Membrane potential (mV)"}'`
will simulate the tripartite synapse under 5 minutes of metabolic stress, when the baseline pump strength is set to twice its initial strength. The name of the experiment is `HyperNKA2` and the result is written to `Code/Experiments.txt`. After the simulation plots of potassium concentrations and membrane potentials are stored in separate figures.

