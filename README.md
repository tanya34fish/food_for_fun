# food_for_fun
1. testing data: 10,20,30,.....190,200 (不包含180,這篇是"請益",所以刪掉)
2. training data: training/training_merge/中共193篇 - testing data
3. ngram/
  + total/1-7.txt : training/training_merge/中共193篇每一類的ngram
  + total/1-7total.txt : 1-7.txt合起來的所有ngram
  + total/1-8total.txt : 1-8.txt合起來的所有ngram
  + train/1-7.txt : training/training_merge/中193-19=174篇每一類的ngram
  + train/1-7total.txt : 1-7.txt合起來的所有ngram
  + train/1-8total.txt : 1-8.txt合起來的所有ngram
4. word_importance/ : 取每個類別中count前10名的字去算比例，然後這10個做排序
   ex "服務"在類別1的count / "服務"在全部corpus裡(1-8total.txt)的count
