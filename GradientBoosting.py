import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

class GradientBoosting():
    global model
    def __init__(self):
        pass
      
        
    def fit(self,X_train,Y_train):
        self.model=GradientBoostingClassifier(learning_rate=0.1,n_estimators=500,max_features=0.5,max_depth=3)   
        self.model.fit(X_train,Y_train)
        
    def predict(self,X_test):
        prediction_matrix=pd.DataFrame({'Probability':self.model.predict_proba(X_test)[:,1]})
        from sklearn.externals import joblib

        joblib.dump(self.model,'new.pkl')
        return prediction_matrix
        
        
