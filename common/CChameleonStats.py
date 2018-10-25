class ExecTimeStats():
    # def __init__(self, *args, **kwargs):
    def __init__(self, name_in_output=None):
        self.name_in_output     = name_in_output
        self.time_sum           = 0.0
        self.time_avg           = 0.0
        self.count              = 0

    def parseLine(self, str_line):
        tmp_split               = str_line.split("\t")
        self.name_in_output     = tmp_split[1].strip()
        self.time_sum           = float(tmp_split[3].strip())
        self.time_avg           = float(tmp_split[7].strip())
        self.count              = float(tmp_split[5].strip())

class ChameleonStatsPerRank():

    def __init__(self, rank):
        self.rank                       = rank

        self.num_executed_task_local    = 0
        self.num_executed_task_stolen   = 0
        self.num_task_offloaded         = 0

        self.task_exec_local            = ExecTimeStats()
        self.task_exec_stolen           = ExecTimeStats()
        self.offload_send_task          = ExecTimeStats()
        self.offload_recv_task          = ExecTimeStats()
        self.offload_send_results       = ExecTimeStats()
        self.offload_recv_results       = ExecTimeStats()
        self.encode                     = ExecTimeStats()
        self.decode                     = ExecTimeStats()

    def parseContent(self, arr_content, pre_filtered=True):
        for line in arr_content:
            if not pre_filtered:
                # skip lines if necessary
                if(not line.startswith("Stats R#" + str(self.rank) + ":")):
                    continue

            if "_num_executed_tasks_local" in line:
                tmp_spl                         = line.split("\t")
                self.num_executed_task_local    = int(tmp_spl[2])
            elif "_num_executed_tasks_stolen" in line:
                tmp_spl                         = line.split("\t")
                self.num_executed_task_stolen   = int(tmp_spl[2])
            elif "_num_tasks_offloaded" in line:
                tmp_spl                         = line.split("\t")
                self.num_task_offloaded         = int(tmp_spl[2])
            elif "_time_task_execution_local_sum" in line:
                self.task_exec_local.parseLine(line)
            elif "_time_task_execution_stolen_sum" in line:
                self.task_exec_stolen.parseLine(line)
            elif "_time_comm_send_task_sum" in line:
                self.offload_send_task.parseLine(line)
            elif "_time_comm_recv_task_sum" in line:
                self.offload_recv_task.parseLine(line)
            elif "_time_comm_back_send_sum" in line:
                self.offload_send_results.parseLine(line)
            elif "_time_comm_back_recv_sum" in line:
                self.offload_recv_results.parseLine(line)
            elif "_time_encode_sum" in line:
                self.encode.parseLine(line)
            elif "_time_decode_sum" in line:
                self.decode.parseLine(line)

class ChameleonStatsPerRun():

    def __init__(self):
        self.stats_per_rank = []

    def parseContent(self, arr_content, pre_filtered=False):
        # first we need to identify the number of overall ranks
        num_overall_ranks = -1
        for line in arr_content:
            if("Stats R#" in line and "_num_overall_ranks" in line):
                tmp_spl                         = line.split("\t")
                num_overall_ranks               = int(tmp_spl[2])
                break
        
        if num_overall_ranks == -1:
            raise TypeError("_num_overall_ranks not included in statistics output")

        # init corresponding objects
        self.stats_per_rank = [ChameleonStatsPerRank(i) for i in range(num_overall_ranks)]
        for i in range(num_overall_ranks):
            self.stats_per_rank[i].parseContent(arr_content, pre_filtered=False)

    def parseFile(self, file_path):
        tmp_arr = []
        with open(file_path) as file:
            for line in file:
                tmp_arr.append(line)
        self.parseContent(tmp_arr)
