class CUtilProcessing:
    @staticmethod
    def parse_power_measurement(file_path, cur_stats):
        power_file = file_path[:-4] + "_power.log"

        with open(power_file) as f:
            # get channel values
            cur_stats.consumption_wh_overall = 0.0
            cur_stats.consumption_wh_switches = 0.0

            for line in f:
                if "Channel 4" in line:
                    tmp_split = line.split(":")
                    cur_stats.consumption_wh_switches = float(tmp_split[-1].strip())
                    continue
                elif "Channel" in line:
                    tmp_split = line.split(":")
                    cur_stats.consumption_wh_overall += float(tmp_split[-1].strip())
                    continue

    @staticmethod
    def postprocess(cur_stats):
        cur_stats.consumption_perc_switches = cur_stats.consumption_wh_switches / cur_stats.consumption_wh_overall * 100.0
        cur_stats.power_draw_overall        = cur_stats.consumption_wh_overall / (cur_stats.execution_time / 3600)
        cur_stats.power_draw_switches       = cur_stats.consumption_wh_switches / (cur_stats.execution_time / 3600)
