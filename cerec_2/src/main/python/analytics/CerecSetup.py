'''package jfr.cerec.analytics;

import jfr.cerec.genetics.ICommandGenerator;
import jfr.cerec.genetics.ConstituentCommandGenerator;
import jfr.cerec.genetics.DependencyCommandGenerator;
import jfr.cerec.main.CauseEffectRecognition;
import jfr.cerec.main.ICauseEffectRecognition;
import jfr.cerec.pattern.ConstituentStructureGenerator;
import jfr.cerec.pattern.DependencyStructureGenerator;
import jfr.cerec.pattern.IStructureGenerator;

/**
 *
 * @author Julian Frattini
 * Factory class assembling the components for the cause effect recognition (cerec) system.
 * This class decides, which components to use. The following options are available:
 *  - CommandGenerator: SimpleCommandGenerator
 *  - StructureGenerator: ConstituentStructureGenerator, DependencyStructureGenerator
 *
 */'''
import python.pattern.DependencyStructureGenerator as DependencyStructureGenerator
import python.pattern.ConstituentStructureGenerator as ConstituentStructureGenerator
import python.genetics.DependencyCommandGenerator as DependencyCommandGenerator
import python.genetics.ConstituentCommandGenerator as ConstituentCommandGenerator
import python.main.CauseEffectRecognition as CauseEffectRecognition

class CerecSetup:

  #private ICauseEffectRecognition cerec;

  CG_CONSTITUENT = "ConstituencyCommandGenerator"
  CG_DEPENDENCY = "DependencyCommandGenerator"

  SG_CONSTITUENCY = "ConstituentStructureGenerator"
  SG_DEPENDENCY = "DependencyStructureGenerator"

  def __init__(self, cg, sg, url):
    self.commandGenerator = None
    self.structureGenerator = None

    #switch(cg) {
    if cg == CerecSetup.CG_DEPENDENCY:
      self.commandGenerator = DependencyCommandGenerator.DependencyCommandGenerator()
    
    else:
      self.commandGenerator = ConstituentCommandGenerator.ConstituentCommandGenerator()
      #case : ; break;
      #default : commandGenerator = new ConstituentCommandGenerator(); break;

    if sg == CerecSetup.SG_DEPENDENCY:
      self.structureGenerator = DependencyStructureGenerator.DependencyStructureGenerator()
    
    else:
      self.structureGenerator = ConstituentStructureGenerator.ConstituentStructureGenerator()
      
    self.cerec = CauseEffectRecognition.CauseEffectRecognition(self.commandGenerator, self.structureGenerator, url)

  def getCerec(self):
    return self.cerec
   