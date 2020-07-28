import random
from recap import recap, do_nothing
from simul_methods import stud_is_sick, teach_is_sick
import csv

#Odds of a person catching the virus outside of school (per day)
DAILY_EXT_ODDS_CHILD = 0.00007866
DAILY_EXT_ODDS_ADULT = 0.0001361

#Used to determine secondary exposure within classroom (0.035*0.4*0.4)
HEAVY_EXPOSURE_ODDS = 0.0056

def simulate_three(schools, days_in_sim, num_sims):
  print("Beginning simulation of Scenario 3")
  sim_ct = 1
  days = days_in_sim
  with open('sickness_sim_3.csv', mode = 'w') as sick_file:
    sick_writer = csv.writer(sick_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    while(sim_ct < num_sims+1):
      testing_flag = False
      day_of_the_week = 1
      days = days_in_sim
      while(days > 0):
        exposed_students = 0
        exposed_teachers = 0
        for school in schools:
          #For healthy students, simulate whether they are a new primary case. For sick students, add to exposure list and decrement sickness counters
          for stud in school.students: 
            if(isinstance(stud, int)):
              do_nothing()
            elif(stud.is_sick):
              stud_is_sick(stud, school, testing_flag)
            else:
              if(random.random() < DAILY_EXT_ODDS_CHILD):
                stud.become_sick("s")
                sick_writer.writerow([days, 'Student', 'Primary', stud.severity, school.school_ID, sim_ct])
      #         print("Student",stud.ID, "is now sick")

          #For healthy teachers, simulate whether they are a new primary case. For sick teachers, add to exposure list and decrement sickness counters
          for teach in school.teachers:
            if(isinstance(teach, int)):
              do_nothing()
            elif(teach.is_sick):
              teach_is_sick(stud, school, testing_flag)
            else:
              if(random.random() < DAILY_EXT_ODDS_ADULT):
                teach.become_sick("t")
                sick_writer.writerow([days, 'Teacher', 'Primary', teach.severity, school.school_ID, sim_ct])
      #         print("Teacher",teach.ID, "is now sick")

          #For each classroom with an infected person, expose all others and determine if anyone becomes a secondary case.
          if(day_of_the_week < 6):
            for stud in school.students:
              if(isinstance(stud, int)):
                do_nothing()
              else:
                if(stud.is_sick):
                  #print("skipping sick student")
                  do_nothing()
                else:
                  if(stud.classroom in school.exposed_classrooms):
                    exposed_students +=1
        #           print("Student", stud.ID, "has been exposed")
                    if(random.random() < HEAVY_EXPOSURE_ODDS):
                      stud.become_sick("s")
                      sick_writer.writerow([days, 'Student', 'Secondary', stud.severity, school.school_ID, sim_ct])
                      if(testing_flag):
                        stud.in_school = False
          #            print("Student", stud.ID, "is now sick")
            for teach in school.teachers:
              if(isinstance(teach, int)):
                do_nothing()
              else:
                if(teach.is_sick):
                  #print("skipping sick teacher")
                  do_nothing()
                else:
                  if(teach.classroom in school.exposed_classrooms):
                    exposed_teachers +=1
            #       print("Teacher", teach.ID, "has been exposed")
                    if(random.random()< HEAVY_EXPOSURE_ODDS):
                      teach.become_sick("t")
                      sick_writer.writerow([days, 'Teacher', 'Secondary', teach.severity, school.school_ID, sim_ct])
                      if(testing_flag):
                        teach.in_school = False
                      print("Teacher", teach.ID, "is now sick")
          school.exposed_classrooms = []
        sick_writer.writerow([days, exposed_students, exposed_teachers, sim_ct])
        day_of_the_week +=1      
        day_of_the_week +=1
        if(day_of_the_week == 7):
          day_of_the_week = 1
        elif(day_of_the_week > 7):
          print("ERROR: exceeded max days of the week")
        days -= 1
        testing_flag = False
      print("Simulation", sim_ct, "complete.")
      sim_ct += 1
# recap(schools)