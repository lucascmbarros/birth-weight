# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 14:45:22 2019
@author: Lani L. Mateo
Purpose: Predict the factors affecting low birth weight.
Note: Two (2) raw data set explored
"""
# Step 1: Import modules
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split # train/test split
from sklearn.neighbors import KNeighborsRegressor
import sklearn.metrics
from sklearn.model_selection import cross_val_score

# Step 2: Import data set
file = 'birthweight.xlsx'
df = pd.read_excel(file)

# Step 3: Get general info about the full data set
print(df.columns)
print(df.head())
print(df.shape)
print(df.info())
print(df.describe().round(2))

# Step 4: Flag missing values: 
print(df.isnull().sum())
print(df.isnull().sum().sum())
print(((((df[:].isnull().sum())/df[:].count()))).sum().round(2))

for col in df:
    if df[col].isnull().astype(int).sum() > 0:
        df['m_'+col] = df[col].isnull().astype(int)
        
df= pd.DataFrame.copy(df)

# Step 5: Check if there is any significant correlation
corr = df.iloc[:, :-9].corr()
print(corr)

plt.figure(figsize=(15,15))
sns.set(font_scale=1.05)
sns.heatmap(corr,
            square = True,
            annot = True,
            linecolor = 'white',
            linewidths = 0.05)

"""
DATA SET INSIGHT
There are 18 variables and 1832 observations.
Nine (9) variables have null values.
There are 387 total null values.
More than 20% of the observations have missing values.
There is no correlation between birth weight and any of the variables
There isn't significant variance among the variables.
No point doing any further analysis on this data set
"""

# Step 1: Clear variable explorer and console
# Step 2: Run packages
# Step 3: Import new data set
file = 'birthweight_feature_set.xlsx'
df1 = pd.read_excel(file)

# Step 4: Get general info about the full data set
print(df1.columns)
print(df1.shape)
print(df1.info())
df1_summary = df1.iloc[:,:-3].describe().round(2)
print(df1_summary)

# Step 5: Identify and flag missing values
print(df1.isnull().sum())
print(df1.isnull().sum().sum())
print(((((df1[:].isnull().sum())/df1[:].count()))).sum().round(2))

for col in df1:
    if df1[col].isnull().astype(int).sum() > 0:
        df1['m_'+col] = df1[col].isnull().astype(int)      
df1= pd.DataFrame.copy(df1)

a = df1.isnull().sum().sum()
b = df1.iloc[:,-3:].sum().sum()

if a == b:
    print('All missing values accounted for.')
else:
    print('Some missing values may be unaccounted for, please audit.')

"""
DATA SET INSIGHT
There are 18 variables and 196 observations.
Three (3) variables have null values - meduc, npvis and feduc
There are 13 total null values.
7% of the observations having missing values.
"""

# Step 6: Create independent dataframes to test imputation methods
df_0 = pd.DataFrame.copy(df1)
df_median = pd.DataFrame.copy(df_0)

# Step 6a: Impute missing data with zero (0)
df_0= pd.DataFrame.copy(df1)
df_0= df_0.fillna(0)

for col in df_0.iloc[:, :-3]:
    sns.distplot(df_0[col])
    plt.tight_layout()
    plt.show()

# Step 6b: Impute missing data with median
for col in df_median:
        if df_median[col].isnull().astype(int).sum() > 0:
            col_median = df_median[col].median()
            df_median[col] = df_median[col].fillna(col_median).round(2)
            
for col in df_median.iloc[:, :-3]:
    sns.distplot(df_0[col])
    plt.tight_layout()
    plt.show()

# Step 7: Explore data
# Step 7a: Correlation
corr1 = df_median.iloc[:, :-3].corr()
print(corr1)

plt.figure(figsize=(15,12))
sns.set(font_scale=1.15)
sns.heatmap(corr1,
            square = True,
            annot = True,
            linecolor = 'white',
            linewidths = 0.02,
            cbar = True)

"""
CORRELATION INTERPRETATION
There is a low negative correlation between parents' age and child's birthweight.
This means that the older the parents are, the likelihood that their child's
birthweight will be lower than average increases.

Meanwhile there is a moderate negative correlation for both cigarette and
alcohol consumption with child's birthweight. This means that the higher a
mother's consumption of cigarette and alcohol are, the higher the likelihood
that a child's birthweight will be lower than average.
"""

# Step 7b: Outlier Analysis
df_median_quantiles = df_median.loc[:, :].quantile([0.20,
                                                    0.40,
                                                    0.60,
                                                    0.80,
                                                    1.00])    
print(df_median_quantiles)

for col in df_median:
    print(col)

# Step 7c: Distribution
# Birthweight distribution
plt.figure(figsize=(12,8))
sns.distplot(df_median['bwght'],
             bins = None,
             color = 'b')
plt.xlabel('Birthweight')

# Birthweight outliers
plt.figure(figsize=(12,8))
plt.boxplot(x = 'bwght',
            data = df_median,
            vert = False,
            patch_artist = True,
            meanline = True,
            showmeans = True)
plt.xlabel ('Birthweight')
plt.show()

# Mother's age
plt.figure(figsize=(12,8))
sns.distplot(df_median['mage'],
             bins = None,
             color = 'b')

plt.xlabel("Mother's age")

# Mother's Age outliers
plt.figure(figsize=(12,8))
plt.boxplot(x = 'mage',
            data = df_median,
            vert = False,
            patch_artist = True,
            meanline = True,
            showmeans = True)
plt.xlabel ("Mother's Age")
plt.show()

# Mother's Education
plt.figure(figsize=(12,8))
sns.distplot(df_median['meduc'],
             bins = None,
             color = 'b')

plt.xlabel("Mother's Education")

# Mother's Education outliers
plt.figure(figsize=(12,8))
plt.boxplot(x = 'meduc',
            data = df_median,
            vert = False,
            patch_artist = True,
            meanline = True,
            showmeans = True)
plt.xlabel ("Mother's Education")
plt.show()

# Month of Prenatal Care
plt.figure(figsize=(12,8))
sns.distplot(df_median['monpre'],
             bins = None,
             color = 'b')

plt.xlabel("Timing of Prenatal Care")

# Month of Prenatal Care Outliers
plt.figure(figsize=(12,8))
plt.boxplot(x = 'monpre',
            data = df_median,
            vert = False,
            patch_artist = True,
            meanline = True,
            showmeans = True)
plt.xlabel ("Mother's Education")
plt.show()

# Number of Prenatal Care
plt.figure(figsize=(12,8))
sns.distplot(df_median['npvis'],
             bins = None,
             color = 'b')

plt.xlabel("Number of Prenatal Care Visits")

# Number of Prenatal Care Outliers
plt.figure(figsize=(12,8))
plt.boxplot(x = 'npvis',
            data = df_median,
            vert = False,
            patch_artist = True,
            meanline = True,
            showmeans = True)
plt.xlabel ("Number of prenatal care visits")
plt.show()

# Father's Age
plt.figure(figsize=(12,8))
sns.distplot(df_median['fage'],
             bins = 25,
             color = 'b')

plt.xlabel("Father's age")

# Father's Age outliers
plt.figure(figsize=(12,8))
plt.boxplot(x = 'fage',
            data = df_median,
            vert = False,
            patch_artist = True,
            meanline = True,
            showmeans = True)
plt.xlabel ("Father's Age")
plt.show()

# Average cigarette consumption
plt.figure(figsize=(12,8))
sns.distplot(df_median['cigs'],
             bins = 25,
             color = 'g')

plt.xlabel("Average cigarette consumption")

# Average cigarette consumption outliers
plt.figure(figsize=(12,8))
plt.boxplot(x = 'cigs',
            data = df_median,
            vert = False,
            patch_artist = True,
            meanline = True,
            showmeans = True)
plt.xlabel ("Average cigarette consumption")
plt.show()

# Average alcohol consumption
plt.figure(figsize=(12,8))
sns.distplot(df_median['drink'],
             bins = 15,
             color = 'y')

plt.xlabel("Average alcohol consumption")

# Average alcohol consumption outliers
plt.figure(figsize=(12,8))
plt.boxplot(x = 'drink',
            data = df_median,
            vert = False,
            patch_artist = True,
            meanline = True,
            showmeans = True)
plt.xlabel ("Average alcohol consumption")
plt.show()

# Step 7d Scatterplots
# Mother's Age
sns.set(font_scale=1.5)
df_mage = sns.lmplot(x = 'mage',
                y = 'bwght',
                height=8,
                aspect= 1.5,
                fit_reg = True,
                scatter_kws={"s": 300},
                palette = 'plasma',
                data = df_median)
plt.title ("Birthweight and Mother's Age")
plt.ylabel ('Birthweight')
plt.xlabel ("Mother's Age")
plt.show()

# Mother's Education
sns.set(font_scale=1.5)
df_mage = sns.lmplot(x = 'meduc',
                y = 'bwght',
                height=8,
                aspect= 1.5,
                fit_reg = True,
                scatter_kws={"s": 300},
                palette = 'plasma',
                data = df_median)
plt.title ("Birthweight and Mother's Education")
plt.ylabel ('Birthweight')
plt.xlabel ("Mother's Education")
plt.show()

# Father's Age
sns.set(font_scale=1.5)
df_mage = sns.lmplot(x = 'fage',
                y = 'bwght',
                height=8,
                aspect= 1.5,
                fit_reg = True,
                scatter_kws={"s": 300},
                palette = 'plasma',
                data = df_median)
plt.title ("Birthweight and Father's Age")
plt.ylabel ('Birthweight')
plt.xlabel ("Father's Age")
plt.show()

# Father's Education
sns.set(font_scale=1.5)
df_mage = sns.lmplot(x = 'feduc',
                y = 'bwght',
                height=8,
                aspect= 1.5,
                fit_reg = True,
                scatter_kws={"s": 300},
                palette = 'plasma',
                data = df_median)
plt.title ("Birthweight and Father's Education")
plt.ylabel ('Birthweight')
plt.xlabel ("Father's Education")
plt.show()

# Month of prenatal visits
sns.set(font_scale=1.5)
df_mage = sns.lmplot(x = 'monpre',
                y = 'bwght',
                height=8,
                aspect= 1.5,
                fit_reg = True,
                scatter_kws={"s": 300},
                palette = 'plasma',
                data = df_median)
plt.title ("Birthweight and Month of Prenatal Visit")
plt.ylabel ('Birthweight')
plt.xlabel ("Month of Prenatal Visit")
plt.show()

#Number of prenatal visits
sns.set(font_scale=1.5)
df_mage = sns.lmplot(x = 'npvis',
                y = 'bwght',
                height=8,
                aspect= 1.5,
                fit_reg = True,
                scatter_kws={"s": 300},
                palette = 'plasma',
                data = df_median)
plt.title ("Birthweight and Number of Prenatal Visit")
plt.ylabel ('Birthweight')
plt.xlabel ("Number of Prenatal Visit")
plt.show()

#Average cigarette consumption
sns.set(font_scale=1.5)
df_mage = sns.lmplot(x = 'cigs',
                y = 'bwght',
                height=8,
                aspect= 1.5,
                fit_reg = True,
                scatter_kws={"s": 300},
                palette = 'plasma',
                data = df_median)
plt.title ("Birthweight and Average cigarette consumption")
plt.ylabel ('Birthweight')
plt.xlabel ("Average cigarette consumption")
plt.show()

#Average alcohol consumption
sns.set(font_scale=1.5)
df_mage = sns.lmplot(x = 'drink',
                y = 'bwght',
                height=8,
                aspect= 1.5,
                fit_reg = True,
                scatter_kws={"s": 300},
                palette = 'plasma',
                data = df_median)
plt.title ("Birthweight and Average alcohol consumption")
plt.ylabel ('Birthweight')
plt.xlabel ("Average alcohol consumption")
plt.show()

##############################################################################
#Regression Analysis
##############################################################################
# Full Model
df_median_bwght = smf.ols(formula = """bwght ~ df_median['mage'] +
                                              df_median['meduc'] +
                                              df_median['monpre'] +
                                              df_median['npvis'] +
                                              df_median['fage'] +
                                              df_median['feduc'] +
                                              df_median['omaps'] +
                                              df_median['fmaps'] +
                                              df_median['cigs'] +
                                              df_median['drink'] +
                                              df_median['male'] +
                                              df_median['mwhte'] +
                                              df_median['mblck'] +
                                              df_median['moth'] +
                                              df_median['fwhte'] +
                                              df_median['fblck'] +
                                              df_median['foth'] +
                                              df_median['bwght'] +
                                              df_median['m_meduc'] +
                                              df_median['m_npvis'] +
                                              df_median['m_feduc']
                                              """,
                                              data = df_median)
results_bwght = df_median_bwght.fit()
print(results_bwght.summary())

print(f"""
Summary Statistics:
R-Squared:          {results_bwght.rsquared.round(3)}
Adjusted R-Squared: {results_bwght.rsquared_adj.round(3)}
""")
    
predict = results_bwght.predict()
y_hat   = pd.DataFrame(predict).round(2)
resids  = results_bwght.resid.round(2)

# We can find more functions available using the dir() command.
dir(results_bwght)

# Saving as a new dataset for future use.
df_median.to_excel('Birthweight_Dummies.xlsx')

"""
INSIGHT
The full model doesn't help and results to strong multicollinearity.
Some of the variables doesn't inform the model and should be dropped.
"""

# Prioritize and drop variables
df_median_data = df_median.drop(['bwght',
                            'omaps',
                            'fmaps',
                            'fage',
                            'feduc',
                            'm_meduc',
                            'm_feduc',
                            'm_npvis',                            
                            'male' ,
                           'mwhte' ,
                           'mblck' ,
                           'moth' ,
                           'fwhte' ,
                           'fblck' ,
                           'foth'],
                           axis = 1)

print(df_median_data)

# Train Data Set
df_median_target = df_median.loc[:, 'bwght']

X_train, X_test, y_train, y_test = train_test_split(
                                               df_median_data,
                                               df_median_target)

# Training set 
print(X_train.shape)
print(y_train.shape)

# Testing set
print(X_test.shape)
print(y_test.shape)

"""
67% of the data went to the training dataset,
while 33% went to the testing dataset
"""

X_train, X_test, y_train, y_test = train_test_split(
            df_median_data,
            df_median_target,
            test_size = 0.25,
            random_state = 508)

# Training set 
print(X_train.shape)
print(y_train.shape)

# Testing set
print(X_test.shape)
print(y_test.shape)

knn_reg = KNeighborsRegressor(algorithm = 'auto',
                              n_neighbors = 1)

# Checking the type of this new object
type(knn_reg)

# Teaching (fitting) the algorithm based on the training data
knn_reg.fit(X_train, y_train)

# Predicting on the X_data that the model has never seen before
y_pred = knn_reg.predict(X_test)

# Printing out prediction values for each test observation
print(f"""
Test set predictions:
{y_pred}
""")
    
y_score = knn_reg.score(X_test, y_test)#rsquared value
y_score_train = knn_reg.score(X_train, y_train)
y_score_test = knn_reg.score(X_test, y_test)

# The score is directly comparable to R-Square
print(y_score)
print(y_score_train)#training data should never be one, overfit data
print(y_score_test)

"""
y_score_train is equal to 1. Hence data is overfit.
"""
# Creating two lists, one for training set accuracy and the other for test
# set accuracy
training_accuracy = []
test_accuracy = []

# Building a visualization to check to see  1 to 50
neighbors_settings = range(1, 50)#set number of neighbors


for n_neighbors in neighbors_settings:
    # Building the model
    clf = KNeighborsRegressor(n_neighbors = n_neighbors)
    clf.fit(X_train, y_train)
    
    # Recording the training set accuracy
    training_accuracy.append(clf.score(X_train, y_train))
    
    # Recording the generalization accuracy
    test_accuracy.append(clf.score(X_test, y_test))
    
fig, ax = plt.subplots(figsize=(12,9))
plt.plot(neighbors_settings, training_accuracy, label = "training accuracy")
plt.plot(neighbors_settings, test_accuracy, label = "test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()
plt.show()

########################
# What is the optimal number of neighbors?
########################

print(max(test_accuracy))
print(test_accuracy.index(max(test_accuracy))+1)
# The best results occur when k = 5.

# Building a model with k = 5
knn_reg = KNeighborsRegressor(algorithm = 'auto',
                              n_neighbors = 5)

# Fitting the model based on the training data
knn_reg.fit(X_train, y_train)
y_pred = knn_reg.predict(X_test)
y_score = knn_reg.score(X_test, y_test)

# The score is directly comparable to R-Square
print(y_score)
print(f"""
Our base to compare other models is {y_score.round(3)}.
    
This base helps us evaluate more complicated models and lets us consider
tradeoffs between accuracy and interpretability.
""")
#Test score based on top 4 var by corr mage, fage, cigs, drink is 0.496
#Test score with mage, monpre, npvis, fage, cigs, drink is 0.462
#Test score with mage, fage, meduc, feduc, monpre, npvis, cigs, drink is 0.512
#Test score for mage, fage, meduc, monpre, npvis, cigs, drink is 0.534
#Test score with mage, meduc, monpre, npvis, cigs, drink is 0.546
