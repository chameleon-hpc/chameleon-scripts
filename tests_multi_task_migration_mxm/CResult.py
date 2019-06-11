import os

class CResult():
    def __init__(self, result_type="multi"):
        self.result_type        = result_type
        self.n_threads          = 0
        self.task_granularity   = 0
        self.n_repetition       = 0

        self.time_chameleon     = 0
        self.time_openmp_only   = 0
        self.speedup            = 0

        self.n_local_tasks      = 0
        self.n_remote_tasks     = 0

    def parseFile(self, file_path):
        cur_file_name           = os.path.basename(file_path)
        cur_file_name           = os.path.splitext(cur_file_name)[0]
        tmp_split               = cur_file_name.split("_")

        self.result_type        = tmp_split[1].strip() + "_" + tmp_split[2].strip()
        self.n_threads          = float(tmp_split[4].strip()[:-1])
        self.task_granularity   = float(tmp_split[3].strip())
        self.n_repetition       = float(tmp_split[5].strip())

        with open(file_path) as file:
            for line in file:
                if "with chameleon took" in line:
                    tmp_split = line.split(" ")
                    self.time_chameleon = float(tmp_split[-1].strip())
                    continue
                if "with normal tasking took" in line:
                    tmp_split = line.split(" ")
                    self.time_openmp_only = float(tmp_split[-1].strip())
                    continue
                if "_num_executed_tasks_local" in line:
                    tmp_split = line.split("\t")
                    self.n_local_tasks = self.n_local_tasks + float(tmp_split[-1].strip())
                    continue
                if "_num_executed_tasks_stolen" in line:
                    tmp_split = line.split("\t")
                    self.n_remote_tasks = self.n_remote_tasks + float(tmp_split[-1].strip())
                    continue

        self.speedup = self.time_openmp_only / self.time_chameleon