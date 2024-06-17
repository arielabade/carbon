# modelo que de fato roda a RNN

class CodanRNN(tf.keras.Model):
    def __init__(self, input_shape, hidden_units, output_units):
        super(CodanRNN, self).__init__()
        self.rnn = tf.keras.layers.SimpleRNN(hidden_units, return_sequences=True)
        self.fc = tf.keras.layers.Dense(output_units)
    
    def call(self, inputs):
        x = self.rnn(inputs)
        x = self.fc(x[:, -1, :])  # Use only the last time step's output
        return x
