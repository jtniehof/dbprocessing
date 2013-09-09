#!/usr/bin/env python2.6

"""Combined unit test suite for all dbprocessing classes"""

from test_DBfile import *
from test_DBqueue import *
from test_DBUtils import *
from test_Diskfile import *
from test_ProcessQueue import *
from test_Version import *
from test_DBStrings import *


__version__ = '2.0.3'


if __name__ == "__main__":
    unittest.main()