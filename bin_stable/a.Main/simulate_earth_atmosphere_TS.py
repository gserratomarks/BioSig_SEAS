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

Generate a List of atmospheres and calculate their windows.

Hash is first introduced here for temporary file saving

"""
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
ml = MultipleLocator(10)

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '../..'))

import SEAS_Main.simulation.transmission_spectra_simulator as theory
import SEAS_Main.simulation.observed_spectra_simulator as observe
import SEAS_Main.simulation.spectra_analyzer as analyze

from SEAS_Utils.common_utils.timer import simple_timer
from SEAS_Utils.common_utils.DIRs import Mixing_Ratio_Data, TP_Profile_Data
import SEAS_Utils.common_utils.configurable as config





if __name__ == "__main__":
    
    
    Timer = simple_timer()
    
    user_input = config.Configuration("../../bin_stable/a.Main/user_input_dev.cfg")
    
    Filename = "Test_Earth"
    
    user_input["Simulation_Control"]["DB_DIR"]              = "Simulation_Band"
    user_input["Simulation_Control"]["DB_Name"]             = None#"cross_sec_Example.db"
    user_input["Simulation_Control"]["TP_Profile_Name"]     = "earth.txt"
    user_input["Simulation_Control"]["Mixing_Ratio_Name"]   = "earth.txt"

    user_input["Save"]["Intermediate_Data"]["cross_section_savename"] = "%s_Cross_Section.npy"%Filename
    user_input["Save"]["Window"]["path"] = "../../output/Simple_Atmosphere_Window"
    user_input["Save"]["Window"]["name"] = "%s_Window_A1000_S100.txt"%Filename
    
    user_input["Save"]["Plot"] = {}
    user_input["Save"]["Plot"]["path"] = "../../output/Plot_Result"
    user_input["Save"]["Plot"]["name"] = "%s_Plot.png"%Filename
    
    simulation = theory.TS_Simulator(user_input)
    observer = observe.OS_Simulator(user_input)
    
    Raw_nu, Raw_TS = simulation.simulate_example()
    
    nu, Trans = observer.calculate_convolve(Raw_nu, Raw_TS)
    
    plt.plot(10000./Raw_nu,Raw_TS)
    plt.plot(10000./nu,Trans)
    plt.show()
    
    
    