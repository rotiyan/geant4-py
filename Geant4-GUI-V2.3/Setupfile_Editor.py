from Geant4 import *

import tkMessageBox

import g4py.NISTmaterials

from Tkinter import *

import yaml

# Main Function

def Setupfile_Editor_cmd(mother):
   MainWindow = Toplevel(mother)
   title = Label(MainWindow, text="Batch Mode Setupfile Editor", bg="red")
   title.grid(row=0, column=0, columnspan=6)

   # File name Input
   layerLabel = Label(MainWindow, bg="yellow",  text="Yaml File Name(ex:setup.yml)")
   layerLabel.grid(row=1, column=0, sticky=W)
   file_Name = StringVar()
   file_Name.set("setup.yml")
   layer = Entry(MainWindow, textvariable=file_Name, width=35)
   layer.grid(row=1, column=1, sticky=W)

   # Total Event NUmber
   layerLabel = Label(MainWindow, bg="yellow",  text="Total Event Number")
   layerLabel.grid(row=2, column=0, sticky=W)
   Event_num=IntVar()
   Event_num.set(0)
   layer = Entry(MainWindow, textvariable=Event_num, width=25)
   layer.grid(row=2, column=1, sticky=W)

   # Physics List
   layerLabel = Label(MainWindow, bg="yellow",  text="Physics List Name")
   layerLabel.grid(row=3, column=0, sticky=W)
   PL_name=StringVar()
   PL_name.set("QGSP_BIC_HP")
   layer = Entry(MainWindow, textvariable=PL_name, width=25)
   layer.grid(row=3, column=1, sticky=W)

   # Output File Name
   layerLabel = Label(MainWindow, bg="yellow",  text="Output File Name(ex:output.h5)")
   layerLabel.grid(row=4, column=0, sticky=W)
   OFP_name=StringVar()
   OFP_name.set("output.txt")
   layer = Entry(MainWindow, textvariable=OFP_name, width=25)
   layer.grid(row=4, column=1, sticky=W)

   # Traget Define File
   layerLabel = Label(MainWindow, bg="yellow",  text="Target Define File(ex:MyTarget.txt)")
   layerLabel.grid(row=5, column=0, sticky=W)
   file_TD=StringVar()
   file_TD.set("MyTarget.txt")
   layer = Entry(MainWindow, textvariable=file_TD, width=25)
   layer.grid(row=5, column=1, sticky=W)

   # Minimum Atomic Mass
   layerLabel = Label(MainWindow, bg="yellow",  text="Minimum Atomic Mass")
   layerLabel.grid(row=6, column=0, sticky=W)
   AtomicM_Thres=DoubleVar()
   AtomicM_Thres.set(0.0)
   layer = Entry(MainWindow, textvariable=AtomicM_Thres, width=25)
   layer.grid(row=6, column=1, sticky=W)

   # Active Layer Name
   layerLabel = Label(MainWindow, bg="yellow",  text="Active Layer Name")
   layerLabel.grid(row=7, column=0, sticky=W)
   Active_Layer=StringVar()
   Active_Layer.set("GaN")
   layer = Entry(MainWindow, textvariable=Active_Layer, width=25)
   layer.grid(row=7, column=1, sticky=W)

   # Minimum Step Length
   layerLabel = Label(MainWindow, bg="yellow",  text="Minimum Step Length(um)")
   layerLabel.grid(row=8, column=0, sticky=W)
   min_dX=DoubleVar()
   min_dX.set("0.0")
   layer = Entry(MainWindow, textvariable=min_dX, width=25)
   layer.grid(row=8, column=1, sticky=W)

   # Minimum Energy Deposition
   layerLabel = Label(MainWindow, bg="yellow",  text="Minimum Energy Deposition(eV)")
   layerLabel.grid(row=9, column=0, sticky=W)
   min_dE=DoubleVar()
   min_dE.set("0.0")
   layer = Entry(MainWindow, textvariable=min_dE, width=25)
   layer.grid(row=9, column=1, sticky=W)

   # Traget Define File
   layerLabel = Label(MainWindow, bg="yellow",  text="Particle Setup File(ex:beam.mac)")
   layerLabel.grid(row=10, column=0, sticky=W)
   file_NS=StringVar()
   file_NS.set("beam.mac")
   layer = Entry(MainWindow, textvariable=file_NS, width=25)
   layer.grid(row=10, column=1, sticky=W)

   # Save
   def Save_File():
      yaml_data = {'Event_num':Event_num.get(), 'PL_name':PL_name.get(), 'OFP_name':OFP_name.get(), 'file_TD':file_TD.get(), 'AtomicM_Thres':AtomicM_Thres.get(), 'Active_Layer':Active_Layer.get(), 'min_dX':min_dX.get(), 'min_dE':min_dE.get(), 'file_NS':file_NS.get()}
      temp_path = 'Batch Mode Setupfiles/' + file_Name.get()
      yaml_file = open(temp_path, 'w')
      yaml.dump(yaml_data, yaml_file ,default_flow_style=False,encoding='utf-8',allow_unicode=True)
      yaml_file.flush()
      yaml_file.close()
      tkMessageBox.showinfo("Message", "File Saved")

   visLabel = Label(MainWindow, text="Save The Yaml File", bg="yellow")
   visLabel.grid(row=11, column=0, sticky=W)
   # Generate the Dictionary Instance
   SaveBut = Button(MainWindow, bg="orange", text="Save To Target Folder", command=Save_File)
   SaveBut.grid(row=11, column=1, sticky=W)
