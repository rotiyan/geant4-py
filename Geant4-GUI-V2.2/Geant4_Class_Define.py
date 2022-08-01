from Geant4 import *

import g4py.NISTmaterials

# Class for passing parameters

class Parameter_Pass():

    def __init__(self):
	
	self.world__side = 0
        self.world__material = ''
        self.layer_name = []
        self.layer_sidex = []
        self.layer_sidey = []
        self.layer_sidez = []
        self.layer_translation = []
        self.layer_material = []
        self.layer_color = []
        self.layer_mother = []
        self.layer_num = 0
  
    def world_add(self, side, material):
        self.world__side = side
        self.world__material = material

    def Layer_add(self, name, sidex, sidey, sidez, translation, material, color, mother):
        self.layer_name.append(name)
        self.layer_sidex.append(sidex)
        self.layer_sidey.append(sidey)
        self.layer_sidez.append(sidez)
        self.layer_translation.append(translation)
        self.layer_material.append(material)
        self.layer_color.append(color)
        self.layer_mother.append(mother)
        self.layer_num = len(self.layer_name)

# Main Function Define Target Material and Particle Gun

class MyDetectorConstruction(G4VUserDetectorConstruction):
    "My Detector Construction"

    def __init__(self, solid={}, logical={}, physical={}):

        G4VUserDetectorConstruction.__init__(self)
        
        
        self.solid = solid
        self.logical = logical
        self.physical = physical   
 
    
    def create_world(self, **kwargs):
        
        material = G4Material.GetMaterial(kwargs['material'])
        side = kwargs['side']
        
        self.solid['world'] = G4Box("world", side/2., side/2., side/2.)
        
        self.logical['world'] = G4LogicalVolume(self.solid['world'], 
                                                material, 
                                                "world")
        
        self.physical['world'] = G4PVPlacement(G4Transform3D(), 
                                               self.logical['world'], 
                                               "world", None, False, 0)

        visual = G4VisAttributes()
        visual.SetVisibility(False)
        
        self.logical['world'].SetVisAttributes(visual)
        
    
    
    def create_box(self, **kwargs):
        
        name = kwargs['name']
        sidex = kwargs['sidex']
        sidey = kwargs['sidey']
        sidez = kwargs['sidez']
        translation = G4ThreeVector(*kwargs['translation'])
        material = kwargs['material']
        visual = G4VisAttributes(G4Color(*kwargs['color']))
        mother = self.physical[kwargs['mother']]
        
        self.solid[name] = G4Box(name, sidex/2., sidey/2., sidez/2.)
        
        self.logical[name] = G4LogicalVolume(self.solid[name], 
                                             material,
                                             name)
        
        self.physical[name] = G4PVPlacement(None, translation, 
                                            name, 
                                            self.logical[name],
                                            mother, False, 0)

        self.logical[name].SetVisAttributes(visual)

        
        
    # -----------------------------------------------------------------
    def Construct(self): # return the world volume
        
        return self.physical['world']

# wrap the g4 primary generator action
class MyPrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):
    "My Primary Generator Action"

    def __init__(self, file_name):
        
        G4VUserPrimaryGeneratorAction.__init__(self)
        
        beam = G4GeneralParticleSource()
	gControlExecute(file_name)

        self.particleGun = beam

        
    def GeneratePrimaries(self, event):
        
        self.particleGun.GeneratePrimaryVertex(event)

# Data recording Class runaction, stepaction
class MyUserRunAction(G4UserRunAction):
  "My Run Action"

  def SetFilePath(self, file_name):
    self.filename = file_name
  def BeginOfRunAction(self,run):
    self.Ofile = open(self.filename,"w")
  def EndOfRunAction(self, run):
    print "*** Writing out dEdX"
    self.Ofile.close()

class MyUserSteppingAction(G4UserSteppingAction):
  "My Stepping Action"
  def __init__(self, AtomicM_Thres, Active_Layer, min_dX, min_dE):        
      G4UserSteppingAction.__init__(self)
      self.AtomicM_Thres = AtomicM_Thres
      self.Active_Layer = Active_Layer
      self.min_dX = min_dX
      self.min_dE = min_dE

  def UserSteppingAction(self, step):
    print "In stepping action "
    print (str(self.AtomicM_Thres) + ',' + self.Active_Layer + ',' + str(self.min_dX) + ',' + str(self.min_dE))
    ra = gRunManager.GetUserRunAction()
    oFile = ra.Ofile

    Prepoint = step.GetPreStepPoint()
    Preposi = Prepoint.GetPosition()
    Pre_x = Preposi.getX()
    Pre_y = Preposi.getY()
    Pre_z = Preposi.getZ()
    PreE = Prepoint.GetKineticEnergy()
    Postpoint = step.GetPostStepPoint()
    Postposi = Postpoint.GetPosition()
    Post_x = Postposi.getX()
    Post_y = Postposi.getY()
    Post_z = Postposi.getZ()
    PostE = Postpoint.GetKineticEnergy()   
    dEt = step.GetTotalEnergyDeposit()
    dEn = step.GetNonIonizingEnergyDeposit()
    dx = step.GetStepLength()
    dE = dEt - dEn

    Track = step.GetTrack()
    ID = Track.GetTrackID()
    Particle = Track.GetDefinition()
    Volume = Track.GetVolume()
    AtomicM = Particle.GetAtomicMass()
    pName = Particle.GetParticleName()
    vName = Volume.GetName()
    depth = 0

    ###############################################################

    if AtomicM > self.AtomicM_Thres and vName == self.Active_Layer and dx > self.min_dX and dE > self.min_dE:

        oFile.write(str(vName))
	oFile.write('          ')
	oFile.write(str(pName))  
	oFile.write('          ')
	oFile.write('%i'%ID)
	oFile.write('          ')
	oFile.write('%f'%dEt)
	oFile.write('          ')
	oFile.write('%f'%dEn)
	oFile.write('          ')
	oFile.write('%f'%dE)
	oFile.write('          ')
	oFile.write('%f'%PreE)
	oFile.write('          ')
	oFile.write('%f'%PostE)
	oFile.write('          ')
	oFile.write('%f'%dx)
	oFile.write('          ')
        oFile.write('%f'%Pre_x)
	oFile.write('          ')
        oFile.write('%f'%Pre_y)
	oFile.write('          ')
        oFile.write('%f'%Pre_z)
	oFile.write('          ')
        oFile.write('%f'%Post_x)
	oFile.write('          ')
        oFile.write('%f'%Post_y)
	oFile.write('          ')
        oFile.write('%f'%Post_z)
	oFile.write('\n')
	oFile.write(str(vName))
	oFile.write('          ')

    elif AtomicM > self.AtomicM_Thres and self.Active_Layer == "None" and dx > self.min_dX and dE > self.min_dE:

	oFile.write(str(vName))
	oFile.write('          ')
	oFile.write(str(pName))  
	oFile.write('          ')
	oFile.write('%i'%ID)
	oFile.write('          ')
	oFile.write('%f'%dEt)
	oFile.write('          ')
	oFile.write('%f'%dEn)
	oFile.write('          ')
	oFile.write('%f'%dE)
	oFile.write('          ')
	oFile.write('%f'%PreE)
	oFile.write('          ')
	oFile.write('%f'%PostE)
	oFile.write('          ')
	oFile.write('%f'%dx)
	oFile.write('          ')
        oFile.write('%f'%Pre_x)
	oFile.write('          ')
        oFile.write('%f'%Pre_y)
	oFile.write('          ')
        oFile.write('%f'%Pre_z)
	oFile.write('          ')
        oFile.write('%f'%Post_x)
	oFile.write('          ')
        oFile.write('%f'%Post_y)
	oFile.write('          ')
        oFile.write('%f'%Post_z)
	oFile.write('\n')
	oFile.write(str(vName))
	oFile.write('          ')

    else:
        pass

 
            

