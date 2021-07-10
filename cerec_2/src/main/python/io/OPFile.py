# -*- coding: utf-8 -*-
import os, pickle
class OPFile:
  
  def __init__(self, dir, label, folderName=None):
    self.dir = dir
    self.label = label
    
    if folderName is not None:
      if not os.path.exists(self.dir + folderName):
        os.mkdir(self.dir + folderName)
    
      self.dir = self.dir + folderName + '/'
    
    try:
      self.f1 = open(self.dir + self.label + '.txt', 'w+')
      self.f2 = open(self.dir + self.label + '_debug.txt', 'w+')
    
    except FileNotFoundError:
      print('err')
    
  def __del__(self):
    self.f1.close()
    self.f2.close()
    
  def writeToF1(self, st, end='\n'):
    try:
      self.f1.write(str(st) + end)
    except IOError:
      print('problem')
      
  def writeToF2(self, st, end='\n'):
    try:
      self.f2.write(str(st) + end)
    except IOError:
      print('problem')
      
  def writeToAll(self, st, end='\n'):
    try:
      self.f1.write(str(st) + end)
      self.f2.write(str(st) + end)
    except IOError:
      print('problem')
      
  def flushAll(self):
    self.f1.flush()
    self.f2.flush()
    
  def savePatterns(self, pdb):
    with open(self.dir + self.label + '_patterns.bin', 'wb') as fp:
      pickle.dump(pdb.patterns, fp)
      fp.flush()
    
  def saveNonCausals(self, ncs):
    with open(self.dir + self.label + '_non_causals.bin', 'wb') as fp:
      pickle.dump(ncs, fp)
      fp.flush()
    