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
str_states = ['S','I','H','U','O','R']
states = dict(zip(list(range(1,len(a)+1)), str_states))
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
n_inicio=282 # dias, entre o dia do primeiro infetado em Portugal e o dia da submissão do projeto
dia274=C.pow(state, n_inicio)
n_fim=365-(31+28+1)
fim2020=C.pow(state, n_fim)

# % aumento de recuperados esperado entre 09/12/2020 e 01/01/2021
rate_r=(fim2020-dia274)['R']*100
# média de recuperados diários esperada entre 09/12/2020 e 01/01/2021
pop = 10.28*10**6
dias = n_fim - n_inicio
avg_r_daily=(rate_r / 100 * pop / dias)
print('rate_r {}\navg_r_daily {}\n'.format(round(rate_r,2), round(avg_r_daily)))



n=10

# Prob ( recuperar no primeiro dia após ser infetado )
walk = ['I', 'R']
p1=math.exp(C.walk_probability(walk))

# Prob( um infetado recuperar no Nº dia )
walk = ['I']*n + ['R']
p2=math.exp(C.walk_probability(walk))

# Prob ( um infetado recuperar entre o Nº e o (N+M)º dia sem ser hospitalizado )
m=4
walk[1:1] = ['I']*m
p3=sum( [math.exp(C.walk_probability(walk[i:])) for i in range(m+1)] )

# Prob ( um infetado passar menos de N dias (seguintes) hospitalizado)
walk = ['I'] + ['H']*n
p4=sum( [ math.exp(C.walk_probability(walk[:-i])) for i in range(1, n) ])

# Prob ( estando infetado ou hospitalizado, passar apenas os 2 dias seguintes em UCI )
walks = [['H','U','U','H'], ['H','U','U','O'], ['I','U','U','H'], ['I','U','U','O']]
p5=sum([math.exp(C.walk_probability(w)) for w in walks])

# Prob ( entrar em UCI e morrer em menos de N dias, sabendo estava infetado/hospitalizado )
walks = [ ['H'] + ['U']*(n-1) + ['O'], ['I'] + ['U']*(n-1) + ['O'] ]
p6=sum([math.exp(C.walk_probability(w[:1]+w[1+h:len(w)])) for w in walks for h in range(n-2)])

print('p1 {}\np2 {}\np3 {}\np4 {}\np5 {}\np6 {}\n'.format(round(p1,2),round(p2,2), round(p3,2), round(p4,2), round(p5,2), round(p6,2)))



# Mean First Passage Times

days=10**4
times=10**5

def mfpt(days, f_state, l_state, times):
	return np.mean([len(C.walk(days, f_state, l_state))-1 for i in range(times)])


# S -> I (~99 ~101)
print('MFPG (S->I) {}'.format(round(mfpt(days, 'S', 'I', times))))
# I -> R
#print('MFPG (S->I) {}'.format(round(mfpt(days, 'I', 'R', times))))
# I -> H
#print('MFPG (S->I) {}'.format(round(mfpt(days, 'I', 'H', times))))
# I -> U
#print('MFPG (S->I) {}'.format(round(mfpt(days, 'I', 'U', times))))
# H -> I
#print('MFPG (H->I) {}'.format(round(mfpt(days, 'H', 'I', times))))
# H -> U
#print('MFPG (H->U) {}'.format(round(mfpt(days, 'H', 'U', times))))
# U -> O
#print('MFPG (U->O) {}'.format(round(mfpt(days, 'U', 'O', times))))



# Distribuição Estacionária
days=10**4
v_states = [pykov.Vector(S=1), pykov.Vector(I=1), pykov.Vector(H=1), pykov.Vector(U=1), pykov.Vector(O=1), pykov.Vector(R=1)]
steady = dict(zip(str_states, [C.pow(init, days) for init in v_states]))


