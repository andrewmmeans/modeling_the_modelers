# Modeling the Modelers

![splash](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/main_page.png?raw=true)

## Introduction

cgtrader is an online marketplace for 3d-models. Users can buy and sell models on the site. Each model has a page detailing it with pictures, tags (categories), views and likes as well as description and price. I wrote a web scraper that pull a categorically stratified sample of 3d-models. I wanted to know if there is a significant difference between the number of categories (tags) a model creator tags their model with and the number of views they receive.

## Table of contents
* [Technologies](#technologies)
* [Background](#background)
* [Data Acquisition](#data-acquisition)
* [Data Processing](#data-processing)
* [Exploratory Data Analysis](#exploratory-data-analysis)
* [Hypothesis](#hypothesis)
* [Conclusion](#conclusion)
* [Future Work](#future-work)

## Technologies
Project created with:
* Python
* Pandas
* Matplotlib/Seaborn
* Scipy
* BeautifulSoup
* Espresso Machine

## Background

Working with a dataset that hasn't been analyzed before seemed very appealing to me, albeit challenging. I set out to scrape cgtrader for the purpose of academic analysis of the models posted to the website and their associated data. 

## Data Acquisition

### Overview
1. Discover all categories of models on the site
   * Initial 50+ categories discovered
   * Some categories contained over 3000 pages of models (36 per page)
2. Select categories with the largest number of models available
3. Build the url pages for each category, 276 pages for each category = (50 * 276) = ~ 14,000 pages of models to view
4. Scrape the pages of models for each model url @ 36 models per page = (36 * 14,000) = ~500,000 pages to scrape
   * After analyzing the model urls I noticed that several are counted multiple times
   * After deduplication there were just under 250,000 pages to fetch (whew!)
5. Fetch the deduplicated models and store them to disk for processing

### Lessons Learned

Not everything a site displays is true, most categories contained no more than 277 pages of models, despite claiming 3000+. I guessing that they limit the number of models viewable for users who are not signed into their website. I intent to test this in the future by making an account and observing if more pages are viewable. After deduplication the original even distribution of categories became imbalanced.


![max_pages](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/or_do_they.png?raw=true)


*If you fail to except, try try again.*

I also made the mistake of not retaining the full url when saving the individual pages and so when I attempted to retry all status code 503s the urls were not valid. Some adjustments were made and now the process will retain the full data in the case where retries need to be performed.

## Data Processing

### Overview

The goal was to identify pertinent information on a given model page that would be interesting to include in the exploratory data analysis and modeling. I decided to forego a database creation and leverage local storage for analysis and processing.

### Process
1. Determine the grain of the data, for this I decided the model-level would be sufficient
2. Open a given models page and visually parse the page for important fields
3. Build a list of fields that make sense to parse
4. Associate the visual field with the field's CSS Selector
5. Write regex, beautifulsoup functions to parse the fields
6. Parse each model response for all the data fields that were relevant to the task at hand as well as others for future analysis
   * Fields included: (Model ID, Modeler, Views, Likes, Picture Count, Model Description, Comments

## Exploratory Data Analysis



## Hypothesis


## Conclusion




## Future Work

I will be pursuing further refinement in this project in regards to data acquisition, storage, processing, and analysis. 

### General

* Reapproach the project from a containerization perspective
* Build a docker image for the development and deployment environments
* Leverage a database solution
* Consider cloud services such as AWS, Azure, GCP for platform

### Acquisition Improvements

* Restructure the project in a more object oriented (OOP) fashion
* Leverage a large number of cores in a cloud instance to achieve better parallelization of acquiring the data
* Store the timestamp of retrieval

### Storage Improvements

Due to the semi-structured nature of the data I would consider both SQL and NoSQL solutions

* Store structured data in a SQL DB with tables for Models, Modelers, Comments
* Store unstructured data in NoSQL solution, examples include Images, nested data, model descritions
* Ensure all structured and unstructured tables can be rejoined to their original grain

### Processing

In hindsight, an earlier estimate of the amount of records that would be processed combined with the time of processing each record, I would move this project to a distributed compute environment for processing.

* Leverage Spark for lazy-evaluation time savings
* Leverage Spark for its massive parallel processing capabilities

### Analysis

I would like to further analyze this dataset, I believe that I have barely scratched the surface of the insights that are hidden away in these data.

#### Techniques to explore

* Normalization of variables
* Best fit distributions of the numeric variables
* Apply natural language processing to model descriptions
* Clustering models based on attributes
* Comment sentiment anlysis
* 



