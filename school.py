class School:
  def __init__(self, name, teacher_ct, student_ct):
    self.students = [student_ct]
    self.teachers = [teacher_ct]
    self.num_students = student_ct
    self.num_teachers = teacher_ct
    self.classroom_count = teacher_ct/1.5
    self.school_ID = name
    self.exposed_classrooms = []
    self.exposed_lunch = []
    self.symptomatic_classrooms = []
    self.recovered_students = []
    self.recovered_teachers = []
    self.fatalities = []