#!/usr/bin/env python
'''
Subbuilder of APAFrame
'''

from math import cos, sin, tan
import gegede.builder
from gegede import Quantity as Q
from gegede import units

class APAFrameBuilder(gegede.builder.Builder):
    '''
    Build the FRAME.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  size          = None,
                  footsize      = None,
                  footthickness = None,
                  nribs         = None,
                  ribsize       = None,
                  ribthickness  = None,
                  **kwds):

        self.size          = size
        self.footsize      = footsize
        self.footthickness = footthickness
        self.nribs         = nribs
        self.ribsize       = ribsize
        self.ribthickness  = ribthickness


    def ConstructHollowBeam(self, geom, name, sizeouter, thickness):
         SurroundingBox = geom.shapes.Box(name+'Box',
                                          dx=0.5*sizeouter[0],
                                          dy=0.5*sizeouter[1],
                                          dz=0.5*sizeouter[2])

         SubtractionBox = geom.shapes.Box(name+'SubtractionBox',
                                          dx=0.5*sizeouter[0]-thickness, 
                                          dy=0.5*sizeouter[1]-thickness,
                                          dz=0.5*sizeouter[2])
         Pos = geom.structure.Position(name+'SubtractionPos',
                                       Q('0m'), Q('0m'), Q('0m'))
         
         SubVol = geom.shapes.Boolean(name+"_BoolSub",
                                      type='subtraction',
                                      first=SurroundingBox,
                                      second=SubtractionBox,
                                      pos=Pos)
         Vol_lv = geom.structure.Volume('vol'+name, material='Steel', shape=SubVol)
         return Vol_lv
     
        
    def construct(self, geom):
         FrameBox = geom.shapes.Box('Frame',
                                    dx=0.5*self.footsize[0],
                                    dy=0.5*self.size[1],
                                    dz=0.5*self.size[2])
         frame_lv = geom.structure.Volume('volAPAFrame', material='LAr', shape=FrameBox)
         self.add_volume(frame_lv)


         Foot_lv = self.ConstructHollowBeam(geom, 'APAFrameFoot', self.footsize, self.footthickness)

         size_middle = [self.footsize[0], self.footsize[1], self.size[1]-2*self.footsize[0]]
         Middle_lv = self.ConstructHollowBeam(geom, 'APAFrameMiddle',  size_middle, self.footthickness)

         size_rib    = [self.ribsize[0], self.ribsize[1], 0.5*self.size[2]-1.5*self.footsize[0]]
         Rib_lv    = self.ConstructHollowBeam(geom, 'APAFrameRib',     size_rib   , self.ribthickness)
         

         FootPosition = geom.structure.Position('APAFrameFootPos',
                                                Q('0m'),0.5*(-self.size[1]+self.footsize[1]), Q('0m'))

         TopPosition  = geom.structure.Position('APAFrameTopPos',
                                                Q('0m'),0.5*(self.size[1]-self.footsize[1]), Q('0m'))

         MiddlePosition = geom.structure.Position('APAFrameMiddlePos',
                                                  Q('0m'), Q('0m'), Q('0m'))

         LeftPosition = geom.structure.Position('APAFrameLeftPos',
                                                Q('0m'), Q('0m'), 0.5*(-self.size[2]+self.footsize[1]))

         RightPosition = geom.structure.Position('APAFrameRightPos',
                                                Q('0m'), Q('0m'), 0.5*(self.size[2]-self.footsize[1]))



         Placement_Foot = geom.structure.Placement("placeAPAFrameFoot", volume=Foot_lv, pos=FootPosition,
                                                   rot='identity')

         Placement_Top = geom.structure.Placement("placeAPAFrameTop", volume=Foot_lv, pos=TopPosition,
                                                   rot='identity')

         Placement_Middle = geom.structure.Placement("placeAPAFrameMiddle", volume=Middle_lv, pos=MiddlePosition,
                                                     rot='r90aboutX')

         Placement_Left = geom.structure.Placement("placeAPAFrameLeft", volume=Middle_lv, pos=LeftPosition,
                                                     rot='r90aboutX')

         Placement_Right = geom.structure.Placement("placeAPAFrameRight", volume=Middle_lv, pos=RightPosition,
                                                     rot='r90aboutX')


         
         frame_lv.placements.append(Placement_Foot  .name)
         frame_lv.placements.append(Placement_Top   .name)
         frame_lv.placements.append(Placement_Middle.name)
         frame_lv.placements.append(Placement_Left  .name)
         frame_lv.placements.append(Placement_Right .name)

         print("low "+str(-0.5*self.size[1]))
         print("hig "+str(0.5*self.size[1]))
         
         for iRib in range(self.nribs):
             #posy = -0.5*self.size[1] + self.footsize[1] + (iRib+1) * (self.size[1] - 2*self.footsize[1]) / self.nribs
             posy = -0.5 * size_middle[2] + (1+iRib) * size_middle[2] / (self.nribs+1)
             print("Rib "+str(posy))
             name = 'APAFrameRib'+str(2*iRib+1)
             RibPosition = geom.structure.Position(name+'Pos',
                                                   Q('0m'), posy, 0.25*(self.size[2]-self.footsize[1]))
             Placement_Rib = geom.structure.Placement("place"+name, volume=Rib_lv, pos=RibPosition,
                                                      rot='r90aboutZ')

             frame_lv.placements.append(Placement_Rib.name)

             name = 'APAFrameRib'+str(2*iRib)
             RibPosition = geom.structure.Position(name+'Pos',
                                                   Q('0m'), posy, -0.25*(self.size[2]-self.footsize[1]))
             Placement_Rib = geom.structure.Placement("place"+name, volume=Rib_lv, pos=RibPosition,
                                                      rot='r90aboutZ')
             frame_lv.placements.append(Placement_Rib.name)
             
             