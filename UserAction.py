from Geant4 import *
import ROOT
from array import array


class MyRunAction(G4UserRunAction):
  "My Run Action"
 
  def BeginOfRunAction(self,run):
    pass
    #self.Ofile = ROOT.TFile.Open("output.root","RECREATE")
    #self.eDep  = array('d',[0])
    #self.stepL = array('d',[0])
    #self.tree  = ROOT.TTree("g4tree","g4tree")
    #self.tree.Branch("eDep",self.eDep,"eDep/D")
    #self.tree.Branch("stepLen",self.stepL,"stepLen/D")
    
  def EndOfRunAction(self, run):
    pass 
    #print "*** Writing out dEdX"
    #self.tree.Write()
    #self.Ofile.Close()
    
# ------------------------------------------------------------------
class MyEventAction(G4UserEventAction):
  def __init__(self):
      self.ra = gRunManager.GetUserRunAction()

  def EndOfEventAction(self, event):
      pass 


# ------------------------------------------------------------------
class MySteppingAction(G4UserSteppingAction):
  "My Stepping Action"

  def UserSteppingAction(self, step):
    ra = gRunManager.GetUserRunAction()
    #oFile = ra.Ofile
    #ra.eDep[0]  = step.GetTotalEnergyDeposit()
    #ra.stepL[0]  = step.GetStepLength()
    #ra.tree.Fill()
    #print "*** dE/dx in current step=", step.GetTotalEnergyDeposit()
    preStepPoint= step.GetPreStepPoint()
    track= step.GetTrack()
    touchable= track.GetTouchable()
    #print "*** vid= ", touchable.GetReplicaNumber()
