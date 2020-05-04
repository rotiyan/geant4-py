from Geant4 import *


class GeneratorAction(G4VUserPrimaryGeneratorAction):
    "My Primary Generator Action"

    def __init__(self):
        
        G4VUserPrimaryGeneratorAction.__init__(self)
        
        particle_table = G4ParticleTable.GetParticleTable()

        electron = particle_table.FindParticle(G4String("e-"))
        positron = particle_table.FindParticle(G4String("e+"))
        muPlus   = particle_table.FindParticle(G4String("mu+"))
        muMinus  = particle_table.FindParticle(G4String("mu-"))
        gamma    = particle_table.FindParticle(G4String("gamma"))
        proton   = particle_table.FindParticle(G4String("proton"))
        
        beam = G4ParticleGun()
        beam.SetParticleEnergy(20*MeV)
        beam.SetParticleMomentumDirection(G4ThreeVector(0,0,-1))
        beam.SetParticleDefinition(muPlus)
        beam.SetParticlePosition(G4ThreeVector(0,0,1005))
        
        self.particleGun = beam

        
    def GeneratePrimaries(self, event):
        
        self.particleGun.GeneratePrimaryVertex(event)
