# Masked Bias Detection

This code accompanies the EMNLP 2020 short paper: 

Robert (Munro) Monarch and Alex (Carmen) Morrison. 2020. Detecting Independent Pronoun Bias with Partially-Synthetic Data Generation. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP).

## Paper abstract:

We report that state-of-the-art parsers consistently failed to identify "hers" and "theirs" as pronouns, but identified the masculine equivalent, "his". We find that the same biases exist in recent language models like BERT. While some of the bias comes from known sources, like training data with gender imbalances, we find that the bias is _amplified_ in the language models. We also find that linguistic differences between English pronouns that are not inherently biased can become biases in some machine learning models. We introduce a new technique for measuring bias in models, using Bayesian approximations to generate partially-synthetic data from the model itself.


## Usage:

> python detect_bert_bias.py 

This will complete the 7 steps in the paper, reporting progress to standard error:

- STEP 1: LOADING BERT MODEL
- STEP 2: LOAD UNIVERSAL DEPENDENCY DATASET
- STEPS 3 & 4: MASK ATTRIBUTES TO PREDICT NEW ONES
- STEPS 5, 6 & 7: CREATE NEW SENTENCES AND PREDICT PRONOUNS

Note that "STEP 3 & 4" will take the longest: 10-15 minutes on a personal computer or < 5 minutes on a GPU server.

The output (to standard output) will then be a tab-separated list of attributes their his/hers bias in BERT:

```
attribute	ratio (<0=hers, >0=his)
land	9.511597535648015
world	11.417896388643772
rest	12.898568006243396
...
```

## Interpretting the outputs 

The attribute ratios will be identical in multiple runs of the code. For example, "land" is 9.51 biased towards "his" above "hers", and that 9.51 number should be consistent across multiple runs. 

However, you should expect different BERT models/versions to have slightly different biases, and the Bayesian Deep Learning step might produce a different attributes in different runs. For example, we found that the bias is consistent across different BERT versions and with the different candidates from the Bayesian Deep Learning step. For example, in many runs with different versions of BERT, you will find that "mom" was consistently the only attribute that was biased towards "hers" and in a 7-11 range.

If you think that the existing or new seed sentences might be introducing bias from other tokens, then use the `also_mask` argument in the `extract_bert_predictions()` function to ensure that those words are also masked.

The HuggingFace library contains many other masked language models that you can test and confirm that the same bias exists. But note that only BERT has widely available training data that allows you to compare how much the bias is amplified from the data, which is why it is the focus of our paper.


## Citation
```
@article{MonarchMorrison2020MaskedBias,
  author    = {Robert (Munro) Monarch and Alex (Carmen) Morrison},
  title     = {{Detecting Independent Pronoun Bias with Partially-Synthetic Data Generation}},
  journal   = {{Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)}},
  location  = {Online},
  year      = {2020}
}
```




