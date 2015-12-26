# food_for_fun
   In order to summarize a dining brief, we extract key terms for each 7 categories:
   + Service (服務)
   + Quantity (份量)
   + Taste (口味)
   + Price (價錢)
   + Environment (環境)
   + Transport (交通)
   + Mood (心情)

Then, we parse food posts and extract important sentences for 7 different categories.

# data
1. training data: data/training_data/training_merge/*, except 10th, 20th, 30th ,.... 200th posts (total: 180 posts)
2. testing data: data/training_data/training_merge/* includes 10th, 20th, 30th ,.... 200th posts (total: 20 posts)

# code
1. termcount.py: calculate term count for every label set, results are in `termcount` directory.
2. train.py: exploit 'word importance' and 'cross entropy' methods to rank terms and decide thresholds for 7 categories. This is based on training data.
3. test.py: use term lists derived from `train.py` to classify every segmented sentence in testing data.
4. naive_bayes/naive_bayes.py: construct feature for every sentence and use naive bayes to train a model. Also, predict on 20 testing posts.
5. web/ : use for demo

# result
1. word_importance/ : term ranking using word importance
2. cross_entropy/ : term ranking using cross entropy
3. statistics/ : results (precision, recall, F1) for different methods
4. err_analysis/ : use for error analysis
