'''
This Module is used for predicting Attrition Probability for the new datapoint
'''
import sys
import json
import pandas as pd
from Pipeline import Pipeline
import joblib
from DataPreprocessing import OneHotEncoder

random='{"EmployeeID":"1234","Age":"41","BusinessTravel":"Travel_Rarely","Department":"Sales","DistanceFromHome":"8","Education":"2","EducationField":"Marketing","EnvironmentSatisfaction":"1","Gender":"Female","JobInvolvement":"2","JobLevel":"2","JobRole":"Research Scientist","JobSatisfaction":"2","MaritalStatus":"Married","MonthlyIncome":"5993","NumCompaniesWorked":"3","OverTime":"No","PercentSalaryHike":"11","PerformanceRating":"1","RelationshipSatisfaction":"1","TotalWorkingHours":"8","TrainingTimesLastYear":"0","WorkLifeBalance":"1","YearsAtCompany":"4","YearsInCurrentRole":"3","YearsSinceLastPromotion":"3","YearsWithCurrManager":"3"}'

dat1=json.loads(sys.argv[1])

dat1=pd.DataFrame(dat1,index=[0])

X_predict1=dat1.drop(['EmployeeID'],axis=1)

X_predict2=dat1.drop(['EmployeeID'],axis=1)
pipe1=joblib.load('gb.pkl')
pipe2=joblib.load('lr.pkl')

prob1=pipe1.predict(X_predict1)

prob2=pipe2.predict(X_predict2)

prob_final=(prob1+prob2)/2.0

print(prob2)