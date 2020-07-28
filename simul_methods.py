def stud_is_sick(stud, school, tflag):
  school.exposed_classrooms.append(stud.classroom)
  if(stud.will_be_symptomatic):
    stud.days_until_symptomatic -= 1
    if(stud.days_until_symptomatic == 0):
      school.symptomatic_classrooms.append(stud.classroom)
      stud.in_school = False
      tflag = True
  stud.days_until_healthy -=1
  if(stud.days_until_healthy == 0):
    if(stud.severity == "fatal"):
      stud.died = True
      school.fatalities.append(stud)
      print("Student", stud.ID, "has passed away")
      school.students.remove(stud)
    else:
      stud.in_school = True #This assumes people come back to school the first day they are no longer healthy - may need to alter depending on the scenario
      stud.is_sick = False
      school.recovered_students.append(stud)
#      print("Student", stud.ID, "is already sick. Adding to future exposure.")


def teach_is_sick(teach, school, tflag):
  school.exposed_classrooms.append(teach.classroom)
  if(teach.will_be_symptomatic):
    teach.days_until_symptomatic -= 1
    if(teach.days_until_symptomatic == 0):
      school.symptomatic_classrooms.append(teach.classroom)
      teach.in_school = False
      tflag = True
  teach.days_until_healthy -=1
  if(teach.days_until_healthy == 0):
    if(teach.severity == "fatal"):
      teach.died = True
      school.fatalities.append(teach)
      print("Teacher", teach.ID, "has passed away")
      school.teachers.remove(teach)
    else:
      teach.in_school = True #This assumes people come back to school the first day they are no longer sick - may need to alter depending on the scenario
      teach.is_sick = False
      school.recovered_teachers.append(teach)
#          print("Teacher is already sick. Adding to future exposure.")
