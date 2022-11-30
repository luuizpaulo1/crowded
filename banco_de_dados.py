import sqlite3


#retorna uma lista de listas com os seguintes termos:
#Nome do Onibus; ultimo ponto; passageiros em pe´, passageiros sentados, data da informação
#TODOs EM STRINGS
class banco_de_dados:
    def __init__(self):
        self.caminho_do_banco = "banco-de-lotacao.db"                      

    def consultar_lista_onibus(self):
        retornar = []
        try:
            conn = sqlite3.connect(self.caminho_do_banco)
            cursor = conn.cursor()
            #self.lista_onibus = cursor.execute("SELECT * FROM [onibus]").fetchall()

            busca = "SELECT [onibus].[nome-onibus], [pontos].[nome-ponto], [dados-recebidos].[passageiros-em-pe],\
            [dados-recebidos].[passageiros-sentados], [dados-recebidos].[data] \
            FROM [dados-recebidos]\
            INNER JOIN [onibus] ON [dados-recebidos].[identificador-onibus] = [onibus].[identificador-onibus] \
            INNER JOIN [pontos] ON [dados-recebidos].[identificador-ultimo-ponto] = [pontos].[identificador-ponto] \
            WHERE chave IN (SELECT MAX(chave) FROM [dados-recebidos] GROUP BY [identificador-onibus]);"
            self.lista_onibus = cursor.execute(busca).fetchall()
            retornar = self.lista_onibus          
        except sqlite3.Error as e:
            print(e)
            #retornar = e
        finally:
            if conn:
                conn.close()
        return retornar

    def inserir_dados(self, query):
        retornar = []
        try:
            conn = sqlite3.connect(self.caminho_do_banco)
            cursor = conn.cursor()   
            retornar = cursor.execute(query).fetchall()
            conn.commit()                   
        except sqlite3.Error as e:
            print("erro", e)            
        finally:
            if conn:
                conn.close()
        return retornar
                
