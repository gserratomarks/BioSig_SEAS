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
Loads biosignature molecules from NIST, etc.

"""

import os
import sys
import numpy as np
from scipy import interpolate

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '../..'))

from SEAS_Utils.common_utils.DIRs import molecule_info, NIST_Spectra
import SEAS_Utils.common_utils.db_management2 as dbm
import SEAS_Utils.common_utils.jdx_Reader as jdx


def load_NIST_spectra(molecule,return_param,is_smile=False):

    kwargs = {"dir":molecule_info,
              "db_name":"molecule_db.db",
              "user":"azariven",
              "DEBUG":False,"REMOVE":False,"BACKUP":False,"OVERWRITE":False}
    
    cross_db = dbm.database(**kwargs)   
    cross_db.access_db()   

    if is_smile:
        cmd = "SELECT inchikey From ID WHERE Smiles='%s'"%molecule
    else:
        cmd = "SELECT inchikey From ID WHERE Formula='%s'"%molecule
    
    result = cross_db.c.execute(cmd)
    
    try:
        fetch = result.fetchall()[0][0]
    except:
        print "Molecule %s Doesn't Exist in NIST Database"%molecule
        sys.exit()
    
    path = os.path.join(NIST_Spectra,fetch)
    
    filename = ""
    for j in os.listdir(path):
        if "jdx" in j:
            filename = os.path.join(path,j)
            break
    
    data = jdx.JdxFile(filename)    
   
    
    if return_param[0] == "wl":
        x = data.wl()
    elif return_param[0] == "wn":
        x = data.wn()
        
    if return_param[1] == "T":
        y = data.trans()
    elif return_param[1] == "A":
        y = data.absorb()


    return x,y

def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or np.fabs(value - array[idx-1]) < np.fabs(value - array[idx])):
        return idx-1#array[idx-1]
    else:
        return idx#array[idx]

def biosig_interpolate(x1,y1,x2, Type):

    x1min = min(x1)
    x1max = max(x1)
    x2min = min(x2)
    x2max = max(x2)


    f = interpolate.interp1d(x1, y1)
    
    if x1min > x2min and x1max < x2max:
        #print "A"
        
        left = find_nearest(x2,min(x1))+1
        right = find_nearest(x2,max(x1))
    
        if Type == "A" or Type == "C":
            yinterp_left = np.zeros(left)
            yinterp_right = np.zeros(len(x2)-right)
        elif Type == "T":
            yinterp_left = np.ones(left)
            yinterp_right = np.ones(len(x2)-right)
        yinterp_middle = f(x2[left:right])
        yinterp = np.concatenate([yinterp_left,yinterp_middle, yinterp_right])

    elif x1min <= x2min and x1max < x2max:
        #print "B"
        right = find_nearest(x2,max(x1))
        
        if Type == "A" or Type == "C":
            yinterp_right = np.zeros(len(x2)-right)
        elif Type == "T":
            yinterp_right = np.ones(len(x2)-right)
        yinterp_middle = f(x2[:right])
        yinterp = np.concatenate([yinterp_middle, yinterp_right])
    
    elif x1min > x2min and x1max >= x2max:
        #print "C"
        left = find_nearest(x2,min(x1))+1
    
        if Type == "A" or Type == "C":
            yinterp_left = np.zeros(left)
        elif Type == "T":
            yinterp_left = np.ones(left)
        yinterp_middle = f(x2[left:])
        
        yinterp = np.concatenate([yinterp_left,yinterp_middle])
    
    else:
        #print "D"
        yinterp = f(x2)

    
    
    return yinterp











