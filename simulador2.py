import datetime  # manipular data e hora
import random  # gerar dados aleatórios
import time  # pausar, suspender, etc a simulação
import requests


def criar_dados():
    dados = {}
    # dados
    dados["identificador_onibus"] = random.randint(1, 10)  # de 1 a 10
    dados["identificador_ultimo_ponto"] = random.randint(1, 40)
    dados["passageiros_em_pe"] = random.randint(0, 35)
    dados["passagerios_sentados"] = random.randint(0, 48)
    dados["data"] = datetime.datetime.now().isoformat()
    
    
    print("posting:")
    print(dados)
    try :
        url = 'https://lotatometro-app.herokuapp.com/post_json_data/'
        myobj = {'somekey': 'somevalue'}
        x = requests.post(url, json = dados)
        print("resultado", x.text)    
    finally:
        pass    


executando = True
while executando:
    print("Gerador aguardando 10 segundos")
    time.sleep(10)
    criar_dados()

print.debug("Encerrando gerador... encerrado")
