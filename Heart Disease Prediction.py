import numpy as np
import pandas as pnd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report,roc_auc_score
import seaborn as sn
import statsmodels.api as sm

## Data Preparation
# reading the file
data=pnd.read_csv("framingham.csv")  
print("Initial Data is: ",'\n',data,'\n')

# Variable education dropped since it has no impact on heart disease prediction
# since we are not creating new data frame we are dropping from data only hence inplace is True.
data.drop(['education'],axis=1,inplace=True)        
print("Data after dropping variable education is:",'\n',data,'\n')

# Renaming variable male
data.rename(columns = {'male':'Male(Y/N)'}, inplace = True)
print("Data after renaming column Male is: ",'\n',data,'\n')

## Checking for missing values

#Step 1 - Count null values for each attribute in a dataset
print("Summary of null values is: ",'\n',data.isnull().sum(),'\n')

#Step 2 - Count null values for whole dataset
count=0
for i in data.isnull().sum(axis=1):
    if i>0:
        count=count+1

print('Count of rows with missing values is ', count, "and total number of rows in dataset is", len(data),'\n')
print('Proportion of missing values in a dataset is: ', (count*100)/len(data),'\n')

# Observing summary of a whole dataset
print("Summary of whole dataset is:",'\n',data.describe(),'\n')

# Checking summary of each column having a null values in a dataset
print("Summary of Attribute Cigs Per Day is:",'\n',data['cigsPerDay'].describe(),'\n')
data['cigsPerDay'].fillna((data['cigsPerDay'].mean()), inplace=True)
print("New Summary of Attribute Cigs Per Day is:",'\n',data['cigsPerDay'].describe(),'\n')

print("Summary of Attribute BP Meds is:",'\n',data['BPMeds'].describe(),'\n')
print(data['BPMeds'].value_counts(),'\n')

# Since BPMeds is 0/1, it is replaced with the value which have maximum occurence in the data which is 1.
data['BPMeds'].fillna(1.0, inplace=True)
print("New Summary of Attribute BP Meds is:",'\n',data['BPMeds'].describe(),'\n')

print("Summary of Total Cholestrol is:",'\n',data['totChol'].describe(),'\n')
data['totChol'].fillna((data['totChol'].mean()), inplace=True)
print("New Summary of Attribute Total Cholestrol is:",'\n',data['totChol'].describe(),'\n')

print("Summary of Total BMI is:",'\n',data['BMI'].describe(),'\n')
data['BMI'].fillna((data['BMI'].mean()), inplace=True)
print("New Summary of Attribute Total BMI is:",'\n',data['BMI'].describe(),'\n')

print("Summary of HeartRate is:",'\n',data['heartRate'].describe(),'\n')
data['heartRate'].fillna((data['heartRate'].mean()), inplace=True)
print("New Summary of Attribute HeartRate is:",'\n',data['heartRate'].describe(),'\n')

print("Summary of Glucose is:",'\n',data['glucose'].describe(),'\n')
data['glucose'].fillna((data['glucose'].mean()), inplace=True)
print("New Summary of Attribute Glucose is:",'\n',data['glucose'].describe(),'\n')

# Now checking number of null values in each column
print("After removing null values in a dataset, summary of null values is:",'\n',data.isnull().sum(),'\n')

## Exploratory Analysis
# Plotting histogram of all attributes with bin size 20
data.hist(bins=20,facecolor = 'green')
# To adjust a spacing between multiple histogram plots
plt.tight_layout() 
plt.show()

# Histogram plot for a varibale to be predicted
print(data.TenYearCHD.value_counts(),'\n')
plt.hist(data['TenYearCHD'], facecolor = 'blue')
plt.xlabel('TenYearCHD')
plt.ylabel('Number of Patients')
plt.title('Histogram of patients heart disease distribution')
plt.show()

## Logistic regression using sklearn
y=data.TenYearCHD
x=data.drop('TenYearCHD',axis=1)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=5)

model = LogisticRegression()

#fitting the model with training data
model.fit(x_train,y_train)

print('Coefficient of model :', model.coef_)
print('Intercept of model',model.intercept_)

# predict the target on the train dataset
#predict_train will give 0/1 based on models predicted value
predict_train = model.predict(x_train)
print('Target on train data',predict_train) 

# Accuray Score on train dataset
accuracy_train = accuracy_score(y_train,predict_train)
print('accuracy_score on train dataset : ', accuracy_train)

# predict the target on the test dataset
predict_test = model.predict(x_test)
print('Target on test data',predict_test) 

# Accuracy Score on test dataset
accuracy_test = accuracy_score(y_test,predict_test)
print('accuracy_score on test dataset : ', accuracy_test)

prob = model.predict_proba(x_test)
prob_df = pnd.DataFrame(data = prob,columns = ['Prob of no heart disease (0)','Prob of Heart Disease (1)'])
print('Probability of predicted value is: ','\n')
print(prob_df)

# Finding confusion matrix
cm=confusion_matrix(y_test,predict_test)
print("Confusion matrix is: ",'\n',cm,'\n')

# Verifying accuracy with the help of confusion matrix (Just another way to check accuracy)
TN=cm[0,0]  # Cases in which no was predicted and they don't have a disease
TP=cm[1,1]  # Cases in which yes was predicted and patients actually have a disease
FN=cm[1,0]  # No is predicted but patients actually have a disease
FP=cm[0,1]  # Yes is predicted but patients do not have a disease

print('The acuuracy of the model is',(TP+TN)/float(TP+TN+FP+FN),'\n',
'and The Missclassification of the model is',1-((TP+TN)/float(TP+TN+FP+FN)),'\n')

conf_matrix=pnd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
plt.figure(figsize = (8,5))
sn.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu")
plt.show()

print("Score(Accuracy) of model is:", model.score(x_test,y_test),"\n")
print(classification_report(y_test,predict_test))
print("\n","ROC_AUC Score is:" ,roc_auc_score(y_test,prob[:,1]))

########## Logistic Regression using Statsmodels ##############
print("Another way to fit logistic regression model","\n")
data_constant = sm.add_constant(data)
print("Data with constant column added is: ",'\n')
print(data_constant)

cols=data_constant.columns[:-1]
model_sm = sm.Logit(data_constant['TenYearCHD'],data_constant[cols])
result=model_sm.fit()
print(result.summary())

def backward_elem (data_frame,dep_var,col_list):
    while len(col_list)>0 :
        model_sm=sm.Logit(dep_var,data_frame[col_list])
        result=model_sm.fit(disp=0)
        largest_pvalue=round(result.pvalues,3).nlargest(1)
        if largest_pvalue[0]<(0.05):
            return result
            break
        else:
            col_list=col_list.drop(largest_pvalue.index)

result=backward_elem(data_constant,data['TenYearCHD'],cols)
print(result.summary())

data_significant=data[['Male(Y/N)','age','cigsPerDay','prevalentStroke','sysBP','glucose','TenYearCHD']]
print(data_significant)

y_data_sig = data_significant.TenYearCHD
x_data_sig = data_significant.drop('TenYearCHD',axis=1)

x_train_sig,x_test_sig,y_train_sig,y_test_sig=train_test_split(x_data_sig,y_data_sig,test_size=.20,random_state=5)

logreg=LogisticRegression()
logreg.fit(x_train_sig,y_train_sig)
y_pred_sig=logreg.predict(x_test_sig)

accuracy_test_sig = accuracy_score(y_test_sig,y_pred_sig)
print('accuracy_score on significant test dataset : ', accuracy_test_sig)

prob_sig = logreg.predict_proba(x_test_sig)
prob_sig_df = pnd.DataFrame(data = prob_sig,columns = ['Prob of no heart disease (0)','Prob of Heart Disease (1)'])
print('Probability of predicted value is: ','\n')
print(prob_sig_df)

cm_sig=confusion_matrix(y_test_sig,y_pred_sig)
print("Confusion matrix of significant model is: ",'\n',cm_sig,'\n')

TN_sig=cm_sig[0,0]  # Cases in which no was predicted and they don't have a disease
TP_sig=cm_sig[1,1]  # Cases in which yes was predicted and patients actually have a disease
FN_sig=cm_sig[1,0]  # No is predicted but patients actually have a disease
FP_sig=cm_sig[0,1]  # Yes is predicted but patients do not have a disease

print('The acuuracy of the model is',(TP_sig+TN_sig)/float(TP_sig+TN_sig+FP_sig+FN_sig),'\n',
'and The Missclassification of the model is',1-((TP_sig+TN_sig)/float(TP_sig+TN_sig+FP_sig+FN_sig)),'\n')

conf_matrix_sig=pnd.DataFrame(data=cm_sig,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
plt.figure(figsize = (8,5))
sn.heatmap(conf_matrix_sig, annot=True,fmt='d',cmap="YlGnBu")
plt.show()

print("Score(Accuracy) of model is:",logreg.score(x_test_sig,y_test_sig),"\n")
print(classification_report(y_test_sig,y_pred_sig))
print("\n","ROC_AUC Score is:" ,roc_auc_score(y_test_sig,prob_sig[:,1]))

from sklearn.metrics import roc_curve
fpr_sig, tpr_sig, thresholds = roc_curve(y_test_sig, prob_sig[:,1])
plt.plot(fpr_sig,tpr_sig)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.title('ROC curve for Heart disease classifier')
plt.xlabel('False positive rate (1-Specificity)')
plt.ylabel('True positive rate (Sensitivity)')
plt.grid(True)
plt.show()

params = np.exp(result.params)    # Odds ratio
conf = np.exp(result.conf_int())  # Odds ratio Confidence Interval
conf['OR'] = params
pvalue=round(result.pvalues,3)
conf['pvalue']=pvalue
conf.columns = ['CI 95%(2.5%)', 'CI 95%(97.5%)', 'Odds Ratio','pvalue']
print ((conf))


