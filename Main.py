#!/home/l00452746/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:52:29 2020

@author: Hao
"""

import os
import sys
import subprocess as sub
import argparse
import logging
import configparser
import time
import numpy as np
import pandas as pd
sys.path.append('/home/hao/Desktop/test/common/')
from init import InitDesign
from common import common as cm
# from common import check_short
# from common import check_short


def log_func(func):
    def wrap_func(self):
        print('test {}'.format(func.__name__))
        return func(self)

    return wrap_func


class Pi_Analysis:

    def __init__(self):
        self.design = 'design'
        # self.currebt_path = os.getcwd()
        self.currebt_path = '/home/hao/Desktop/test/test/60.redhawk/run'
        self.voltage = 0.825

        self.time = time.strftime('%m%d-%H%M',time.localtime())
        self.result_path = '/home/hao/Desktop/test/test/60.redhawk/rpt/{}'.format(self.time)
        cm.check_path_exists(self.result_path, rebuild=1)


        block_file = os.path.join(self.currebt_path.replace('/run',''),'scr/block.info')
        self.df_block = pd.read_table(block_file,names = ['inst','cell','-'], sep = '\s+',header=None,index_col = False)
        self.inst_list =sorted(list(self.df_block.inst), key= lambda ii: len(ii.split('/')),reverse=True)
        self.df_block = self.df_block.set_index(['inst'])
        self.conf_file = '/home/hao/Desktop/test/test/60.redhawk/run/conf.ini'
        self.check_type = { 'grid_check':['short','open','grid_check'],
                            'static': ['short', 'open', 'static'],
                            'cpa_static': ['cpa_static'],
                            'dynamic': ['dynamic'],
                            'cpa_dynamic':['cpa_dynamic'],
                            'vcd': ['vcd'],
                            'cpa_vcd':['cpa_vcd'],
                           }

        pass

    @log_func
    def _init_conf(self):
        '''
        init conf file with
        '''
        init_process = InitDesign(self.currebt_path, self.conf_file)
        init_process.mkcon()


    @log_func
    def _read_conf(self):
        cm.check_path_exists(self.conf_file)
        self.conf = configparser.ConfigParser()
        self.conf.read(self.conf_file)
        pass
    @log_func
    def _back_data(self,process):
        pass
    @log_func
    def _check_short(self,process):
        cm.check_short()
        pass
    @log_func
    def _check_open(self,process):
        sim_path = self.conf.get(process,'sim_path')
        cm.check_open(sim_path)
        pass

    @log_func
    def _check_grid_check(self, process):
        sim_path = self.conf.get(process, 'sim_path')
        threshold = self.conf.get(process, 'threshold')
        other_threshold_dict = self.conf.get(process, 'other_threshold_dict')
        result_path = '{}/grid_check'.format(self.result_path)
        cm.check_path_exists(result_path,rebuild=1)
        cm.check_grid_check(sim_path,self.df_block, self.inst_list ,threshold,other_threshold_dict)
        pass

    @log_func
    def _check_static(self,process):
        sim_path = self.conf.get(process, 'sim_path')
        cm.check_static(sim_path)
        pass

    @log_func
    def _check_cpa_static(self,process):
        sim_path = self.conf.get(process, 'sim_path')
        pass

    @log_func
    def _check_dynamic(self,process):
        sim_path = self.conf.get(process, 'sim_path')
        pass

    @log_func
    def _check_cpa_dynamic(self,process):
        sim_path = self.conf.get(process, 'sim_path')
        pass

    @log_func
    def _check_vcd(self,process):
        sim_path = self.conf.get(process, 'sim_path')
        pass

    @log_func
    def _check_cpa_vcd(self,process):
        sim_path = self.conf.get(process, 'sim_path')
        pass

    @log_func
    def _check_main(self,process):
        self._back_data(process)
        for check_type in self.check_type[process]:
            if 'short' in check_type:
                self._check_short(process)
            elif 'open' in check_type:
                self._check_open(process)
            elif 'grid' in check_type:
                self._check_grid_check(process)
            elif 'static' in check_type:
                self._check_static(process)
            elif 'cpa_static' in check_type:
                self._check_cpa_static(process)
            elif 'dynamic' in check_type:
                self._check_dynamic(process)
            elif 'cpa_dynamic' in check_type:
                self._check_cpa_dynamic(process)
            elif 'vcd' in check_type:
                self._check_vcd(process)
            elif 'cpa_vcd' in check_type:
                self._check_cpa_vcd(process)
        pass


if __name__ == '__main__':
    debug = 1
    def my_opt():
        args = argparse.ArgumentParser(description='help')
        args.add_argument('--process', type=str, help='input check process')
        my_opts = args.parse_args()
        return my_opts
    if not debug:
        if len(sys.argv) < 2:
            args_opts = my_opt()
            args_opts.help()
            sys.exit(-1)
        args_opts = my_opt()

        if args_opts.process is not None:
            PI_ANALYSIS = Pi_Analysis()
            PI_ANALYSIS._check_main(args_opts.process)

    if debug:
        PI_ANALYSIS = Pi_Analysis()
        PI_ANALYSIS._init_conf()
        PI_ANALYSIS._read_conf()







