## Chilling effects online surveillance and Wikipedia use
### Abstract
Persuing the same goal as the authors but with a bigger context. We use more data sources as well as more countries and longer period of time. the goal is to prove or disprove the original authors theory or atleast weaken/strenghthen their argument. We'll use Wikipedia and Google Trends data. Tell the story of the different chilling effects for people across different demographics and countries especially highlighting what those differences might be for people directly affected by the surveillance and those on the fringe of NSA's radar. 

### Research Questions
- Are the chilling effects long lasting or do they dissapear after an extended period of time
- Are the observed chilling effects only present on Wikipedia or do they appear on Google Trends as well
- What are the different patterns of chilling effects on different populations and countries

### Proposed dataset
1. English, German, French, Italian, Spanish, Russian, Japanese, Portuguese, Arabic, Hindu Wikipedia data from January 2011-2016
2. Google trends data from January 2011-2016

We expect to get the data from the public APIs of Wikipedia and Google Trends. We'll apply a similar preprocessing phase for the data as described in the paper, excluding all the irrelevant articles and focusing on the 48 topics identified in the original paper. We expect the Wikipedia data to be similar to the data in the paper, for all languages. We'll also use the Google Trends API to get data by country on the same topics and possibly translate those topics to other languages and get data on those queries as well.  

Data size is not supposed to be a problem since we're limiting it to those 48 topics presented in the original paper.

### Methods

Double linear regression interrupted time series to study the data trends before and after June 2013

### Proposed timeline

Week 1: Data collection and scrapping

Week 2: Method design and Data processing

Week 3: Data analysis and interpretation, report writing

### Organization within the team
![TaskOrganization](./TaskOrganization.png)

### Questions for TAs (optional)

* How big must the outlier be for us to take it into account? Since we have multiple languages there's a very large number of possible outliers.