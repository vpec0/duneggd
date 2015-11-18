#!/usr/bin/env python
'''
Subbuilder of Detector
'''

import gegede.builder
from gegede import Quantity as Q
import math

class ECALEndBuilder(gegede.builder.Builder):
    '''
    Piece together SBPlanes, worry about rotations in DetectorBuilder,
    assuring that lead layer on outside is closest to tracker
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  ecal_z = None, 
                  leadThickness = None, 
                  nSBPlanes = None,
                  **kwds):
        if ecal_z is None:
            raise ValueError("No value given for ecal_z")
        if leadThickness is None:
            raise ValueError("No value given for leadThickness")
        if nSBPlanes is None:
            raise ValueError("No value given for nSBPlanes")

        self.ecalMat        = "Lead"
        self.ecal_z        = ecal_z
        self.leadThickness = leadThickness
        self.nSBPlanes     = nSBPlanes  
        
        self.SBPlaneBldr = self.get_builder('SBPlane')


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Get the SB Plane volume and dimensions
        SBPlane_lv = self.SBPlaneBldr.get_volume('volSBPlane')
        SBPlaneDim = list(self.SBPlaneBldr.SBPlaneDim)
        

        # Calculate ECAL dimensions 
        self.ecalEndDim    = list(SBPlaneDim) # get the right x and y dimension
        self.ecalEndDim[2] = self.nSBPlanes*(self.leadThickness + SBPlaneDim[2])
        print 'ECALEndBuilder: Configured value of ECAL z dimension is '+str(self.ecal_z)+', assigning calculated value: '+str(self.ecalEndDim[2])
      
        # Make main shape/volume for this builder
        ecalEndBox = geom.shapes.Box( self.name,
                                      dx=0.5*self.ecalEndDim[0],
                                      dy=0.5*self.ecalEndDim[1],
                                      dz=0.5*self.ecalEndDim[2])
        ecalEnd_lv = geom.structure.Volume('vol'+self.name, material=self.ecalMat, shape=ecalEndBox)
        self.add_volume(ecalEnd_lv)
  

        #Place the SB Planes in the ECAL

        
        for i in range(self.nSBPlanes):
            zpos = -0.5*self.ecalEndDim[2]+ (i+0.5)*SBPlaneDim[2]+i*self.leadThickness

            rsbp_in_ecalend  = geom.structure.Position('SBPlane-'+str(i)+'_in_'+self.name, 
                                                       '0cm', '0cm', zpos)
            prsbp_in_ecalend = geom.structure.Placement('placeSBPlane-'+str(i)+'_in_'+self.name,
                                                        volume = ecalEnd_lv, 
                                                        pos = rsbp_in_ecalend, rot="r90aboutZ")
            ecalEnd_lv.placements.append( prsbp_in_ecalend.name )
        

        return
