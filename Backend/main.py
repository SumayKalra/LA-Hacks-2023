import scrapping as sc
import classdata as cd
term = "SP23"

for i in cd.CHEM_num:
    term = "SP23"
    L =sc.scrapping_data("CHEM 143C", term)


'''
Currently does not work: CHEM 7LM, CHEM 11
fix disscusions
fix ums
'''
#(Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py).Content | python -
