import matplotlib.pyplot as pl
import numpy as np

from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.tree import DecisionTreeRegressor



def ModelLearning(X, y):
    """ Calculates the performance of several models with varying sizes of training data.
        The learning and testing scores for each model are then plotted. """

    # Create 10 cross-validation sets for training and testing
    cv = ShuffleSplit(n_splits=20, test_size=0.3, train_size=None, random_state=0)

    # Generate the training set sizes increasing by 50
    train_sizes = np.rint(np.linspace(1, X.shape[0]*0.7 - 1, 9)).astype(int)

    # Create the figure window
    fig = pl.figure(figsize=(10, 7))

    # Create three different models based on max_depth
    for k, depth in enumerate([3, 6, 10, 15, 20, 25]):

        # Create a Decision tree regressor at max_depth = depth
        regressor = DecisionTreeRegressor(max_depth=depth)

        # Calculate the training and testing scores
        sizes, train_scores, test_scores = learning_curve(regressor, X, y,
                                            cv=cv, train_sizes=train_sizes, scoring='r2')

        # Find the mean and standard deviation for smoothing
        train_std = np.std(train_scores, axis=1)
        train_mean = np.mean(train_scores, axis=1)
        test_std = np.std(test_scores, axis=1)
        test_mean = np.mean(test_scores, axis=1)

        # Subplot the learning curve
        ax = fig.add_subplot(2, 3, k+1)
        ax.plot(sizes, train_mean, 'o-', color='r', label='Training Score')
        ax.plot(sizes, test_mean, 'o-', color='g', label='Testing Score')
        ax.fill_between(sizes, train_mean - train_std,
                        train_mean + train_std, alpha=0.15, color='r')
        ax.fill_between(sizes, test_mean - test_std,
                        test_mean + test_std, alpha=0.15, color='g')

        # Labels
        ax.set_title('max_depth = %s' % (depth))
        ax.set_xlabel('Number of Training Points')
        ax.set_ylabel('Score')
        ax.set_xlim([0, X.shape[0]*0.8])
        ax.set_ylim([-0.05, 1.05])

    # Visual aesthetics
    ax.legend(bbox_to_anchor=(1.05, 2.05), loc='lower left', borderaxespad=0.)
    fig.suptitle('Decision Tree Regressor Learning Performances',
                 fontsize=16, y=1.03)
    fig.tight_layout()
    fig.show()


def ModelComplexity(X, y):
    """ Calculates the performance of the model as model complexity increases.
        The learning and testing errors rates are then plotted. """

    # Create 10 cross-validation sets for training and testing
    cv = ShuffleSplit(n_splits=20, train_size=None, test_size=0.3, random_state=0)

    # Vary the max_depth parameter from 1 to 10
    max_depth = np.arange(1, 11)

    # Calculate the training and testing scores
    train_scores, test_scores = validation_curve(DecisionTreeRegressor(), X, y,
                                                        param_name="max_depth", param_range=max_depth, cv=cv, scoring='r2')

    # Find the mean and standard deviation for smoothing
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    # Plot the validation curve
    pl.figure(figsize=(7, 5))
    pl.title('Decision Tree Regressor Complexity Performance')
    pl.plot(max_depth, train_mean, 'o-', color='r', label='Training Score')
    pl.plot(max_depth, test_mean, 'o-', color='g', label='Validation Score')
    pl.fill_between(max_depth, train_mean - train_std,
                    train_mean + train_std, alpha=0.15, color='r')
    pl.fill_between(max_depth, test_mean - test_std,
                    test_mean + test_std, alpha=0.15, color='g')

    # Visual aesthetics
    pl.legend(loc='lower right')
    pl.xlabel('Maximum Depth')
    pl.ylabel('Score')
    pl.ylim([-0.05, 1.05])
    pl.show()


def plotWithRegressionLine(features, target, target_name, data,
                           fit=True):

    pl.figure(figsize=(25, 10))
    num_of_subplots = len(features.columns)

    for index, col_name in enumerate(features.columns):
        pl.subplot(1, num_of_subplots, index+1)
        x = data[col_name]
        y = target
        pl.plot(x, y, 'o')

        if fit:
            drawRegressionLine(pl, x, y)

        pl.xlabel(col_name)
        pl.ylabel(target_name)
        pl.title(col_name)


def drawRegressionLine(pl, x, y):
    pl.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
