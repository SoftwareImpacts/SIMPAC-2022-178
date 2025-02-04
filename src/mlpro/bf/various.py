## -------------------------------------------------------------------------------------------------
## -- Project : MLPro - A Synoptic Framework for Standardized Machine Learning Tasks
## -- Package : mlpro.bf
## -- Module  : various
## -------------------------------------------------------------------------------------------------
## -- History :
## -- yyyy-mm-dd  Ver.      Auth.    Description
## -- 2021-04-16  0.0.0     DA       Creation
## -- 2021-05-29  1.0.0     DA       Release of first version
## -- 2021-06-16  1.1.0     SY       Adding the first version of data storing,
## --                                data plotting, and data saving classes
## -- 2021-06-17  1.2.0     DA       New abstract classes Loadable, Saveable
## -- 2021-06-21  1.3.0     SY       Add extensions in classes Loadable,
## --                                Saveable, DataPlotting & DataStoring.
## -- 2021-07-01  1.4.0     SY       Extend save/load functionalities
## -- 2021-08-20  1.5.0     DA       Added property class Plottable
## -- 2021-08-28  1.5.1     DA       Added constant C_VAR0 to class DataStoring
## -- 2021-09-11  1.5.0     MRD      Change Header information to match our new library name
## -- 2021-10-06  1.5.2     DA       Moved class DataStoring to new module mlpro.bf.data.py and
## --                                classes DataPlotting, Plottable to new module mlpro.bf.plot.py
## -- 2021-10-07  1.6.0     DA       Class Log: 
## --                                - colored text depending on log type 
## --                                - new method set_log_level()
## -- 2021-10-25  1.7.0     SY       Add new class ScientificObject
## -- 2021-11-03  1.7.1     DA       Class Log: new type C_LOG_TYPE_SUCCESS for success messages 
## -- 2021-11-15  1.7.2     DA       Class Log: 
## --                                - method set_log_level() removed
## --                                - parameter p_logging is the new log level now
## --                                Class Saveable: new constant C_SUFFIX
## -- 2021-12-07  1.7.3     SY       Add a new attribute in ScientificObject
## -- 2021-12-31  1.7.4     DA       Class Log: udpated docstrings
## -- 2022-07-27  1.7.5     DA       A little refactoring
## -------------------------------------------------------------------------------------------------

"""
Ver. 1.7.5 (2022-07-27)

This module provides various classes with elementry functionalities for reuse in higher level classes. 
For example: logging, load/save, timer...
"""


from datetime import datetime, timedelta
from time import sleep
import dill as pkl
import os
from mlpro.bf.exceptions import *




## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class Loadable:
    """
    This abstract class adds the ability to be loadable to inherited classes. 
    """

## -------------------------------------------------------------------------------------------------
    @staticmethod
    def load(p_path, p_filename):
        """
        Loads content from the given path and file name. If file does not exist, it returns None.

        Parameters:
            p_path          Path that contains the file 
            p_filename      File name

        Returns: 
            A loaded object, if file content was loaded successfully. None otherwise.
        """

        if not os.path.exists(p_path + os.sep + p_filename):
            return None

        return pkl.load(open(p_path + os.sep + p_filename, 'rb'))





## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class Saveable:
    """
    This abstract class adds the ability to be saveable to inherited classes. The filename can be
    generated internally by implementing the method get_filename() or provided from outside otherwise.
    """

    C_SUFFIX = '.pkl'

    ## -------------------------------------------------------------------------------------------------
    def generate_filename(self):
        """
        To be redefined in case of use of internal generated file names.

        Returns: 
            Returns an internal unique filename. 
        """

        raise NotImplementedError

## -------------------------------------------------------------------------------------------------
    def save(self, p_path, p_filename=None) -> bool:
        """
        Saves content to the given path and file name. If file name is None, a unique file name will
        be generated by calling method generate_filename(). If it returns False then the saving method is failed. 

        Parameters:
            p_path          Path where file will be saved
            p_filename      File name (if None an internal filename will be generated)

        Returns: 
            True, if file content was saved successfully. False otherwise.
        """

        if (p_filename is not None) and (p_filename != ''):
            self.filename = p_filename
        else:
            self.filename = self.generate_filename()

        if self.filename is None:
            return False

        try:
            if not os.path.exists(p_path):
                os.makedirs(p_path)
            pkl.dump(self, open(p_path + os.sep + self.filename, "wb"))
            return True
        except:
            return False





## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class LoadSave(Loadable, Saveable):
    """
    This abstract class adds the ability to be loadable and saveable to inherited classes. The 
    filename can be generated internally by implementing the method generate_filename() or provided 
    from outside otherwise. See classes Loadable and Saveable for further information.
    """

    pass





## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class Log:
    """
    This class adds elementry log functionality to inherited classes.
    """

    C_TYPE              = '????'
    C_NAME              = '????'

    # Types of log lines
    C_LOG_TYPE_I        = 'I'  # Information
    C_LOG_TYPE_W        = 'W'  # Warning
    C_LOG_TYPE_E        = 'E'  # Error
    C_LOG_TYPE_S        = 'S'  # Success / Milestone

    C_LOG_TYPES         = [C_LOG_TYPE_I, C_LOG_TYPE_W, C_LOG_TYPE_E, C_LOG_TYPE_S]

    C_COL_WARNING       = '\033[93m'  # Yellow
    C_COL_ERROR         = '\033[91m'  # Red
    C_COL_SUCCESS       = '\033[32m'  # Green
    C_COL_RESET         = '\033[0m'  # Reset color

    # Log levels
    C_LOG_ALL           = True
    C_LOG_NOTHING       = False
    C_LOG_WE            = C_LOG_TYPE_W
    C_LOG_E             = C_LOG_TYPE_E

    C_LOG_LEVELS        = [C_LOG_ALL, C_LOG_NOTHING, C_LOG_WE, C_LOG_E]

    # Internals
    C_INST_MSG          = True

## -------------------------------------------------------------------------------------------------
    def __init__(self, p_logging=C_LOG_ALL):
        """
        Parameters:
            p_logging     Log level (see constants for log levels)
        """

        self.switch_logging(p_logging)
        if self.C_INST_MSG:
            self.log(self.C_LOG_TYPE_I, 'Instantiated')
            self.C_INST_MSG = False


## -------------------------------------------------------------------------------------------------
    def switch_logging(self, p_logging):
        """
        Sets new log level. 

        Parameters
        ----------
        p_logging     
            Log level (constant C_LOG_LEVELS contains valid values)

        """

        if p_logging not in self.C_LOG_LEVELS: raise ParamError('Wrong log level. See class Log for valid log levels')
        self._level = p_logging

 
 ## -------------------------------------------------------------------------------------------------
    def log(self, p_type, *p_args):
        """
        Writes log line to standard output in format:
        yyyy-mm-dd  hh:mm:ss.mmmmmm  [p_type  C_TYPE C_NAME]: [p_args] 

        Parameters:
            p_type      type of log entry
            p_args      log informations

        Returns: 
            Nothing
        """

        if not self._level: return

        if self._level == self.C_LOG_WE:
            if (p_type == self.C_LOG_TYPE_I) or (p_type == self.C_LOG_TYPE_S): return
        elif self._level == self.C_LOG_E:
            if (p_type == self.C_LOG_TYPE_I) or (p_type == self.C_LOG_TYPE_S) or (p_type == self.C_LOG_TYPE_W): return

        now = datetime.now()

        if p_type == self.C_LOG_TYPE_W:
            col = self.C_COL_WARNING
        elif p_type == self.C_LOG_TYPE_E:
            col = self.C_COL_ERROR
        elif p_type == self.C_LOG_TYPE_S:
            col = self.C_COL_SUCCESS
        else:
            col = self.C_COL_RESET

        print(col + '%04d-%02d-%02d  %02d:%02d:%02d.%06d ' % (
        now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond),
              p_type + '  ' + self.C_TYPE + ' ' + self.C_NAME + ':', *p_args, self.C_COL_RESET)





## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class Timer:
    """
    Timer class in two time modes (real/virtual) and with simple lap management.
    """

    C_MODE_REAL = 0  # Real time
    C_MODE_VIRTUAL = 1  # Virtual time

    C_LAP_LIMIT = 999999

## -------------------------------------------------------------------------------------------------
    def __init__(self, p_mode, p_lap_duration: timedelta, p_lap_limit=C_LAP_LIMIT) -> None:
        """
        Parameters:
            p_mode          C_MODE_REAL for real time mode,
                            C_MODE_VIRTUAL for virtual time mode
            p_lap_duration  Duration of a single lap
            p_lap_limit     maximum number of laps until the lap counter restarts with 0  
        """

        self.mode = p_mode
        self.lap_duration = p_lap_duration

        if p_lap_limit == 0:
            self.lap_limit = self.C_LAP_LIMIT
        else:
            self.lap_limit = p_lap_limit

        self.reset()


## -------------------------------------------------------------------------------------------------
    def reset(self) -> None:
        """
        Resets timer.

        Returns: 
            Nothing
        """

        self.time = timedelta(0, 0, 0)
        self.lap_time = timedelta(0, 0, 0)
        self.lap_id = 0

        if self.mode == self.C_MODE_REAL:
            self.timer_start_real = datetime.now()
            self.lap_start_real = self.timer_start_real
            self.time_real = self.timer_start_real


## -------------------------------------------------------------------------------------------------
    def get_time(self) -> timedelta:
        if self.mode == self.C_MODE_REAL:
            self.time_real = datetime.now()
            self.time = self.time_real - self.timer_start_real

        return self.time


## -------------------------------------------------------------------------------------------------
    def get_lap_time(self) -> timedelta:
        if self.mode == self.C_MODE_REAL:
            self.lap_time = datetime.now() - self.lap_start_real

        return self.lap_time


## -------------------------------------------------------------------------------------------------
    def get_lap_id(self):
        return self.lap_id


## -------------------------------------------------------------------------------------------------
    def add_time(self, p_delta: timedelta):
        if self.mode == self.C_MODE_VIRTUAL:
            self.lap_time = self.lap_time + p_delta
            self.time = self.time + p_delta


## -------------------------------------------------------------------------------------------------
    def finish_lap(self) -> bool:
        """
        Finishes the current lap. In timer mode C_MODE_REAL the remaining time
        until the end of the lap will be paused. 

        Returns: 
            True, if the remaining time to the next lap was positive. False, if 
            the timer timed out.
        """

        timeout = False

        # Compute delay until next lap
        delay = self.lap_duration - self.get_lap_time()

        # Check for timeout
        if delay < timedelta(0, 0, 0):
            timeout = True
            delay = timedelta(0, 0, 0)

        # Handle delay depending on timer mode
        if self.mode == self.C_MODE_REAL:
            # Wait until next lap start
            sleep(delay.total_seconds())
        else:
            # Just set next lap start time
            self.time = self.time + delay

        # Update lap data
        self.lap_id = divmod(self.lap_id + 1, self.lap_limit)[1]
        self.lap_time = timedelta(0, 0, 0)
        self.lap_start_real = datetime.now()

        return not timeout





## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class TStamp:
    """
    This class provides elementry time stamp functionality for inherited classes.
    """


## -------------------------------------------------------------------------------------------------
    def __init__(self, p_tstamp: timedelta = None):
        self.set_tstamp(p_tstamp)


## -------------------------------------------------------------------------------------------------
    def get_tstamp(self) -> timedelta:
        return self.tstamp


## -------------------------------------------------------------------------------------------------
    def set_tstamp(self, p_tstamp: timedelta):
        self.tstamp = p_tstamp





## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
class  ScientificObject:
    """
    This class provides elementary functionality for storing a scientific reference.
    """

    C_SCIREF_TYPE_NONE = None
    C_SCIREF_TYPE_ARTICLE = "Journal Article"
    C_SCIREF_TYPE_BOOK = "Book"
    C_SCIREF_TYPE_ONLINE = "Online"
    C_SCIREF_TYPE_PROCEEDINGS = "Proceedings"
    C_SCIREF_TYPE_TECHREPORT = "Technical Report"
    C_SCIREF_TYPE_UNPUBLISHED = "Unpublished"

    C_SCIREF_TYPE = C_SCIREF_TYPE_NONE
    C_SCIREF_AUTHOR = None
    C_SCIREF_TITLE = None
    C_SCIREF_JOURNAL = None
    C_SCIREF_ABSTRACT = None
    C_SCIREF_VOLUME = None
    C_SCIREF_NUMBER = None
    C_SCIREF_PAGES = None
    C_SCIREF_YEAR = None
    C_SCIREF_MONTH = None
    C_SCIREF_DAY = None
    C_SCIREF_DOI = None
    C_SCIREF_KEYWORDS = None
    C_SCIREF_ISBN = None
    C_SCIREF_SERIES = None
    C_SCIREF_PUBLISHER = None
    C_SCIREF_CITY = None
    C_SCIREF_COUNTRY = None
    C_SCIREF_URL = None
    C_SCIREF_CHAPTER = None
    C_SCIREF_BOOKTITLE = None
    C_SCIREF_INSTITUTION = None
    C_SCIREF_CONFERENCE = None
    C_SCIREF_NOTES = None
    C_SCIREF_EDITOR = None