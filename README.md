# Hook N Cook
HookNCook is a laptop recommendation system that uses data from [daraz](https://daraz.com.np). HookNCook scrapes laptop specifications and daily price data. All data is stored in csv files for faster access and easier distribution. HookNCook’s recommendation models use simple vector distances to recommend laptops closest to the given parameters.
## High level overview of the project structure
#### 1. Scraper
Web Scraper that scrapes daraz’s data using selenium. detail_scraper is used for data cleaning.
#### 2. Data
Actual data scraped by scrapers
#### 3. Preparation
Data cleaning and analysis using pandas and seaborn. We have also answered 4 research questions. You can take a look yourself but if don’t want to then the main conclusion is that the laptops with the best money and specs ratio can be found in 1,00,000 to 2,00,000 range after 2,00,000 you may want to consider buying a PC.
#### 4. Model
Recommendation models using pandas and numpy.
#### 5. Hookncook
Flask web app that handles the website frontend and backend. Flask also handles user authentication.
#### 6. Instance
Database instance used by flask for user authentication.
## Datasets Schema
There are 3 kinds of data scraped by the project.
### urls.csv
This acts like a map for the project to look for products online and offline and it also contains encrypted filenames later used as primary key.
![](https://i.imgur.com/c4fYBrV.png)
### laptop.csv
Dataset of laptops available in daraz.
![](https://i.imgur.com/Swjm3in.png)
### prices/{filename}.csv
Prices data of particular laptops.

![](https://i.imgur.com/RtFCqMF.png)

Data of Dell vostro 3520.
## Models
In both models we only use the price and categorical columns of laptop.csv for recommendations. The other columns are used by flask for frontend and redirecting to daraz.
In both models the price column is min-max normalized.
1. One Hot: Categorical columns are one hot encoded.
2. One N: Categorical columns are label encoded.

After the ecoding finishes we also encoded the user input and use numpy to find the vector distances and recommend the laptops closest to the input vector.