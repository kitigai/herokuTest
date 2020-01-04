
import sys
import os
import gym
import numpy as np
import random
from collections import deque

from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

class QLearn:
    def __init__(self, action_size, state_size, max_episode):
      self.state_size = state_size
      self.action_size = action_size
      self.max_episode = max_episode
      
      # These are hyper parameters for the DQN
      self.discount_factor = 0.99
      self.learning_rate = 0.001
      self.epsilon = 1.0
      self.epsilon_decay = 0.99999
      self.epsilon_min = 0.01
      self.batch_size = 64
      self.train_start = 1000
      
      #build models
      self.model = self.defineModel()
      self.target_model = self.defineModel()
      
      # create replay memory using deque
      self.memory = deque(maxlen=2000)   
      self.mini_memory = deque(maxlen=self.max_episode)
      # initialize target model
      self.update_target_model()
      #self.epsilon = 1.0  # exploration constant
      #self.alpha = alpha      # discount constant
      #self.gamma = 1.0      # discount factor
      #self.actions = actions
      #self.exploration_delta = epsilon / iterations
    def defineModel(self):
      
      model = keras.Sequential([
        keras.layers.Dense(24, activation="relu", input_shape=(self.state_size,), kernel_initializer='he_uniform'),
        keras.layers.Dense(24, activation="relu", kernel_initializer='he_uniform'),
        keras.layers.Dense(self.action_size, activation='linear', kernel_initializer='he_uniform')
      ])
      model.summary()
      model.compile(optimizer='adam', 
              loss='mse',
              metrics=['accuracy'])
      
      return model
    
    def update_target_model(self):
      self.target_model.set_weights(self.model.get_weights())
      
    def append_sample(self, sample, action, reward, next_state, done):
      self.memory.append((sample, action, reward, next_state, done))
      if self.epsilon > self.epsilon_min:
        self.epsilon *= self.epsilon_decay
    
    def append_success_sample(self):
      self.memory.extend(self.mini_memory)
      
      for i in range(len(self.mini_memory)):
        if self.epsilon > self.epsilon_min:
          self.epsilon *= self.epsilon_decay
                     
      self.mini_memory.clear()
                     
    def append_mini_sample(self, sample, action, reward, next_state, done):
      self.mini_memory.append((sample, action, reward, next_state, done))
                     
    def getQ(self, state):
      #print(state.shape)
      return self.model.predict(state)
    def learnQ(self):
      if len(self.memory) < self.train_start:
        return
      
      batch_size = min(self.batch_size, len(self.memory))
      mini_batch = random.sample(self.memory, batch_size)
      
      update_input = np.zeros((batch_size, self.state_size))
      update_target = np.zeros((batch_size, self.state_size))
      
      action, reward, done = [], [], []
      
      for i in range(batch_size):
        update_input[i] = mini_batch[i][0]
        action.append(mini_batch[i][1])
        reward.append(mini_batch[i][2])
        update_target[i] = mini_batch[i][3]
        done.append(mini_batch[i][4])
        
      target = self.model.predict(update_input)
      target_val = self.target_model.predict(update_target)
      
      for i in range(batch_size):
        if done[i]:
          target[i][action[i]] = reward[i]
        else:
          target[i][action[i]] = reward[i] + self.discount_factor*np.amax(target_val[i])
          
      self.model.fit(update_input, target, batch_size=self.batch_size,
                       epochs=1, verbose=0)
      #initialQ = self.getQ(state)
      #nextQ = self.getQ(state)
      #print(action)
      #print(initialQ.shape)
      #initialQ[0][action] = reward + self.gamma*np.amax(nextQ)
      
      #self.model.fit(state, initialQ, verbose=0)
      #if initialQ is None:
      #  self.q[(state, action)] = reward
      #else:
      #  nextAction = self.greedyAction(nextState)
      #  nextQ = self.getQ(nextState, nextAction)
      #  self.q[(state, action)] = initialQ + self.alpha * ( reward + self.gamma*nextQ - initialQ)
    def getNextAction(self, state):
      if random.random() > self.epsilon:
        return self.greedyAction(state)
      else:
        return self.randomAction()
    def greedyAction(self, state):
      #qInstate = [self.getQ(state, a) for a in self.actions]
      #print(qInstate)
      #maxQ = max(qInstate)
      #maxQIndex = max(qInstate.items(), lambda x:x[1])[0][1]
      #maxQIndex = self.actions[qInstate.index(maxQ)]
      return np.argmax(self.getQ(state))

    def randomAction(self):
      return random.randrange(self.action_size)