# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''
Pandas Basics: Reading Files, Summarizing, Handling Missing Values, Filtering, Sorting
'''

# read in the CSV file from a URL
drinks = pd.read_csv('drinks.csv')
drinks = pd.read_csv('https://raw.githubusercontent.com/justmarkham/python-data-analysis-workshop/master/drinks.csv')
type(drinks)

# examine the data
drinks                  # print the first 30 and last 30 rows
drinks.head()           # print the first 5 rows
drinks.tail()           # print the last 5 rows
drinks.describe()       # describe any numeric columns
drinks.info()           # concise summary

# find missing values in a DataFrame
drinks.isnull()         # DataFrame of booleans
drinks.isnull().sum()   # convert booleans to integers and add

# handling missing values
drinks.dropna()             # drop a row if ANY values are missing
drinks.fillna(value='NA')   # fill in missing values

# fix the original import
drinks = pd.read_csv('https://raw.githubusercontent.com/justmarkham/python-data-analysis-workshop/master/drinks.csv', na_filter=False)
drinks.isnull().sum()

# selecting a column ('Series')
drinks['continent']
drinks.continent            # equivalent
type(drinks.continent)

# summarizing a non-numeric column
drinks.continent.describe()
drinks.continent.value_counts()

# selecting multiple columns
drinks[['country', 'beer_servings']]
my_cols = ['country', 'beer_servings']
drinks[my_cols]

# add a new column as a function of existing columns
drinks['total_servings'] = drinks.beer_servings + drinks.spirit_servings + drinks.wine_servings
drinks.head()

# logical filtering and sorting
drinks[drinks.continent=='NA']
drinks[['country', 'total_servings']][drinks.continent=='NA']
drinks[['country', 'total_servings']][drinks.continent=='NA'].sort_index(by='total_servings')
drinks[drinks.wine_servings > 300]
drinks[drinks.wine_servings > drinks.beer_servings]
drinks.sort_index(by='beer_servings').tail()
drinks.beer_servings[drinks.continent=='NA'].mean()
drinks.beer_servings[drinks.continent=='EU'].mean()


'''
Split-Apply-Combine
'''

# for each continent, calculate mean beer servings
drinks.groupby('continent').beer_servings.mean()

# for each continent, count number of occurrences
drinks.groupby('continent').continent.count()
drinks.continent.value_counts()

# for each continent, calculate the min, max, and range for total servings
drinks.groupby('continent').total_servings.min()
drinks.groupby('continent').total_servings.max()
drinks.groupby('continent').total_servings.apply(lambda x: x.max() - x.min())


'''
Plotting
'''

# bar plot of number of countries in each continent
drinks.continent.value_counts().plot(kind='bar', title='Countries per Continent')
plt.xlabel('Continent')
plt.ylabel('Count')
plt.show()

# bar plot of average number of beer servings by continent
drinks.groupby('continent').beer_servings.mean().plot(kind='bar')

# histogram of beer servings
drinks.beer_servings.hist(bins=20)

# grouped histogram of beer servings
drinks.beer_servings.hist(by=drinks.continent, sharex=True)

# density plot of beer servings
drinks.beer_servings.plot(kind='density', xlim=(0,500))

# boxplot of beer servings by continent
drinks.boxplot(column='beer_servings', by='continent')

# scatterplot of beer servings versus wine servings
drinks.plot(x='beer_servings', y='wine_servings', kind='scatter', alpha=0.3)

# same scatterplot, except all European countries are colored red
colors = np.where(drinks.continent=='EU', 'r', 'b')
drinks.plot(x='beer_servings', y='wine_servings', kind='scatter', c=colors)


'''
Joining Data
'''

# read 'u.data' into 'ratings'
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_table('u.data', header=None, names=r_cols, sep='\t')

# read 'u.item' into 'movies'
m_cols = ['movie_id', 'title']
movies = pd.read_table('u.item', header=None, names=m_cols, sep='|', usecols=[0,1])

# merge 'movies' and 'ratings' (inner join on 'movie_id')
movies.head()
ratings.head()
movie_ratings = pd.merge(movies, ratings)
movie_ratings.head()


'''
Further Exploration
'''

# for each movie, count number of ratings
movie_ratings.title.value_counts()

# for each movie, calculate mean rating
movie_ratings.groupby('title').rating.mean().order(ascending=False)

# for each movie, count number of ratings and calculate mean rating
movie_ratings.groupby('title').rating.count()
movie_ratings.groupby('title').rating.mean()
movie_stats = movie_ratings.groupby('title').agg({'rating': [np.size, np.mean]})
movie_stats.head()  # hierarchical index

# limit results to movies with more than 100 ratings
movie_stats[movie_stats.rating.size > 100].sort_index(by=('rating', 'mean'))
