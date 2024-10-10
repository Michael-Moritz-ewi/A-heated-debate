# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:34:48 2023

@author: Michael Moritz

Python 3.11.5
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#---------------Description------------------------
# This code calculates the investment costs of heating systems consisting of 
# equipment costs, contribution amrgin and installation costs
# The investment costs of the heating systems are used as input 
# for the caclulation of the levelized cost of heating. 
# Note: In this version of the code we assume a cop of 3 for
# air-water and water-water heat pumps. In the paper, we used a cop depending 
# on the supply temperature and the heat pump type.  
#--------------------------------------------------

#---------------global settings------------------------
# Set the font size
plt.rcParams.update({'font.family': 'Trebuchet MS', 'font.size': 14})

#Set paramFunction to "min", "max" or "avg"
paramFunction ="avg"
#Set settlement type for system to "rural", "village", "urban" or "city"
system = "urban"

#------------Settlement type specififc input parameters------------
if system == "city":
    #heated area per household
    area_per_household = 92
    #heated area per heating central
    area_per_central = 1500 #originally 680, but 1500 fits to the capacity of the dhs from AGFW source
    #capcity district heating station [kW]
    cap_dhs = 75 
    #simultaneously factor district heating
    sf = 0.6
if system == "urban":
    #heated area per household
    area_per_household = 92
    #heated area per heating central
    area_per_central = 680
    #capcity district heating station [kW]
    cap_dhs = 34  
    #simultaneously factor district heating
    sf = 0.68
if system == "village":
    #heated area per household
    area_per_household = 130
    #heated area per heating central
    area_per_central = 130
    #capcity district heating station [kW]
    cap_dhs = 7   
    #simultaneously factor district heating
    sf = 0.78
if system == "rural":
    #heated area per household
    area_per_household = 130
    #heated area per heating central
    area_per_central = 130
    #capcity district heating station [kW]
    cap_dhs = 7   
    #simultaneously factor district heating
    sf = 0.74
    
#------------Equipment, installation and maintenance functions------------
#Equipment and installation cost functions have min and max values calculated by the function fitted to the data +- a scale factor multiplied by the root mean squared error between the fitted function and the data. The scale factor is necessary to prevent negative or very small values for the equipment costs.
scale = 0.33
#ATTENTION: atw and wtw inv cost functions set to zero as calculation happens in LCOH_calc.py depending on the supply temperature. If you want to include heat pump equipment costs in the system cost calculation in this file, delete "return(0)" in their cost functions
#investment cost air water heat pump [EUR], x = capacity [kW_el]
def Inv_awhp(x):    
    if paramFunction== "avg":
        return((7689*x**(0.69)))
    elif paramFunction== "max":
        return((7689*x**(0.69) + scale*5163))
    elif paramFunction== "min":
        return((7689*x**(0.69) - scale*5163))
#    return(0)  
    
#investment cost water water heat pump [EUR], x = capacity [kW_el]
def Inv_wwhp(x):    
    if paramFunction== "avg":
        return((8512*x**(0.58)))
    elif paramFunction== "max":
        return((8512*x**(0.58) + scale*5244))
    elif paramFunction== "min":
        return((8512*x**(0.58) - scale*5244))
     
            
#investment cost water water heat pump [EUR], x = capacity [kW_th]
def Inv_wwhp(x):    
    if paramFunction== "avg":
        return(3119*x**(0.61))
    elif paramFunction== "max":
        return(3119*x**(0.61) + scale*4190)
    elif paramFunction== "min":
        return(3119*x**(0.61) - scale*4190)
    return(0)
#investment cost air air heat pump (outdoor and indoor units) [EUR], x = capacity [kW_th]
def Inv_aahp(x):
    if paramFunction == "avg":
        return (854.64 * x)
    elif paramFunction == "max":
        return (854.64 * x + scale*2226.30)
    elif paramFunction == "min":
        return (854.64 * x - scale*2226.30)

#investment cost gas boiler [EUR], x = capacity [kW_th]
def Inv_gb(x):   
    if x<50:
        if paramFunction== "avg":
            return(124.76*x+3073.75)
        elif paramFunction== "max":
            return(124.76*x+3073.75 + scale*945.39)
        elif paramFunction== "min":
            return(124.76*x+3073.75 - scale*945.39)
    else:
        if paramFunction== "avg":
            return(75.42*x+8149.98)
        elif paramFunction== "max":
            return(75.42*x+8149.98 + scale*4973.58)
        elif paramFunction== "min":
            return(75.42*x+8149.98 - scale*4973.58)

        
#investment cost hydrogen boiler [EUR], x = capacity [kW_th], hydrogen boilers are 10% more expensive than gas boilers according to Viessmann & Vaillant   
def Inv_hb(x):   
    if x<50:
        if paramFunction== "avg":
            return((124.76*x+3073.75)*1.1)
        elif paramFunction== "max":
            return(((124.76*x+3073.75) + scale*945.39)*1.1)
        elif paramFunction== "min":
            return(((124.76*x+3073.75) - scale*945.39)*1.1)
    else:
        if paramFunction== "avg":
            return((75.42*x+8149.98)*1.1)
        elif paramFunction== "max":
            return((75.42*x+8149.98 + scale*4973.58)*1.1)
        elif paramFunction== "min":
            return((75.42*x+8149.98 - scale*4973.58)*1.1)
        
#investment cost electric boiler [EUR], x = capacity [kW_th]
def Inv_eb(x):
    if paramFunction == "avg":
        return (37.35 * x + 1831.27)
    elif paramFunction == "max":
        return (37.35 * x + 1831.27 + scale*343.77)
    elif paramFunction == "min":
        return (37.35 * x + 1831.27 - scale*343.77)

#investment cost electric instant water heater [EUR], x = capacity [kW_th]
def Inv_ihwh(x):
    if paramFunction == "avg":
        return (117.63 * x ** 0.44)
    elif paramFunction == "max":
        return (117.63 * x ** 0.44 + scale*51.58)
    elif paramFunction == "min":
        return (117.63 * x ** 0.44 - scale*51.58)

#investment cost buffer storage [EUR], x = storage volume [l]
def Inv_bs(x):
    if paramFunction == "avg":
        return (93.8 * x ** 0.50)
    elif paramFunction == "max":
        return (93.8 * x ** 0.50 + scale*348.75)
    elif paramFunction == "min":
        return (93.8 * x ** 0.50 - scale*348.75)

#investment cost hot water storage [EUR], x = storage volume [l]
def Inv_hws(x):
    if paramFunction == "avg":
        return (6.33 * x + 714.80)
    elif paramFunction == "max":
        return (6.33 * x + 714.80 + scale*542.39)
    elif paramFunction == "min":
        return (6.33 * x + 714.80 - scale*542.39)

#investment cost heating rod [EUR], x = capacity [kW_th]
def Inv_hr(x):
    if paramFunction == "avg":
        return (8.76 * x + 220.17)
    elif paramFunction == "max":
        return (8.76 * x + 220.17 + scale*32.11)
    elif paramFunction == "min":
        return (8.76 * x + 220.17 - scale*32.11)

#investment cost 15 kW district heating station [EUR]
def Inv_dhs(x): 
    if x<=15:
        y = 4000 #Mail FA PeWo
    else:
        y = 3087*x**(0.3219) #Blesl, Markus; Burkhardt, Alexander; Wendel, Frank (2023): Transformation und Rolle der Wärmenetze.​
    return(y)

#investment cost drilling and bore hole heat exchanger [EUR], x = capacity [kW_th]
def Inv_dbhe(x):  
    #1052*x Blum et al
    return(453.19*x+19011)#Dela

#installation cost heat pumps (small material included) [EUR], x = capacity [kW_th]
def Inst_hp(x):
    if paramFunction == "avg":
        return (3986*x**(0.68))
    elif paramFunction == "max":
        return (3986*x**(0.68) + scale*5865)
    elif paramFunction == "min":
        return (3986*x**(0.68) - scale*5865)

#installation cost gas boilers (small material included) [EUR], x = capacity [kW_th]
def Inst_gb(x):
    if paramFunction == "avg":
        return (1890.54 * x ** (0.62))
    elif paramFunction == "max":
        return (1890.54 * x ** (0.62) + scale*9192)
    elif paramFunction == "min":
        return (1890.54 * x ** (0.62) - scale*9192)

#installation cost district heating station with a capacity of 15 KW. 10% less than istallation cost of gas boilers sinceno  chimney system is necessary (small material and factor on large equiptment included) [EUR], x = capacity [kW_th]
def Inst_dhs(x):
    x=cap_dhs
    if paramFunction == "avg":
        return (1890.54 * x ** (0.62)*0.9)
    elif paramFunction == "max":
        return (1890.54 * x ** (0.62)*0.9 + scale*9192)
    elif paramFunction == "min":
        return (1890.54 * x ** (0.62)*0.9 - scale*9192)
    
#installation cost electric boiler. 20% less than istallation cost of gas boilers since no chimney system and gas piping is necessary (small material and factor on large equiptment included) [EUR], x = capacity [kW_th]
def Inst_eb(x):
    if paramFunction == "avg":
        return (1890.54 * x ** (0.62)*0.8)
    elif paramFunction == "max":
        return (1890.54 * x ** (0.62)*0.8 + scale*9192)
    elif paramFunction == "min":
        return (1890.54 * x ** (0.62)*0.8 - scale*9192)

#installation cost air air heat pump (Excluding Deckungsbeitrag) [EUR], x = capacity [kW_th] (Source: Expert Interview with Aircon-Technik Gesellschaft für Luft-, Klima- und Kälteanlagen mbH & Co. KG)   
def Inst_aahp(x):
    #Parameters
    t_inside = 0.5 #Person days per inside unit [d/unit]
    t_outside = 1  #Person days per outside unit [d/unit]
    t_line = 1/48 #Person days per meter of refrigeration line [d/m]
    P_inside = 2 #Average power of an inside unit [kW]
    P_outside_max = 85 #Largest otside unit available in manufacturers price lists (Bosch AF5300A 85-3)
    sc_branch = 200 #specific costs of refrigeration line branch[EUR 2023/branch]
    branches_per_unit = 1 #number of refrigeration line branches per inside unit [branch/inside_unit]
    sc_line = 20 #specific costs of refrigeration line canal [EUR 2023/m]
    swages = 600 #specific wages per person day [EUR 2023/d]
    if paramFunction == "avg":
        sl_line = 5 #specific average refrigeration line lenght per inside unit[m/inside_unit]    
        sc_cond = 100 #specific costs of condensate pump per inside unit [EUR 2023/inside_unit]
    elif paramFunction == "max":
        sl_line = 7.5 #specific average refrigeration line lenght per inside unit[m/inside_unit]    
        sc_cond = 200 #specific costs of condensate pump per inside unit [EUR 2023/inside_unit]
    elif paramFunction == "min":
        sl_line = 2.5 #specific average refrigeration line lenght per inside unit[m/inside_unit]    
        sc_cond = 0 #specific costs of condensate pump per inside unit [EUR 2023/inside_unit]
    #Calculations
    n_inside = x/P_inside #number of inside units
    n_outside = x/P_outside_max #number of inside units
    n_branches = n_inside*branches_per_unit #number of branches
    l_line = n_inside*sl_line #total lenght of refriceration line
    t_total = swages*(t_outside*n_outside + t_inside*n_inside + t_line*l_line) + l_line*sc_line + n_inside*sc_cond + n_branches*sc_branch
    return(t_total)

#Maintenance cost heat pumps [EUR/kW/yr], x = capacity [kW]
def FOM_hp_de(x):
    return(25*x) #Expert Interview with Moritz & Bramer GmbH: #Heat pump maintenance 10kW ca 250 EUR
def FOM_hp_ce(x):
    return(2.5*x) #Expert Interview with Moritz & Bramer GmbH: #Heat pump maintenance 200 kw 1500 eur
   
#Maintenance cost gas boilers [EUR/kW/yr], x = capacity [kW]
def FOM_gb_de(x):
    return(20*x)#Expert Interview with Moritz & Bramer GmbH: #Gas boiler maintenance 10 kW 200 eur
def FOM_gb_ce(x):
    return(2.5*x)#Expert Interview with Moritz & Bramer GmbH: #Gas boiler maintenance 200 kw 500 eur 
    
#Maintenance cost district heating station [EUR/kW/yr], x = capacity [kW]
def FOM_dhs(x):
    return(FOM_gb_de(x))#same as gas boiler (Source: Expert Interview with Moritz & Bramer GmbH)
    
#Maintenance cost geothermal probe [EUR/kW/yr], x = capacity [kW]
def FOM_gtp(x):
    return(Inv_dbhe(x)*0.03) #3% of capex, Source(https://www.npro.energy/main/en/help/economic-parameters)

#Function to pass on simultaneity factor taken from AGFW settlement types
def sf_dh(x):
    return(sf)

#Aternative function to calculate simultaneity factor
#simultaneity factor of district heating grids [-], x = number of customers, scope: 1<x<200, Source: https://www.verenum.ch/Dokumente/2001_Winter-Gleichzeitig.pdf
# def sf_dh(x):
#     a=0.449677646267461
#     b=0.551234688
#     c=53.84382392
#     d=1.762743268
#     return(a+b/(1+(x/c)**d))

#------------General assumptions------------
#area per occupant [m2/occupant]
area_per_occupant = 30
#specific heat load [W/m2]
spec_hl = 50
#specific hot water storage demand [l/occupant]
spec_hwsd = 40
#specific buffer storage demand [l/kW]
spec_bsd = 20
# specific hot water hat load pr ocupant [W/occupant] (Source: Buderus planning documents)
spec_hlhw = 200
#COP at bivalent point (Source: own calculations)
cop=3
#Contribution margin added to material costs (Source: Assumption based on expert interviews)
contribution_margin = 0.5
#heat pump and heating rod design
if paramFunction == "avg":
    hpc_biv = 0.73 #heat pump capacity at bivalent point [kW/kW specific heat load (peak)] (Source: own calculations)
    awhphr_ce = 0.04 #air water heat pump heating rod capacity at bivalent point [kW/kW specific heat load (peak)] (Source: own calculations)
    awhphr_de = 0.36 #air water heat pump heating rod capacity at bivalent point [kW/kW specific heat load (peak)] (Source: own calculations)
    wwhphr = 0.31 #water water heat pump heating rod capacity at bivalent point [kW/kW specific heat load (peak)] (Source: own calculations)
elif paramFunction == "max":
    hpc_biv = 0.81 
    awhphr_ce = 0.41 
    awhphr_de = 0.46 
    wwhphr = 0.27 
elif paramFunction == "min":
    hpc_biv = 0.61 
    awhphr_ce = 0.25 
    awhphr_de = 0.28 
    wwhphr = 0.19 

#------------Calculation of the costs of individual system components as data table------------
#stepsize for data table generation
stepsize_heated_area = 20
#generate columns and data using list comprehensions
heated_area = range(20, 20001, stepsize_heated_area)
#heated_area = range(20, 8000001, 20)
number_of_households = [area/area_per_household for area in heated_area]
number_of_centrals = [area/area_per_central for area in heated_area]
number_of_occupants = [area/area_per_occupant for area in heated_area]
installed_capacity = [(area*spec_hl)/1000 for area in heated_area]
additional_capacity_hw = [occupants*spec_hlhw/1000 for occupants in number_of_occupants]
hot_water_storage_volume = [occupants*spec_hwsd for occupants in number_of_occupants]
buffer_storage_volume = [capacity*spec_bsd for capacity in installed_capacity]
simultaneity_factor = [sf_dh(households) for households in number_of_households]
inv_cost_awhp = [Inv_awhp((capacity+additional_capacity_hw)*hpc_biv/cop) / capacity for capacity,additional_capacity_hw in zip(installed_capacity,additional_capacity_hw)]    
inv_cost_wwhp = [Inv_wwhp((capacity+additional_capacity_hw)*hpc_biv/cop) / capacity for capacity,additional_capacity_hw in zip(installed_capacity,additional_capacity_hw)]  
inv_cost_aahp = [Inv_aahp(capacity) / capacity for capacity in installed_capacity]  
inv_cost_gb = [Inv_gb(capacity+additional_capacity_hw) / capacity for capacity,additional_capacity_hw in zip(installed_capacity,additional_capacity_hw)]
inv_cost_hb = [Inv_hb(capacity+additional_capacity_hw) / capacity for capacity,additional_capacity_hw in zip(installed_capacity,additional_capacity_hw)]    
inv_cost_eb = [Inv_eb(capacity) / capacity for capacity in installed_capacity]
inv_cost_awhp_ce = [Inv_awhp(capacity*hpc_biv*sf_dh(households)/cop) / capacity for households, capacity in zip(number_of_households, installed_capacity)]    
inv_cost_wwhp_ce = [Inv_wwhp(capacity*hpc_biv*sf_dh(households)/cop) / capacity for households, capacity in zip(number_of_households, installed_capacity)]
inv_cost_gb_ce = [Inv_gb(capacity*sf_dh(households)) / capacity for households, capacity in zip(number_of_households, installed_capacity)]
inv_cost_hb_ce = [Inv_hb(capacity*sf_dh(households)) / capacity for households, capacity in zip(number_of_households, installed_capacity)]       
inv_cost_bs = [Inv_bs(volume) / capacity for volume, capacity in zip(buffer_storage_volume, installed_capacity)] 
inv_cost_hws = [Inv_hws(volume) / capacity for volume, capacity in zip(hot_water_storage_volume, installed_capacity)]
inv_cost_hws_ce = [Inv_hws(hot_water_storage_volume[int(area_per_household/stepsize_heated_area-1)])*households / capacity for capacity, households in zip(installed_capacity, number_of_households)]
inv_cost_dhs_ce = [Inv_dhs(cap_dhs)*centrals / capacity for capacity, centrals in zip(installed_capacity, number_of_centrals)]
inv_cost_dbhe = [Inv_dbhe(capacity) / capacity for capacity in installed_capacity]
inv_cost_dbhe_ce = [Inv_dbhe(capacity*sf_dh(households)) / capacity for households, capacity in zip(number_of_households, installed_capacity)]  
inv_cost_hrawhp = [Inv_hr((capacity+additional_capacity_hw)*awhphr_de) / capacity for capacity,additional_capacity_hw in zip(installed_capacity,additional_capacity_hw)] #investment cost of heating rod for awhp and hot water storage
inv_cost_hrawhp_ce = [Inv_hr((capacity)*awhphr_de) / capacity for capacity in installed_capacity] #investment cost of heating rod for awhp central
inv_cost_hrwwhp = [Inv_hr((capacity+additional_capacity_hw)*wwhphr) / capacity for capacity,additional_capacity_hw in zip(installed_capacity,additional_capacity_hw)] #investment cost of heating rod for wwhp and hot water storage
inv_cost_hrwwhp_ce = [Inv_hr((capacity)*wwhphr) / capacity for capacity in installed_capacity] #investment cost of heating rod for wwhp central
inv_cost_hrhw_ce = [Inv_hr(additional_capacity_hw[int(area_per_household/stepsize_heated_area-1)])*awhphr_ce*households / capacity for capacity, households in zip(installed_capacity, number_of_households)] #investment cost of heating rod for hot water storage central
inv_cost_ihwh = [Inv_ihwh(capacity) / capacity for capacity in installed_capacity]
inst_cost_hp = [Inst_hp(capacity+additional_capacity_hw*hpc_biv) / capacity for capacity,additional_capacity_hw in zip(installed_capacity,additional_capacity_hw)]   
inst_cost_aahp = [Inst_aahp(capacity) / capacity for capacity in installed_capacity]
inst_cost_gb = [Inst_gb(capacity) / capacity for capacity in installed_capacity]
inst_cost_hp_ce = [Inst_hp(capacity*sf_dh(households)) / capacity for households, capacity in zip(number_of_households, installed_capacity)]    
inst_cost_gb_ce = [Inst_gb(capacity*sf_dh(households)) / capacity for households, capacity in zip(number_of_households, installed_capacity)]    
inst_cost_dhs_ce = [Inst_dhs(cap_dhs)*centrals / capacity for capacity, centrals in zip(installed_capacity, number_of_centrals)]

#------------Calculation of the system costs------------
#calculate system costs decentral gas boiler heating system
cm_gb_dc = [sum(x)*contribution_margin for x in zip(inv_cost_gb,inv_cost_hws)]#contribtion margin on investment costs
sys_cost_gb_dc = [sum(x) for x in zip(inv_cost_gb,inv_cost_hws,cm_gb_dc, inst_cost_gb)]

#calculate system costs decentral hydrogen boiler heating system
cm_hb_dc = [sum(x)*contribution_margin for x in zip(inv_cost_hb,inv_cost_hws)]#contribtion margin on investment costs
sys_cost_hb_dc = [sum(x) for x in zip(inv_cost_hb,inv_cost_hws, cm_hb_dc, inst_cost_gb)]

#calculate system costs decentral water-water heat pump system
cm_wwhp_dc = [sum(x)*contribution_margin for x in zip(inv_cost_wwhp ,inv_cost_hrwwhp,inv_cost_hws,inv_cost_bs,inv_cost_dbhe)]#contribtion margin on investment costs
sys_cost_wwhp_dc = [sum(x) for x in zip(inv_cost_wwhp ,inv_cost_hrwwhp,inv_cost_hws,inv_cost_bs,inv_cost_dbhe, cm_wwhp_dc, inst_cost_hp)]

#calculate system costs central gas boiler heating system with district heating
cm_gb_ce = [sum(x)*contribution_margin for x in zip(inv_cost_gb_ce,inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce)]#contribtion margin on investment costs
sys_cost_gb_ce = [sum(x) for x in zip(inv_cost_gb_ce,inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce, cm_gb_ce, inst_cost_gb_ce,inst_cost_dhs_ce)]

#calculate system costs central hydrogen boiler heating system with district heating
cm_hb_ce = [sum(x)*contribution_margin for x in zip(inv_cost_hb_ce,inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce)]#contribtion margin on investment costs
sys_cost_hb_ce = [sum(x) for x in zip(inv_cost_hb_ce,inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce, cm_hb_ce, inst_cost_gb_ce,inst_cost_dhs_ce)]

#calculate system costs central water-water heat pump system with district heating
cm_wwhp_ce = [sum(x)*contribution_margin for x in zip(inv_cost_wwhp_ce, inv_cost_dhs_ce, inv_cost_hrwwhp_ce, inv_cost_hrhw_ce, inv_cost_dbhe_ce,inv_cost_hws_ce,inv_cost_hrhw_ce)]#contribtion margin on investment costs
sys_cost_wwhp_ce = [sum(x) for x in zip(inv_cost_wwhp_ce, inv_cost_dhs_ce, inv_cost_hrwwhp_ce, inv_cost_hrhw_ce, inv_cost_dbhe_ce, inv_cost_hws_ce,inv_cost_hrhw_ce, cm_wwhp_ce, inst_cost_hp_ce,inst_cost_dhs_ce)]

#calculate system costs decentral air-air heat pump heating and cooling system
cm_aahp_de = [sum(x)*contribution_margin for x in zip(inv_cost_aahp,inv_cost_ihwh)]#contribtion margin on investment costs
sys_cost_aahp_de = [sum(x) for x in zip(inv_cost_aahp,inv_cost_ihwh, cm_aahp_de, inst_cost_aahp)]

#calculate system costs decentral direct electric heating system
cm_deh_de = [sum(x)*contribution_margin for x in zip(inv_cost_eb,inv_cost_ihwh)]#contribtion margin on investment costs
sys_cost_eb_de = [sum(x) for x in zip(inv_cost_eb,inv_cost_ihwh, cm_deh_de, inst_cost_gb)]

#calculate system costs decentral air-water heat pump system
cm_awhp_dc = [sum(x)*contribution_margin for x in zip(inv_cost_awhp, inv_cost_hrawhp, inv_cost_hws,inv_cost_bs)]#contribtion margin on investment costs
sys_cost_awhp_dc = [sum(x) for x in zip(inv_cost_awhp, inv_cost_hrawhp, inv_cost_hws,inv_cost_bs, cm_awhp_dc, inst_cost_hp)]

#calculate system costs central air-water heat pump system with district heating
cm_awhp_ce = [sum(x)*contribution_margin for x in zip(inv_cost_awhp_ce, inv_cost_hrawhp_ce, inv_cost_hrhw_ce, inv_cost_dhs_ce,inv_cost_hws_ce, inv_cost_hrhw_ce)]
sys_cost_awhp_ce = [sum(x) for x in zip(inv_cost_awhp_ce, inv_cost_hrawhp_ce, inv_cost_hrhw_ce, inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce, cm_awhp_ce, inst_cost_hp_ce,inst_cost_dhs_ce)]


systems = [
    ("AWHP DC", inv_cost_awhp, inv_cost_hrawhp, inv_cost_hws, inv_cost_bs, cm_awhp_dc, inst_cost_hp),
    ("GB DC", inv_cost_gb, inv_cost_hws, cm_gb_dc, inst_cost_gb),
    ("HB DC", inv_cost_hb, inv_cost_hws, cm_hb_dc, inst_cost_gb),
    ("WWHP DC", inv_cost_wwhp, inv_cost_hrwwhp, inv_cost_hws, inv_cost_bs, inv_cost_dbhe, cm_wwhp_dc, inst_cost_hp),
    ("GB CE", inv_cost_gb_ce, inv_cost_dhs_ce, inv_cost_hws_ce, inv_cost_hrhw_ce, cm_gb_ce, inst_cost_gb_ce, inst_cost_dhs_ce),
    ("HB CE", inv_cost_hb_ce, inv_cost_dhs_ce, inv_cost_hws_ce, inv_cost_hrhw_ce, cm_hb_ce, inst_cost_gb_ce, inst_cost_dhs_ce),
    ("AWHP CE", inv_cost_awhp_ce, inv_cost_hrawhp_ce, inv_cost_hrhw_ce, inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce, cm_awhp_ce, inst_cost_hp_ce,inst_cost_dhs_ce),
    ("WWHP CE", inv_cost_wwhp_ce, inv_cost_dhs_ce, inv_cost_hrwwhp_ce, inv_cost_hrhw_ce, inv_cost_dbhe_ce, inv_cost_hws_ce, inv_cost_hrhw_ce, cm_wwhp_ce, inst_cost_hp_ce, inst_cost_dhs_ce),
    ("AAHP DE", inv_cost_aahp, inv_cost_ihwh, cm_aahp_de, inst_cost_aahp),
    ("EB DE", inv_cost_eb, inv_cost_ihwh, cm_deh_de, inst_cost_gb),
    # Add more systems here in the same format
]

#sys_cost_awhp_dc = [sum(x) for x in zip(inv_cost_awhp, inv_cost_hrawhp, inv_cost_hws,inv_cost_bs,inst_cost_hp)]
#sys_cost_awhp_ce = [sum(x) for x in zip(inv_cost_awhp_ce, inv_cost_hrawhp_ce, inv_cost_hrhw_ce, inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce,inst_cost_hp_ce,inst_cost_dhs_ce)]

#------------Compile data table------------
data = {
        "heated area [m2]": heated_area, 
        "installed capacity [kW_th]": installed_capacity,
        "number of households [#]": number_of_households,
        "number of occupants [#]": number_of_occupants,
        "hot water storage volume [l]": hot_water_storage_volume,
        "buffer storage volume [l]": buffer_storage_volume,
        "Simultaneity_factor [-]": simultaneity_factor,
        'Inv Cost AWHP [EUR/kW]': inv_cost_awhp,
        'Inv Cost WWHP [EUR/kW]': inv_cost_wwhp,
        'Inv Cost AAHP [EUR/kW]': inv_cost_aahp,
        'Inv Cost GB [EUR/kW]': inv_cost_gb,
        'Inv Cost HB [EUR/kW]': inv_cost_hb,
        'Inv Cost EB [EUR/kW]': inv_cost_eb,
        'Inv Cost AWHP central [EUR/kW]': inv_cost_awhp_ce,
        'Inv Cost WWHP central [EUR/kW]': inv_cost_wwhp_ce,
        'Inv Cost GB central [EUR/kW]': inv_cost_gb_ce,
        'Inv Cost HB central [EUR/kW]': inv_cost_hb_ce,
        'Inv Cost BS [EUR/kW]': inv_cost_bs,
        'Inv Cost HWS [EUR/kW]': inv_cost_hws,
        'Inv Cost HWS central [EUR/kW]': inv_cost_hws_ce,
        'Inv Cost DHS [EUR/kW]': inv_cost_dhs_ce,
        'Inv Cost DBHE [EUR/kW]': inv_cost_dbhe,
        'Inv Cost DBHE central [EUR/kW]': inv_cost_dbhe_ce,
        'Inv Cost HR for HWS and AWHP [EUR/kW]' : inv_cost_hrawhp,
        'Inv Cost HR for AWHP central [EUR/kW]' : inv_cost_hrawhp_ce,
        'Inv Cost HR for WWHP and HWS [EUR/kW]' : inv_cost_hrwwhp,
        'Inv Cost HR for WWHP central [EUR/kW]' : inv_cost_hrwwhp_ce,
        'Inv Cost HR for HWS central[EUR/kW]' : inv_cost_hrhw_ce,
        'Inv Cost IHWH [EUR/kW]': inv_cost_ihwh,
        'Inst Cost HP [EUR/kW]': inst_cost_hp,
        'Inst Cost GB [EUR/kW]': inst_cost_gb,
        'Inst Cost HP central [EUR/kW]': inst_cost_hp_ce,
        'Inst Cost AAHP [EUR/kW]': inst_cost_aahp,
        'Inst Cost GB central [EUR/kW]': inst_cost_gb_ce,
        'Inst Cost DHS [EUR/kW]': inst_cost_dhs_ce,
        'Sys Cost Gas Boiler Decentral [EUR/kW]': sys_cost_gb_dc,
        'Sys Cost Gas Boiler Central [EUR/kW]': sys_cost_gb_ce,
        'Sys Cost Hydrogen Boiler Decentral [EUR/kW]': sys_cost_hb_dc,
        'Sys Cost Hydrogen Boiler Central [EUR/kW]': sys_cost_hb_ce,
        'Sys Cost AW Heat Pump Decentral [EUR/kW]': sys_cost_awhp_dc,
        'Sys Cost AW Heat Pump Central [EUR/kW]': sys_cost_awhp_ce,
        'Sys Cost WW Heat Pump Decentral [EUR/kW]': sys_cost_wwhp_dc,
        'Sys Cost WW Heat Pump Central [EUR/kW]': sys_cost_wwhp_ce,
        'Sys Cost AA Heat Pump Decentral [EUR/kW]': sys_cost_aahp_de,
        'Sys Cost Electric Boiler Decentral [EUR/kW]': sys_cost_eb_de}
data = pd.DataFrame(data)

#------------Filter data table for export------------

cap_to_keep=np.arange(1,int(max(installed_capacity)+1))
columns_to_keep = ["installed capacity [kW_th]", 
                'Sys Cost Gas Boiler Decentral [EUR/kW]', 
                'Sys Cost Hydrogen Boiler Decentral [EUR/kW]', 
                'Sys Cost AW Heat Pump Decentral [EUR/kW]',
                'Sys Cost WW Heat Pump Decentral [EUR/kW]',
                'Sys Cost Gas Boiler Central [EUR/kW]', 
                'Sys Cost Hydrogen Boiler Central [EUR/kW]',
                'Sys Cost AW Heat Pump Central [EUR/kW]',
                'Sys Cost WW Heat Pump Central [EUR/kW]',
                'Sys Cost AA Heat Pump Decentral [EUR/kW]',
                'Sys Cost Electric Boiler Decentral [EUR/kW]']
data_filtered = data[data['installed capacity [kW_th]'].isin(cap_to_keep)]
data_filtered = data_filtered.filter(columns_to_keep)
# Create column with cost level
new_df = pd.DataFrame({"cost level": [paramFunction] * len(data_filtered)})
data_filtered = pd.concat([data_filtered.iloc[:, :1], new_df, data_filtered.iloc[:, 1:]], axis=1)


#------------Plot system costs of all systems over the heating capacity------------

sys_cost_gb_dc = data['Sys Cost Gas Boiler Decentral [EUR/kW]']
sys_cost_gb_ce = data['Sys Cost Gas Boiler Central [EUR/kW]']
sys_cost_hb_dc = data['Sys Cost Hydrogen Boiler Decentral [EUR/kW]']
sys_cost_hb_ce = data['Sys Cost Hydrogen Boiler Central [EUR/kW]']
sys_cost_aw_dc = data['Sys Cost AW Heat Pump Decentral [EUR/kW]']
sys_cost_aw_ce = data['Sys Cost AW Heat Pump Central [EUR/kW]']
sys_cost_ww_dc = data['Sys Cost WW Heat Pump Decentral [EUR/kW]']
sys_cost_ww_ce = data['Sys Cost WW Heat Pump Central [EUR/kW]']
sys_cost_aa_dc = data['Sys Cost AA Heat Pump Decentral [EUR/kW]']
sys_cost_deh_dc = data['Sys Cost Electric Boiler Decentral [EUR/kW]']

## Plot system costs and cost composition
#define colors
grey = "#5c6162"
gold = "#ffbf27"
blue = '#649bff'
red = '#bf3347'
green = '#2a721e'
light_grey = '#5c616280'
light_gold = '#ffbf2780'
light_blue = '#649bff80'
light_red = '#bf334780'
light_green = '#47bf33'

# Create figure and axis objects
fig, ax1 = plt.subplots()

# Set axis labels and title
ax1.set_xlabel('Installed Capacity [kW_th]')
ax1.set_ylabel('System Cost [EUR/kW]')
ax1.set_title('Comparison of system costs')

# Plot sys_cost_gb_dc as a line on the secondary y-axis
ax1.plot(data['installed capacity [kW_th]'], sys_cost_ww_ce, color=red, label='WtW hp ce')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_ww_dc, color=light_red, label='WtW hp dc')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_aw_ce, color=blue, label='AtW hp ce')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_aw_dc, color=light_blue, label='AtW hp dc')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_aa_dc, color=gold, label='AtA hp dc')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_gb_ce, color=grey, label='GB ce')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_gb_dc, color=light_grey, label='GB dc')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_gb_ce, color=green, label='HB ce')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_gb_dc, color=light_green, label='HB dc')
ax1.plot(data['installed capacity [kW_th]'], sys_cost_deh_dc, color='black', label='DEH dc')

# Add legend
lines, labels = ax1.get_legend_handles_labels()
ax1.legend(lines, labels, loc='upper right')

# Set xlim and ylim based on the data range
xmin = np.min(data['installed capacity [kW_th]'])
xmax = np.max(data['installed capacity [kW_th]'])
ymax = np.max(sys_cost_ww_ce)

ax1.set_xlim(5, 650)
ax1.set_ylim(0, 9000)

# Show the plot
plt.show()

#------------Plot area plot of the costs of individual compoenents of a system over the heating capacity------------

#Plot system cost components as area plots
# Define custom colors
colors = [
    '#5c6162',  # grey
    '#ffbf27',  # gold
    '#649bff',  # blue
    '#bf3347',  # red
    '#458B74',  # green
    '#B23AEE',  # violet
    '#5c616280',  # light grey
    '#ffbf2780',  # light gold
    '#649bff80',  # light blue
    '#bf334780',  # light red
    '#47bf3380'  # light green
]

# System 1: AWHP DC
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_awhp, inv_cost_hrawhp, inv_cost_hws,inv_cost_bs, cm_awhp_dc, inst_cost_hp, colors=colors)
plt.legend(['Inv Cost AWHP', 'Inv Cost HRAWHP', 'Inv Cost HWS', 'Inv Cost BS', 'Contribution margin', 'Inst Cost HP'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost AWHP DC Components')
plt.show()

# System 2: GB DC
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_gb,inv_cost_hws,cm_gb_dc, inst_cost_gb, colors=colors)
plt.legend(['Inv Cost GB', 'Inv Cost HWS', 'Contribution margin', 'Inst Cost GB'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost GB DC Components')
plt.show()

# System 3: HB DC
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_hb,inv_cost_hws, cm_hb_dc, inst_cost_gb, colors=colors)
plt.legend(['Inv Cost HB', 'Inv Cost HWS', 'Contribution margin', 'Inst Cost GB'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost HB DC Components')
plt.show()

# System 4: WWHP DC
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_wwhp ,inv_cost_hrwwhp,inv_cost_hws,inv_cost_bs,inv_cost_dbhe, cm_wwhp_dc, inst_cost_hp, colors=colors)
plt.legend(['Inv Cost WWHP', 'Inv Cost HRWWHP', 'Inv Cost HWS', 'Inv Cost BS', 'Inv Cost DBHE', 'Contribution margin', 'Inst Cost HP'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost WWHP DC Components')
plt.show()

# System 5: GB CE
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_gb_ce,inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce, cm_gb_ce, inst_cost_gb_ce,inst_cost_dhs_ce, colors=colors)
plt.legend(['Inv Cost GB CE', 'Inv Cost DHS CE', 'Inv Cost HWS CE', 'Inv Cost HRHW CE', 'Contribution margin', 'Inst Cost GB CE', 'Inst Cost DHS CE'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost GB CE Components')
plt.show()

# System 6: HB CE
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_hb_ce,inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce, cm_hb_ce, inst_cost_gb_ce,inst_cost_dhs_ce, colors=colors)
plt.legend(['Inv Cost HB CE', 'Inv Cost DHS CE', 'Inv Cost HWS CE', 'Inv Cost HRHW CE', 'Contribution margin', 'Inst Cost GB CE', 'Inst Cost DHS CE'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost HB CE Components')
plt.show()

# System 7: AWHP CE 
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_awhp_ce, inv_cost_hrawhp_ce, inv_cost_hrhw_ce, inv_cost_dhs_ce,inv_cost_hws_ce,inv_cost_hrhw_ce, cm_awhp_ce, inst_cost_hp_ce,inst_cost_dhs_ce, colors=colors)
plt.legend(['Inv Cost AWHP CE', 'Inv Cost HRAWHP CE', 'Inv Cost HRHW CE', 'Inv Cost DHS CE', 'Inv Cost HWS CE', 'Inv Cost HRHW CE', 'Contribution Margin', 'Inst Cost HP CE', 'Inst Cost DHS CE'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost AWHP CE Components')
plt.show()

# System 8: WWHP CE
x = np.arange(1, int(max(installed_capacity)+1))

plt.stackplot(x, inv_cost_wwhp_ce, inv_cost_dhs_ce, inv_cost_hrwwhp_ce, inv_cost_hrhw_ce, inv_cost_dbhe_ce, inv_cost_hws_ce,inv_cost_hrhw_ce, cm_wwhp_ce, inst_cost_hp_ce,inst_cost_dhs_ce, colors=colors)
plt.legend(['Inv Cost WWHP CE','Inv Cost DHS CE', 'Inv Cost HRWWHP CE', 'Inv Cost HRHW CE', 'Inv Cost DBHE CE', 'Inv Cost HWS CE', 'Inv Cost HRHW CE', 'Contribution margin', 'Inst Cost HP CE', 'Inst Cost DHS CE'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost WWHP CE Components')
plt.show()

# System 9: AAHP DE
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_aahp,inv_cost_ihwh, cm_aahp_de, inst_cost_aahp, colors=colors)
plt.legend(['Inv Cost AAHP', 'Inv Cost IHWH', 'Contribution margin', 'Inst Cost AAHP'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost AAHP DE Components')
plt.show()

# System 10: EB DE
x = np.arange(1, int(max(installed_capacity)+1))
plt.stackplot(x, inv_cost_eb,inv_cost_ihwh, cm_deh_de, inst_cost_gb, colors=colors)
plt.legend(['Inv Cost EB', 'Inv Cost IHWH', 'Contribution margin', 'Inst Cost GB'], loc='upper right')
plt.xlabel('Installed capacity [kW$_{th}$]')
plt.ylabel('Spec. investment costs [EUR/kW$_{th}$]')
plt.ylim(0,9000)
plt.xlim(5,650)
plt.title('System Cost EB DE Components')
plt.show()
