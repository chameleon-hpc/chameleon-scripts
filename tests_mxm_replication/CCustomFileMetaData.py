import os
from CChameleonMetaObjectBase import *

class CCustomFileMetaData(CChameleonMetaObjectBase):

    def __init__(self, file_path):
        super().__init__()
        
        # get file name and split
        file_name = os.path.basename(file_path)
        #file_name = file_name.split(".")[0]
        tmp_split = file_name.split("_")
        print (tmp_split)
        
        
        self.run                    = int(tmp_split[4].split(".")[0])
        self.percentage             = tmp_split[1]
        self.task_granularity       = int(tmp_split[2])
        # self.nr_ranks               = int(tmp_split[4][:-1]) # TODO: add nr of ranks to file name to be able to parse it here
        self.nr_threads             = int(tmp_split[3][:-1])
        

