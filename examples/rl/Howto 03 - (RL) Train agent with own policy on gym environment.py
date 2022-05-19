## -------------------------------------------------------------------------------------------------
## -- Project : MLPro - A Synoptic Framework for Standardized Machine Learning Tasks
## -- Package : mlpro
## -- Module  : Howto 03 - Train agent with own policy on gym environment
## -------------------------------------------------------------------------------------------------
## -- History :
## -- yyyy-mm-dd  Ver.      Auth.    Description
## -- 2021-06-03  0.0.0     DA       Creation
## -- 2021-06-06  1.0.0     DA       Released first version
## -- 2021-06-25  1.1.0     DA       Extended by data logging/storing (user home directory)
## -- 2021-07-06  1.1.1     SY       Bugfix due to method Training.save_data() update
## -- 2021-08-28  1.2.0     DA       Introduced Policy
## -- 2021-09-11  1.2.0     MRD      Change Header information to match our new library name
## -- 2021-09-28  1.2.1     SY       Updated due to implementation of method get_cycle_limits()
## -- 2021-09-29  1.2.2     SY       Change name: WrEnvGym to WrEnvGYM2MLPro
## -- 2021-10-06  1.2.3     DA       Refactoring 
## -- 2021-10-18  1.2.4     DA       Refactoring 
## -- 2021-11-15  1.3.0     DA       Refactoring 
## -- 2021-12-03  1.3.1     DA       Refactoring 
## -- 2021-12-07  1.3.2     DA       Refactoring 
## -- 2022-05-19  1.3.3     SY       Remove MyPolicy and add RandomGenerator
## -------------------------------------------------------------------------------------------------

"""
Ver. 1.3.3 (2022-05-19)

This module shows how to train an agent with a custom policy inside on an OpenAI Gym environment using the fhswf_at_ml framework.
"""


from sys import path
from mlpro.bf.math import *
from mlpro.rl.models import *
from mlpro.wrappers.openai_gym import WrEnvGYM2MLPro
import gym
import random
from pathlib import Path
from mlpro.rl.pool.policies.randomgenerator import RandomGenerator




# 1 Implement your own RL scenario
class MyScenario (RLScenario):

    C_NAME      = 'Matrix'

    def _setup(self, p_mode, p_ada, p_logging):
        # 1 Setup environment
        gym_env     = gym.make('CartPole-v1')
        self._env   = WrEnvGYM2MLPro(gym_env, p_logging=p_logging) 

        # 2 Setup and return standard single-agent with own policy
        return Agent(
                p_policy=RandomGenerator(
                    p_observation_space=self._env.get_state_space(),
                    p_action_space=self._env.get_action_space(),
                    p_buffer_size=10,
                    p_ada=p_ada,
                    p_logging=p_logging,
                    p_seed=0
                ),    
            p_envmodel=None,
            p_name='Smith',
            p_ada=p_ada,
            p_logging=p_logging
        )




# 2 Create scenario and start training

if __name__ == "__main__":
    # 2.1 Parameters for demo mode
    cycle_limit = 500
    logging     = Log.C_LOG_WE
    visualize   = True
    path        = str(Path.home())
 
else:
    # 2.2 Parameters for internal unit test
    cycle_limit = 50
    logging     = Log.C_LOG_NOTHING
    visualize   = False
    path        = None


# 2.3 Create and run training object
training = RLTraining(
        p_scenario_cls=MyScenario,
        p_cycle_limit=cycle_limit,
        p_path=path,
        p_visualize=visualize,
        p_logging=logging )

training.run()