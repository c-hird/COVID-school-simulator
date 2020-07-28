#Importing classes and external packages to be used in the simulation
from person import Person
from simulate_one import simulate_one
from simulate_two import simulate_two
from simulate_three import simulate_three
from school import School
import pandas
import copy
import csv

#This represents the number of days in the Fall semester, including weekends
NUM_DAYS = 126

#Counters used to give each student and teacher a unique ID in the simulation, useful for debugging and diagnostics
total_students = 0
total_teachers = 0

#Reads in csv file containing the name, number of teachers, and number of students at each Spartanburg County elementary school
schoolset = pandas.read_csv("school_data.csv")
#This array will contain all of our School objects
schools = []
#This is a simple integer counter used to run our while loops
counter = 0

#Measures total teachers & students in our simulation
totteach = 0
totstud = 0

#This loops through the 39 schools in the "schoolset" dataframe and creates School objects for each.
#Each school object is added to the end of our "schools" list
while(counter < len(schoolset.index)):
  schools.append(School(schoolset.at[counter,"School"], int(schoolset.at[counter,"Teachers"]), int(schoolset.at[counter, "Students"])))
  totteach = totteach + schoolset.at[counter, "Teachers"]
  totstud = totstud + schoolset.at[counter, "Students"]
  counter += 1
#This resets our counter
counter=0

#This iterates over each of the 39 schools in our dataset
for school in schools:
  #This loop allow us to create a Person object for each student in the given school.
  #Each Person is marked with an "s" to identify it as a student.
  while(counter<school.num_students):
    #This allows us to divide the student population into distinct classrooms
    class_num = (counter%school.classroom_count)+1
    #This allows us to assign a student to one of three lunch periods in the simulation (note: this is only used for Scenario 1)
    lunch = (counter%3)+1 
    #This generates the student object with a unique ID
    school.students.append(Person(total_students,"s", class_num, lunch))
    counter += 1
    total_students += 1

  #This again resets our counter. Notice we are still in the original "for" loop, meaning we are still referencing the same school as in the previous "while" loop
  counter = 0

  #This loop runs the same as the previous "while" loop, instead generating a Person object for each teacher in the school
  while(counter<school.num_teachers):
    class_num = (counter%school.classroom_count)+1
    lunch = (counter%3)+1
    school.teachers.append(Person(total_teachers, "t", class_num, lunch))
    counter += 1
    total_teachers += 1
  counter = 0

#This creates three unique copies of the "schools" arrays. This is necessary so one simulation is not overwriting changes made in another
schoolspt2 = copy.deepcopy(schools)
schoolspt3 = copy.deepcopy(schools)

#This runs each of the three simulations
num_sims = 20
simulate_one(schools, NUM_DAYS, num_sims)
print("Simulation of Scenario 1 complete.")
simulate_two(schoolspt2, NUM_DAYS, num_sims)
print("Simulation of Scenario 2 complete.")
simulate_three(schoolspt3, NUM_DAYS, num_sims)
print("Simulation of Scenario 3 complete.")