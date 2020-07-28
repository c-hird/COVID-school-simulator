import random
from recap import recap, do_nothing
from simul_methods import stud_is_sick, teach_is_sick
import csv

#Odds of a person catching the virus outside of school (per day)
DAILY_EXT_ODDS_CHILD = 0.00007866
DAILY_EXT_ODDS_ADULT = 0.0001361

#Used to determine secondary exposure within classroom
HEAVY_EXPOSURE_ODDS = .035

def simulate_one(schools, days_in_sim, num_sims):
  print("Beginning simulation of Scenario 1")
  sim_ct = 1
  days = days_in_sim
  assembly_days = [int(days/1.5), int(days/2), int(days/3)]

  #Here we open our writer and print out a header to the sickness_sim_1.csv file
  with open('sickness_sim_1.csv', mode = 'w') as sick_file:
    sick_writer = csv.writer(sick_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)sick_writer.writerow(["Days", "Person_Type", "Infection_Type", "Severity", "School_Name", "Simulation_Iteration", "Scenario"])

    #This allows us to loop through the total number of simulations
    while(sim_ct < num_sims+1):
      day_of_the_week = 1
      days = days_in_sim

      #This allows us to loop through the total number of days in the semester
      while(days > 0):
        exposed_students = 0
        exposed_teachers = 0
        for school in schools:
          #For healthy students, simulate whether they are a new primary case. For sick students, add to exposure list and decrement sickness counters
          for stud in school.students: 
            #Ignore this
            if(isinstance(stud, int)):
              do_nothing()
            #If student is sick, we want to track which classroom and lunch period he/she is in. This allows us to later expose the healthy individuals in those groups.
            elif(stud.is_sick):
              stud_is_sick(stud, school, False)
              school.exposed_classroom.append(stud.classroom)
              school.exposed_lunch.append(stud.lunch)
            #If student is healthy, we simulate their chances of catching COVID-19 outside of school
            else:
              if(random.random() < DAILY_EXT_ODDS_CHILD):
                stud.become_sick("s")
                sick_writer.writerow([days, 'Student', 'Primary', stud.severity, school.school_ID, sim_ct])
          #For healthy teachers, simulate whether they are a new primary case. For sick teachers, add to exposure list and decrement sickness counters
          for teach in school.teachers:
            if(isinstance(teach, int)):
              do_nothing()
            #If teacher is sick, we want to track which classroom and lunch period he/she is in. This allows us to later expose the healthy individuals in those groups.
            elif(teach.is_sick):
              school.exposed_classroom.append(teach.classroom)
              school.exposed_lunch.append(teach.lunch)
              teach_is_sick(teach,school, False)
            #If teacher is healthy, we simulate their chances of catching COVID-19 outside of school
            else:
              if(random.random() < DAILY_EXT_ODDS_ADULT):
                teach.become_sick("t")
                sick_writer.writerow([days, 'Teacher', 'Primary', teach.severity, school.school_ID, sim_ct])

          #For each classroom with an infected person, expose all others and determine if anyone becomes a secondary case.
          #day_of_the_week allows us to ignore weekends
          if(day_of_the_week < 6):
            for stud in school.students:
              #Ignore this
              if(isinstance(stud, int)):
                do_nothing()
              elif(stud.is_sick):
                do_nothing()
              #If student is healthy, we determine whether or not they were exposed to a COVID-19 positive individual
              else:
                if(stud.classroom in school.exposed_classrooms):
                  exposed_students += 1
                  if(random.random() < HEAVY_EXPOSURE_ODDS):
                    stud.become_sick("s")
                    sick_writer.writerow([days, 'Student', 'Secondary', stud.severity, school.school_ID, sim_ct])
                if(stud.classroom in school.exposed_lunch and not(stud.is_sick)):
                  exposed_students += 1
                  if(random.random() < HEAVY_EXPOSURE_ODDS/10):
                    stud.become_sick("s")    
                    sick_writer.writerow([days, 'Student', 'Secondary', stud.severity, school.school_ID, sim_ct])           
            for teach in school.teachers:
              if(isinstance(teach, int)):
                do_nothing()
              elif(teach.is_sick):
                do_nothing()
              #If student is healthy, we determine whether or not they were exposed to a COVID-19 positive individual
              else:
                #Determine if teacher was exposed in classroom
                if(teach.classroom in school.exposed_classrooms):
                  exposed_teachers += 1
                  if(random.random()< HEAVY_EXPOSURE_ODDS):
                    teach.become_sick("t")
                    sick_writer.writerow([days, 'Teacher', 'Secondary', teach.severity, school.school_ID, sim_ct])
                #Determine if teacher was exposed in lunchroom
                if(teach.classroom in school.exposed_lunch and not(teach.is_sick)):
                  exposed_teachers +=1
                  if(random.random()< HEAVY_EXPOSURE_ODDS/10):
                    teach.become_sick("t")
                    sick_writer.writerow([days, 'Teacher', 'Secondary', teach.severity, school.school_ID, sim_ct])     
            #Allows us to simulate assemblies three times a semester
            if(days in assembly_days):
              for stud in school.students:
                if(isinstance(stud,int)):
                  do_nothing()
                elif(stud.is_sick):
                  do_nothing()
                else:
                  exposed_students += 1
                  if(random.random() < HEAVY_EXPOSURE_ODDS/10):
                    stud.become_sick("s")
                    sick_writer.writerow([days, 'Student', 'Secondary', stud.severity, school.school_ID, sim_ct])
              for teach in school.teachers:
                if(isinstance(teach,int)):
                  do_nothing()
                elif(teach.is_sick):
                  do_nothing()
                else:
                  exposed_teachers += 1
                  if(random.random() < HEAVY_EXPOSURE_ODDS/10):
                    teach.become_sick("t")
                    sick_writer.writerow([days, 'Teacher', 'Secondary', teach.severity, school.school_ID, sim_ct])               
          #This clears exposed classrooms & lunches for the next school
          school.exposed_classrooms = []
          school.exposed_lunch = []
        #Tracks the number of exposures in the day
        sick_writer.writerow([days, exposed_students, exposed_teachers, sim_ct])

        #This accounts for weekends
        day_of_the_week +=1
        if(day_of_the_week == 7):
          day_of_the_week = 1
        elif(day_of_the_week > 7):
          print("ERROR: exceeded max days of the week")

        #Decrement our day count
        days -= 1
      print("Simulation", sim_ct, "complete.")
      sim_ct += 1

  #Uncomment this if you would like to see a printout of the results after each simulation
  #recap(schools)