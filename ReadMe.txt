O nosso projeto teve por base um ficheiro csv de 10.000 pessoas ao longo de 1000 dias, onde em cada dia é registado o estado da pessoa: 
Suscetivel, infetado, Hospitalizado, UCI, Óbito, Recuperado. Este ficheiro é artificial, criado por nós. 
Não encontramos nenhum dataset idêntico real. Através deste ficheiro:

1.Estimamos a matriz de transição via máxima verosimilhança no R. Ficheiro: markovchainfit.R
2.Utilizar a matriz obtida no ponto 1 para previsão. Ficheiro: DTMC_COVID19Forecast.ipynb
3.Cálculo da distribuição estacionária. Ficheiro: CalculoDistEst.py
4.Miscelânea de problemas associados à DTMC. Cálculo de probabilidades entre estados, número médio de passos entre dois estados. Ficheiro: problems.py
5.Por último, também utilizamos o algoritmo de PageRank, que pode ser visto como uma cadeia de markov, para descobrir quais as fontes mais importantes na citação. Através dos campos cited e citing, construímos o grafo e calculamos o Rank.
6.Não incluímos o PageRank no nosso documento, porque o nosso projeto é sobre DTMC aplicadas ao COVID-19. Considere-se o PageRank como um extra.