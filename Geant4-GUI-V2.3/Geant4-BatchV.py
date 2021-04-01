from Geant4 import *
import g4py.NISTmaterials
import os
import random 
import time
import pickle
import argparse
import yaml

from datetime import datetime

# import material list
from Geant4_Material_List import *

# import class list
from Geant4_Class_Define import *

parser = argparse.ArgumentParser(description='Yaml File Name')
parser.add_argument('--Setupfile', type = str, required=True, default = 'defaultsetup.yml')
parser.add_argument('--Seed', default='',type = int, help = 'Random Seed For Geant4 Simulation')

args = parser.parse_args()

# creating random seed
seed = args.Seed
if args.Seed=='':
   seed = random.randint(10,800000)


rand_engine = Ranlux64Engine()
HepRandom.setTheEngine(rand_engine)
HepRandom.setTheSeed(seed)

# Simulation Setup

file_name = args.Setupfile
temp = file_name
file_Yaml = open(temp, 'r')
file_data = file_Yaml.read()
file_Yaml.close()
Setup_data = yaml.load(file_data, Loader=yaml.FullLoader)

# Run the simulation
start = time.clock()
Event_num = Setup_data['Event_num']

# set physics list
PL_name = Setup_data['PL_name']
if PL_name == "QGSP":
   physics_list = QGSP()
elif PL_name == "QGSP_EMV":
   physics_list = QGSP_EMV()
elif PL_name == "QGSC":
   physics_list = QGSC()
elif PL_name == "QGSC_EMV":
   physics_list = QGSC_EMV()
elif PL_name == "QGSP_EFLOW":
   physics_list = QGSP_EFLOW()
elif PL_name == "QGSP_BERT":
   physics_list = QGSP_BERT()
elif PL_name == "QGSP_BERT_EMV":
   physics_list = QGSP_BERT_EMV()
elif PL_name == "QGSP_BERT_HP":
   physics_list = QGSP_BERT_HP()
elif PL_name == "QGSP_BERT_TRV":
   physics_list = QGSP_BERT_TRV()
elif PL_name == "QGSP_BIC":
   physics_list = QGSP_BIC()
elif PL_name == "QGSP_BIC_HP":
   physics_list = QGSP_BIC_HP()
elif PL_name == "QGSP_NEQ":
   physics_list = QGSP_NEQ()
elif PL_name == "QGSP_EMV_NQE":
   physics_list = QGSP_EMV_NQE()
elif PL_name == "FTFP_BERT":
   physics_list = FTFP_BERT()
elif PL_name == "FTFP_EMV":
   physics_list = FTFP_EMV()
else:
   physics_list = QGSP_BIC_HP()
gRunManager.SetUserInitialization(physics_list)

# set user run action
myRA = MyUserRunAction()
saving_path = 'OutputFile/'
OFP_name = Setup_data['OFP_name']
temp = saving_path + "%d_"%seed + OFP_name
myRA.SetFilePath(temp)
gRunManager.SetUserAction(myRA)

# set geometry
file_TD = Setup_data['file_TD']
detector = MyDetectorConstruction()
Buffer = Parameter_Pass()
temp = 'Target/' + file_TD
if os.path.isfile(temp):
    data_str = open(temp, 'rb')
    Buffer = pickle.load(data_str)
    detector.create_world(side=Buffer.world__side, material=Buffer.world__material)
    for i in range(Buffer.layer_num):
        temp_name = Buffer.layer_material[i]
        print(temp_name)
        detector.create_box(name = Buffer.layer_name[i],
                     sidex = Buffer.layer_sidex[i],
                     sidey = Buffer.layer_sidey[i],
                     sidez = Buffer.layer_sidez[i],
                     translation = Buffer.layer_translation[i],
                     material =  G4Material.GetMaterial(temp_name),
                     color = Buffer.layer_color[i],
                     mother = Buffer.layer_mother[i])
    gRunManager.SetUserInitialization(detector)
else:
    raise Exception("Invalid Target Define File Name")

# set user stepping action
AtomicM_Thres = Setup_data['AtomicM_Thres']
Active_Layer = Setup_data['Active_Layer']
min_dX = Setup_data['min_dX']
min_dE = Setup_data['min_dE']

mySA= MyUserSteppingAction(AtomicM_Thres, Active_Layer, min_dX, min_dE)
gRunManager.SetUserAction(mySA)

# set particle
file_NS = Setup_data['file_NS']
particle_path = 'ParticleFile/'
temp = particle_path + file_NS
if os.path.isfile(temp):
    primary_generator_action = MyPrimaryGeneratorAction(temp)
    gRunManager.SetUserAction(primary_generator_action)
else:
    raise Exception("Invalid Particle Setup File Name")

# Initialise
gRunManager.Initialize()
gTrackingManager.SetStoreTrajectory(1)
gApplyUICommand("/tracking/storeTrajectory 1")
gApplyUICommand("/tracking/verbose 1")

# Run Simulation
gRunManager.BeamOn(Event_num)

# User Action
end = time.clock()
t = (end-start)/60
print "Total Computation Time: %s mins" %(str(t))

