#!/usr/bin/env python
#
# Copyright (C) 2017 - Massachusetts Institute of Technology (MIT)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This code test the generation of mixing_ratios

need a better system for reading in what molecules we should generate.
"""

import os
import sys

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '../..'))

import SEAS_Aux.atmosphere_processes.mixing_ratio_generator as mix
import SEAS_Utils.common_utils.configurable as config

def generate_water():

    ratio_input = config.Configuration("water_only_selection.cfg")
    simulator = mix.mixing_ratio_generator(ratio_input,filler=False,name="selection/water_only2.txt")
    simulator.generate()
    simulator.save()

if __name__ == "__main__":
    
    ratio_input = config.Configuration("selection/h2_only_selection.cfg")

    simulator = mix.mixing_ratio_generator(ratio_input,
                                           filler=True,
                                           filler_molecule="He",
                                           pressures = [100000.0, 36800.0, 13500.0, 4980.0, 1830.0, 674.0, 248.0, 91.2, 33.5, 12.3, 4.54, 1.67, 0.614, 0.226, 0.0832, 0.0306, 0.0113, 0.00414, 0.00152, 0.00056, 0.000206, 7.58e-05, 2.79e-05, 1.03e-05],
                                           name="H2&He.txt",
                                           overwrite=True)
    simulator.generate()
    simulator.save()
    
    
    
    
    
    
    
    
    
    
    
    