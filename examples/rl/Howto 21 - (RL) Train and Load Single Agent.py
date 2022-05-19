## -------------------------------------------------------------------------------------------------
## -- Project : MLPro - A Synoptic Framework for Standardized Machine Learning Tasks
## -- Package : mlpro
## -- Module  : Howto 21 - Train and Load Single Agent
## -------------------------------------------------------------------------------------------------
## -- History :
## -- yyyy-mm-dd  Ver.      Auth.    Description
## -- 2022-01-28  0.0.0     MRD      Creation
## -- 2022-01-28  1.0.0     MRD      Released first version
## -- 2022-05-19  1.0.1     MRD      Re-use the agent not for the re-training process
## --                                Remove commenting and numbering
## -------------------------------------------------------------------------------------------------

"""
Ver. 1.0.1 (2022-05-19)

This module shows how to train a single agent and load it again to do some extra cycles
"""

import gym
from stable_baselines3 import PPO
from mlpro.rl.models import *
from mlpro.wrappers.openai_gym import WrEnvGYM2MLPro
from mlpro.wrappers.sb3 import WrPolicySB32MLPro
from pathlib import Path

class MyScenario(RLScenario):
    C_NAME = 'Matrix'

    def _setup(self, p_mode, p_ada, p_logging):
        gym_env = gym.make('CartPole-v1')
        self._env = WrEnvGYM2MLPro(gym_env, p_logging=p_logging)

        policy_sb3 = PPO(
            policy="MlpPolicy",
            n_steps=5,
            env=None,
            _init_setup_model=False,
            device="cpu",
            seed=1)

        policy_wrapped = WrPolicySB32MLPro(
            p_sb3_policy=policy_sb3,
            p_cycle_limit=self._cycle_limit,
            p_observation_space=self._env.get_state_space(),
            p_action_space=self._env.get_action_space(),
            p_ada=p_ada,
            p_logging=p_logging)

        return Agent(
            p_policy=policy_wrapped,
            p_envmodel=None,
            p_name='Smith',
            p_ada=p_ada,
            p_logging=p_logging
        )

if __name__ == "__main__":
    cycle_limit = 5000
    adaptation_limit = 50
    stagnation_limit = 5
    eval_frequency = 5
    eval_grp_size = 5
    logging = Log.C_LOG_WE
    visualize = True
    path = str(Path.home())

else:
    cycle_limit = 50
    adaptation_limit = 5
    stagnation_limit = 5
    eval_frequency = 2
    eval_grp_size = 1
    logging = Log.C_LOG_NOTHING
    visualize = False
    path = None

training = RLTraining(
    p_scenario_cls=MyScenario,
    p_cycle_limit=cycle_limit,
    p_adaptation_limit=adaptation_limit,
    p_stagnation_limit=stagnation_limit,
    p_eval_frequency=eval_frequency,
    p_eval_grp_size=eval_grp_size,
    p_path=path,
    p_visualize=visualize,
    p_logging=logging)

training.run()
training_path = training._root_path

class MyNdScenario(RLScenario):
    C_NAME = 'Matrix2'

    def _setup(self, p_mode, p_ada, p_logging):
        gym_env = gym.make('CartPole-v1')
        self._env = WrEnvGYM2MLPro(gym_env, p_logging=p_logging)

        return self.load(training_path, "trained model.pkl")

scenario = MyNdScenario(p_mode=Mode.C_MODE_SIM, 
                        p_ada=False,
                        p_cycle_limit=cycle_limit,
                        p_visualize=visualize,
                        p_logging=logging)

scenario.reset()      
scenario.run()
