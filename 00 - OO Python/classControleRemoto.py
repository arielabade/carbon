class controleRemoto:

    def __init__ (self, televisao, comodo):
        self.televisao = televisao # chama o objeto para ele mesmo
        self.comodo = comodo 

    def avancar_canal(self):
        print('Canal Avancado')

    def voltar_canal(self):
        print('Voltar o canal')

    def escolher_canal(self, canal):
        print('Altrado para o canal: {}'.format(canal))

controle_sala = controleRemoto('samsung', 'sala')
print(controle_sala.comodo)
print(controle_sala.televisao)
controle_sala.avancar_canal()
controle_sala.escolher_canal(12)

controle_quarto = controleRemoto('LG', 'quarto')
print(controle_sala.comodo)
print(controle_sala.televisao)

