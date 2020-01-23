import numpy as np
from lib.tilegame import TileGame, KeyMap
from lib.deepQ import QLearn
from collections import deque

class Learning:
  def learn(self):
    env = TileGame("../static/grid.csv")
    np.set_printoptions(linewidth=200)

    goal_average_steps = 195
    max_number_of_steps = 200
    last_time_steps = np.ndarray(0)
    iterations = 1000


    #number_of_features = env.observation_space.shape[0]
    last_time_steps = np.ndarray(0)
    mean_steps = np.ndarray(0)

    scores, episodes = [], []

    # Number of states is huge so in order to simplify the situatio
    # we discretize the space to: 10 ** number_of_features

    state_size = env.map.flatten().shape[0]
    action_size = 4

    # The Q-learn algorithm
    qlearn = QLearn(action_size,
                    state_size, max_number_of_steps)

    #special custom for MountainCar
    myMemory = deque(maxlen=200)

    for e in range(iterations):
      state = env.reset()
      state = state.flatten()
      state = np.reshape(state, [1, state_size])
      score = 0
      done = False
      

      while not done:
        #print(observation.shape)
        #old_state = state
        #print(old_observation.shape)
        action = qlearn.getNextAction(state)
        act = KeyMap().convert(action)
        new_state, reward, done = env.step(act)
        new_state = new_state.flatten()
        new_state = np.reshape(new_state, [1, state_size])
        # if an action make the episode end, then gives penalty of -100
        #reward = reward if not done or score == 499 else -100
        # reward = reward if not done or score != -200 else 100
        if ((not done) and (score < -50000)):
          done = True
          reward = -1000

        reward = -1 if not done else reward
          
        qlearn.append_mini_sample(state, action, reward, new_state, done)

        qlearn.learnQ()
        score += reward
        state = new_state

        if done:
          #reward = -200
          #qlearn.learnQ(old_observation.reshape(1,len(old_observation)), action , reward, new_observation.reshape(1,len(new_observation)))
          if not score == -51001:
            print("good")
            qlearn.append_success_sample()
          print("finished iterate : " , e, "score : ", score)
          # every episode, plot the play time
          # for printing, write off penalty
          qlearn.update_target_model()
          #score = score if score == -200 else score - 100

          #last_time_steps = np.append(last_time_steps, [int(t + 1)])
          scores.append(score)
          episodes.append(e)
          
          #break
          # if the mean of scores of last 10 episode is bigger than 490
          # stop training
      #if np.mean(scores[-min(10, len(scores)):]) > 490:
        #break