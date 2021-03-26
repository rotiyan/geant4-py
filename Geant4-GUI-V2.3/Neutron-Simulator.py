from Geant4 import *

from IPython.display import Image

import tkMessageBox

import g4py.NISTmaterials

import os

import random 

from Tkinter import *

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

# creating length unit 
micrometer= um= mm/1000

# Initial Visulization 
gControlExecute("oglx.mac")

# define the Sub GUI structure
class Application(Frame):
    def cmd_rotateTheta(self):
       self.rotTheta +=5
       gApplyUICommand("/vis/viewer/set/viewpointThetaPhi %f %f"%(self.rotTheta,self.rotPhi))

    def cmd_rotatePhi(self):
       self.rotPhi +=5
       gApplyUICommand("/vis/viewer/set/viewpointThetaPhi %f %f"%(self.rotTheta,self.rotPhi))


    def cmd_rotateReset(self):
       self.rotTheta=80
       self.rotPhi=10
       gApplyUICommand("/vis/viewer/set/viewpointThetaPhi %f %f"%(self.rotTheta,self.rotPhi))


    def cmd_expand(self):
        gApplyUICommand("/vis/viewer/zoom 1.2")

    def cmd_up(self):
        gApplyUICommand("/vis/viewer/pan "   + " 0.  10. mm")

    def cmd_down(self):
        gApplyUICommand("/vis/viewer/pan " +  " 0. -10.  mm")

    def cmd_right(self):
        gApplyUICommand("/vis/viewer/pan " +  " -1. 0.  mm")

    def cmd_left(self):
        gApplyUICommand("/vis/viewer/pan "   + " 1. 0. mm")

    def cmd_shrink(self):
        gApplyUICommand("/vis/viewer/zoom 0.8")

    def ConditionDef(self):
        #Condition Define
        window2 = Toplevel(self)
	title1 = Label(window2, text="Saving Condition Defination")
	title1.grid(row=1, column=0, columnspan=6)
	#Condition 1, atomic mass
	AtomicThres = Label(window2, bg="yellow",  text="Minimum Atomic Mass")
        self.AtomicM_Thres=DoubleVar()
        self.AtomicM_Thres.set("0")
        layer = Entry(window2, textvariable=self.AtomicM_Thres, width=25)
	AtomicThres.grid(row=2, column=0, sticky=W)
        layer.grid(row=2, column=1, columnspan=5, sticky=W)
	#Condition 2, active layer
	ActiveLayer = Label(window2, bg="yellow",  text="Active Layer Name")
        self.Active_Layer=StringVar()
        self.Active_Layer.set("ex: My First Layer")
        layer = Entry(window2, textvariable=self.Active_Layer, width=25)
	ActiveLayer.grid(row=3, column=0, sticky=W)
        layer.grid(row=3, column=1, columnspan=5, sticky=W)
	#Condition 3, active layer
	MinidX = Label(window2, bg="yellow",  text="Minimum Step Length(um)")
        self.min_dX=DoubleVar()
        self.min_dX.set("0")
        layer = Entry(window2, textvariable=self.min_dX, width=25)
	MinidX.grid(row=4, column=0, sticky=W)
        layer.grid(row=4, column=1, columnspan=5, sticky=W)
	#Condition 4, active layer
	MinidE = Label(window2, bg="yellow",  text="Minimum Energy Deposition(eV)")
        self.min_dE=DoubleVar()
        self.min_dE.set("0")
        layer = Entry(window2, textvariable=self.min_dE, width=25)
	MinidE.grid(row=5, column=0, sticky=W)
        layer.grid(row=5, column=1, columnspan=5, sticky=W)
        # Create Botton
        def Confirm_cmd():
            tkMessageBox.showinfo("Message", "Succeed")
	    window2.destroy()
	CreateBotton = Button(window2, text="Confirm Your Conditions", command=Confirm_cmd, bg="red")
	CreateBotton.grid(row=6, column=0, columnspan=6)

    def Beam_on(self):
        # set physics list
        if self.PhysicsListVar.get() == "QGSP":
           physics_list = QGSP()
        elif self.PhysicsListVar.get() == "QGSP_EMV":
           physics_list = QGSP_EMV()
        elif self.PhysicsListVar.get() == "QGSC":
           physics_list = QGSC()
        elif self.PhysicsListVar.get() == "QGSC_EMV":
           physics_list = QGSC_EMV()
        elif self.PhysicsListVar.get() == "QGSP_EFLOW":
           physics_list = QGSP_EFLOW()
        elif self.PhysicsListVar.get() == "QGSP_BERT":
           physics_list = QGSP_BERT()
        elif self.PhysicsListVar.get() == "QGSP_BERT_EMV":
           physics_list = QGSP_BERT_EMV()
        elif self.PhysicsListVar.get() == "QGSP_BERT_HP":
           physics_list = QGSP_BERT_HP()
        elif self.PhysicsListVar.get() == "QGSP_BERT_TRV":
           physics_list = QGSP_BERT_TRV()
        elif self.PhysicsListVar.get() == "QGSP_BIC":
           physics_list = QGSP_BIC()
        elif self.PhysicsListVar.get() == "QGSP_BIC_HP":
           physics_list = QGSP_BIC_HP()
        elif self.PhysicsListVar.get() == "QGSP_NEQ":
           physics_list = QGSP_NEQ()
        elif self.PhysicsListVar.get() == "QGSP_EMV_NQE":
           physics_list = QGSP_EMV_NQE()
        elif self.PhysicsListVar.get() == "FTFP_BERT":
           physics_list = FTFP_BERT()
        elif self.PhysicsListVar.get() == "FTFP_EMV":
           physics_list = FTFP_EMV()
        else:
           physics_list = QGSP_BIC_HP()
        gRunManager.SetUserInitialization(physics_list)
        # set user run action
	myRA = MyUserRunAction()
        saving_path = 'Output File/'
        temp = saving_path + self.file_OP.get()
	myRA.SetFilePath(temp)
	gRunManager.SetUserAction(myRA)
        # set user stepping action
	mySA= MyUserSteppingAction(self.AtomicM_Thres.get(), self.Active_Layer.get(), self.min_dX.get(), self.min_dE.get())
	gRunManager.SetUserAction(mySA)
	# set geometry
	detector = MyDetectorConstruction()
        Buffer = Parameter_Pass()
        temp = 'Target/' + self.file_TD.get()
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
	# set particle
        particle_path = 'Particle File/'
        temp = particle_path + self.file_NS.get()
        if os.path.isfile(temp):
	    primary_generator_action = MyPrimaryGeneratorAction(temp)
	    gRunManager.SetUserAction(primary_generator_action)
        else:
            raise Exception("Invalid Particle Setup File Name")

	# Initialise
	gRunManager.Initialize()
	# Set Process Activation
	for i in self.processList:
	    if self.processVar[i].get() == 0:
	       gProcessTable.SetProcessActivation(i, 0)
	       print("Process " + i + " inactivated")
	    else:
	       gProcessTable.SetProcessActivation(i, 1)
	       print("Process " + i + " activated")
	# Set Visualization
	gTrackingManager.SetStoreTrajectory(1)
	gApplyUICommand("/tracking/storeTrajectory 1")
	gApplyUICommand("/tracking/verbose 1")
	gApplyUICommand("/vis/viewer/flush")

        # Run Simulation
	gRunManager.BeamOn(self.layerVar.get())

    def Draw_pic(self):
	gApplyUICommand("/vis/viewer/flush")
		
    def createWidgets(self):

        #exit row = 0
        exitBut = Button(self, bg="red", text="QUIT", command=self.quit)
        exitBut.grid(row=0, column=5, sticky=W)

        #run row = 0
        runBut = Button(self, bg="green", text="RUN", command=self.Beam_on)
        runBut.grid(row=0, column=0, sticky=W)

        #title and header    row=0, 1
        title = Label(self, text="Geant4 Particle Simulator--SMU Relaibility Lab", bg="red")
        title.grid(row=1, column=0, columnspan=4)

        # number of Particles
        layerLabel = Label(self, bg="yellow",  text="Number of Events(Particles)")
        self.layerVar=IntVar()
        self.layerVar.set(10)
        layer = Entry(self, textvariable=self.layerVar, width=15)
        layerLabel.grid(row=2, column=0, sticky=W)
        layer.grid(row=2, column=1, sticky=W)

        # set the physics list
	PhysicsListLabel = Label(self, bg="yellow", text="Physics List(more info in help)")
	PhysicsListLabel.grid(row=3, column=0, sticky=W)
	self.Physics_List = ["QGSP","QGSP_EMV","QGSC","QGSC_EMV","QGSP_EFLOW","QGSP_BERT","QGSP_BERT_EMV","QGSP_BERT_HP","QGSP_BERT_TRV","QGSP_BIC","QGSP_BIC_HP","QGSP_NEQ","QGSP_EMV_NQE","QGSP_BERT_NQE","FTFP_BERT","FTFP","FTFP_EMV"]
	self.PhysicsListVar = StringVar()
        self.PhysicsListVar.set("QGSP_BIC_HP")
        PhysicsList = Menubutton(self, text='Physics List', relief=RAISED, bg='orange')
        PhysicsList.menu = Menu(PhysicsList, tearoff=0)
        PhysicsList["menu"] = PhysicsList.menu
        for index in self.Physics_List:
            PhysicsList.menu.add_radiobutton(label=index, variable=self.PhysicsListVar, value=index, activebackground="green")
        PhysicsList.grid(row=3, column=1, sticky=W)

	# File name Input
        layerLabel=Label(self, bg="yellow",  text="Particel Setup File(ex:beam.mac)")
        self.file_NS=StringVar()
        self.file_NS.set("MonoE-Neutron.mac")
        layer = Entry(self, textvariable=self.file_NS, width=25)
        layerLabel.grid(row=4, column=0, sticky=W)
        layer.grid(row=4, column=1, sticky=W)

	# File name Input 2
        layerLabel=Label(self, bg="yellow",  text="Target Define File(ex:MyTarget.txt)")
        self.file_TD=StringVar()
        self.file_TD.set("MyTarget.txt")
        layer = Entry(self, textvariable=self.file_TD, width=25)
        layerLabel.grid(row=5, column=0, sticky=W)
        layer.grid(row=5, column=1, sticky=W)

	# File name Input 3
        layerLabel = Label(self, bg="yellow",  text="Output File(ex:output.h5)")
        self.file_OP = StringVar()
        self.file_OP.set("output.txt")
        layer = Entry(self, textvariable=self.file_OP, width=25)
        layerLabel.grid(row=6, column=0, sticky=W)
        layer.grid(row=6, column=1, sticky=W)

	# Activate Processes 
	PhysicsProcessLabel = Label(self, bg="yellow", text="Activate Processes")
	PhysicsProcessLabel.grid(row=7, column=0, sticky=W)
	procTab = {}
	self.processList = ["hadElastic","neutronInelastic","protonInelastic","ionElastic","ionInelastic"]
	self.processVar = {}
        ProcessList = Menubutton(self, text='Process List', relief=RAISED, bg='orange')
        ProcessList.menu = Menu(ProcessList, tearoff=0)
        ProcessList["menu"] = ProcessList.menu
        for index in self.processList:
            self.processVar[index] = IntVar()
            ProcessList.menu.add_checkbutton(label=index, variable=self.processVar[index], activebackground="green")
        ProcessList.grid(row=7, column=1, sticky=W)

        # set the saving condition
        SavingLabel = Label(self, bg="yellow", text="Data Saving Condition")
        SavingLabel.grid(row=8, column=0, sticky=W)
        ConditionBut = Button(self, bg="orange", text="Set Your Filter Condition", command=self.ConditionDef)
	ConditionBut.grid(row=8, column=1, sticky=W)

	# set cuts row 14
	#cutLabel = Label(self, bg="yellow",  text="Cut (mm)")

	#self.cutVar=DoubleVar()
	#self.cutVar.set(1.)
	#cut = Scale(self, orient=HORIZONTAL, length=400, from_=0., to=10., tickinterval=1., resolution=0.005, variable=self.cutVar, digits=5 )
	#cutLabel.grid(row=11, column=0, sticky=W)
	#cut.grid(row=11, column=1, columnspan=5, sticky=W)

	#draw 
        visLabel = Label(self, text="Update Viewer", bg="yellow")
        visLabel.grid(row=10, column=0, sticky=W)
        drawBut = Button(self, bg="orange", text="DRAW", command=self.Draw_pic)
        drawBut.grid(row=10, column=1, sticky=W)

        #Zoom in/out Pan X Y 
        visLabel = Label(self, text="Viewer Options", bg="yellow")
        expandBut = Button(self, text="Zoom in", command=self.cmd_expand, bg="orange")
        shrinkBut = Button(self, text="Zoom out", command=self.cmd_shrink, bg="orange")
        visLabel.grid(row=11, column=0, sticky=W)
        expandBut.grid(row=11, column=1, sticky=W)
        shrinkBut.grid(row=11, column=2, sticky=W)

        upBut = Button(self, text="Up", command=self.cmd_up, bg="cyan")
        downBut = Button(self, text="Down", command=self.cmd_down, bg="cyan")
        upBut.grid(row=12, column=1, sticky=W)
        downBut.grid(row=14, column=1, sticky=W)

        leftBut = Button(self, text="Left", command=self.cmd_left, bg="cyan")
        rightBut = Button(self, text="Right", command=self.cmd_right, bg="cyan")
        leftBut.grid(row=13, column=0, columnspan=1)
        rightBut.grid(row=13, column=1, columnspan=3)

        # Rotate
        self.rotTheta = 80
        self.rotPhi = 10
        rotLabel = Label(self,text="Rotate Options",bg="yellow")
        rotLabel.grid(row=15,column=0,sticky=W)
        thetaBut = Button(self,text="Rotate(theta)",command=self.cmd_rotateTheta, bg="orange")
        phiBut   = Button(self,text="Rotate(ph)",command=self.cmd_rotatePhi, bg="orange")
        resetBut = Button(self,text="Reset",command=self.cmd_rotateReset, bg="magenta")
        thetaBut.grid(row=15,column=1,sticky=W)
        phiBut.grid(row=15,column=2, sticky=W)
        resetBut.grid(row=13,column=1, sticky=W)

	
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()
        self.grid()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()


