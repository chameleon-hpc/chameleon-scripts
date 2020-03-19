import os
from CChameleonMetaObjectBase import *

class CCustomFileMetaData(CChameleonMetaObjectBase):

    def __init__(self, file_path):
        super().__init__()
        
        # get file name and split
        file_name = os.path.basename(file_path)
        file_name = file_name.split(".")[0]
        tmp_split = file_name.split("_")
        
        self.category               = tmp_split[1]
        self.version                = tmp_split[2]
        self.matrix_size            = int(tmp_split[3])
        self.block_size             = int(tmp_split[4])

        self.nr_ranks               = int(tmp_split[5][:-5])
        self.nr_threads             = int(tmp_split[6][:-1])
        self.run                    = int(tmp_split[7])


        

