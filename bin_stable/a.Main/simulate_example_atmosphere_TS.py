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
This is an example simulation for beginner users to try out the code
"""

import os
import sys

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '../..'))

import SEAS_Main.simulation.transmission_spectra_simulator as theory
import SEAS_Main.simulation.observed_spectra_simulator as observe
import SEAS_Main.simulation.spectra_analyzer as analyze

import SEAS_Utils.common_utils.configurable as config
import SEAS_Utils.common_utils.data_plotter as plt

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
ml = MultipleLocator(10)


if __name__ == "__main__":
    
    user_input = config.Configuration("user_input_dev.cfg")
    
    user_input["Simulation_Control"]["DB_DIR"]              = "Example"
    user_input["Simulation_Control"]["DB_Name"]             = "cross_sec_Example.db"
    user_input["Simulation_Control"]["TP_Profile_Name"]     = "isothermal_300K.txt"
    user_input["Simulation_Control"]["Mixing_Ratio_Name"]   = "H2O_only.txt"


    user_input["Save"]["Intermediate_Data"]["cross_section_savename"] = "Temp_H2O_Cross_Section.npy"

    simulation = theory.TS_Simulator(user_input)
    observer = observe.OS_Simulator(user_input)
    analyzer = analyze.Spectra_Analyzer(user_input)
    
    Raw_nu, Raw_TS = simulation.simulate_example()
    
    nu, Trans = observer.calculate_convolve(Raw_nu, Raw_TS)
    
    
    
    plt.plot(10000./Raw_nu,Raw_TS)
    plt.plot(10000./nu,Trans)
    plt.show()
    
    