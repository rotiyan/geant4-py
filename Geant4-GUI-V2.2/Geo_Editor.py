from Geant4 import *

import tkMessageBox

import g4py.NISTmaterials

from Tkinter import *

# import material list
from Geant4_Material_List import *

# import class list
from Geant4_Class_Define import *

rotTheta = 80
rotPhi = 10

import cPickle

# Define sub functions
def Save_File(path):
    temp_path = 'Target/' + path
    file_path = open(temp_path, 'wb')
    temp_str = cPickle.dump(Buffer, file_path)
    file_path.close()
    tkMessageBox.showinfo("Message", "File Saved")

def Draw_pic():
   # Initial Visulization 
   gControlExecute("oglx_Geo_editor.mac")
   gRunManager.GeometryHasBeenModified()
   gApplyUICommand("/vis/viewer/flush")

def cmd_rotateTheta():
    global rotTheta
    rotTheta +=5
    gApplyUICommand("/vis/viewer/set/viewpointThetaPhi %f %f"%(rotTheta,rotPhi))

def cmd_rotatePhi():
    global rotPhi
    rotPhi +=5
    gApplyUICommand("/vis/viewer/set/viewpointThetaPhi %f %f"%(rotTheta,rotPhi))


def cmd_rotateReset():
    gApplyUICommand("/vis/viewer/reset")

def cmd_expand():
    gApplyUICommand("/vis/viewer/zoom 1.2")

def cmd_up():
    gApplyUICommand("/vis/viewer/pan "   + " 0.  0.01  mm")

def cmd_down():
        gApplyUICommand("/vis/viewer/pan " +  " 0.  -0.01  mm")

def cmd_right():
        gApplyUICommand("/vis/viewer/pan " +  " -0.01  0.  mm")

def cmd_left():
        gApplyUICommand("/vis/viewer/pan "   + " 0.01  0.  mm")

def cmd_shrink():
        gApplyUICommand("/vis/viewer/zoom 0.8")

def WorldDefine(mother):
	#New world 
	global detector
        global Buffer
	detector = MyDetectorConstruction()
        Buffer = Parameter_Pass()
	window1 = Toplevel(mother)
	title1 = Label(window1, text="Simulation Environment Defination")
	title1.grid(row=1, column=0, columnspan=6)
	#Layer Name Input, StringVar
	SideL = Label(window1, bg="yellow",  text="Side Length in mm (Square)")
	SideVar=DoubleVar()
	SideVar.set("50")
	layer = Entry(window1, textvariable=SideVar, width=25)
	SideL.grid(row=2, column=0, sticky=W)
	layer.grid(row=2, column=1, columnspan=5, sticky=W)
	# Material Input, Pull Down Menu
	LayerLabel = Label(window1, bg="yellow",  text="World Composition")
	LayerLabel.grid(row=3, column=0, sticky=W)
	WorldMVar = StringVar()
	WorldMVar.set("G4_AIR")
	WorldMName = Menubutton(window1, text='Material Name List', relief=RAISED)
	WorldMName.menu = Menu(WorldMName, tearoff=0)
	WorldMName["menu"] = WorldMName.menu
	for index in World_List:
	    WorldMName.menu.add_radiobutton(label=index, variable=WorldMVar, value=index, activebackground="red")
	WorldMName.grid(row=3, column=1, sticky=W)
	# Create Botton
	def Create_World():
	    #Gather all the parameters
	    detector.create_world(side=SideVar.get(), material=WorldMVar.get())
            Buffer.world_add(side=SideVar.get(), material=WorldMVar.get())
	    tkMessageBox.showinfo("Message", "Simulation Environment Created")
            # Initilization for visulization 
            physics_list = QGSP_BIC_HP()
            gRunManager.SetUserInitialization(physics_list)
	    gRunManager.SetUserInitialization(detector)
            gRunManager.Initialize()
	    window1.destroy()

	CreateBotton = Button(window1, text="Create The World!", command=Create_World, bg="red")
	CreateBotton.grid(row=4, column=1, sticky=W)

def GeoDefine(mother):
        window = Toplevel(mother)
	title1 = Label(window, text="Target Geometry Defination")
	title1.grid(row=1, column=0, columnspan=6)
	#Layer Name Input, StringVar
	LayerName = Label(window, bg="yellow",  text="Layer Name")
        NameVar=StringVar()
        NameVar.set("Layer Name")
        layer = Entry(window, textvariable=NameVar, width=25)
	LayerName .grid(row=2, column=0, sticky=W)
        layer.grid(row=2, column=1, columnspan=5, sticky=W)
	#Side X Input, DoubleVar
	SideX = Label(window, bg="yellow",  text="X Axis Dimension (um)")
        SideXVar=DoubleVar()
        SideXVar.set("10")
        layer = Entry(window, textvariable=SideXVar, width=25)
	SideX.grid(row=3, column=0, sticky=W)
        layer.grid(row=3, column=1, columnspan=5, sticky=W)
	#Side Y Input, DoubleVar
	SideY = Label(window, bg="yellow",  text="Y Axis Dimension (um)")
        SideYVar=DoubleVar()
        SideYVar.set("10")
        layer = Entry(window, textvariable=SideYVar, width=25)
	SideY.grid(row=4, column=0, sticky=W)
        layer.grid(row=4, column=1, columnspan=5, sticky=W)
	#Side Z Input, DoubleVar
	SideZ = Label(window, bg="yellow",  text="Z Axis Dimension (um)")
        SideZVar=DoubleVar()
        SideZVar.set("10")
        layer = Entry(window, textvariable=SideZVar, width=25)
	SideZ.grid(row=5, column=0, sticky=W)
        layer.grid(row=5, column=1, columnspan=5, sticky=W)
	# Translation Input x	
        TranslationVec = Label(window, bg="yellow",  text="Translation-X(um)")
	TranslationVec.grid(row=6, column=0, sticky=W)
        TranslationVecXVar=DoubleVar()
        TranslationVecXVar.set(0.0)
        layer = Entry(window, textvariable=TranslationVecXVar, width=25)
        layer.grid(row=6, column=1, sticky=W)
	# Translation Input y	
        TranslationVec = Label(window, bg="yellow",  text="Translation-Y(um)")
	TranslationVec.grid(row=7, column=0, sticky=W)    
        TranslationVecYVar=DoubleVar()
        TranslationVecYVar.set(0.0)
        layer = Entry(window, textvariable=TranslationVecYVar, width=25)
        layer.grid(row=7, column=1, sticky=W)
	# Translation Input y
        TranslationVec = Label(window, bg="yellow",  text="Translation-Z(um)")
	TranslationVec.grid(row=8, column=0, sticky=W)
        TranslationVecZVar=DoubleVar()
        TranslationVecZVar.set(0.0)
        layer = Entry(window, textvariable=TranslationVecZVar, width=25)
        layer.grid(row=8, column=1, sticky=W)
	# Material Input, Pull Down Menu
	LayerLabel = Label(window, bg="yellow",  text="Target Composition")
	LayerLabel.grid(row=9, column=0, sticky=W)
        MaterialNameVar = StringVar()
        MaterialNameVar.set("G4_Si")
        MaterialName = Menubutton(window, text='Material Name List', relief=RAISED)
        MaterialName.menu = Menu(MaterialName, tearoff=0)
        MaterialName["menu"] = MaterialName.menu
        for index in Material_Name_List:
            MaterialName.menu.add_radiobutton(label=index, variable=MaterialNameVar, value=index, activebackground="red")
        MaterialName.grid(row=9, column=1, sticky=W)
	# Color of the Material, pull down menu
	LayerLabel = Label(window, bg="yellow",  text="Layer Color")
	LayerLabel.grid(row=10, column=0, sticky=W)
        ColorNameVar = StringVar()
        ColorNameVar.set("White")
        ColorName = Menubutton(window, text='Color List', relief=RAISED)
        ColorName.menu = Menu(ColorName, tearoff=0)
        ColorName["menu"] = ColorName.menu
        Color_List = ["White", "Gray", "Black", "Red", "Green", "Blue", "Cyan", "Magenta", "Yellow"]
        for index in Color_List:
            ColorName.menu.add_radiobutton(label=index, variable=ColorNameVar, value=index, activebackground=index)
        ColorName.grid(row=10, column=1, sticky=W)
	# Create Botton
        def Create_Layer():
            #Gather all the parameters
            Translation_temp = [TranslationVecXVar.get()/1000, TranslationVecYVar.get()/1000, TranslationVecZVar.get()/1000]
            ColorNameVar_temp = ColorNameVar.get()
            if ColorNameVar_temp == "White": color_vec = [1.0, 1.0, 1.0]
            elif ColorNameVar_temp == "Gray": color_vec = [0.5, 0.5, 0.5]
            elif ColorNameVar_temp == "Black": color_vec = [0.0, 0.0, 0.0]
            elif ColorNameVar_temp == "Red": color_vec = [1.0, 0.0, 0.0]
            elif ColorNameVar_temp == "Green": color_vec = [0.0, 1.0, 0.0]
            elif ColorNameVar_temp == "Blue": color_vec = [0.0, 0.0, 1.0]
            elif ColorNameVar_temp == "Cyan": color_vec = [0.0, 1.0, 1.0]
            elif ColorNameVar_temp == "Magenta": color_vec = [1.0, 0.0, 1.0]
            elif ColorNameVar_temp == "Yellow": color_vec = [1.0, 1.0, 0.0]
            Material_Temp = G4Material.GetMaterial(MaterialNameVar.get())
            detector.create_box(name = NameVar.get(),
                         sidex = SideXVar.get()/1000,
                         sidey = SideYVar.get()/1000,
                         sidez = SideZVar.get()/1000,
                         translation = Translation_temp,
                         material = Material_Temp,
                         color = color_vec,
                         mother = 'world')
            Buffer.Layer_add(name = NameVar.get(),
                         sidex = SideXVar.get()/1000,
                         sidey = SideYVar.get()/1000,
                         sidez = SideZVar.get()/1000,
                         translation = Translation_temp,
                         material = MaterialNameVar.get(),
                         color = color_vec,
                         mother = 'world')
            tkMessageBox.showinfo("Message", "Layer Added To The Target")
	
	CreateBotton = Button(window, text="Add This Layer To Your Traget!", command=Create_Layer, bg="red")
	CreateBotton.grid(row=11, column=0, columnspan=6)
	# Finish Botton
        def Finish_cmd():
            gControlExecute("oglx_Geo_editor.mac")
            gRunManager.GeometryHasBeenModified()           
            gApplyUICommand("/vis/viewer/flush")
            tkMessageBox.showinfo("Message", "Target Setup Finished")
            gRunManager.BeamOn(0)
            window.destroy()
 
	CreateBotton = Button(window, text="Finish Your Target Setup And Exit", command=Finish_cmd, bg="red")
	CreateBotton.grid(row=12, column=0, columnspan=6)

# Define the main function
def Geo_Editor_cmd(mother):
   MainWindow = Toplevel(mother)
   title = Label(MainWindow, text="Target Geometry Editor", bg="red")
   title.grid(row=0, column=0, columnspan=6)
   # world defination
   layerLabel = Label(MainWindow, bg="yellow",  text="World Defination")
   layerLabel.grid(row=1, column=0, sticky=W)
   GeoDefBut = Button(MainWindow, bg="orange", text="Simulation Environment Defination", command=lambda : WorldDefine(mother=MainWindow))
   GeoDefBut.grid(row=1, column=1, sticky=W)

   # detector defination 
   layerLabel = Label(MainWindow, bg="yellow",  text="Target Geometry")
   layerLabel.grid(row=2, column=0, sticky=W)
   GeoDefBut = Button(MainWindow, bg="orange", text="Target Geometry Defination", command=lambda : GeoDefine(mother=MainWindow))
   GeoDefBut.grid(row=2, column=1, sticky=W)

   # File name Input 
   layerLabel = Label(MainWindow, bg="yellow",  text="Output File Name(ex:MyTarget.txt)")
   file_Name = StringVar()
   file_Name.set("MyTarget.txt")
   layer = Entry(MainWindow, textvariable=file_Name, width=35)
   layerLabel.grid(row=3, column=0, sticky=W)
   layer.grid(row=3, column=1, sticky=W)

   # Draw
   visLabel = Label(MainWindow, text="Update Viewer", bg="yellow")
   visLabel.grid(row=4, column=0, sticky=W)
   drawBut = Button(MainWindow, bg="orange", text="DRAW Target Geometry", command=Draw_pic)
   drawBut.grid(row=4, column=1, sticky=W)

   # Save
   visLabel = Label(MainWindow, text="Save The Target", bg="yellow")
   visLabel.grid(row=5, column=0, sticky=W)
   drawBut = Button(MainWindow, bg="orange", text="Save To Target Folder", command=lambda : Save_File(path=file_Name.get()))
   drawBut.grid(row=5, column=1, sticky=W)

   #Zoom in/out Pan X Y 
   visLabel = Label(MainWindow, text="Viewer Options", bg="yellow")
   expandBut = Button(MainWindow, text="Zoom in", command=cmd_expand, bg="orange")
   shrinkBut = Button(MainWindow, text="Zoom out", command=cmd_shrink, bg="orange")
   visLabel.grid(row=6, column=0, sticky=W)
   expandBut.grid(row=6, column=1, sticky=W)
   shrinkBut.grid(row=6, column=2, sticky=W)

   upBut = Button(MainWindow, text="Up", command=cmd_up, bg="cyan")
   downBut = Button(MainWindow, text="Down", command=cmd_down, bg="cyan")
   upBut.grid(row=7, column=1, sticky=W)
   downBut.grid(row=9, column=1, sticky=W)

   leftBut = Button(MainWindow, text="Left", command=cmd_left, bg="cyan")
   rightBut = Button(MainWindow, text="Right", command=cmd_right, bg="cyan")
   leftBut.grid(row=8, column=0, columnspan=1)
   rightBut.grid(row=8, column=1, columnspan=3)

   # Rotate
   rotLabel = Label(MainWindow,text="Rotate Options",bg="yellow")
   rotLabel.grid(row=10,column=0,sticky=W)
   thetaBut = Button(MainWindow,text="Rotate(theta)",command=cmd_rotateTheta, bg="orange")
   phiBut   = Button(MainWindow,text="Rotate(ph)",command=cmd_rotatePhi, bg="orange")
   resetBut = Button(MainWindow,text="Reset",command=cmd_rotateReset, bg="magenta")
   thetaBut.grid(row=10,column=1,sticky=W)
   phiBut.grid(row=10,column=2, sticky=W)
   resetBut.grid(row=8,column=1, sticky=W)

