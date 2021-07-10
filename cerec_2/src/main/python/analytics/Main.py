import os, sys, argparse
#os.chdir('..' + os.path.sep + '..')
sys.path.append(os.getcwd())

import python.data.DataPaths as DataPaths
from python.io.JSONCausalityDataReader import JSONCausalityDataReader
from python.analytics.CerecSetup import CerecSetup
from python.analytics.Study import Study
from python.data.DataSet import DataSet
from python.util.Utils import Utils
import pickle

def main(url='http://localhost:9000'):
  '''
    Original author : juf, modified by rawr.
    Auxiliary main method to perform studies on the CEREC system
  '''
  
  # cause effect recognition using constituency structures
  crs_const = CerecSetup(CerecSetup.CG_CONSTITUENT, CerecSetup.SG_CONSTITUENCY, url)
  
  # cause effect recognition using dependency structures (not used till now)
  #crs_dep = CerecSetup(CerecSetup.CG_DEPENDENCY, CerecSetup.SG_DEPENDENCY, url)

  RQs = []
  # RQ1 = []
  # RQ2 = []
  RQ3 = []

  # RQ1.extend(generateStudiesForRQ1_3(crs_const.getCerec()))
  # RQs.append(RQ1)
  # RQ2.extend(generateStudiesForRQ2(crs_const.getCerec()))
  # RQs.append(RQ2)
  RQ3.extend(generateStudiesForRQ1_3(crs_const.getCerec(), 1))
  RQs.append(RQ3)

  # perform all studies
  index = 0
  for RQ in RQs:
    index += 1
    table = ""
    for study in RQ:
      table = table + study.perform() + "\n"
      study.cerec.opfile.flushAll()
      study.savePatterns()
      study.saveNonCausals()
      
    print("Research Question " + str(index) + ":")
    print(table)

def generateStudiesForRQ1_3(cerec, flag=0):  # if flag = 1 then rq3 else rq1
  studies = []

  for pure in DataPaths.PURE_COLL_min:
    label = pure.split(os.path.sep)[-1]
    if flag==1:
      arr = []
      ncs = []
      for fpath in Utils.generateListWithout(DataPaths.PURE_COLL, pure):
        fname = fpath.split(os.path.sep)[-1][:-5]
        #print(fname)
        fp1 = open("./resources/output/untrained_" + fname + "_patterns.bin", 'rb')
        fp2 = open("./resources/output/untrained_" + fname + "_non_causals.bin", 'rb')
        try:
          arr.extend(pickle.load(fp1))
          ncs.extend(pickle.load(fp2))
        except EOFError:
          print('Problemma')
          print(fname)
      print(len(arr))
      print(len(ncs))
      study = Study(cerec, "trained_prev_" + label.split('.')[0],  prev_patts=arr, non_causals_all=ncs)
    else:
      study = Study(cerec, "untrained_" + label.split('.')[0])
    
    study.setSet1(readSetFromJSON(pure))
    study.setIterations(2)
    studies.append(study)
  
  return studies
    

def generateStudiesForRQ2(cerec):
  from datetime import datetime

  now = datetime.now()
  studies = []
  folder_name = "training_"+ now.strftime("%Y%m%d_%H%M%S")

  for pure in DataPaths.PURE_COLL_min:
    label = pure.split(os.path.sep)[-1]
    study = Study(cerec, "trained_" + label.split('.')[0], folderName=folder_name)
    study.setSet1(readSetFromJSON(Utils.generateListWithout(DataPaths.PURE_COLL_min, pure)))
    study.setSet2(readSetFromJSON(pure))
    study.setIterations(1)
    studies.append(study)
  return studies

def readSetFromJSON(file):
  '''
  Reads one or more file and extracts all sentences from it.
  
  Parameters: 
    files (str / list): Full path to the file
  
  Returns:
    list : Set of sentences contained in the file, correctly annotated if causal
  '''
  
  if type(file).__name__ != 'list':
     file = [file]
     
  set = DataSet()
  for f in file:
    reader = JSONCausalityDataReader()
    reader.initialize(f)
    set.addSet(reader.readExamples())
 
  return set


'''* Reads multiple files and extracts all sentences from each one
 * @param files List of paths to the files
 * @return Set of sentences contained in each file, correctly annotated if causal


def readSetFromJSON(files):
  DataSet set = new DataSet()
  ICausalityDataReader reader = null
  for file in files:
    reader = new JSONCausalityDataReader()
    reader.initialize(file)
    if(reader.isInitialized()):
      set.addSet(reader.readExamples())

  return set;



 * Reads multiple files and extracts all sentences from each one
 * @param files List of paths to the files
 * @return Set of sentences contained in each file, correctly annotated if causal


def readSetFromJSON(files):
  String[] fA = new String[files.size()]
  for(int i = 0; i < fA.length; i++)
  fA[i] = files.get(i);
  return readSetFromJSON(fA);

/**
 * Reads a SemEval file, utilizes a specific reader tailored towards the SemEval format
 * @param filename Full path to the SemEval file
 * @return Set of sentences contained in the SemEval file, correctly annotated if causal
 */

def readSetFromSemEval(filename):
  DataSet set = new DataSet();
  ICausalityDataReader reader = new SEMEVALCausalityDataReader();
  reader.initialize(filename);
  if(reader.isInitialized()) {
    set.addSet(reader.readExamples());

  return set;'''


if __name__ == '__main__':
  # Initialize parser
  parser = argparse.ArgumentParser()
   
  # Command line argument for accepting link to server
  parser.add_argument("-l", "--link", help = "Link to server")
   
  # Read arguments from command line
  args = parser.parse_args()
   
  if args.link is not None:
    main(url=args.link)
    
  else:
    main()