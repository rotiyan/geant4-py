from Geant4 import *

#import g4py.NISTmaterials
import h5py
import numpy
from array import array
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
        self.dt = h5py.special_dtype(vlen=str)
        self.Ofile = h5py.File(self.filename,"w")
        # Predefine the h5py file
        self.size = 100
        self.vNset = self.Ofile.create_dataset('Volume Name', (self.size,), maxshape=(None,), dtype=self.dt, chunks=(self.size,))
        self.pNset = self.Ofile.create_dataset('Particle Name', (self.size,), maxshape=(None,), dtype=self.dt, chunks=(self.size,))
        self.IDset = self.Ofile.create_dataset('ID Number', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.dEtset = self.Ofile.create_dataset('Total Energy Deposition', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.dEnset = self.Ofile.create_dataset('Nonionizing Energy Deposition', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.dEiset = self.Ofile.create_dataset('Ionizing Energy Deposition', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.PreEset = self.Ofile.create_dataset('Initial Energy', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.PostEset = self.Ofile.create_dataset('Post Energy', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.dXset = self.Ofile.create_dataset('Step Length', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.Prxset = self.Ofile.create_dataset('Initial X', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.Pryset = self.Ofile.create_dataset('Initial Y', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.Przset = self.Ofile.create_dataset('Initial Z', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.Poxset = self.Ofile.create_dataset('Post X', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.Poyset = self.Ofile.create_dataset('Post Y', (self.size,), maxshape=(None,), chunks=(self.size,))
        self.Pozset = self.Ofile.create_dataset('Post Z', (self.size,), maxshape=(None,), chunks=(self.size,))
        # Initialize the data array
        self.vName_array = [None]*self.size
        self.pName_array = [None]*self.size
        self.TrackID_array = numpy.arange(self.size)
        self.dEt_array = numpy.arange(self.size)
        self.dEn_array = numpy.arange(self.size)
        self.dEi_array = numpy.arange(self.size)
        self.PreE_array = numpy.arange(self.size)
        self.PostE_array = numpy.arange(self.size)
        self.dx_array = numpy.arange(self.size)
        self.Pre_x_array = numpy.arange(self.size)
        self.Pre_y_array = numpy.arange(self.size)
        self.Pre_z_array = numpy.arange(self.size)
        self.Post_x_array = numpy.arange(self.size)
        self.Post_y_array = numpy.arange(self.size)
        self.Post_z_array = numpy.arange(self.size)
        # index: count 100 outputs falg: mark 1st run
        self.index = 0
        self.flag = 1
    def EndOfRunAction(self, run):
        print ("*** Writing out dEdX")
        if self.index != 0:
            self.vNset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.pNset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.IDset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.dEtset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.dEnset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.dEiset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.PreEset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.PostEset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.dXset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.Prxset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.Pryset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.Przset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.Poxset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.Poyset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.Pozset.resize(self.vNset.shape[0]+self.index, axis=0)
            self.vNset[-self.index:] = self.vName_array[0:self.index]
            self.pNset[-self.index:] = self.pName_array[0:self.index]
            self.IDset[-self.index:] = self.TrackID_array[0:self.index]
            self.dEtset[-self.index:] = self.dEt_array[0:self.index]
            self.dEnset[-self.index:] = self.dEn_array[0:self.index]
            self.dEiset[-self.index:] = self.dEi_array[0:self.index]
            self.PreEset[-self.index:] = self.PreE_array[0:self.index]
            self.PostEset[-self.index:] = self.PostE_array[0:self.index]
            self.dXset[-self.index:] = self.dx_array[0:self.index]
            self.Prxset[-self.index:] = self.Pre_x_array[0:self.index]
            self.Pryset[-self.index:] = self.Pre_y_array[0:self.index]
            self.Przset[-self.index:] = self.Pre_z_array[0:self.index]
            self.Poxset[-self.index:] = self.Post_x_array[0:self.index]
            self.Poyset[-self.index:] = self.Post_y_array[0:self.index]
            self.Pozset[-self.index:] = self.Post_z_array[0:self.index]
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
        print ("In stepping action ")
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
        dEi = dEt - dEn

        Track = step.GetTrack()
        ID = Track.GetTrackID()
        Particle = Track.GetDefinition()
        Volume = Track.GetVolume()
        AtomicM = Particle.GetAtomicMass()
        pName = Particle.GetParticleName()
        vName = Volume.GetName()

    
        ##############################################################
        if self.Active_Layer != 'None':
            if (AtomicM > self.AtomicM_Thres and vName == self.Active_Layer and dx > self.min_dX/1000 and dE > self.min_dE):
                ra.vName_array[ra.index]    = vName
                ra.pName_array[ra.index]    = pName
                ra.TrackID_array[ra.index]  = ID
                ra.dEt_array[ra.index]      = dEt
                ra.dEn_array[ra.index]      = dEn
                ra.dEi_array[ra.index]      = dEi
                ra.PreE_array[ra.index]     = PreE
                ra.PostE_array[ra.index]    = PostE
                ra.dx_array[ra.index]       = dx
                ra.Pre_x_array[ra.index]    = Pre_x
                ra.Pre_y_array[ra.index]    = Pre_y
                ra.Pre_z_array[ra.index]    = Pre_z
                ra.Post_x_array[ra.index]   = Post_x
                ra.Post_y_array[ra.index]   = Post_y
                ra.Post_z_array[ra.index]   = Post_z
                ra.index                    = ra.index+1
            else:
                pass
        else:
            ra.vName_array[ra.index] = str(vName)
            ra.pName_array[ra.index] = str(pName)
            ra.TrackID_array[ra.index] = ID
            ra.dEt_array[ra.index] = dEt
            ra.dEn_array[ra.index] = dEn
            ra.dEi_array[ra.index] = dEi
            ra.PreE_array[ra.index] = PreE
            ra.PostE_array[ra.index] = PostE
            ra.dx_array[ra.index] = dx
            ra.Pre_x_array[ra.index] = Pre_x
            ra.Pre_y_array[ra.index] = Pre_y
            ra.Pre_z_array[ra.index] = Pre_z
            ra.Post_x_array[ra.index] = Post_x
            ra.Post_y_array[ra.index] = Post_y
            ra.Post_z_array[ra.index] = Post_z
            ra.index = ra.index+1

        if ra.index == ra.size and ra.flag == 1:
            ra.index = 0
            ra.flag = 0
            ra.vNset[:] = ra.vName_array
            ra.pNset[:] = ra.pName_array
            ra.IDset[:] = ra.TrackID_array
            ra.dEtset[:] = ra.dEt_array
            ra.dEnset[:] = ra.dEn_array
            ra.dEiset[:] = ra.dEi_array
            ra.PreEset[:] = ra.PreE_array
            ra.PostEset[:] = ra.PostE_array
            ra.dXset[:] = ra.dx_array
            ra.Prxset[:] = ra.Pre_x_array
            ra.Pryset[:] = ra.Pre_y_array
            ra.Przset[:] = ra.Pre_z_array
            ra.Poxset[:] = ra.Post_x_array
            ra.Poyset[:] = ra.Post_y_array
            ra.Pozset[:] = ra.Post_z_array
        elif ra.index == ra.size and ra.flag == 0:
            ra.index = 0
            ra.vNset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.pNset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.IDset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.dEtset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.dEnset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.dEiset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.PreEset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.PostEset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.dXset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.Prxset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.Pryset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.Przset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.Poxset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.Poyset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.Pozset.resize(ra.vNset.shape[0]+ra.size, axis=0)
            ra.vNset[-ra.size:] = ra.vName_array
            ra.pNset[-ra.size:] = ra.pName_array
            ra.IDset[-ra.size:] = ra.TrackID_array
            ra.dEtset[-ra.size:] = ra.dEt_array
            ra.dEnset[-ra.size:] = ra.dEn_array
            ra.dEiset[-ra.size:] = ra.dEi_array
            ra.PreEset[-ra.size:] = ra.PreE_array
            ra.PostEset[-ra.size:] = ra.PostE_array
            ra.dXset[-ra.size:] = ra.dx_array
            ra.Prxset[-ra.size:] = ra.Pre_x_array
            ra.Pryset[-ra.size:] = ra.Pre_y_array
            ra.Przset[-ra.size:] = ra.Pre_z_array
            ra.Poxset[-ra.size:] = ra.Post_x_array
            ra.Poyset[-ra.size:] = ra.Post_y_array
            ra.Pozset[-ra.size:] = ra.Post_z_array
