
class minhaClasse:

    def _init_(self, att):
        self.meu_atributo = 'Ola Mundo' #construtor (inicializa recursos do objeto e aloca recursos). A instanciação pode ser feita através da chamada do objeto, ou do construtor.
        self.meu_atributo2 = att

    # os atirbutos são acessíveis a todo o restante da classe

    def meu_metodo(self):
        print('Estou no método!')

    def meu_metodo2(self, num, mult):
        return num * mult


