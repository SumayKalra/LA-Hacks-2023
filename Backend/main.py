import scrapping as sc
import classdata as cd
term = "SP23"
activate_driver = sc.activate_driver()

for i in cd.CHEM_num[70:]:
    term = "SP23"
    L =sc.scrapping_data(i, term, activate_driver)


'''
Currently does not work: CHEM 7LM, CHEM 11
fix disscusions
fix ums
'''
#(Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py).Content | python -
