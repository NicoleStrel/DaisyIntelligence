import numpy as np
from typing import List, Dict, Optional, Tuple
import copy
import random
import os
from site_location import SiteLocationPlayer, Store, SiteLocationMap, euclidian_distances, attractiveness_allocation

class CDLCPlayer(SiteLocationPlayer):
    def place_stores(self, slmap: SiteLocationMap, 
                     store_locations: Dict[int, List[Store]],
                     current_funds: float):

      store_conf = self.config['store_config']

      #1-----find store type---
      #NEEED STORE TYPE
      # Choose largest store type possible:
      if current_funds >= store_conf['large']['capital_cost']:
          store_type = 'large'
      elif current_funds >= store_conf['medium']['capital_cost']:
          store_type = 'medium'
      else:
          store_type = 'small'
      
      #2-----Find the attractiveness values---
      sample_pos = []
      num_stores = 0
      for player, player_stores in store_locations.items():
        num_stores= num_stores + len(player_stores)
      if num_stores < 2:
        for i in range(400):
            x = random.randint(0, slmap.size[0])
            y = random.randint(0, slmap.size[1])
            sample_pos.append((x,y))
      else:
        for i in range(100):
            x = random.randint(0, slmap.size[0])
            y = random.randint(0, slmap.size[1])
            sample_pos.append((x,y))

      best_score = 0
      _pos = []
      best_pos = []
      score = []
      for pos in sample_pos:
        sample_store = Store(pos, store_type)
        temp_store_locations = copy.deepcopy(store_locations)
        temp_store_locations[self.player_id].append(sample_store)
        sample_alloc = attractiveness_allocation(slmap, temp_store_locations, store_conf)
        sample_score = (sample_alloc[self.player_id] * slmap.population_distribution).sum()
        if num_stores < 2:
            if sample_score > best_score:
                best_score = sample_score
                _pos = [pos]
            elif sample_score == best_score:
                _pos.append(pos)
        best_pos.append(pos)
        score.append(sample_score)
      sorted_score = sorted(score) # sorted rewards
      sorted_10 = sorted_score[-11:-1]
      # Get the state and indices
      '''
      rewardfile = "data/q_rewards.txt"
      rewards = correctingrewards(rewardfile)
      statefile = "data/q_states.txt"
      states = state_values(statefile)
      actionfile = "data/q_action.txt"
      actions = action_values(actionfile)
      q_table = q_table(states, actions, rewards)
      '''
      #file = open(os.path.join(os.path.dirname(__file__),"data/Q_player_current_data.txt"),"r")
      ansFile = open(os.path.join(os.path.dirname(__file__), "data/MLdata.txt"), 'r')
      lines = ansFile.readlines()
      # lines = data.split("\n")
      answer = {}
      for line in lines:
        num = line.split(" ")
        answer[int(num[0])]=[int(num[1]), int(num[2])]

      # Get indicies
      indices = answer[num_stores] # [2, 3]
      attract0 = sorted_10[indices[0]] #top 1 score
      attract1 = sorted_10[indices[1]] #top 2 score
      
      index0 = score.index(attract0)
      index1 = score.index(attract1)
      loc0 = best_pos[index0]
      loc1 = best_pos[index1]
      loc = best_pos[score.index(min(attract0, attract1))]
      '''
      if current_funds > (store_conf[store_type]['capital_cost'])*2:
        self.stores_to_place = [Store(loc0, store_type), Store(loc1, store_type)]
      else:
        '''
      if num_stores < 2:
        loc = _pos[0]
      self.stores_to_place = [Store(loc, store_type)]
      return