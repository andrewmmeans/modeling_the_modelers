# Natural Language Processing

## Example product description

```python
print(df.model_description.values[0])
```

    High quality 3d models of Barazza. The models are made with much attention to details. They have reasonable amount of polygons and accurate grid. cod: 1LFS81D (500*790) - sinks  cod: 1LFS82 (500*790) - sinks  cod: 1LFS91D (500*860) - sinks  cod: 1LFS92 (500*860) - sinks  cod: 1LFS10D (500*1000) - sinks  cod: 1LFS12D (500*1160) - sinks  cod: 1LFS82A (830*830) - sinks  cod: 1CI33 (403*346,5) - accessorie Geometry:   Polygonal Quads only  TurboSmooth iterations=0 Polys: 273 224 Verts: 365 483 (All models) TurboSmooth iterations=1 Polys: 2 163 038 Verts: 1 245 905 (All models) 


## Feature Engineering


### Removing stopwords
```python
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(['3d','model'])
```

### Stemming and tokenization
```python
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

def tokenize(text):
    # A pattern to only keep letter tokens
    pattern = re.compile('[a-zA-Z]')
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    # A list of tokens to keep
    valid_tokens = []
    for token in tokens:
        if re.search(pattern, token):
            valid_tokens.append(token)
    return valid_tokens

def stem(tokens):
    # Uses SnowballStemmer from NLTK
    stems = [stemmer.stem(token) for token in tokens]
    return stems

def tokenize_and_stem(text):
    return stem(tokenize(text))
```

### Finding the median price of the models

```python
np.median(df['price_usd'])
```

    14.48

### Compute the Term-Frequency Inverse-Document-Frequency

TF-IDF is a statistical measure that evaluates how relevant a word is to a document in a collection of documents. In this case, how relevant a word is in model's description text compared to all model descriptions. 
We accomplish this by multiplying the number of times a word appears in a model's description, and the inverse model description frequency of the word across a set of model descriptions.

It is useful in down-weighting words that appear frequently across all documents while preserving those that occur frequently in any single document.

```python
from sklearn.feature_extraction.text import TfidfVectorizer

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=200000,
                                 min_df=0.1, stop_words=stopwords,
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(df.model_description.values) #fit the vectorizer to synopses

print(tfidf_matrix.shape)
```

    (68039, 48) - 68,000 Rows and 48 Features


```python
train_desc = tfidf_vectorizer.transform(df['model_description'].values)
```

### Separate the data into two bins: price <= median price, and price > median price.

```python
df.loc[(df.price_usd <= 14.48), 'ltett'] = 1
df.loc[(df.price_usd > 14.48), 'ltett'] = 0
```

### Split the data into training and validation data sets, in this case at a ratio of 1/3 held out for validation.

```python
from sklearn.model_selection import train_test_split

labels = df['ltett'].values
X = train_desc
y = labels.reshape(-1, )

X_train,X_valid,y_train,y_valid = train_test_split(X,y, test_size = 0.33, random_state = 42)
```

```python
from sklearn.metrics import f1_score, classification_report, accuracy_score
```

## Train the model

```python
import xgboost as xgb
xgb_model = xgb.XGBClassifier(max_depth=50, n_estimators=80, learning_rate=0.1, colsample_bytree=.7, gamma=0, reg_alpha=4, objective='binary:logistic', eta=0.3, silent=1, subsample=0.8).fit(X_train, y_train) 
```

### Use the model to predict labels for the validation dataset
```python
xgb_prediction = xgb_model.predict(X_valid)
```

### Compute the F1 Score for the predicted labels against our known labels
```python
print('word level tf-idf training score:', f1_score(y_train.astype(int), xgb_model.predict(X_train).astype(int)))
```

    word level tf-idf training score: 0.9066285050605608



```python
print('word level tf-idf validation score:', f1_score(y_valid.astype(int), xgb_model.predict(X_valid).astype(int), average='macro'))
```

    word level tf-idf validation score: 0.7809556207365078



```python
print(classification_report(y_valid.astype(int).reshape(-1, 1), xgb_prediction.astype(int).reshape(-1, 1)))
```

                  precision    recall  f1-score   support
    
               0       0.81      0.74      0.77     11290
               1       0.76      0.83      0.79     11163
    
        accuracy                           0.78     22453
       macro avg       0.78      0.78      0.78     22453
    weighted avg       0.78      0.78      0.78     22453
    

### Plot the ROC Curve

```python
from sklearn.metrics import roc_curve

pos_probs = xgb_model.predict_proba(X_valid)
```


```python
false_pos_rate, true_pos_rate, thresholds = roc_curve(y_valid.reshape(-1, 1).astype(int), pos_probs[:, 1])
```


```python
fig, ax = plt.subplots()

ax.plot(false_pos_rate, true_pos_rate, marker=',', label='XGB')
ax.plot([0,1], [0,1], linestyle='--', label='Random Guessing')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title("ROC Curve")
plt.legend();
```


![max_pages](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/output_27_0.png)



```python
from sklearn.metrics import roc_auc_score

# calculate roc auc
roc_auc = roc_auc_score(y_valid.reshape(-1, 1).astype(int), pos_probs[:, 1])
```


```python
roc_auc
```




    0.872204276797947


### Precision Recall Curve


```python
from sklearn.metrics import precision_recall_curve

precision, recall, _ = precision_recall_curve(y_valid.reshape(-1, 1).astype(int), pos_probs[:, 1])
```


```python
fig, ax = plt.subplots()

ax.plot(recall, precision, marker='.', label='XGB')
ax.plot([0, 1], [len(y[y==1]) / len(y), len(y[y==1]) / len(y)], linestyle='--', label='Guessing')
ax.set_xlabel('Recall')
ax.set_ylabel('Precision')
ax.set_title("Precision Recall Curve")
ax.legend();
```


![max_pages](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/output_31_0.png)

### Class balance

```python
fig, ax = plt.subplots()

sns.barplot([x[0] for x in list(Counter(y_valid).items())], [x[1] for x in list(Counter(y_valid).items())])
ax.set_xticklabels(['Model Price > $14.48', 'Model Price <= $14.48'])
ax.set_ylabel('Records')
ax.set_title('Class Balance')
plt.show()
```


![max_pages](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/output_33_0.png)



```python
from sklearn.metrics import auc

auc_score = auc(recall, precision)
```


```python
print(f"XGBoost PR AUC: {auc_score:.2f}")
```

    XGBoost PR AUC: 0.87


### Which features were most important in terms of predictive power?

```python
from xgboost import plot_importance

fig, ax = plt.subplots(figsize=(10,8))

ax = plot_importance(xgb_model, color='teal', grid=False, ax=ax)

word_features = [tfidf_vectorizer.get_feature_names()[int(x.get_text()[1:])] for x in ax.get_yticklabels()]

ax.set_yticklabels(word_features)
plt.show()
```


![max_pages](https://github.com/andrewmmeans/modeling_the_modelers/blob/master/images/output_36_0.png)
