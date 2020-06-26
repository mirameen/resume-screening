import pandas as pd

class OneHotEncoder():
    
    global X
    
    def __init__(self):
        pass
    
    def fit(self,X):
        pass
        
    
    def transform(self,X):
        columns=['BusinessTravel','Department','EducationField','OverTime','Gender','MaritalStatus','JobRole']
        for item in columns:
            dummy=pd.get_dummies(X[item])
            dummy.drop(dummy.columns[0],axis=1,inplace=True)
            X=pd.concat([X,dummy],axis=1)
            X.drop([item],axis=1,inplace=True)
        return X.astype(float)
        
        
        
    def transformp(self,X):
        
        columns=['BusinessTravel','Department','EducationField','OverTime','Gender','MaritalStatus','JobRole']
        for item in columns:
            if item=='BusinessTravel':
                Travel_Rarely=0
                Travel_frequently=0
                if X[item][0]=='Travel_Rarely':
                    Travel_Rarely=1
           
                elif X[item][0]=='Travel_Frequently':
                    Travel_frequently=1
                 
                X['Travel_Rarely']=Travel_Rarely
                X['Travel_frequently']=Travel_frequently
                X.drop(['BusinessTravel'],axis=1,inplace=True)
       
            elif item=='Department':
                Sales=0
                rnd = 0
                if X[item][0]=='Sales':
                    Sales=1
                elif X[item][0]=='Research & Development':
                    rnd=1
                
                X['Sales']=Sales
                X['Research & Development']=rnd
                X.drop(['Department'],axis=1,inplace=True)
            
            elif item == 'EducationField':
                LifeSciences = 0
                Medical=0
                Marketing=0
                TechnicalDegree=0
                HumanResources=0
                if X[item][0]=='Life Sciences':
                    LifeSciences=1
                elif X[item][0]=='Medical':
                    Medical=1
                elif X[item][0]=='Marketing':
                    Marketing=1  
                elif X[item][0]=='Technical Degree':
                    TechnicalDegree=1
                elif X[item][0]=='Human Resources':
                    HumanResources=1
                 
                X['Life Sciences']=LifeSciences
                X['Medical']=Medical
                X['Marketing']=Marketing
                X['Technical Degree']=TechnicalDegree
                X['Human Resources']=HumanResources
                X.drop(['EducationField'],axis=1,inplace=True)
        
            elif item=='Gender':
                Male=0
                if X[item][0]=='Male':
                    Male=1
            
                X['Male']=Male
                X.drop(['Gender'],axis=1,inplace=True)
                
            elif item=='OverTime':
                Y=0
                if X[item][0]=='Yes':
                    Y=1
            
                X['Yes']=Y
                X.drop(['OverTime'],axis=1,inplace=True)
            
            elif item=='MaritalStatus':
                Si=0
                Ma = 0
                if X[item][0]=='Single':
                    Si=1
                elif X[item][0]=='Married':
                    Ma=1
                
                X['Single']=Si
                X['Married']=Ma
                X.drop(['MaritalStatus'],axis=1,inplace=True)
            
            elif item == 'JobRole':
                SalesExecutive = 0
                ResearchScientist=0
                LaboratoryTechnician=0
                ManufacturingDirector=0
                Manager=0
                ResearchDirector=0
                SalesRepresentative=0
                HealthcareRepresentative=0
                if X[item][0]=='Sales Executive':
                    SalesExecutive=1
                elif X[item][0]=='Research Scientist':
                    ResearchScientist=1
                elif X[item][0]=='Laboratory Technician':
                    LaboratoryTechnician=1  
                elif X[item][0]=='Manufacturing Director':
                    ManufacturingDirector=1
                elif X[item][0]=='Manager':
                    Manager=1
                elif X[item][0]=='Research Director':
                    ResearchDirector=1
                elif X[item][0]=='Sales Representative':
                    SalesRepresentative=1
                elif X[item][0]=='Healthcare Representative':
                    HealthcareRepresentative=1
                 
                X['Sales Executive']=SalesExecutive
                X['Research Scientist']=ResearchScientist
                X['Laboratory Technician']=LaboratoryTechnician
                X['Manufacturing Director']=ManufacturingDirector
                X['Manager']=Manager
                X['Research Director']=ResearchDirector
                X['Sales Representative']=SalesRepresentative
                X['Healthcare Representative']=HealthcareRepresentative
                X.drop(['JobRole'],axis=1,inplace=True)
        X=X.astype(float)
        return X