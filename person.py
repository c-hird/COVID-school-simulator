#Importing classes and external packages to be used in the simulation
import random

#Groups adult ages into ranges that allow us to match up age ranges with illness severity data. (Note: read "range(20,44,1)" as "ages 20-44")
AGE_RANGES = [range(20,44,1),range(45,54,1),range(55,74,1)]
#Represents the proportion of teachers in SC within each age range (i.e. 60% of teachers fall within age range 20-44)
AGE_RANGE_WEIGHTS = [60, 21.2, 18.8]

#Defining possible range of days the infection will last
INFECTION_LENGTH = [7,8,9,10]

#Defining possible range of days until the patient begins displaying symptoms. Note: this does not apply to asymptomatic cases
ASYMPTOMATIC_LENGTH = [5,6]

#Odds of an infection reaching a given level of severity; SEVERITY_WEIGHTS_XX_YY represents age range XX-YY
#Example: a 57 year old uses SEVERITY_WEIGHTS_55_64, and has a 64.75% chance of mild infection, 25.3% chance of being hospitalized, 7.95% of ICU admission, and 2% chance of fatality
SEVERITY_OPTIONS = ["mild", "hospitalized", "ICU", "fatal"]
SEVERITY_WEIGHTS_CHILD = [97.95, 2.05, 0, 0]
SEVERITY_WEIGHTS_20_44 = [79.2, 17.55, 3.1, .15]
SEVERITY_WEIGHTS_45_54 = [66.69, 24.75, 7.9, .65]
SEVERITY_WEIGHTS_55_64 = [64.75 , 25.3, 7.95, 2]
SEVERITY_WEIGHTS_65_74 = [46.7 , 36.05, 13.45, 3.8]

#Odds an infected person remains asymptomatic throughout the entire infection period
ODDS_ASYMPTOMATIC_STUD = .28
ODDS_ASYMPTOMATIC_TEACH = .179

class Person:
  def __init__(self, ID, p_type, croom, lunch):
    self.ID = ID
    self.person_type = p_type
    self.classroom = croom
    self.is_sick = False
    self.will_be_symptomatic = True
    self.days_until_healthy = -1
    self.days_until_symptomatic = -1
    self.in_school = True
    self.severity = "not sick"
    self.died = False
    self.lunch = lunch
    #Note that we only assign an age to teachers - students are all within the same age range, so assigning an age would have no purpose
    if(p_type == "t"):
      age_range = random.choices(AGE_RANGES, weights=AGE_RANGE_WEIGHTS)[0]
      self.age = random.choice(age_range)
      

  def become_sick(self, p_type):
    if(p_type == "s"):
      self.is_sick = True
      self.days_until_healthy = random.choice(INFECTION_LENGTH)
      #Determine if student will be an asymptomatic patient throughout the infection
      #A random number between 0-1 is generated, and if that value is less than the odds of a patient becoming asymptomatic, then the patient is
      if(random.random() < ODDS_ASYMPTOMATIC_STUD):
        self.will_be_symptomatic = False
        self.days_until_symptomatic = -1
        self.severity = "asymptomatic"
      else:
        self.will_be_symptomatic = True 
        self.days_until_symptomatic = random.choice(ASYMPTOMATIC_LENGTH)
        self.severity = random.choices(SEVERITY_OPTIONS, weights=SEVERITY_WEIGHTS_CHILD, k=1)[0]
    elif(p_type == "t"):
      self.is_sick = True
      self.days_until_healthy = random.choice(INFECTION_LENGTH)
      #Determine if teacher will be an asymptomatic patient throughout the infection
      if(random.random() < ODDS_ASYMPTOMATIC_TEACH):
        self.will_be_symptomatic = False
        self.days_until_symptomatic = -1
        self.severity = "asymptomatic"
      else:
        self.will_be_symptomatic = True
        self.days_until_symptomatic = random.choice(ASYMPTOMATIC_LENGTH)
        if(self.age < 45):
          self.severity = random.choices(SEVERITY_OPTIONS, weights=SEVERITY_WEIGHTS_20_44, k=1)[0]        
        elif(self.age >= 45 and  self.age < 55):
          self.severity = random.choices(SEVERITY_OPTIONS, weights=SEVERITY_WEIGHTS_45_54, k=1)[0]                 
        elif(self.age >= 55 and self.age < 65):
          self.severity = random.choices(SEVERITY_OPTIONS, weights=SEVERITY_WEIGHTS_55_64, k=1)[0]                 
        elif(self.age >= 65):
          self.severity = random.choices(SEVERITY_OPTIONS, weights=SEVERITY_WEIGHTS_65_74, k=1)[0]               
        else:
          print("Invalid age. Exiting...")
          exit(0)

    else:
      print("become_sick() received an invalid person_type. Exiting...")
      exit(0)