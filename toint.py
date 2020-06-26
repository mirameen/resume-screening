
class Convert():
    def __init__(self):
        pass
    def fit(self,data):
        
        #converting 'yes'==1 and 'no'==0 to numeric
        data.Attrition_numeric=data.Attrition
        data.loc[data.Attrition=='Yes','Attrition_numeric']=1
        data.loc[data.Attrition=='No','Attrition_numeric']=0
        
        #droping Attrition
        data.drop(['Attrition'],axis=1,inplace=True)
        return data