class CStatsDataPoint():
    def __init__(self, cumulative=True, name_in_output=None):
        self.name_in_output     = name_in_output
        self.cumulative         = cumulative
        if(cumulative):
          self.data_sum         = 0.0
          self.data_avg         = 0.0
          self.data_count       = 0
        else:
          self.data_sum         = []
          self.data_avg         = []
          self.data_count       = []

    def setMeasurment(self, val_sum, val_avg, val_count):
        if(self.cumulative):
          self.data_sum         = val_sum
          self.data_avg         = val_avg
          self.data_count       = val_count
        else:
          self.data_sum         = []
          self.data_avg         = []
          self.data_count       = []

    def parseLine(self, str_line):
        tmp_split               = str_line.split("\t")
        self.name_in_output     = tmp_split[1].strip()
        if(self.cumulative):
          self.data_sum         = float(tmp_split[3].strip())
          self.data_avg         = float(tmp_split[7].strip())
          self.data_count       = float(tmp_split[5].strip())
        else: 
          self.data_sum.append(float(tmp_split[3].strip()))
          self.data_avg.append(float(tmp_split[7].strip()))
          self.data_count.append(float(tmp_split[5].strip()))

class CChameleonStatsPerRank():

    def __init__(self, rank, cumulative=True):
        self.rank                       = rank

        self.num_executed_tasks_local   = CStatsDataPoint(cumulative, "_num_executed_tasks_local")
        self.num_executed_tasks_stolen  = CStatsDataPoint(cumulative, "_num_executed_tasks_stolen")
        self.num_task_offloaded         = CStatsDataPoint(cumulative, "_num_tasks_offloaded")

        self.task_exec_local            = CStatsDataPoint(cumulative)
        self.task_exec_stolen           = CStatsDataPoint(cumulative)
        self.task_exec_overall          = CStatsDataPoint(cumulative)

        self.time_taskwait              = CStatsDataPoint(cumulative)

        self.offload_send_task          = CStatsDataPoint(cumulative)
        self.offload_recv_task          = CStatsDataPoint(cumulative)
        self.offload_send_results       = CStatsDataPoint(cumulative)
        self.offload_recv_results       = CStatsDataPoint(cumulative)
        self.encode                     = CStatsDataPoint(cumulative)
        self.decode                     = CStatsDataPoint(cumulative)

    def parseContent(self, arr_content, pre_filtered=True):
        for line in arr_content:
            if not pre_filtered:
                # skip lines if necessary
                if(not line.startswith("Stats R#" + str(self.rank) + ":")):
                    continue

            if "_num_executed_tasks_local" in line:
                tmp_spl     = line.split("\t")
                tmp_val     = int(tmp_spl[2])
                self.num_executed_tasks_local.setMeasurment(tmp_val, tmp_val, 1)
            elif "_num_executed_tasks_stolen" in line:
                tmp_spl     = line.split("\t")
                tmp_val     = int(tmp_spl[2])
                self.num_executed_tasks_stolen.setMeasurment(tmp_val, tmp_val, 1)
            elif "_num_tasks_offloaded" in line:
                tmp_spl     = line.split("\t")
                tmp_val     = int(tmp_spl[2])
                self.num_task_offloaded.setMeasurment(tmp_val, tmp_val, 1)
            elif "_time_task_execution_local_sum" in line:
                self.task_exec_local.parseLine(line)
            elif "_time_task_execution_stolen_sum" in line:
                self.task_exec_stolen.parseLine(line)
            elif "_time_task_execution_overall" in line:
                self.task_exec_overall.parseLine(line)
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
            elif "_time_taskwait_sum" in line:
                self.time_taskwait.parseLine(line)

class CChameleonStatsPerRun():

    def __init__(self):
        # per rank information
        self.stats_per_rank     = []

        # per run information (fixed list for now)
        self.execution_time     = 0

    def addMeasurement(self, sig_name, value):
        eval("self." + sig_name + " = " + str(value))

    def parseContent(self, arr_content, pre_filtered=False):
        # first we need to identify the number of overall ranks
        num_overall_ranks = -1
        self.stats_per_rank = None
        
        for line in arr_content:
            if("Stats R#" in line and "_num_overall_ranks" in line):
                tmp_spl                         = line.split("\t")
                num_overall_ranks               = int(tmp_spl[2])
                break
        
        if num_overall_ranks == -1:
            print("WARNING: _num_overall_ranks not included in statistics output")
            return

        # init corresponding objects
        self.stats_per_rank = [CChameleonStatsPerRank(i) for i in range(num_overall_ranks)]
        for i in range(num_overall_ranks):
            self.stats_per_rank[i].parseContent(arr_content, pre_filtered=False)

    def parseFile(self, file_path, signal_filter=None):
        tmp_arr = []
        check_signals = signal_filter is not None
        if check_signals:
            signal_filter.append("_num_overall_ranks") # required field

        with open(file_path) as file:
            for line in file:
                if check_signals:
                    import_line = False
                    for s in signal_filter:
                        if s in line:
                            import_line = True
                            break
                    if import_line:
                        tmp_arr.append(line)
                else:
                    tmp_arr.append(line)
        self.parseContent(tmp_arr)
