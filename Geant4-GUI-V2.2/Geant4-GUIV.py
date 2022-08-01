from Tkinter import *
import os
import webbrowser
import tkMessageBox
from Geo_Editor import *
from Setupfile_Editor import *

# Menu Function Define
def callback(url):
   webbrowser.open_new(url)

def NewSession():
   os.system("python Neutron-Simulator.py")

def help_cmd():
   filewin = Toplevel(root)
   title = Label(filewin, text="Help", bg="red")
   title.pack()
   helptext = "New Simulation Session: Open a new session for Geant4 simulation.\nNew Particle Source: Define a new G4GeneralPartilceSource .mac file."
   help = Label(filewin, text=helptext)
   help.pack()
   linklabel = Label(filewin, text="Click to See More G4GeneralParticleSource Info", bg='green')
   linklabel.pack()
   linklabel.bind("<Button-1>", lambda e: callback("https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/GettingStarted/generalParticleSource.html#g4gps"))

def about_cmd():
   filewin2 = Toplevel(root)
   title = Label(filewin2, text="About", bg="red")
   title.pack()
   aboutlable = Label(filewin2, text="SMU Reliability Lab Geant4 GUI Version 2.2\nPython 2.7.17 based\nFor Research Purpose Only-All Right Reserved\n Han Gao 1/1/2021")
   aboutlable.pack()
   contactlabel = Label(filewin2, text="Contact us: smureliabilitylab@gmail.com", bg='yellow')
   contactlabel.pack()
   updatelabel = Label(filewin2, text="Last Update, 1/9/2021", bg='yellow')
   updatelabel.pack()

def Physics_List_cmd():
   filewin3 = Toplevel(root)
   scrollbar = Scrollbar(filewin3)
   scrollbar.pack( side = RIGHT, fill = Y )
   scrollbar2 = Scrollbar(filewin3, orient=HORIZONTAL)
   scrollbar2.pack( side = BOTTOM, fill = X)
   title = Label(filewin3, text="Reference Physics List", bg="red")
   title.pack()
   reference = open("Physics_List_Reference.txt","r")
   text = Text(filewin3)
   text.insert(INSERT, reference.read())
   text.pack()
   scrollbar.config(command=text.yview)
   scrollbar2.config(command=text.xview)

def G4source_ref_cmd():
   filewin4 = Toplevel(root)
   button = Label(filewin4, text="Genaral Particle Source Reference", bg="red")
   button.pack()
   scrollbar = Scrollbar(filewin4)
   scrollbar.pack( side = RIGHT, fill = Y )
   scrollbar2 = Scrollbar(filewin4, orient=HORIZONTAL)
   scrollbar2.pack(side = BOTTOM, fill = X)
   reference = open("General_Particle_Source_help.txt","r")
   text = Text(filewin4)
   text.insert(INSERT, reference.read())
   text.pack()
   scrollbar.config(command=text.yview)
   scrollbar2.config(command=text.xview)

def partice_def_cmd():
   filewin5 = Toplevel(root)
   title = Label(filewin5, text="Mono Energy Particle Source Define", bg="red")
   title.grid(row=1, column=0, columnspan=4)

   # number of Particles
   layerLabel = Label(filewin5, bg="yellow",  text="Saving Path (end with '/')")
   layerVar=StringVar()
   layerVar.set('Particle File/')
   layer = Entry(filewin5, textvariable=layerVar, width=25)
   layerLabel.grid(row=2, column=0, sticky=W)
   layer.grid(row=2, column=1, sticky=W)

   layerLabel2 = Label(filewin5, bg="yellow",  text="File Name")
   layerVar2=StringVar()
   layerVar2.set('Mono-Energy-Source')
   layer2 = Entry(filewin5, textvariable=layerVar2, width=25)
   layerLabel2.grid(row=3, column=0, sticky=W)
   layer2.grid(row=3, column=1, sticky=W)

   # Paticle Name Define
   layerLabel3 = Label(filewin5, bg="yellow",  text="Particle Name")
   ParticeName=StringVar()
   ParticeName.set('neutron')
   layer3 = Menubutton(filewin5, text='Particle List', relief=RAISED)
   layer3.menu = Menu(layer3, tearoff=0)
   layer3["menu"] = layer3.menu
   Particle_List = ["gamma", "e-","mu-","tau-","nu_e","proton","neutron","alpha","He3","deutron"]
   for index in Particle_List:
       layer3.menu.add_radiobutton(label=index, variable=ParticeName, value=index, activebackground='green')
   layer3.grid(row=4, column=1, sticky=W)
   layerLabel3.grid(row=4, column=0, sticky=W)

   # Sqaure size x
   layerLabel4 = Label(filewin5, bg="yellow",  text="Half Length in X (mm)")
   halfx=StringVar()
   halfx.set('0')
   layer4 = Entry(filewin5, textvariable=halfx, width=25)
   layer4.grid(row=5, column=1, sticky=W)
   layerLabel4.grid(row=5, column=0, sticky=W)

   # Sqaure size y
   layerLabel5 = Label(filewin5, bg="yellow",  text="Half Length in Y (mm)")
   halfy=StringVar()
   halfy.set('0')
   layer5 = Entry(filewin5, textvariable=halfy, width=25)
   layer5.grid(row=6, column=1, sticky=W)
   layerLabel5.grid(row=6, column=0, sticky=W)

   # Sqaure size z
   layerLabel6 = Label(filewin5, bg="yellow",  text="Half Length in Z (mm)")
   halfz=StringVar()
   halfz.set('0')
   layer6 = Entry(filewin5, textvariable=halfz, width=25)
   layer6.grid(row=7, column=1, sticky=W)
   layerLabel6.grid(row=7, column=0, sticky=W)

   # center position
   layerLabel7 = Label(filewin5, bg="yellow",  text="Center Position (x,y,z) in mm")
   center=StringVar()
   center.set('0 0 0')
   layer7 = Entry(filewin5, textvariable=center, width=25)
   layer7.grid(row=8, column=1, sticky=W)
   layerLabel7.grid(row=8, column=0, sticky=W)

   # Energy
   layerLabel8 = Label(filewin5, bg="yellow",  text="Particle Energy (MeV)")
   energy=StringVar()
   energy.set('10')
   layer8 = Entry(filewin5, textvariable=energy, width=25)
   layer8.grid(row=9, column=1, sticky=W)
   layerLabel8.grid(row=9, column=0, sticky=W)

   # make the file
   def Create_File():
       monoE_file = open(layerVar.get() + layerVar2.get() + '.mac','w')
       monoE_file.write('/gps/verbose 1\n')
       monoE_file.write('/gps/particle ' + ParticeName.get() + '\n')
       monoE_file.write('/gps/pos/type Plane\n')
       monoE_file.write('/gps/pos/shape Square\n')
       monoE_file.write('/gps/pos/centre ' + center.get() + ' mm\n')
       monoE_file.write('/gps/pos/halfx ' + halfx.get() + ' mm\n')
       monoE_file.write('/gps/pos/halfy ' + halfy.get() + ' mm\n')
       monoE_file.write('/gps/pos/halfz ' + halfz.get() + ' mm\n')
       monoE_file.write('/gps/ang/type planar\n')
       monoE_file.write('/gps/ene/mono ' + energy.get() + ' MeV\n')
       tkMessageBox.showinfo("Message", "File Created!")
       filewin5.destroy()

   CreateBotton = Button(filewin5, text="Create The File!", command=Create_File, bg="red")
   CreateBotton.grid(row=10, column=0, columnspan=4) 

# Main Window Define
root = Tk()

filename = PhotoImage(file="Login-Pic.PNG")
login_page = Canvas(root, width =451, height=200)
login_page.create_image(1, 1, anchor=NW, image=filename)
login_page.pack()

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New Simulation Session", command=NewSession)
filemenu.add_command(label="New Mono Energy Particle Source", command=partice_def_cmd)
filemenu.add_command(label="New Target Geometry", command=lambda : Geo_Editor_cmd(mother=root))
filemenu.add_command(label="New Batch Mode Setupfile", command=lambda : Setupfile_Editor_cmd(mother=root))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=help_cmd)
helpmenu.add_command(label="Geant4 Physics List", command=Physics_List_cmd)
helpmenu.add_command(label="Geant4 General Particle Source", command=G4source_ref_cmd)
helpmenu.add_command(label="About...", command=about_cmd)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()
