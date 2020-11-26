class Shark:
  def __init__(self, name, age):
    self.name = name
    self.age = age
    
  def swim(self):
    print(self.name, "swims")
    
  def be_grr(self):
    print(self.name, "of age", self.age, "is being grr")
    
sammy = Shark("Sammy", 11)

sammy.swim()
sammy.be_grr()