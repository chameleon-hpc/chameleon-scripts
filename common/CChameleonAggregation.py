from enum import Enum
import statistics as st

class EnumAggregationMetric(Enum):
    AVG = 0
    SUM = 1
    COUNT = 2

class EnumAggregationTypeRun(Enum):
    MIN = 0
    MAX = 1
    AVG = 2
    SUM = 3
    ALL = 4

class EnumAggregationTypeGroup(Enum):
    MIN = 0
    MAX = 1
    AVG = 2
    SUM = 3
    ALL = 4

def aggregate_chameleon_statistics( stats_objects_group,                                    # CChameleonStatsPerRun objects
                                    signal_list,                                            # signals to be aggregated (see object fields)
                                    aggregation_metric=EnumAggregationMetric.AVG,           # accecssing the count, sum or avg metric inside statistics (if there is only one, both are the same)
                                    aggregation_for_run=EnumAggregationTypeRun.AVG,         # aggregation between ranks in single run
                                    aggegration_for_group=EnumAggregationTypeGroup.AVG,     # aggregation between different runs in same group (e.g. multiple runs with same setup)
                                    default_vals_run=None,
                                    default_vals_group=None):
    # init field that will be returned
    return_data = []

    for idx_sig in range(len(signal_list)):
        s = signal_list[idx_sig]
        data_group = []

        for stat in stats_objects_group:            
            # === 1 Apply aggregation on run basis stats obj; some per run metrics dont need that
            if s == "execution_time":
                data_group.append(stat.execution_time)
                continue
            
            tmp_field_name = "data_avg"
            if aggregation_metric == EnumAggregationMetric.COUNT:
                tmp_field_name = "data_count"
            elif aggregation_metric == EnumAggregationMetric.SUM:
                tmp_field_name = "data_sum"
            
            try:
                # get data from ranks
                cur_data = eval("[x." + s + "." + tmp_field_name + " for x in stat.stats_per_rank]")
            except:
                try: 
                    # fallback if custom signal added to structure
                    cur_data = [eval("stat." + s )]
                except:
                    # fallback None
                    if default_vals_run is not None:
                        cur_data = default_vals_run[idx_sig]
                    else:
                        cur_data = None

            if cur_data is not None:
                if aggregation_for_run == EnumAggregationTypeRun.ALL:
                    data_group.extend(cur_data)
                elif aggregation_for_run == EnumAggregationTypeRun.AVG:
                    if len(cur_data) == 1:
                        data_group.append(cur_data[0])
                    else:
                        data_group.append(st.mean(cur_data))
                elif aggregation_for_run == EnumAggregationTypeRun.SUM:
                    data_group.append(sum(cur_data))
                elif aggregation_for_run == EnumAggregationTypeRun.MIN:
                    data_group.append(min(cur_data))
                elif aggregation_for_run == EnumAggregationTypeRun.MAX:
                    data_group.append(max(cur_data))

        # === 2 Apply aggregation on group basis; some per run metrics dont need that
        if len(data_group) == 0:
            if default_vals_group is not None:
                data_group = default_vals_group[idx_sig]
            else:
                data_group = None

        if data_group is None:
            return_data.append([])
            continue
        
        if not isinstance(data_group, list):
            data_group = [data_group]

        if aggegration_for_group == EnumAggregationTypeGroup.ALL:
            return_data.append(data_group)
        elif aggegration_for_group == EnumAggregationTypeGroup.AVG:
            if len(data_group) == 1:
                return_data.append(data_group[0])
            else:
                return_data.append(st.mean(data_group))
        elif aggegration_for_group == EnumAggregationTypeGroup.SUM:
            return_data.append(sum(data_group))
        elif aggegration_for_group == EnumAggregationTypeGroup.MIN:
            return_data.append(min(data_group))
        elif aggegration_for_group == EnumAggregationTypeGroup.MAX:
            return_data.append(max(data_group))
    
    return return_data