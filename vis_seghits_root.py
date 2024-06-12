import ROOT as rt
from math import sqrt, cos, sin
from panel_geo import corner_panel_placements, corner_panel_dimensions, side_panel_dimensions, side_panel_placements, side_panel_rotz_angle


def get_panel_topview_geo():
    # side panels
    side_panels_geo = []
    for i in range(4):
        # center (x,y) of panel
        x = side_panel_placements[i][0]
        y = side_panel_placements[i][1]
        # dimension
        l = side_panel_dimensions[0]
        th = side_panel_rotz_angle[i]
        rad = th*3.14159/180.0
        
        # rotate then push
        x1 = -0.5*l
        y1 = 0.0
        rotx1 = x1*cos( rad ) - y1*sin( rad )
        roty1 = x1*sin( rad ) + y1*cos( rad )
        x2 = 0.5*l
        y2 = 0.0
        rotx2 = x2*cos( rad ) - y2*sin( rad )
        roty2 = x2*sin( rad ) + y2*cos( rad )
        # translate
        rotx1 += x
        roty1 += y
        rotx2 += x
        roty2 += y
        panel_line = rt.TLine( rotx1, roty1, rotx2, roty2 )
        side_panels_geo.append( panel_line )
    return side_panels_geo

def vis_seghits_root( seghit_v,
                      cryostat_radius_cm=37.50,
                      cryostat_height_cm=133.70,
                      peak_wins=None,
                      entry=None ):

    cvis = rt.TCanvas("cvisseghits", "Visualizae Seghits", 1500,600)
    cvis.Divide(2,1)
    
    # just setting up the view for the event
    hxy = rt.TH2D("hxy","; x (cm); y (cm)",10, -3*cryostat_radius_cm, 3*cryostat_radius_cm, 10, -3*cryostat_radius_cm, 3*cryostat_radius_cm )
    hrz = rt.TH2D("hrz","; r (cm); z (cm)",10, 0, 3*cryostat_radius_cm, 10, -3*cryostat_height_cm/2.0, 3*cryostat_height_cm/2.0 )
    
    if entry is not None:
        hxy.SetTitle(entry)
        hrz.SetTitle(entry)

    # XY
    cvis.cd(1)
    hxy.Draw()
    tcirc = rt.TEllipse( 0.0, 0.0, cryostat_radius_cm, cryostat_radius_cm )
    tcirc.SetFillStyle(0)
    tcirc.SetLineColor( rt.kBlack )
    tcirc.Draw()

    obj_v = get_panel_topview_geo()
    for obj in obj_v:
        obj.Draw()

    # get hist inside windows
    g_v = []
    hits_vv = []
    if type(seghit_v) is list:
        hits_vv = seghit_v
    else:
        hist_vv = [seghit_v]
    iseg = 0
    for seghit in hits_vv:
        gxy= rt.TGraph( seghit.size() )
        for ii in range(seghit.size()):
            hit = seghit.at(ii)
            gxy.SetPoint(ii, hit.GetStart()[0]*0.1, hit.GetStart()[1]*0.1 )
        gxy.SetMarkerColor( rt.kRed+iseg )
        iseg += 1
        gxy.SetMarkerStyle(20)
        gxy.Draw("P")
        g_v.append(gxy)

    cvis.Update()

    # RZ
    cvis.cd(2)
    hrz.Draw()
    tbox = rt.TBox( 0, -0.5*cryostat_height_cm, cryostat_radius_cm, 0.5*cryostat_height_cm )
    tbox.SetFillStyle(0)
    tbox.SetLineColor( rt.kBlack )
    tbox.Draw()

    iseg = 0
    for seghit in hits_vv:
        grz= rt.TGraph( seghit.size() )
        for ii in range(seghit.size()):
            hit = seghit.at(ii)
            x = hit.GetStart()[0]*0.1
            y = hit.GetStart()[1]*0.1
            r = sqrt(x*x+y*y)
            z = hit.GetStart()[2]*0.1
            grz.SetPoint(ii, r, z )
        grz.SetMarkerColor( rt.kRed+iseg )
        iseg+=1
        grz.SetMarkerStyle(20)
        grz.Draw("P")
        g_v.append(grz)
    cvis.Update()

    print("[ENTER] to continue")
    input()
    return [cvis, hxy, hrz, tcirc, tbox]+obj_v+g_v
    
    
    

