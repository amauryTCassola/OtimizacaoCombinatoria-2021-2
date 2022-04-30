using GLPK
using JuMP;

M = 100
n = 4
D = [0, 15, 7, 13]
L = [0, 35, 40, 20]
d = [[0, 5, 3, 7] [5, 0, 3, 2] [3, 3, 0, 4] [7, 2, 4, 0]]

model = Model();

set_optimizer(model, GLPK.Optimizer);

@variable(model, X[1:n, 1:n], Bin) #Rota
@variable(model, P[1:n], Int) #Pesos
@variable(model, mtzu[1:n], Int); #variável auxiliar para eliminação de sub-ciclos

@constraint(model, grau_saida[u in 1:n], sum(X[u, v] for v in 1:n) == 1)
@constraint(model, grau_entrada[v in 1:n], sum(X[u, v] for u in 1:n) == 1)
@constraint(model, si_mesmo[v in 1:n], X[v, v] == 0)
#remoção de sub-ciclos:
@constraint(model, subciclo[ui = 1:n, uj = 2:n], mtzu[ui] + X[ui, uj] <= mtzu[uj]+ (n - 1) * (1 - X[ui, uj]) )
#restrições de peso e limite
@constraint(model, P1, P[1] == sum(D[v] for v in 1:n))

@constraint(model, peso0[v in 2:n, u in 1:n], P[v] <= P[u] - D[u] + M*(1-X[u,v]));
@constraint(model, peso1[v in 2:n, u in 1:n], -P[v] <= -(P[u] - D[u]) + M*(1-X[u,v]));
@constraint(model, peso2[v in 2:n], P[v] <= L[v]);

@objective(model, Min, sum( sum( d[u,v]*X[u,v] for u=1:n) for v=1:n));

print(model)

optimize!(model)

@show objective_value(model)

@show value.(X) #o . vetoriza a operação

@show termination_status(model)


