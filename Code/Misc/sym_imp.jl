using SymPy
NAi = symbols("NAi",positive=true)
NAe = symbols("NAe",positive=true)
NBe = symbols("NBe",positive=true)
NAg = symbols("NAg",positive=true)
NBg = symbols("NBg",positive=true)
NAp = symbols("NAp",positive=true)
NBp = symbols("NBp",positive=true)
NaCi0,KCi0,ClCi0,CaCi0,GluCi0,Wi0,NaCe0,KCe0,ClCe0,CaCc0,GluCc0,We0,NaCg0,KCg0,ClCg0,CaCg0,GluCg0,Wg0,NaCp0,KCp0,ClCp0,CaCp0,GluCp0,Wp0,CNa,CK,CCl,CCa,CGlu,Vi0,Vg0,Vp0,F,C,VolPAP, VolPreSyn, Volc, VolPostSyn, NBi= symbols("NaCi0,KCi0,ClCi0,CaCi0,GluCi0,Wi0,NaCe0,KCe0,ClCe0,CaCc0,GluCc0,We0,NaCg0,KCg0,ClCg0,CaCg0,GluCg0,Wg0,NaCp0,KCp0,ClCp0,CaCp0,GluCp0,Wp0,CNa,CK,CCl,CCa,CGlu,Vi0,Vg0,Vp0,F,C,VolPAP, VolPreSyn, Volc, VolPostSyn, NBi")

ex1 = -NaCi0 - KCi0 - ClCi0 - NAi/Wi0 + NaCe0 + KCe0 + ClCe0  + NAe/We0 + NBe/We0
ex2 = -NaCg0 - KCg0 - ClCg0  - NAg/Wg0 - NBg/Wg0 + NaCe0 + KCe0 + ClCe0  + NAe/We0 + NBe/We0
ex3 = -NaCp0 - KCp0 - ClCp0 - NAp/Wp0 -NBp/Wp0  + NaCe0 + KCe0 + ClCe0  + NAe/We0 + NBe/We0
ex4 = CNa + CK - CCl + 2*CCa - CGlu - NAi - NAe + NBe - NAg + NBg - NAp + NBp
ex5 = (F/ C) * ((NaCi0 + KCi0 - ClCi0)*Wi0 + 2*CaCi0*VolPreSyn - GluCi0*VolPreSyn-NAi) - Vi0
ex6 = (F / C) * ((NaCg0 + KCg0 - ClCg0)*Wg0 + (2*CaCg0 - GluCg0)*VolPAP - NAg + NBg) - Vg0
ex7 = (F / C) * ((NaCp0 + KCp0 - ClCp0)*Wp0 + 2*CaCp0*VolPostSyn - NAp + NBp) - Vp0

sol = solve([ex1,ex2,ex3,ex4,ex5,ex6,ex7],NAi,NAe,NBg,NAg,NAp,NBp,NBe)

for key in keys(sol)
    println("$key: ",sol[key])
end
    
for key in keys(sol)
    #Neuron
    sol[key] = subs(sol[key],NaCi0,13.0)
    sol[key] = subs(sol[key],KCi0,145.0)
    sol[key] = subs(sol[key],ClCi0,7.0)
    sol[key] = subs(sol[key],CaCi0,0.0001)
    sol[key] = subs(sol[key],GluCi0,3.0)
    sol[key] = subs(sol[key],Wi0,2.0)
    sol[key] = subs(sol[key],VolPreSyn,0.001)
    sol[key] = subs(sol[key],Vi0,-65.5)
    #ECS
    sol[key] = subs(sol[key],NaCe0,152.0)
    sol[key] = subs(sol[key],KCe0,3.0)
    sol[key] = subs(sol[key],ClCe0,135.0)
    sol[key] = subs(sol[key],We0,1.425)
    #PostSyn
    sol[key] = subs(sol[key],NaCp0,12.0)
    sol[key] = subs(sol[key],KCp0,145.0)
    sol[key] = subs(sol[key],ClCp0,7.0)
    sol[key] = subs(sol[key],CaCp0,0.0001)
    sol[key] = subs(sol[key],Wp0,2.0)
    sol[key] = subs(sol[key],VolPostSyn,0.001)
    sol[key] = subs(sol[key],Vp0,-65.5)
    #Glia
    sol[key] = subs(sol[key],NaCg0,13.0)
    sol[key] = subs(sol[key],KCg0,80.0)
    sol[key] = subs(sol[key],ClCg0,35.0)
    sol[key] = subs(sol[key],CaCg0,0.00011)
    sol[key] = subs(sol[key],GluCg0,2.0)
    sol[key] = subs(sol[key],Wg0,1.7)
    sol[key] = subs(sol[key],VolPAP,0.001)
    sol[key] = subs(sol[key],Vg0,-80.0)
    # Others
    sol[key] = subs(sol[key],F,96485.333)
    sol[key] = subs(sol[key],C,20.0)
    sol[key] = subs(sol[key],CNa,288.7)
    sol[key] = subs(sol[key],CK,720.275)
    sol[key] = subs(sol[key],CCl,279.875)
    sol[key] = subs(sol[key],CGlu,0.0050001)
    sol[key] = subs(sol[key],CCa,0.0018003100000000003)
end

for key in keys(sol)
    println("$key: ",sol[key])
end
    

