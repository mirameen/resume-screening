import pandas as pd
from Pipeline import Pipeline
from toint import Convert
from sklearn.model_selection import train_test_split

global pipe


    
#loading the dataset
data=pd.read_csv('C:/web dev/EmployeeChurnAnalysis/Dataset.csv')
    
#converting Attrition String column to Attrition Numeric column
cvt=Convert()
data=cvt.fit(data)
        
#preparing data for train-test split
x=data.drop(['EmployeeID','Attrition_numeric'],axis=1)
y=data['Attrition_numeric']
    


# split the dataset into training and testing 
X_train, X_test, Y_train, Y_test = train_test_split(x,y, test_size=0.20, random_state=9)
    
pipe=Pipeline('GradientBoosting')
pipe.fit(X_train,Y_train)
#Prediction_matrix has the Attrition Probability 
Prediction_matrix=pipe.predict(X_test)

#Model Performance
score=pipe.score(Y_test,Prediction_matrix)
print(score)
pipe.plot_roc_curve(Y_test,Prediction_matrix)

#Saving the Model
import joblib

joblib.dump(pipe,'gb.pkl')

#Printing the model output

EmployeeID=pd.DataFrame(data['EmployeeID'])
Predicted_probability=pd.DataFrame(pipe.predict(x))
Predicted_probability.columns=['Predicted_Probability']
Prediction=pd.DataFrame((Predicted_probability>0.5))
Prediction.columns=['Prediction']
Actual_Attrition=pd.DataFrame(data['Attrition_numeric'])

dataset=pd.concat([EmployeeID, Predicted_probability, Prediction, Actual_Attrition],axis=1)

print(dataset)

    
dataset.to_csv('C:/web dev/EmployeeChurnAnalysis/OutputLR.csv')



