# Hook N Cook
Hook N Cook is a web scraping and data science project that aims to scrape the data of all the laptops available on daraz.com.np store them into csv files and give the best deals.
Also with enough data we can also predict if a products prices are going to drop or rise.
This feature is essential because we want to give the user the ability to track a certain product if he want to buy it but is willing to wait incase the prices drop.
## Datasets Schema
The starting point of this project is the urls of each laptop on daraz they can be found on the file urls_and_filenames.csv along with the unique filenames for each url to store the long term price data.
![](https://i.imgur.com/TNQzCBe.png)

It looks something like this.
Then the price data of each products looks like this.
![](https://i.imgur.com/Kdgh9do.png)

Right now the file is very short but it will have many more rows.
Lastly the actual dataset that we will be creating which will have all the data about laptops available on daraz look like this.
![](https://i.imgur.com/9eseS6t.png)

## Recommendation model
After the data has been collected and cleaned we can begin the actual project of recommending the best laptop taylored to each user in the current market.