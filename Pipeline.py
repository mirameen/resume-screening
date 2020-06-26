'''
Pipeline Class
'''
from DataPreprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from LogisticRegression import LogisticRegression 
from GradientBoosting import GradientBoosting
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve,auc,roc_auc_score
import matplotlib.pyplot as plt


class Pipeline():
    global scaler
    global instance
    global X_test
    global X_train
    global Y_train
    def __init__(self,Classifier):
        
        self.Classifier=Classifier
        
        
    
    def fit(self,X_train,Y_train):
        self.X_train=X_train
        self.Y_train=Y_train
        encoder=OneHotEncoder()
        self.X_train=encoder.transform(self.X_train)
        
        self.scaler=StandardScaler().fit(self.X_train)
        self.X_train=self.scaler.transform(self.X_train)
        
        if self.Classifier=='LogisticRegression':
            self.instance=LogisticRegression()
            self.instance.fit(self.X_train,self.Y_train)
        
        elif self.Classifier=='GradientBoosting':
            self.instance=GradientBoosting()
            self.instance.fit(self.X_train,self.Y_train)
        
        else:
            print('Please enter a Valid Classifier')
       
        
    def predict(self,X_test):
       
        self.X_test=X_test
        encoder=OneHotEncoder()
        if len(X_test)==1:
            self.X_test=encoder.transformp(self.X_test)
        else:
            self.X_test=encoder.transform(self.X_test)
            
       
        self.X_test=self.scaler.transform(self.X_test)
       
        
        prediction_matrix=self.instance.predict(self.X_test)
        
        return prediction_matrix
       
        
    #score method returns the full classification report of the model
    def score(self,Y_test,predictions):
        predictions=(predictions>0.5)
        c_report=classification_report(Y_test,predictions)
        return c_report
    
    #plot_roc_curve plots the ROC curve on the console
    def plot_roc_curve(self,Y_test,predictions):
        predictions=(predictions>0.5)
        fpr=dict()
        tpr=dict()
        roc_auc=dict()
        fpr,tpr,_=roc_curve(Y_test,predictions)
        roc_auc=auc(fpr,tpr)
        plt.figure()
        plt.plot(fpr,tpr,label='ROC_CURVE(area=%0.2f)'%roc_auc)
        plt.plot([0,1],[0,1],color='navy',linestyle='--')
        plt.xlim([0.0,1.0])
        plt.ylim([0.0,1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristics Curve')
        plt.legend(loc='lower right')
        plt.show()
        return        
        
        
        
      
        
        
    