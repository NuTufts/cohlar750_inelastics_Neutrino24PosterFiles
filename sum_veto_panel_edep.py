import os,sys
from math import sqrt, cos, sin
import ROOT
from panel_geo import corner_panel_placements, corner_panel_dimensions, side_panel_dimensions, side_panel_placements, side_panel_rotz_angle

def sum_veto_panel_edep( seghits ):
    
    # test side panels
    side_panel_MeV = []
    for iside in range(4):
        # we transpose the hit into the panel coordinate system
        # panel info
        # center (x,y) of panel
        x = side_panel_placements[iside][0]
        y = side_panel_placements[iside][1]
        z = side_panel_placements[iside][2]
        # dimension
        l = side_panel_dimensions[0]
        th = side_panel_rotz_angle[iside]
        rad = th*3.14159/180.0

        panel_MeV = 0.0

        print("Test Side Panel[",iside,"] ===============")
        
        for ihit in range(seghits.size()):
            hit = seghits.at(ihit)
            hitx = 0.5*(hit.GetStart()[0]+hit.GetStop()[0])*0.1
            hity = 0.5*(hit.GetStart()[1]+hit.GetStop()[1])*0.1
            hitz = 0.5*(hit.GetStart()[2]+hit.GetStop()[2])*0.1
            # translate back
            hitx -= x
            hity -= y
            hitz -= z

            # rot back
            rotx = hitx*cos( -rad ) - hity*sin( rad )
            roty = hitx*sin( -rad ) + hity*cos( rad )
            rotz = hitz
            rotpos = (rotx,roty,rotz)

            
            # test
            passes = True
            dim_pass = [True,True,True]
            for v in range(3):
                if rotpos[v]<-side_panel_dimensions[v]*0.5 or rotpos[v]>side_panel_dimensions[v]*0.5:
                    passes = False
                    dim_pass[v] = False
                
            print("hit: (",(hitx, hity, hitz),") -> rotpos=",rotpos," passes=",passes," dim_pass=",dim_pass)
            if passes:
                panel_MeV += hit.GetEnergyDeposit()
        # done with hit loop
        side_panel_MeV.append( panel_MeV )
    return side_panel_MeV
            
