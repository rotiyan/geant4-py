from Geant4 import *

import g4py.NISTmaterials

# creating target materials
a= 69.72*g/mole
elGa= G4Element("Galium", "Ga", 31., a)

a= 14.01*g/mole
elN= G4Element("Nitrogen", "N", 7., a)

a= 28.09*g/mole
Silicon= G4Element("Silicon", "Si", 14., a)

a= 12.011*g/mole
elC= G4Element("Carbon", "C",  6., a)

a= 10.012*g/mole
elB10= G4Element("Boron10", "B_10",  5., a)

density= 6.15*g/cm3
GaN= G4Material("GaN", density, 2)
GaN.AddElement(elGa, 0.83272)
GaN.AddElement(elN, 0.16728)

g4py.NISTmaterials.Construct()

density= 3.17*g/cm3
SiN= G4Material("SiN", density, 2)
SiN.AddElement(Silicon, 0.60062)
SiN.AddElement(elN, 0.39938)

density= 3.21*g/cm3
SiC= G4Material("SiC", density, 2) 
SiC.AddElement(Silicon, 0.70045)
SiC.AddElement(elC, 0.29955)

density= 2.34*g/cm3
B10= G4Material("B10", density, 1)
B10.AddElement(elB10, 1.)

# See G$ NIST Material to add more
Material_Name_List = ["G4_Al", "G4_Si", "GaN", "SiC", "SiN", "G4_AIR", "G4_ALUMINUM_OXIDE", "G4_WATER", 'B10']
World_List = ["G4_AIR", "G4_WATER", "G4_Galactic"]
