import banco_de_dados
import dados_recebidos
from flask import Flask, request, jsonify

banco = banco_de_dados.banco_de_dados()

app = Flask(__name__)

@app.route("/")
@app.route('/home/')
def index():
    pagina = '<h1>{}</h><br />'.format("Escolha um onibus:")      
    
    dados = banco.consultar_lista_onibus()

    #pagina = '<h1>{}</h><br />'.format(dados)   
    for dado in dados:              
        pagina += '<a href="/onibus/{}"><button>{} atualmente em:   {}</button></a><br />'.format(dado[0],str(dado[0]),dado[1] ) 
    return pagina


#função para retornar dados no formato json
@app.route('/get_json/')
def get_data():        
    dados = banco.consultar_lista_onibus()    
    return jsonify(dados)

#função para receber dados de um onibus no formato json
@app.route('/post_json_data/', methods=['POST'])
def post_data():   
    if request.method == 'POST':     

        #nossa classe de dados
        dados = dados_recebidos.dados_recebidos()    

        request_data = request.get_json()
        
        #lendo valores recebidos
        dados.identificador_onibus = request_data['identificador_onibus']
        dados.identificador_ultimo_ponto = request_data['identificador_ultimo_ponto']
        dados.passageiros_em_pe = request_data['passageiros_em_pe']
        dados.passagerios_sentados = request_data['passagerios_sentados']
        dados.data = request_data['data']

        insert = dados.gerar_comando_insert()   

        resposta = banco.inserir_dados(insert)  
        print("Tentativa de INSERT:",insert, resposta)       
        #print("Tentativa de INSERT (resposta):", resposta)       
        return jsonify(resposta)


@app.route('/onibus/<nome_onibus>/')
def onibus_info(nome_onibus):
    pagina = ""

    dados = banco.consultar_lista_onibus()
    for dado in dados:
        if dado[0] == nome_onibus:
            pagina = "<html>\
                    <body>\
                    \
                    <h1>{}</h1>\
                    <p>Localização: {}</p>\
                    <p>Passageiros em pé: {}</p>\
                    <p>Passageiros Sentados: {}</p>\
                    <p>Data: {}</p>\
                    \
                    </body>\
                    </html>".format(nome_onibus, dado[1], dado[2], dado[3], dado[4])      
    return pagina