from Geant4 import *

class MySensitiveDetector(G4VSensitiveDetector):
    def __init__(self,name,outTree,brDict):
        G4VSensitiveDetector.__init__(self,name)
        self.brDict = brDict
        self.outTree= outTree
    def ProcessHits(self,step,hist):
        preStepPoint = step.GetPreStepPoint()
        if (preStepPoint.GetCharge()==0):
            return False 
        
        self.brDict["dEdX"][0]       = step.GetTotalEnergyDeposit()/MeV
        self.brDict["stepL"][0]      = step.GetStepLength()
        self.outTree.Fill()

        
      

class MyDetector(G4VUserDetectorConstruction):
    "My Detector Construction"

    def __init__(self,outTree,brDict):

        G4VUserDetectorConstruction.__init__(self)
        self.brDict = brDict
        self.outTree= outTree
        
        self.solid = {}
        self.logical = {}
        self.physical = {}
       

        self.create_world(side = 4000,
                          material = "G4_Galactic")
        
        self.create_cylinder(name = "tracker",
                             rMin = 150,
                             rMax = 200,
                             length = 320,
                             translation = [0,0,900],
                             material = "G4_Pb",
                             colour = [0.5,0.5,0.5,0.5],
                             mother = 'world')
        
        
        
        self.create_cube(name = "phantom",
                         side = 500,
                         translation = [0,0,-250],
                         material = "G4_Si",
                         colour = [0,0,1,0.4],
                         mother = 'world')
    
 
    
    def create_world(self, **kwargs):
        material = gNistManager.FindOrBuildMaterial(kwargs['material'])
        #material = G4Material.GetMaterial(kwargs['material'])
        side = kwargs['side']
        
        self.solid['world']   = G4Box("world", side/2., side/2., side/2.)
        self.logical['world'] = G4LogicalVolume(self.solid['world'], material, "world")
        self.physical['world']= G4PVPlacement(G4Transform3D(), self.logical['world'], "world", None, False, 0)

        visual = G4VisAttributes()
        visual.SetVisibility(False)
        self.logical['world'].SetVisAttributes(visual)
        
    
    
    def create_cylinder(self, **kwargs):
        
        name        = kwargs['name']
        rMin        = kwargs['rMin']
        rMax        = kwargs['rMax']
        length      = kwargs['length']
        translation = G4ThreeVector(*kwargs['translation'])
        material    = gNistManager.FindOrBuildMaterial(kwargs['material'])
        visual      = G4VisAttributes(G4Color(*kwargs['colour']))
        mother      = self.physical[kwargs['mother']]
        
        
        self.solid[name] = G4Tubs(name, rMin, rMax, length/2., 0., 2*pi)
        
        self.logical[name] = G4LogicalVolume(self.solid[name], 
                                             material,
                                             name)
        
        self.physical[name] = G4PVPlacement(None, translation, 
                                            name, 
                                            self.logical[name],
                                            mother, False, 0)

        self.logical[name].SetVisAttributes(visual)
    
    
    def create_cube(self, **kwargs):
        
        name = kwargs['name']
        side = kwargs['side']
        translation = G4ThreeVector(*kwargs['translation'])
        material = gNistManager.FindOrBuildMaterial(kwargs['material'])
        visual = G4VisAttributes(G4Color(*kwargs['colour']))
        mother = self.physical[kwargs['mother']]
        
        self.solid[name] = G4Box(name, side/2., side/2., side/2.)
        
        self.logical[name] = G4LogicalVolume(self.solid[name], 
                                             material,
                                             name)
        self.sensitive      = MySensitiveDetector(name,self.outTree,self.brDict)
        #sdman               = G4SDManager.GetSDMPointer()
        #sdman.AddNewDetector(self.sensitive)
        self.logical[name].SetSensitiveDetector(self.sensitive)
        
        self.physical[name] = G4PVPlacement(None, translation, 
                                            name, 
                                            self.logical[name],
                                            mother, False, 0)

        self.logical[name].SetVisAttributes(visual)

    def Construct(self): # return the world volume
        
        return self.physical['world'] 
