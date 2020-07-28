def recap(schools):
  print("*************************************************************************")
  print("*************************************************************************")
  print("Simulation complete.")
  print("")
  for school in schools:
    print("**********************Recap for school:", school.school_ID, "*****************************")
    for stud in school.students:
      if(isinstance(stud, int)):
        print("")
      elif(stud.is_sick):
        print("Student", stud.ID, "is sick,", stud.days_until_healthy, "days until healthy. Severity =",stud.severity)
    for teach in school.teachers:
      if(isinstance(teach, int)):
        print("")
      elif(teach.is_sick):
        print("Teacher", teach.ID, ", age", teach.age, ", is sick,", teach.days_until_healthy, "days until healthy. Severity =",teach.severity)
    print("")
    for stud in school.recovered_students:
      if(isinstance(stud, int)):
        print("")
      else:
        print("Student", stud.ID, "has recovered")
    for teach in school.recovered_teachers:
      if(isinstance(teach, int)):
        print("")
      else:
        print("Teacher", teach.ID, "has recovered")
    for person in school.fatalities:
      if(person.person_type == "s"):
        print("Student", person.ID, "has passed away")
      elif(person.person_type == "t"):
        print("Teacher", person.ID, "has passed away")
      else:
        print("Invalid person type detected. Exiting...")
        exit(0)

def do_nothing():
  2+2