## -------------------------------------------------------------------------------------------------
## -- Project : MLPro - A Synoptic Framework for Standardized Machine Learning Tasks
## -- Package : mlpro.wrappers
## -- Module  : hyperopt.py
## -------------------------------------------------------------------------------------------------
## -- History :
## -- yyyy-mm-dd  Ver.      Auth.    Description
## -- 2021-12-07  0.0.0     SY       Creation 
## -- 2021-12-08  1.0.0     SY       Release of first version
## -- 2022-01-21  1.0.1     DA       Fixed some bugs
## -- 2022-01-27  1.0.2     SY       Wrapper enhancement
## -------------------------------------------------------------------------------------------------

"""
Ver. 1.0.2 (2022-01-27)
This module provides a wrapper class for hyperparameter tuning by reusinng Hyperopt framework
"""


from hyperopt import *
from mlpro.bf.ml import *
from mlpro.bf.math import *
from mlpro.bf.various import *
from mlpro.rl.models import *
from mlpro.gt.models import *
import os




## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class WrHPTHyperopt(HyperParamTuner, ScientificObject, Log):
    """
    This class is a ready to use wrapper class for Hyperopt framework. 
    Objects of this type can be treated as a hyperparameter tuner object.
    
    Parameters
    ----------
    p_arg1 : TYPE
        explanation of the first parameter.
    p_arg2 : TYPE, optional
        explanation of the second parameter. The default is True.
        
    Attributes
    ----------
    C_NAME: str
        Name of the class.
    C_ALGO_TPE: str
        Refer to Tree of Parzen Estimators (TPE) algorithm.
    C_ALGO_RAND: str
        Refer to Random Grid Search algorithm.
    """
    
    C_NAME              = 'Hyperopt'
    
    C_ALGO_TPE          = 'TPE'
    C_ALGO_RAND         = 'RND'
        
    C_SCIREF_TYPE       = ScientificObject.C_SCIREF_TYPE_PROCEEDINGS
    C_SCIREF_AUTHOR     = "James Bergstra, Dan Yamins, David D. Cox"
    C_SCIREF_TITLE      = "Hyperopt: A Python Library for Otimizing the Hyperparameters of Machine Learning Algorithms"
    C_SCIREF_CONFERENCE = "Proceedings of the 12th Python in Science Conference"
    C_SCIREF_YEAR       = "2013"
    C_SCIREF_PAGES      = "13-19"
    C_SCIREF_DOI        = "10.25080/Majora-8b375195-003"
    C_SCIREF_EDITOR     = "Stefan van der Walt, Jarrod Millman, Katy Huff"
    

## -------------------------------------------------------------------------------------------------
    def __init__(self, p_logging=Log.C_LOG_ALL, p_algo=C_ALGO_RAND, p_ids=None):
        """
        Parameters:
            p_logging     Log level (see constants for log levels)
        p_algo : str, optional    
            Selection of a hyperparameter tuning algorithm, default: C_ALGO_RAND
        p_ids : list of str, optional
            List of hyperparameter ids to be tuned, otherwise all hyperparameters, default: None
        """
        super().__init__(p_logging=p_logging)

        if p_algo is None:
            raise ParamError('Mandatory parameter p_algo is not supplied')
        else:
            self._algo  = p_algo
        
        self._ids       = p_ids
        self.num_trials = 0
        self.main_path  = None
        
        self.log(self.C_LOG_TYPE_I, 'Hyperopt configuration is successful')
            

## -------------------------------------------------------------------------------------------------
    def _maximize(self) -> TrainingResults:
        """
        This method is a place to setup a hp tuner based on hp structure of the model
        and run the hp tuner.

        Returns
        -------
        best_result : float
            The best result after a number of evaluations.

        """
        
        if self._training_cls is None:
            raise ParamError('Mandatory parameter self._training_cls is not supplied')
        
        if self._num_trials <= 0:
            raise ParamError('Parameter self._num_trials must be greater than 0')
        
        if self._training_param is None:
            raise ParamError('Mandatory parameter self._training_param is not supplied')
        
        #change root path in training param
        self.main_path = self._training_param['p_training_param']['p_path']
        self._training_param['p_training_param']['p_path'] = self.main_path+os.sep+'HyperparameterTuning'
        if not os.path.exists(self._training_param['p_training_param']['p_path']):
            os.mkdir(self._training_param['p_training_param']['p_path'])
        
        #ignore collecting data during tuning to save tuning time and memory
        self._training_param['p_training_param']['p_collect_states'] = False
        self._training_param['p_training_param']['p_collect_actions'] = False
        self._training_param['p_training_param']['p_collect_rewards'] = False
        self._training_param['p_training_param']['p_logging'] = Log.C_LOG_NOTHING
        self._training_param['p_training_param']['p_visualize'] = False
        self._training_param['p_training_param']['p_collect_eval'] = True
        
        #instantiate a scenario class and define the model in a variable
        training_cls = self._training_cls(**self._training_param['p_training_param'])
        self._model = training_cls._scenario._model
        
        spaces              = self.SetupSpaces()
        
        if self._algo == 'TPE':
            self.algo       = tpe.suggest
        elif self._algo == 'RND':
            self.algo       = rand.suggest
            
        best_result         = fmin(self._ofct_hyperopt, spaces, self.algo, self._num_trials, trials=Trials())
        return -best_result

## -------------------------------------------------------------------------------------------------
    def _ofct_hyperopt(self, p_params):
        """
        This method is a place to run the evaluations by getting next set of hps from the tuner,
        inducting hps to the model, and running the the objective function.

        Returns
        -------
        result : float
            The result of an evaluations.
            
        """
        
        #change root path in training param
        self._training_param['p_training_param']['p_path'] = self.main_path+os.sep+'HyperparameterTuning'+os.sep+'Trial_'+str(self.num_trials)
        if not os.path.exists(self._training_param['p_training_param']['p_path']):
            os.mkdir(self._training_param['p_training_param']['p_path'])
        
        #instantiate a scenario class
        training_cls = self._training_cls(**self._training_param['p_training_param'])
        
        #change the parameter according to p_params generated by hyperopt
        param_id                = 0
        for x in range(len(self.hp_tuple)):
            if not self._ids:
                _id             = self.hp_tuple[x].get_dim_ids()
            else:
                _id             = self._ids
                
            for i in range(len(_id)):
                if isinstance(self._model, MultiAgent) or isinstance(self._model, MultiPlayer):
                    for x in range(len(self._model.get_agents())):
                        self._model.get_agents()[x][0]._policy._hyperparam_tuple.set_value(_id[i], p_params[param_id])
                elif isinstance(self._model, Agent) or isinstance(self._model, Player):
                    self._model._policy._hyperparam_tuple.set_value(_id[i], p_params[param_id])
                else:
                    try:
                        self._model._hyperparam_tuple.set_value(_id[i], p_params[param_id])
                    except:
                        raise NotImplementedError
        
        #run the scenario and retrieve the high score
        result                  = self.training_cls.run()
        self.num_trials         += 1
        
        return -(result.highscore)

## -------------------------------------------------------------------------------------------------
    def SetupSpaces(self):
        """
        This method is used to setup the hyperparameter spaces, including the tuning boundaries and a suitable discrete value.
        The hyperparameter should be bounded both above and below.
        We are using the "quantized" continuous distributions for natural and integer numbers.
        Meanwhile the real numbers are not quantized.
        For different parameter expressions, please redefined this method and check http://hyperopt.github.io/hyperopt/getting-started/search_spaces/!
        For big data handling, please redifined this method!
        
        Returns
        -------
        spaces : list
            List of parameter expressions.

        """
        self.hp_tuple = []
        if isinstance(self._model, MultiAgent) or isinstance(self._model, MultiPlayer):
            for x in range(len(self._model.get_agents())):
                self.hp_tuple.append(self._model.get_agents()[x][0]._policy._hyperparam_tuple)
        elif isinstance(self._model, Agent) or isinstance(self._model, Player):
            self.hp_tuple.append(self._model._policy._hyperparam_tuple)
        else:
            try:
                self.hp_tuple.append(self._model._hyperparam_tuple)
            except:
                raise NotImplementedError
        
        spaces = []
        for x in range(len(self.hp_tuple)):
            if not self._ids:
                _id             = self.hp_tuple[x].get_dim_ids()
            else:
                _id             = self._ids
            for i in range(len(_id)):
                hp_id           = _id[i]
                hp_set          = self.hp_tuple[x].get_related_set().get_dim(hp_id)
                hp_base_set     = hp_set._base_set
                hp_boundaries   = hp_set.get_boundaries()
                hp_name_short   = hp_set.get_name_short()
                if not hp_boundaries:
                    raise ImplementationError('Missing boundary of a hyperparameter!')
                else:
                    hp_low      = hp_boundaries[0]
                    hp_high     = hp_boundaries[1]
                    if hp_base_set == Dimension.C_BASE_SET_N or hp_base_set == Dimension.C_BASE_SET_Z:
                        spaces.append(hp.quniform(hp_name_short+'_'+str(x),hp_low,hp_high,1))
                    elif hp_base_set == Dimension.C_BASE_SET_R:
                        spaces.append(hp.uniform(hp_name_short+'_'+str(x),hp_low,hp_high))
                    else:
                        raise NotImplementedError
        return spaces
