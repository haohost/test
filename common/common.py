#!/home/l00452746/python3
# created by luhao
# usage: common
# date : Feb-06
# ----------------

import os
import sys
import glob
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)


def check_path_exists(file_or_path, rebuild=0):
    if not os.path.exists(file_or_path):
        if not rebuild:
            print('ERROR: {} not exists\n'.format(file_or_path))
            sys.exit(-1)
        else:
            os.mkdir(file_or_path)


def dump_vios(df_result, result_file):
    if os.path.exists(result_file):
        df_all = pd.read_csv(result_file, index_col=False)
        df_all = df_all.append(df_result)
        df_all = df_all.drop_duplicates('inst')
        df_all.to_csv(result_file, index=False)
    else:
        df_result.to_csv(result_file, index=False)
    pass


def devide_vios(inst_list, df_vios):
    result_dict = {}
    for inst in inst_list:
        df_tmp = df_vios[df_vios.inst.str.contains(inst)]
        df_vios = df_vios[~df_vios.inst.str.contains(inst)]
        df_tmp.inst = df_tmp.inst.str.replace(inst, '')
        if df_tmp.empty:
            continue
        result_dict[inst] = df_tmp
    return result_dict


def devide_vios_other(inst_list, df_vios):
    result_dict = {}
    for inst in inst_list:
        df_tmp = df_vios[df_vios.inst.str.contains(inst)]
        df_vios = df_vios[~df_vios.inst.str.contains(inst)]
        df_tmp.inst = df_tmp.inst.str.replace(inst, '')
        if df_tmp.empty:
            continue
        result_dict[inst] = df_tmp
    return result_dict


def get_summary(df_block, result_dict, result_path, sim_type):
    vio_type = 'MaxRes' if 'res' in sim_type else 'MaxIR'
    summary_dict = {cell: {vio_type: 0, 'VioCount': 0} for cell in df_block.cell}
    for inst, df_result in result_dict.items():
        cell = df_block.loc[inst].cell
        summary_dict[cell][vio_type] = max(df_result[sim_type].max(), summary_dict[cell][vio_type])
        summary_dict[cell]['VioCount'] = sum(df_result[sim_type].shape[0], summary_dict[cell]['VioCount'])
        result_file = '{}/{}.rpt'.format(result_path, df_block.loc[inst].cell)
        dump_vios(df_result['inst', sim_type], result_file)
    return summary_dict


def get_summary_other(df_block, result_dict, result_path):
    summary_dict = {cell: {'VioCount': 0} for cell in df_block.cell}
    for inst, df_result in result_dict.items():
        cell = df_block.loc[inst].cell
        summary_dict[cell]['VioCount'] = sum(df_result.shape[0], summary_dict[cell]['VioCount'])
        result_file = '{}/{}.rpt'.format(result_path, df_block.loc[inst].cell)
        dump_vios(df_result['inst'], result_file)
    return summary_dict


def get_other_vios(result_dict, df_block, other_threshold_dict, check_type):
    '''
    1. get vios by using other threasold
    '''

    for cell, new_threshold in other_threshold_dict.items():
        insts_list = list(df_block[df_block.cell == cell].index)
        for inst in insts_list:
            result_dict[inst] = result_dict[inst][check_type] > new_threshold
    return result_dict


def check_short(sim_path):
    ## complex, and dont consider now, consider calibre method
    rpt_file = os.path.join(sim_path, 'shorts.rpt')
    check_path_exists(rpt_file)
    pass


def check_open(sim_path, df_block, inst_list, result_path):
    rpt_file = glob.glob('{}/adsRpt/*PinInst.unconnect'.format(sim_path))
    check_path_exists(rpt_file[0])
    rpt_file_logic = glob.glob('{}/adsRpt/*PinInst.unconnect_logic'.format(sim_path))
    check_path_exists(rpt_file_logic[0])
    df_rpt = pd.read_table(rpt_file[0], names=['inst', 'pg', '-'], sep='\s+', header=None, index_col=False, comment='#')
    if df_rpt.empty:
        logging.info('no open')

    result_dict = devide_vios(inst_list, df_rpt)
    ## get summary and dump result vios
    summary_dict = get_summary_other(df_block, result_dict, result_path)
    return 0


def check_grid_check(sim_path, df_block, inst_list, threshold, other_threshold_dict, result_path):
    rpt_file = '{}/adsRpt/apache.grid_check'.format(sim_path)
    check_path_exists(rpt_file)
    with open(rpt_file, 'r') as fd:
        for line in fd.read():
            if 'TOTAL res' in line:
                max_res = line.strip().split()[-1]
                break
    if max_res < threshold:
        logging.info('all grid check pass!!!')
        return 1

    df_rpt = pd.read_table(rpt_file, names=['inst', 'res', '-'], sep='\s+', header=None, index_col=False)
    df_rpt.res = df_rpt.res * max_res
    ## get vios
    df_vios = df_rpt[df_rpt.res > threshold]
    ## devide vios
    result_dict = devide_vios(inst_list, df_vios)
    ## dump result vios
    ## get summary and dump result vios
    summary_dict = get_summary(df_block, result_dict, result_path)
    return 0


def check_static(sim_path):
    pass


def check_cpa_static(sim_path):
    pass


def check_dynamic(sim_path, df_block, inst_list, threshold, other_threshold_dict, result_path, check_type, voltage):
    dvd_file = glob.glob('{}/*.dvd'.format(sim_path))
    df_dvd = pd.read_table(dvd_file[0], names=['-' * 2] + ['maxtw', 'avgtw', 'mintw', 'minwc', 'inst', '-'],
                           sep='\s+', header=None, index_col=False, comment='#')
    df_dvd = df_dvd[[check_type, 'inst']]
    df_vios = df_dvd[df_dvd[check_type] > threshold]
    result_dict = devide_vios(inst_list, df_vios)
    if not other_threshold_dict:
        result_dict = get_other_vios(result_dict, df_block, other_threshold_dict, check_type)
    summary_dict = get_summary(df_block, result_dict, result_path)
    return summary_dict
