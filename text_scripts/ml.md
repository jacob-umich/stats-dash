We can use machine learning to predict the life expectancy of a population based on their health statistics. First we will need to determine which machine learning model is the most appropriate given our data. Since our data set size is limited, only decision trees, linear regression, and support vector machines will be considered. Several parameters for each model type were considered. The results of the hyper parameter tuning are below. Then, you can use the trained model to predict the life expectancy of a population.

|                   |          Coefficient of Determination |
|:------------------|-----------:|
| dt_0              | -0.291158  |
| dt_1              | -0.190431  |
| dt_2              |  0.195415  |
| linear_regression |  0.438447  |
| svm_0             |  0.417338  |
| svm_1             |  0.41994   |
| svm_2             | -0.0675991 |
| svm_3             | -0.281357  |
| svm_4             | -0.322533  |
| svm_5             | -0.322534  |

It appears a simple linear regression produces the best results