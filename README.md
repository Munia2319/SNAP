
# SNAP: Efficient Extraction of Private Properties with Poisoning
**Authors: Harsh Chaudhari, John Abascal, Alina Oprea, Matthew Jagielski, Florian Tramèr, Jonathan Ullman.**

Code is implemented in this paper [SNAP: Efficient Extraction of Private Properties with Poisoning](https://arxiv.org/pdf/2208.12348.pdf) paper that will appear at IEEE S&P 2023.
This code is collected from the author's [SNAP repository](https://github.com/johnmath/snap-sp23/tree/main)

## Running the Model Confidence attack
This version of our attack obtains the model confidence from the target models for the distinguishing test. 
The following script modifies the training dataset, trains target and shadow models, runs the attack, and prints the results.
```shell
python run_attacks.py -dat [--dataset] -tp [--targetproperties] -t0 [--t0frac] -t1 [--t1frac] \
                      -sm [--shadowmodels] -p [--poisonlist] -d [--device] -fsub [--flagsub] \
                      -subcat [--subcategories] -q [--nqueries] -nt [--ntrials]

```
# Enhancements in the Code for Poisoning Attack Accuracy

### Overview
This section describes the modifications I made to the code to enhance its functionality. Initially, the provided codebase was set up to evaluate attack accuracy for a single poisoning rate. I extended its functionality to dynamically handle multiple poisoning rates for different property sizes, allowing for better evaluation and visualization. Below is a detailed breakdown of the steps and enhancements made:

---

### Step 1: Setting Up the Environment
- I created a virtual environment and installed all the required packages listed in the repository.
- During the initial run, I encountered a **TypeError** related to converting `numpy.ndarray` to `torch.Tensor`. The error traceback can be seen below:

![Error Screenshot 1](./error.png)

- Additionally, there was a **KeyError** indicating missing categorical columns in the dataset. The corresponding traceback is shown below:

![Error Screenshot 2](./error-2.png)

---

### Step 2: Resolving Initial Errors
- The **TypeError** was resolved by ensuring all datasets were properly converted to supported data types (`float`, `int`) before creating `torch.Tensor`.
- The **KeyError** was addressed by verifying and correctly defining the categorical and continuous columns used in the data preprocessing step.

After resolving these errors, the code was successfully executed, producing attack accuracy for a **single poisoning rate**.

---

### Step 3: Adding Support for Multiple Poisoning Rates
- I extended the code to handle **multiple poisoning rates** dynamically for different property sizes (e.g., small, medium, large).
- This was achieved by modifying the argument parser to accept a list of poisoning rates:

```python
parser.add_argument(
    '-p',
    '--poisonlist',
    help='list of poison percent',
    type=str,
    default="[0.0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05]"
)

