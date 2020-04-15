import os, sys
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'common')))
from CChameleonMetaObjectBase import *

class CCustomFileMetaData_Exp5(CChameleonMetaObjectBase):

    def __init__(self, file_path):
        super().__init__()
        
        # get file name and split
        file_name = os.path.basename(file_path)
        file_name = file_name.split(".")[0]
        tmp_split = file_name.split("_")
        
        self.type                   = tmp_split[1]
        self.nr_nodes               = int(tmp_split[2][:-5])
        self.nr_threads             = int(tmp_split[3][:-3])
        if(tmp_split[4].strip() == "ccp"):
            self.type += "_ccp"
            self.run                = int(tmp_split[5])
        else:
            self.run                = int(tmp_split[4])
        
