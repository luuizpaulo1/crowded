class dados_recebidos:
    def __init__(self):        
        self.identificador_onibus = 0
        self.identificador_ultimo_ponto = 0
        self.passageiros_em_pe = 0
        self.passagerios_sentados = 0
        self.data = ""

    #Cria a querry para inserir os dados no BD
    def gerar_comando_insert(self):
        query = "INSERT INTO [dados-recebidos] ([identificador-onibus], [identificador-ultimo-ponto], [passageiros-em-pe], [passageiros-sentados], [data])"
        query += "\n" + "VALUES ("
        query += str(self.identificador_onibus) + ","
        query += str(self.identificador_ultimo_ponto) + ","
        query += str(self.passageiros_em_pe) + ","
        query += str(self.passagerios_sentados) + ","
        query += '"' + str(self.data) + '"' + ")"
        return query
