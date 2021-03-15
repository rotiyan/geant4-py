from Geant4 import *

import g4py.NISTmaterials

import os

import random 

import time

import pickle

# import material list
from Geant4_Material_List import *

# import class list
from Geant4_Class_Define import *

# creating random seed
from datetime import datetime
seed = random.randint(10,800000)

rand_engine = Ranlux64Engine()
HepRandom.setTheEngine(rand_engine)
HepRandom.setTheSeed(seed)

flag = True

while flag:
        # Run the simulation
	start = time.clock()
        temp = input("Enter Total Event Number (Integer): \n")
	Event_Num = int(temp)

        # set physics list
	print "Physics List Name (default:QGSP_BIC_HP):"
        PL_name = raw_input()
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
        saving_path = 'Output File/'
	print "Output File Name (ex: Test.txt):"
        OFP_name = raw_input()
	temp = saving_path + OFP_name
	myRA.SetFilePath(temp)
	gRunManager.SetUserAction(myRA)

	# set geometry
	print "Target Define File(ex:MyTarget.txt):"
	file_TD = raw_input()
	detector = MyDetectorConstruction()
        Buffer = Parameter_Pass()
        temp = 'Target/' + file_TD
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

        # set user stepping action
	print "Minimum Atomic Mass:"
        AtomicM_Thres = raw_input()
	print "Active Layer Name:"
        Active_Layer = raw_input()
	print "Minimum Step Length:"
        min_dX = raw_input()
	print "Minimum Energy Deposition:"
        min_dE = raw_input()
        
	mySA= MyUserSteppingAction(AtomicM_Thres, Active_Layer, min_dX, min_dE)
	gRunManager.SetUserAction(mySA)

	# set particle
	print "Particel Setup File(ex:beam.mac):"
	file_NS = raw_input()
        particle_path = 'Particle File/'
        temp = particle_path + file_NS
	primary_generator_action = MyPrimaryGeneratorAction(temp)
	gRunManager.SetUserAction(primary_generator_action)

	# Initialise
	gRunManager.Initialize()
	gTrackingManager.SetStoreTrajectory(1)
	gApplyUICommand("/tracking/storeTrajectory 1")
	gApplyUICommand("/tracking/verbose 1")

	# Run Simulation
	gRunManager.BeamOn(Event_Num)

	# User Action
	end = time.clock()
	t = (end-start)/60
	print "Total Computation Time: %s mins" %(str(t))
	print "Continue? Y/N:"
	con = raw_input()
	if con == "Y":
	   print "New Simulation Session..."
	   continue
	elif con == "N":
	   flag = False
	   print "End of Session..."
	   break
	else:
	   print "Wrong Input"
