import numpy as np
import pykov
import math

s = [0.99,0.01,0.00,0.00,0.00,0.00]
i = [0.00,0.80,0.04,0.01,0.00,0.15]
h = [0.00,0.15,0.80,0.05,0.00,0.00]
u = [0.00,0.00,0.05,0.80,0.15,0.00]
o = [0.00,0.00,0.00,0.00,1.00,0.00]
r = [0.00,0.00,0.00,0.00,0.00,1.00]

a = np.array([s,i,h,u,o,r])

states = dict(zip(list(range(1,len(a)+1)), ['S','I','H','U','O','R']))
dic = { (states[i+1], states[j+1]):a[i][j] for i in range(len(a)) for j in range(len(a[i])) }
M = pykov.Matrix( dic )
print(M, end='\n\n')

# Todos os estados
print(M.states(), end='\n\n')
# Antecessores de cada estado
print(M.pred(), end='\n\n')
# Sucessores de cada estado
print(M.succ(), end='\n\n')

C = pykov.Chain( dic )
state = pykov.Vector(S=1)
# Distribuição de prob após N dias, começando no estado state
n_inicio=274 # dias, entre o dia do primeiro infetado em Portugal e o dia da submissão do projeto
dia274=C.pow(state, n_inicio)
n_fim=365-(31+28+1)
fim2020=C.pow(state, n_fim)

# % aumento de recuperados esperado entre 09/12/2020 e 01/01/2021
rate_r=(fim2020-dia274)['R']
# média de recuperados diários esperada entre 09/12/2020 e 01/01/2021
pop = 10.28*10**6
dias= n_fim - n_inicio
avg_r_daily=((fim2020-dia274)['R']*pop/dias)


# Random walk de N transições; opcional: começar no estado A e acabar no estado B
n=1
C.walk(n, 'I', 'R') #descartar?


# Prob ( recuperar no primeiro dia após ser infetado )
walk = ['I', 'R']
p1=math.exp(C.walk_probability(walk))

# Prob( um infetado recuperar no Nº dia )
n=10
walk = ['I']*n + ['R']
p2=math.exp(C.walk_probability(walk))

# Prob ( um infetado recuperar entre o Nº e o (N+M)º dia sem ser hospitalizado )
m=4
walk[1:1] = ['I']*4
p3=sum( [math.exp(C.walk_probability(walk[i:])) for i in range(5)] )

# Prob ( um infetado passar menos de N dias (seguintes) hospitalizado)
n=5
walk = ['I'] + ['H']*n
p4=sum( [ math.exp(C.walk_probability(walk[:-i])) for i in range(1, n) ])

# Prob ( estando infetado ou hospitalizado, passar apenas os 2 dias seguintes em UCI )
walks = [['H','U','U','H'], ['H','U','U','I'], ['H','U','U','O'], ['I','U','U','O']]
p5=sum([math.exp(C.walk_probability(w)) for w in walks])

# Prob ( entrar em UCI e morrer em menos de N+1 dias, sabendo estava infetado/hospitalizado )
n=9
walks = [ ['H'] + ['U']*n + ['O'], ['I'] + ['U']*n + ['O'] ]
p6=sum([math.exp(C.walk_probability(w[:1]+w[1+h:len(w)])) for w in walks for h in range(n-1)])



# Distribuição de equilibrio (não está a funcionar somehow)
print(C.steady())
