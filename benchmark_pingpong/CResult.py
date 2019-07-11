import os

class CResult():
    def __init__(self):

        self.send_type              = "none"
        self.process_distribution   = ""

        self.msg_size_bytes         = []
        self.msg_size_kb            = []
        self.transfer_time          = []
        self.throughput_mb_s        = []

        self.l3_accesses            = []
        self.l3_misses              = []
        self.l3_miss_ratio          = []

        self.l3_load_misses         = []
        self.l3_load_miss_ratio     = []

        self.total_instructions     = []

    def parseFile(self, file_path):
        cur_file_name               = os.path.basename(file_path)
        cur_file_name               = os.path.splitext(cur_file_name)[0]
        tmp_split                   = cur_file_name.split("_")

        self.send_type              = tmp_split[-2].strip()
        self.process_distribution   = tmp_split[-1].strip()

        with open(file_path) as file:            
            for line in file:
                if "PingPong with msg_size" in line:
                    tmp_split = line.split("\t")
                    self.msg_size_bytes.append(int(tmp_split[1].strip()))
                    self.msg_size_kb.append(float(tmp_split[3].strip()))
                    self.transfer_time.append(float(tmp_split[5].strip()))
                    self.throughput_mb_s.append(float(tmp_split[7].strip()))
                    self.l3_accesses.append(int(tmp_split[10].strip()))
                    self.l3_misses.append(int(tmp_split[12].strip()))
                    self.l3_miss_ratio.append(float(tmp_split[14].strip()))
                    self.l3_load_misses.append(int(tmp_split[16].strip()))
                    self.l3_load_miss_ratio.append(float(tmp_split[18].strip()))
                    self.total_instructions.append(int(tmp_split[20].strip()))
                    continue
                