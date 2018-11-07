Tripartite synapse paper

Goal: SImulation of both models

File structure
1. sm_model: contains model in a function model(struct,t,y,*str)
2. sm_params: contains parameters estimated as a function of baseline rest and test parameters in a function parameters(struct,testparams,initvals)
3. sm_class: generates a class such that any class instance defined by classinstance = smclass(initvals,testparams) can refer to the model and parameters from sm_model and sm_params
4. sm_sim: simulates model using assimulo+sundials, also contains plotter(t,y,*str) which plots and saves any component from sm_model
