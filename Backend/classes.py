

#PULL NUM OF CLASSES AND CLASS NAME FROM REACT INPUT
num_of_classes = 5 #input from front end 
classes = {}
class_master_dic = {"AERO ST" : "Aerospace Studies", "AF AMERA": "African American Studies", 
                    "AM IND": "American Indian Studies", "ASL": "American Sign+Language",
                      "AN N EA": "Ancient Near East", "ANES": "Anesthesiology", "COM SCI": "Computer+Science" } 
student_classes = ["COM SCI 1", "COM SCI 19" , "COM SCI 30", "COM SCI 31", "COM SCI 33"]

for i in range(num_of_classes):
    class_num = "class" + str(i)
    classes[class_num] = student_classes[i] #input for class name


