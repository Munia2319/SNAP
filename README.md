
# SNAP: Efficient Extraction of Private Properties with Poisoning
**Authors: Harsh Chaudhari, John Abascal, Alina Oprea, Matthew Jagielski, Florian Tramèr, Jonathan Ullman.**

Code is implemented on this paper [SNAP: Efficient Extraction of Private Properties with Poisoning](https://arxiv.org/pdf/2208.12348.pdf) paper that will appear at IEEE S&P 2023.  

## Running the Model Confidence attack
 This version of our attack obtains the model confidences from the target models for the distinguishing test. The **Label-Only** version of our attack where the target model returns only the predicted label can be found in the 'label-only' branch of our repository.
The following script modifies the training dataset, trains target and shadow models, runs the attack, and prints the results.
```shell
python run_attacks.py -dat [--dataset] -tp [--targetproperties] -t0 [--t0frac] -t1 [--t1frac] \
                      -sm [--shadowmodels] -p [--poisonlist] -d [--device] -fsub [--flagsub] \
                      -subcat [--subcategories] -q [--nqueries] -nt [--ntrials]

```


