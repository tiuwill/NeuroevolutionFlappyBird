import numpy as np
import random

class NeuralNetwork:
  
  
  def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate=0.01):
   # np.random.seed(1)
    
    #Initialize weights from the network
    self.weights_input_hidden = 2*np.random.random((input_nodes,hidden_nodes)) - 1
    self.weights_hidden_output = 2*np.random.random((hidden_nodes,output_nodes)) - 1
    
    #initialize bias
    self.bias_input_hidden = np.ones((1,hidden_nodes))
    self.bias_hidden_output = np.ones((1,output_nodes))
    
    #initialize learning rate
    self.learning_rate = learning_rate
  
  
  def sigmoid(self,x, deriv=False):
    if(deriv):
      return x * (1 - x)
    return 1/(1+np.exp(-x))
  
  def predict(self,inputs):
    #Foward
    first_layer = inputs
    hidden_layer = np.dot(first_layer, self.weights_input_hidden) + self.bias_input_hidden
    hidden_layer = self.sigmoid(hidden_layer)


    output_layer = np.dot(hidden_layer, self.weights_hidden_output)
    output_layer = self.sigmoid(output_layer) 
    return output_layer
  
  def train(self, inputs, targets, epochs):
    #train the network
    for i in range(epochs):
      #Feed Foward
      first_layer = inputs
      hidden_layer = np.dot(first_layer, self.weights_input_hidden) + self.bias_input_hidden
      hidden_layer = self.sigmoid(hidden_layer)

      output_layer = np.dot(hidden_layer, self.weights_hidden_output)
      output_layer = self.sigmoid(output_layer) 

       #Backwards
      error = targets - output_layer #measure error
      output_layer_delta = error * self.sigmoid(output_layer, True) #calculate delta for output layer
      self.bias_hidden_output += np.sum(output_layer_delta, axis=0,keepdims=True) * self.learning_rate #update output bias values

      #calculate hidden layer error
      hidden_layer_error = np.dot(output_layer_delta, self.weights_hidden_output.T) 
      hidden_layer_delta = hidden_layer_error * self.sigmoid(hidden_layer, True) #calculate delta for the hidden 
      self.bias_input_hidden += np.sum(hidden_layer_delta, axis=0,keepdims=True) * self.learning_rate #update hidden bias values

      self.weights_input_hidden += np.dot(first_layer.T, (hidden_layer_delta * self.learning_rate))
      self.weights_hidden_output += np.dot(hidden_layer.T, (output_layer_delta * self.learning_rate))

  def mutate(self, rate):
    lines, columns = self.weights_input_hidden.shape
    for i in range(lines):
      for j in range(columns):
        r = random.uniform(0,1)
        if r < rate:
          self.weights_input_hidden[i][j]+= random.uniform(-1, 1)

        
    lines, columns = self.weights_hidden_output.shape
    for i in range(lines):
      for j in range(columns):
        r = random.uniform(0,1)
        if r < rate:
          self.weights_hidden_output[i][j]+= random.uniform(-1, 1)

    lines,columns = self.bias_input_hidden.shape
    print(columns)
    for i in range(columns):
      r = random.uniform(0,1)
      if r < rate:
        self.bias_input_hidden[0][i]+= random.uniform(-1,1)
    
    lines, columns = self.bias_hidden_output.shape
    for i in range(columns):
      r = random.uniform(0,1)
      if r < rate:
        self.bias_hidden_output[0][i]+= random.uniform(-1,1)
      

    
    
    
  
  
  