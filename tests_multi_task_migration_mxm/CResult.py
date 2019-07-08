import os

class CResult():
    def __init__(self, result_type="multi"):
        self.n_ranks            = 0

        self.result_type        = result_type
        self.n_threads          = 0
        self.task_granularity   = 0
        self.n_repetition       = 0

        self.time_chameleon     = 0
        self.time_openmp_only   = 0
        self.speedup            = 0

        self.n_local_tasks      = 0
        self.n_remote_tasks     = 0

        # used from rank 0
        self.sends_happened = False
        self.bytes_send_per_msg_min = 0
        self.bytes_send_per_msg_max = 0
        self.bytes_send_per_msg_avg = 0
        self.throughput_send_min = 0
        self.throughput_send_max = 0
        self.throughput_send_avg = 0

        # used from last rank
        self.recvs_happened = False
        self.bytes_recv_per_msg_min = 0
        self.bytes_recv_per_msg_max = 0
        self.bytes_recv_per_msg_avg = 0
        self.throughput_recv_min = 0
        self.throughput_recv_max = 0
        self.throughput_recv_avg = 0

    def parseFile(self, file_path):
        cur_file_name           = os.path.basename(file_path)
        cur_file_name           = os.path.splitext(cur_file_name)[0]
        tmp_split               = cur_file_name.split("_")

        self.result_type        = tmp_split[1].strip() + "_" + tmp_split[2].strip()
        self.n_threads          = float(tmp_split[4].strip()[:-1])
        self.task_granularity   = float(tmp_split[3].strip())
        self.n_repetition       = float(tmp_split[5].strip())

        with open(file_path) as file:
            # first get number of ranks
            for line in file:
                if "_num_overall_ranks" in line:
                    tmp_split = line.split("\t")
                    self.n_ranks = float(tmp_split[-1].strip())
                    break

            last_rank = int(self.n_ranks - 1)
            file.seek(0)
            
            # now parse rest
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
                if "Stats R#0" in line:
                    tmp_split = line.split("\t")
                    if "_throughput_send_count" in tmp_split[1]:
                        tmp_sends_happened = float(tmp_split[-1].strip())
                        if tmp_sends_happened > 0:
                            self.sends_happened = True
                    elif "_throughput_send_min" in tmp_split[1]:
                        if self.sends_happened:
                            self.throughput_send_min = float(tmp_split[-1].strip())
                        else:
                            self.throughput_send_min = float('nan')
                    elif "_throughput_send_max" in line:
                        self.throughput_send_max = float(tmp_split[-1].strip())
                    elif "_throughput_send_avg" in line:
                        self.throughput_send_avg = float(tmp_split[-1].strip())
                    elif "_bytes_send_per_message_min" in line:
                        if self.sends_happened:
                            self.bytes_send_per_msg_min = float(tmp_split[-1].strip())
                        else:
                            self.bytes_send_per_msg_min = float('nan')
                    elif "_bytes_send_per_message_max" in line:
                        self.bytes_send_per_msg_max = float(tmp_split[-1].strip())
                    elif "_bytes_send_per_message_avg" in line:
                        self.bytes_send_per_msg_avg = float(tmp_split[-1].strip())
                if "Stats R#" + str(last_rank) in line:
                    tmp_split = line.split("\t")
                    if "_throughput_recv_count" in tmp_split[1]:
                        tmp_recvs_happened = float(tmp_split[-1].strip())
                        if tmp_recvs_happened > 0:
                            self.recvs_happened = True
                    elif "_throughput_recv_min" in tmp_split[1]:
                        if self.recvs_happened:
                            self.throughput_recv_min = float(tmp_split[-1].strip())
                        else:
                            self.throughput_recv_min = float('nan')
                    elif "_throughput_recv_max" in line:
                        self.throughput_recv_max = float(tmp_split[-1].strip())
                    elif "_throughput_recv_avg" in line:
                        self.throughput_recv_avg = float(tmp_split[-1].strip())
                    elif "_bytes_recv_per_message_min" in line:
                        if self.recvs_happened:
                            self.bytes_recv_per_msg_min = float(tmp_split[-1].strip())
                        else:
                            self.bytes_recv_per_msg_min = float('nan')
                    elif "_bytes_recv_per_message_max" in line:
                        self.bytes_recv_per_msg_max = float(tmp_split[-1].strip())
                    elif "_bytes_recv_per_message_avg" in line:
                        self.bytes_recv_per_msg_avg = float(tmp_split[-1].strip())

        self.speedup = self.time_openmp_only / self.time_chameleon