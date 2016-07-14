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

h = db[-5:]
evs = get_events(h)
field = ['time', 'gas', 'temperature','rga_mass1', 'rga_mass2','rga_mass3']
col_num = len(field)
full_list = []
for ev in evs:
    row_list = []
    for el in field:
        try:
            row_list.append(ev['data'].get(el))
        except:
            row_list.append(None)
    full_list.append(rga_mass_list)
md_array = np.reshape(full_list, (len(full_list)/col_num, col_num))
md_df = pd.DataFrame(md_array, field)
md_df.to_csv('med_md.csv', index=False)


#DataOut = c_[Time,Temperature]
#np.savetxt("/home/xf28id1/xpdUser/tiff_base/T_profile.DAT", DataOut)


# Plot the T vs Time
#D = np.loadtxt("/home/xf28id1/xpdUser/tiff_base/T_profile.DAT")
#plot(D[:,0],D[:,1],'o-')
#xlabel('Time')
#ylabel('Temperature')
#show()


