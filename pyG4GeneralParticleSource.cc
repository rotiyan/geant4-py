#include <boost/python.hpp>
#include <G4GeneralParticleSource.hh>

using namespace boost::python;
void export_G4GeneralParticleSource()
{
    class_<G4GeneralParticleSource,G4GeneralParticleSource*> ("G4GeneralParticleSource", "G4General particle source")
        .def("GeneratePrimaryVertex",&G4GeneralParticleSource::GeneratePrimaryVertex)
        .def("GetNumberofSource",&G4GeneralParticleSource::GetNumberofSource)
        .def("ListSource",&G4GeneralParticleSource::ListSource)
        .def("SetCurrentSourceto",&G4GeneralParticleSource::SetCurrentSourceto)
        .def("SetCurrentSourceIntensity",&G4GeneralParticleSource::SetCurrentSourceIntensity)
        .def("GetCurrentSource",&G4GeneralParticleSource::GetCurrentSource,return_internal_reference<>())
        .def("GetCurrentSourceIndex",&G4GeneralParticleSource::GetCurrentSourceIndex)
        .def("GetCurrentSourceIntensity",&G4GeneralParticleSource::GetCurrentSourceIntensity)
        .def("ClearAll",&G4GeneralParticleSource::ClearAll)
        .def("AddaSource",&G4GeneralParticleSource::AddaSource)
        .def("DeleteaSource",&G4GeneralParticleSource::DeleteaSource)
        .def("SetVerbosity",&G4GeneralParticleSource::SetVerbosity)
        .def("SetMultipleVertex",&G4GeneralParticleSource::SetMultipleVertex)
        .def("SetFlatSampling",&G4GeneralParticleSource::SetFlatSampling)
        .def("SetParticleDefinition",&G4GeneralParticleSource::SetParticleDefinition)
        .def("GetParticleDefinition",&G4GeneralParticleSource::GetParticleDefinition,
        	return_value_policy<reference_existing_object>())
        .def("SetParticleCharge",&G4GeneralParticleSource::SetParticleCharge)
        .def("SetParticlePolarization",&G4GeneralParticleSource::SetParticlePolarization)
        .def("GetParticlePolarization",&G4GeneralParticleSource::GetParticlePolarization)
        .def("SetParticleTime",&G4GeneralParticleSource::SetParticleTime)
        .def("GetParticleTime",&G4GeneralParticleSource::GetParticleTime)
        .def("SetNumberOfParticles",&G4GeneralParticleSource::SetNumberOfParticles)
        .def("GetNumberOfParticles",&G4GeneralParticleSource::GetNumberOfParticles)
        .def("GetParticlePosition",&G4GeneralParticleSource::GetParticlePosition)
        .def("GetParticleMomentumDirection",&G4GeneralParticleSource::GetParticleMomentumDirection)
        .def("GetParticleEnergy",&G4GeneralParticleSource::GetParticleEnergy)
        ;

}
