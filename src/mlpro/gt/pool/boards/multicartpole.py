## -------------------------------------------------------------------------------------------------
## -- Project : FH-SWF Automation Technology - Common Code Base (CCB)
## -- Package : mlpro
## -- Module  : multicartpole
## -------------------------------------------------------------------------------------------------
## -- History :
## -- yyyy-mm-dd  Ver.      Auth.    Description
## -- 2021-06-06  0.0.0     DA       Creation
## -- 2021-06-06  1.0.0     DA       Released first version
## -- 2021-09-11  1.0.0     MRD      Change Header information to match our new library name
## -------------------------------------------------------------------------------------------------

"""
Ver. 1.0.0 (2021-06-06)

This module provides game board classes based on the Multi-CartPole environment
of the reinforcement learning pool.
"""

from mlpro.rl.models import Reward
from mlpro.rl.pool.envs.multicartpole import MultiCartPole
from mlpro.gt.models import *




## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class MultiCartPoleGT(MultiCartPole, GameBoard):

    """
    Game theoretical pendant for the reinforcement learning environment class MultiCartPole.
    """

    C_NAME          = 'MultiCartPole(GT)'

    def __init__(self, p_num_envs=2, p_logging=True):
        MultiCartPole.__init__(self, p_num_envs=p_num_envs, p_reward_type=Reward.C_TYPE_EVERY_AGENT, p_logging=p_logging)






## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class MultiCartPolePGT(MultiCartPole, PGameBoard):
    """
    Potential Game theoretical pendant for the reinforcement learning environment class MultiCartPole.
    """

    C_NAME          = 'MultiCartPole(PGT)'

    def __init__(self, p_num_envs=2, p_logging=True):
        MultiCartPole.__init__(self, p_num_envs=p_num_envs, p_reward_type=Reward.C_TYPE_EVERY_AGENT, p_logging=p_logging)
