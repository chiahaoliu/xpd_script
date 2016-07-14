#====================================================
# Author: Chia-Hao Liu, S. Ghose
# Date written: 07-14-2016
# Function: Get metadata info from Database 
#			Use headers from events and fields to extrcat data
#			For example: rga_mass1
#			Save to a file and plot them on screen
#====================================================


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

h = db[-5:]
evs = get_events(h)
field = ['time', 'gas', 'temperature','rga_mass1', 'rga_mass2','rga_mass3']
col_num = len(field)
full_list = []
for ev in evs:
    for el in field:
        try:
            full_list.append(ev['data'].get(el))
        except:
            full_list.append('N/A')
md_array = np.reshape(full_list, (len(full_list)/col_num, col_num))
md_df = pd.DataFrame(md_array, columns=field)
md_df.to_csv('med_md.csv', index=False)


# Plot temperature vs rga_mass1
"""
fig = plt.figure()
plt.plot(md_array[2,:],D[:,3],'o-')
xlabel('temperature')
ylabel('rga_mass1')
plt.show()
"""
