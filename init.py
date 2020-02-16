#!/home/l00452746/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:52:29 2020

@author: Hao
"""

import os
import sys
import glob


class InitDesign:
    __version__ = 'v1.0'

    def __init__(self, current_path, conf_file):
        self.sim_pros = ['grid_check', 'static', 'cpa_static', 'dynamic', 'cpa_dynamic', 'vcd', 'cpa_vcd']
        self.threshold = {'grid_check': 500, 'static': 0.03,
                          'cpa_static': 0.04, 'dynamic': 0.1,
                          'cpa_dynamic': 0.1, 'vcd': 0.1,
                          'cpa_vcd': 0.1}
        self.design = 'design'
        self.current_path = current_path
        self.conf_file = conf_file

    def mkcon(self):
        # cwd = os.getcwd().replace('/run','')
        cwd = self.current_path.replace('/run', '')

        sim_paths = glob.glob('{}/{}/rh_db/*'.format(cwd, self.design))
        self.sim_path_dict = {sim_pro: sim_path
                              for sim_pro in self.sim_pros
                              for sim_path in sim_paths
                              if sim_pro in sim_path}
        self.sim_path_dict = {}
        for sim_pro in self.sim_pros:
            for sim_path in sim_paths:
                if sim_pro in sim_path:
                    self.sim_path_dict[sim_pro] = sim_path
            if not self.sim_path_dict.get(sim_pro, 0):
                self.sim_path_dict[sim_pro] = '{}/{}/rh_db/{}.mlg'.format(cwd, self.design, sim_pro)

        # conf_file = '{}/conf.ini'.format(os.getcwd())

        with open(self.conf_file, 'w') as fd:
            for sim_pro in self.sim_pros:
                fd.write('[{}]\n'.format(sim_pro))
                fd.write('path = {}\n'.format(self.sim_path_dict[sim_pro]))
                fd.write('threshold = {}\n'.format(self.threshold[sim_pro]))
                fd.write('other_threshold_dict = {}\n')


if __name__ == '__main__':
    design = InitDesign()
    design.mkcon()

# def init_design():
#    '''
#    init design
#    '''
#    sim_pros = ['grid_check','static','cpa_static','dynamic','cpa_dynamic','vcd','cpa_vcd']
#    cwd = os.getcwd().replace('/run','')
#    
#    sim_paths = glob.glob('{}/*/rh_db/*'.format(cwd))
#    sim_path_dict = {sim_pro:sim_path 
#                     for sim_pro in sim_pros 
#                     for sim_path in sim_paths 
#                     if sim_pro in sim_path}
