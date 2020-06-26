'''
Logistic Regression Class
'''
import numpy as np
import pandas
class LogisticRegression():
    global learned_weights
    def __init__(self):
        pass
    
    
    #link function
    def sigmoid(self,score):
        return 1/(1+np.exp(-score))

    def predict_probability(self,features,weights):
        score=np.dot(features,weights)
        return self.sigmoid(score)

    # feature derivative computation with L2 regularization
    def l2_feature_derivative(self,errors, feature, weight, l2_penalty, feature_is_constant):
        derivative = np.dot(np.transpose(errors), feature)
  
        if not feature_is_constant:
            derivative -= 2 * l2_penalty * weight

        return derivative

    # log-likelihood computation with L2 regularization
    def l2_compute_log_likelihood(self,features, labels, weights, l2_penalty):
        indicator = (labels==+1)
        scores    = np.dot(features, weights)
        ll        = np.sum((np.transpose(np.array([indicator]))-1)*scores - np.log(1. + np.exp(-scores))) - (l2_penalty * np.sum(weights[1:]**2))
        return ll

    # logistic regression with L2 regularization
    def l2_logistic_regression(self,features, labels, lr, epochs, l2_penalty):
       
        # add bias (intercept) with features matrix
        bias      = np.ones((features.shape[0], 1))
        features  = np.hstack((bias, features))

      # initialize the weight coefficients
        weights = np.zeros((features.shape[1], 1))
        
        logs = []

      # loop over epochs times
        for epoch in range(epochs):

            # predict probability for each row in the dataset
            predictions = self.predict_probability(features, weights)
            
            # calculate the indicator value
            indicators = (labels==+1)
            
            # calculate the errors
            errors = np.transpose(np.array([indicators])) - predictions
            
            # loop over each weight coefficient
            for j in range(len(weights)):
                
                isIntercept = (j==0)
                
                # calculate the derivative of jth weight cofficient
                derivative = self.l2_feature_derivative(errors, features[:,j], weights[j], l2_penalty, isIntercept)
                weights[j] += lr * derivative
                
            # compute the log-likelihood
            ll = self.l2_compute_log_likelihood(features, labels, weights, l2_penalty)
            logs.append(ll)
                
        import matplotlib.pyplot as plt
        x = np.linspace(0, len(logs), len(logs))
        fig = plt.figure()
        plt.plot(x, logs)
        fig.suptitle('Training the classifier (with L2)')
        plt.xlabel('Epoch')
        plt.ylabel('Log-likelihood')
        #fig.savefig('train_with_l2.jpg')
        plt.show()
                
        return weights
            

    def fit(self,X_train,Y_train):
        # hyper-parameters
        learning_rate = 1e-6
        epochs        = 2000
        l2_penalty    = 0.001
        
        # perform logistic regression and get the learned weights
        
        self.learned_weights= self.l2_logistic_regression(X_train, Y_train, learning_rate, epochs, l2_penalty)
        
    
    def predict(self,X_test):
       
         bias_test      = np.ones((X_test.shape[0], 1))
         features_test  = np.hstack((bias_test, X_test))
         test_predictions  = (self.predict_probability(features_test, self.learned_weights).flatten())
         
         #print(self.learned_weights)
         #print(type(self.learned_weights))
         return pandas.DataFrame({'Probability':test_predictions})