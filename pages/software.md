---
layout: site
permalink: /software.html
---

# Key4HEP and the FCC software environment

[Key4hep](https://cern.ch/key4hep/) is a common software ecosystem for future collider experiments, developed collaboratively across the HEP community. FCC uses Key4hep as the foundation for its application software, building on shared core components — including the event data model [EDM4hep](https://edm4hep.web.cern.ch/), the Gaudi event processing framework, DD4hep detector description, and Geant4 simulation — to carry out detector simulation, reconstruction, and physics analysis. FCC-specific packages extend this stack with detector geometries, calorimeter reconstruction, and the [FCCAnalyses](https://hep-fcc.github.io/FCCAnalyses/) analysis framework.

### FCC packages
* [FCCAnalyses Framework](https://hep-fcc.github.io/FCCAnalyses/)
    ([Doxygen](https://hep-fcc.github.io/FCCAnalyses/doc/latest/)): Analysis
    framework for FCC-related studies.
* [FCC-config](https://github.com/HEP-FCC/FCC-config): Configurations used for
    the sample productions.
* [EventProducer](https://github.com/HEP-FCC/EventProducer):
    Produce events for FCC.
* [hep-fcc/k4RecCalorimeter](https://github.com/hep-fcc/k4RecCalorimeter):
    Calorimeter reconstruction code.

### key4hep packages
* [Key4hep Documentation](https://cern.ch/key4hep/): Growing documentation of
    the Key4hep and its components.
* [key4hep/k4FWCore](https://github.com/key4hep/k4FWCore): Basic Gaudi I/O
    components.
* [key4hep/k4Gen](https://github.com/key4hep/k4gen): Generators and Particle
    Guns.
* [key4hep/k4SimDelphes](https://github.com/key4hep/k4SimDelphes): Delphes Fast
    Sim.
* [key4hep/k4geo](https://github.com/key4hep/k4geo) DD4hep models of FCC
    detector geometries for Full Sim of FCC-ee.
* [key4hep/k4SimGeant4](https://github.com/key4hep/k4SimGeant4)
    ([Doxygen](https://key4hep.github.io/k4SimGeant4/)): Geant4 Full Sim of
    FCC-hh.
* [key4hep/k4RecTracker](https://github.com/key4hep/k4RecTracker): Tracker
    reconstruction code.
* [key4hep/k4ActsTracking](https://github.com/key4hep/k4ActsTracking): Acts
    integration in the Key4hep framework.
* [key4hep/k4DetectorPerformance](https://github.com/key4hep/k4DetectorPerformance):
    Gaudi/EDM4hep based detector performance code.
* [key4hep/k4Bench](https://github.com/key4hep/k4Bench): Performance
    benchmarking for DD4hep-based simulations and reconstruction.
* [key4hep/k4PFHitML](https://github.com/key4hep/k4PFHitML): Inference of
    hit-based particle flow with machine learning.
* [key4hep-validation](https://key4hep-validation.web.cern.ch/): Physics
    validation of the Key4hep stack.
* [key4hep-spack](https://github.com/key4hep/key4hep-spack): Key4hep specific
    Spack packages.

The full list of all Key4hep repositories can be found [here](https://github.com/key4hep)
all FCC Software repositories can be found [here](https://github.com/hep-fcc).

### Core Software Components
* [ROOT](https://root.cern/): An open-source data analysis framework used by
    high energy physics and others.
* [EDM4hep](https://edm4hep.web.cern.ch/): Event Data Model of Key4hep.
* [podio](https://github.com/AIDASoft/podio): Data model generator and I/O
    layer.
* [Gaudi](https://gaudi.web.cern.ch/gaudi/): Main event processing framework
    used by Key4hep.
* [Geant4](https://geant4.web.cern.ch/): Toolkit for the simulation of the
    passage of particles through matter.
* [DD4hep](https://dd4hep.web.cern.ch/): Detector Description Toolkit used by
    Key4hep.

