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

Not everything a site displays is true, most categories contained no more than 277 pages of models, despite claiming 3000+. It is possible cgtrader limits the number of models viewable for users who are not signed into their website. I intent to test this in the future by making an account and observing if more pages are viewable. After model deduplication, what was an even distribution of categories became imbalanced.

![max_pages](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/or_do_they.png?raw=true)

I made the mistake of not retaining the full url when saving the individual pages and so when I attempted to retry all status code 503s the urls were not valid. I adjusted the script and now the process will keep the full data in the case a retry is necessary.

*If you fail to except, try try again.*

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

### View of the data


```python
df.head()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>modeler</th>
      <th>modeler_response</th>
      <th>modeler_ratings</th>
      <th>tags</th>
      <th>views</th>
      <th>likes</th>
      <th>review_count</th>
      <th>comments</th>
      <th>price</th>
      <th>pic_count</th>
      <th>model_description</th>
      <th>model_details</th>
      <th>price_usd</th>
      <th>tag_count</th>
      <th>response_time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>andriy115599</td>
      <td>{'percent': 100, 'time': '5.0h'}</td>
      <td>{'avg_rating': 3.9, 'num_rating': 14}</td>
      <td>[accessorie, appliance, barazza, furniture, ki...</td>
      <td>351</td>
      <td>0</td>
      <td>0</td>
      <td>{'authors': [], 'texts': [], 'datetimes': []}</td>
      <td>$6.00</td>
      <td>30</td>
      <td>High quality 3d models of Barazza. The models ...</td>
      <td>{'model_id': '801556', 'geometry': 'Subdivisio...</td>
      <td>6.00</td>
      <td>7</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>sinartur</td>
      <td>{'percent': 0, 'time': 0}</td>
      <td>{'avg_rating': 0, 'num_rating': 0}</td>
      <td>[bed, furniture, pillow, comfort, modern, styl...</td>
      <td>96</td>
      <td>1</td>
      <td>0</td>
      <td>{'authors': ['GGAF'], 'texts': ['cool'], 'date...</td>
      <td>$14.99</td>
      <td>10</td>
      <td>This 3d model Lipende sofa has a fully texture...</td>
      <td>{'model_id': '2095846', 'geometry': 'Polygon m...</td>
      <td>14.99</td>
      <td>19</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>hq3dmodel</td>
      <td>{'percent': 0, 'time': 0}</td>
      <td>{'avg_rating': 5.0, 'num_rating': 1}</td>
      <td>[rug, carpet, fur, interior, floor, cloth, woo...</td>
      <td>15</td>
      <td>0</td>
      <td>0</td>
      <td>{'authors': [], 'texts': [], 'datetimes': []}</td>
      <td>$5.00</td>
      <td>8</td>
      <td>The set consists of 3 rugs. All high quality t...</td>
      <td>{'model_id': '2418972', 'geometry': 'Polygon m...</td>
      <td>5.00</td>
      <td>20</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-snake-</td>
      <td>{'percent': 0, 'time': 0}</td>
      <td>{'avg_rating': 0, 'num_rating': 0}</td>
      <td>[aquanet, modena, furniture, sink, mixer, mirr...</td>
      <td>19</td>
      <td>0</td>
      <td>0</td>
      <td>{'authors': [], 'texts': [], 'datetimes': []}</td>
      <td>$7.00</td>
      <td>9</td>
      <td>Furniture set Modena 65/85/100 White gloss. Di...</td>
      <td>{'model_id': '2372429', 'geometry': 'Polygon m...</td>
      <td>7.00</td>
      <td>18</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>zifir3d</td>
      <td>{'percent': 88, 'time': '0.2h'}</td>
      <td>{'avg_rating': 4.7, 'num_rating': 33}</td>
      <td>[flexform, ettore, sofa, divan, lounge, pillow...</td>
      <td>77</td>
      <td>2</td>
      <td>0</td>
      <td>{'authors': [], 'texts': [], 'datetimes': []}</td>
      <td>$39.00</td>
      <td>8</td>
      <td>Flexform Ettore https://www.flexform.it/en/pro...</td>
      <td>{'model_id': '2251378', 'geometry': 'Polygon m...</td>
      <td>39.00</td>
      <td>21</td>
      <td>0.2</td>
    </tr>
  </tbody>
</table>
</div>

### Distributions

![splash](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/output_10_0.png)

![splash](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/output_12_0.png)


Here we break the tags into two buckets: [5, 10] and [15, 20] tag_counts respectively

```python
df.loc[(df.tag_count <= 10) & (df.tag_count >= 5), 'tag_bucket'] = "5-10"
df.loc[(df.tag_count <= 20) & (df.tag_count >= 15), 'tag_bucket'] = "15-20"
```

### Mean & Standard Deviation of Bucketed Tags

![splash](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/output_19_0.png)

## Hypothesis

![formula](https://render.githubusercontent.com/render/math?math=H_0=) The number of views from tag counts in the [5,10] bin does not differ from the [15,20] tag count bin.

![formula](https://render.githubusercontent.com/render/math?math=H_A=) The number of views differs

![formula](https://render.githubusercontent.com/render/math?math=\alpha=0.2)

### Perform a T-Test to calculate the T-Statistic and evaluate for the p-value

P Values less than the significance threshold of alpha informs us that the two samples are significantly different


```python
tstat, pval = stats.ttest_ind(five_to_ten, fifteen_to_twenty, equal_var=False)

print(f"T-Statistic: {tstat}, P-Value: {pval}, P < alpha: {pval < alpha}")
```

    T-Statistic: -7.698108109328321, P-Value: 1.4143692004864982e-14, P < alpha: True



```python
# The two-sample Kolmogorov-Smirnov test is one of the most useful and general nonparametric methods for comparing two samples, 
# as it is sensitive to differences in both location and shape of the empirical cumulative distribution functions of the two samples. 

stats.ks_2samp(five_to_ten, fifteen_to_twenty, alternative='less')
```




    Ks_2sampResult(statistic=0.040260062966528565, pvalue=1.409790749779635e-14)




```python
# The K Sample Anderson-Darling tests
# that k-samples are drawn from the same population without having
# to specify the distribution function of that population.

stats.anderson_ksamp([five_to_ten, fifteen_to_twenty])
```




    Anderson_ksampResult(statistic=46.689500638621936, critical_values=array([0.325, 1.226, 1.961, 2.718, 3.752, 4.592, 6.546]), significance_level=0.001)



After running the three tests (Standard T-Test, Kolmogorov-Smirnov, Anderson-Darling) we observe p-values all less than the intial alpha threshold

And so we reject the Null Hypothesis which stated that there is no significant difference in view counts for samples drawn from the two bins of [5,10] and [15, 20] tags


## Conclusion

Upon visitation of a webpage on which a model contains between 5 and 10 tags we would expect to see fewer views than of another webpage on which a model contains between 15 and 20 tags. Tags can be viewed as additional paths to finding a given model and while it matches our intuition, it does not necessarily hold for extreme samples. Some models contained tag counts greater than 90 and had little views, so there appears to be a diminishing return. Further examination of binned tag counts versus views could lead to interesting results.

## Future Work

I will be pursuing further refinement in this project in regards to data acquisition, storage, processing, and analysis. 

### General

* Reapproach the project from a containerization perspective
* Build a docker image for the development and deployment environments
* Leverage databases 
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
* Sentiment anlysis on comments
* Price prediction given model attributes
* Time series analysis given date attributes
