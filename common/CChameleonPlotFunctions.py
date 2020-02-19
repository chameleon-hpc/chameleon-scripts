import os, sys
import numpy as np
import statistics as st
import matplotlib.pyplot as plt

F_SIZE = 16
plt.rc('font', size=F_SIZE)             # controls default text sizes
plt.rc('axes', titlesize=F_SIZE)        # fontsize of the axes title
plt.rc('axes', labelsize=F_SIZE)        # fontsize of the x and y labels
plt.rc('xtick', labelsize=F_SIZE)       # fontsize of the tick labels
plt.rc('ytick', labelsize=F_SIZE)       # fontsize of the tick labels
plt.rc('legend', fontsize=F_SIZE)       # legend fontsize
plt.rc('figure', titlesize=F_SIZE)      # fontsize of the figure title

def plot_data_normal(   target_file_path, 
                        arr_x_axis, 
                        arr_labels,             # nx1 array of labels
                        arr_arr_data,           # nx1 array of arrays of data 
                        text_title,
                        text_x_axis,
                        text_y_axis,
                        enforced_y_limit=None,
                        save_fig=True):

    xtick = list(range(len(arr_x_axis)))
    tmp_colors = ['darkorange', 'green', 'red']
    fig = plt.figure(figsize=(16, 9),frameon=False)
    ax = fig.gca()
    # plot data for labels
    for idx_type in range(len(arr_labels)):
        ax.plot(xtick, np.array(arr_arr_data[idx_type]), 'x-', linewidth=2, color=tmp_colors[idx_type])
    plt.xticks(xtick, arr_x_axis)
    ax.minorticks_on()
    ax.legend(arr_labels, fancybox=True, shadow=False)
    ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
    ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
    ax.set_xlabel(text_x_axis)
    ax.set_ylabel(text_y_axis)
    ax.set_title(text_title)
    if enforced_y_limit is not None:
        ax.set_ylim(bottom=enforced_y_limit)

    if save_fig:
        fig.savefig(target_file_path, dpi=None, facecolor='w', edgecolor='w', 
            format="png", transparent=False, bbox_inches='tight', pad_inches=0, metadata=None)
        plt.close(fig)
    return fig

def plot_data_min_max_avg(  target_file_path, 
                            arr_x_axis, 
                            arr_labels,         # nx1 array of labels
                            arr_min,            # nx1 array of arrays of data
                            arr_max,            # nx1 array of arrays of data
                            arr_avg,            # nx1 array of arrays of data
                            text_header, 
                            text_x_axis, 
                            text_y_axis, 
                            plot_per_label=False, 
                            divisor=None):

    xtick = list(range(len(arr_x_axis)))
    if divisor is not None:
        for idx_type in range(len(arr_labels)):
            arr_min[idx_type] = [x/divisor for x in arr_min[idx_type]]
            arr_max[idx_type] = [x/divisor for x in arr_max[idx_type]]
            arr_avg[idx_type] = [x/divisor for x in arr_avg[idx_type]]

    tmp_colors = ['darkorange', 'green', 'red']
    # ========== MinMaxAvg Plot
    if plot_per_label:
        for idx_type in range(len(arr_labels)):
            path_result_img = target_file_path + "_" + arr_labels[idx_type] + ".png"
            fig = plt.figure(figsize=(16, 9),frameon=False)
            ax = fig.gca()
            labels = []
            cur_line = ax.plot(xtick, np.array(arr_min[idx_type]), ':', linewidth=2, color=tmp_colors[idx_type])
            cur_color = cur_line[0].get_color()
            labels.append(arr_labels[idx_type] + "_min")
            cur_line = ax.plot(xtick, np.array(arr_max[idx_type]), '--', linewidth=2)
            cur_line[0].set_color(cur_color)
            labels.append(arr_labels[idx_type] + "_max")
            cur_line = ax.plot(xtick, np.array(arr_avg[idx_type]), '-', linewidth=2)
            cur_line[0].set_color(cur_color)
            labels.append(arr_labels[idx_type] + "_avg")
        
            plt.xticks(xtick, arr_x_axis)
            ax.minorticks_on()
            ax.legend(labels, fancybox=True, shadow=False)                
            ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
            ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
            ax.set_xlabel(text_x_axis)
            ax.set_ylabel(text_y_axis)
            ax.set_title(text_header + " (" + arr_labels[idx_type] + ")")
            fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
                format="png", transparent=False, bbox_inches='tight', pad_inches=0,
                frameon=False, metadata=None)
            plt.close(fig) 
    else:
        path_result_img = target_file_path + ".png"
        fig = plt.figure(figsize=(16, 9),frameon=False)
        ax = fig.gca()
        labels = []
        # now versions
        for idx_type in range(len(arr_labels)):
            cur_line = ax.plot(xtick, np.array(arr_min[idx_type]), ':', linewidth=2, color=tmp_colors[idx_type])
            cur_color = cur_line[0].get_color()
            labels.append(arr_labels[idx_type] + "_min")
            cur_line = ax.plot(xtick, np.array(arr_max[idx_type]), '--', linewidth=2)
            cur_line[0].set_color(cur_color)
            labels.append(arr_labels[idx_type] + "_max")
            cur_line = ax.plot(xtick, np.array(arr_avg[idx_type]), '-', linewidth=2)
            cur_line[0].set_color(cur_color)
            labels.append(arr_labels[idx_type] + "_avg")
        plt.xticks(xtick, arr_x_axis)
        ax.minorticks_on()
        ax.legend(labels, fancybox=True, shadow=False)                
        ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
        ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
        ax.set_xlabel(text_x_axis)
        ax.set_ylabel(text_y_axis)
        ax.set_title(text_header)
        fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
            format="png", transparent=False, bbox_inches='tight', pad_inches=0,
            frameon=False, metadata=None)
        plt.close(fig)