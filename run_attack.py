import argparse
import numpy as np
from tqdm import tqdm
import warnings 
warnings.filterwarnings("ignore")
from propinf.attack.attack_utils import AttackUtil
import propinf.data.ModifiedDatasets as data
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def remove_chars(string, chars):
    out = ""
    for c in string:
        if c not in chars:
            out += c
    return out

def string_to_float_list(string):
    # Remove spaces
    string = remove_chars(string, " ")
    # Remove brackets
    string = string[1:-1]    
    # Split string over commas
    tokens = string.split(",")
    
    out_array = []
    for token in tokens:
        out_array.append(float(token))
    return out_array



def string_to_tuple_list(string):
    # Remove spaces
    string = remove_chars(string, " ()")
    print
    # Remove brackets
    string = string[1:-1]    
    # Split string over commas
    tokens = string.split(",")
    
    targets = []
    for i in range(0, len(tokens)//2+1, 2):
        targets.append((tokens[i], tokens[i+1]))
    return targets


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '-dat',
        '--dataset',
        help='dataset name',
        type=str,
        #default='census'
        default='adult'
    )
    
    parser.add_argument(
        '-tp',
        '--targetproperties',
        help='list of categories and target attributes. e.g. [(sex, Female), (occupation, Sales)]',
        type=str,
        default='[(sex, Female), (occupation, Sales)]'
    )
    
    parser.add_argument(
        '-t0',
        '--t0frac',
        help='t0 fraction of target property',
        type=float,
        default=0.4
    )
    
    parser.add_argument(
        '-t1',
        '--t1frac',
        help='t1 fraction of target property',
        type=float,
        default=0.6
    )
    
    parser.add_argument(
        '-sm',
        '--shadowmodels',
        help='number of shadow models',
        type=int,
        default=4
    )
    
    parser.add_argument(
        '-p',
        '--poisonlist',
        help='list of poison percent',
        type=str,
        #default= '[0.0,0.005, 0.01,0.015, 0.02, 0.025, 0.03,0.035, 0.04, 0.045, 0.05]'
        #Uncomment the following For medium size property
        #default ='[0.00,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01]'
        #Uncomment the following For large size property
        default ='[0.0, 0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]'
        #Uncomment the following For small size property
        #default= '[0.00,0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008]'
        #default='[0.000,0.001 ]'
    )
    
    parser.add_argument(
        '-d',
        '--device',
        help='PyTorch device',
        type=str,
        default= 'cpu'
    )
    
    parser.add_argument(
        '-fsub',
        '--flagsub',
        help='set to True if want to use the optimized attack for large propertie',
        type=bool,
        default= False
    )
    
    parser.add_argument(
        '-subcat',
        '--subcategories',
        help='list of sub-catogories and target attributes, e.g. [(marital-status, Never-married)]',
        type=str,
        default='[(marital-status, Never-married)]'
    )
    
    parser.add_argument(
        '-q',
        '--nqueries',
        help='number of black-box queries',
        type=int,
        default=1000
    )
    
    parser.add_argument(
        '-nt',
        '--ntrials',
        help='number of trials',
        type=int,
        default=1
    )
    
    arguments = vars(parser.parse_args())
    arguments["poisonlist"] = string_to_float_list(arguments["poisonlist"])
    arguments["targetproperties"] = string_to_tuple_list(arguments["targetproperties"])
    if arguments["subcategories"]:
        arguments["subcategories"] = string_to_tuple_list(arguments["subcategories"])
    
    print("Running SNAP on the Following Target Properties:")
    for i in range(len(arguments["targetproperties"])):
        print(f"{arguments['targetproperties'][i][0]}={arguments['targetproperties'][i][1]}")
    print("-"*10)
    
    #cat_columns, cont_columns = data.get_census_columns()
    cat_columns, cont_columns = data.get_adult_columns()
    dataset = arguments["dataset"]
    df_train, df_test = data.load_data(dataset, one_hot=False)
    
    categories = [prop[0] for prop in arguments["targetproperties"]]
    target_attributes = [" " + prop[1] for prop in arguments["targetproperties"]]
    if arguments["subcategories"]:
        sub_categories = [prop[0] for prop in arguments["subcategories"]]
        sub_attributes = [" " + prop[1] for prop in arguments["subcategories"]]
    else:
        sub_categories = None
        sub_attributes = None
        
    t0 = arguments["t0frac"]
    t1 = arguments["t1frac"]

    n_trials = arguments["ntrials"]
    n_queries = arguments["nqueries"]
    num_query_trials = 10
    avg_success = {}
    pois_list = arguments["poisonlist"]
    
    
    attack_util = AttackUtil(
    target_model_layers=[32, 16],
    df_train=df_train,
    df_test=df_test,
    cat_columns=cat_columns,
    verbose=False,
    )
    

    for pois_idx, user_percent in enumerate(pois_list):

        avg_success[user_percent] = 0.0
        
        attack_util.set_attack_hyperparameters(
            categories=categories,
            target_attributes=target_attributes,
            sub_categories=sub_categories,
            sub_attributes=sub_attributes,
            subproperty_sampling=arguments["flagsub"],
            poison_percent=user_percent,
            poison_class=1,
            t0=t0,
            t1=t1,
            num_queries=n_queries,
            num_target_models=10,
        )

        attack_util.set_shadow_model_hyperparameters(
            device=arguments["device"],
            num_workers=1,
            batch_size=256,
            layer_sizes=[32,16],
            verbose=False,
            mini_verbose=False,
            epochs=20,
            tol=1e-6,
        )

        for i in range(n_trials):

            attack_util.generate_datasets()

            attack_util.train_and_poison_target(need_metrics=False)

            (
                out_M0,
                out_M1,
                threshold,
                correct_trials,
            ) = attack_util.property_inference_categorical(
                num_shadow_models=arguments["shadowmodels"],
                query_trials=num_query_trials,
            )

            avg_success[user_percent] = (
                avg_success[user_percent] + correct_trials / n_trials
            )

    print("Attack Accuracy:")
    poisoning_rates = []
    accuracies = []

    for key in avg_success:
        print(f"{key*100:.2f}% Poisoning: {avg_success[key]}")
        poisoning_rates.append(key*100)
        accuracies.append(avg_success[key])
    
    # **Modified Section for Dynamic Plot**
    # Extract target properties
    target_properties = arguments["targetproperties"]
    # Multiply t0 and t1 fractions by 100
    t0_percentage = t0 * 100
    t1_percentage = t1 * 100
    

   # Determine the size of the property based on t0 and t1
    property_size = ""
    if t0 * 100 < 1 and t1 * 100 < 1:
        property_size = "small property"
    elif 1 <= t0 * 100 <= 9 or 1 <= t1 * 100 <= 9:
        property_size = "medium-sized property"
    else:
        property_size = "large, optimized property"

    # Dynamically create the title in the desired format
    target_properties_text = ", ".join([f"{prop[0].capitalize()} = {prop[1]}" for prop in target_properties])
    corner_title = (
        f"Target Properties ({property_size})\n"
        f"✱ {target_properties_text}; {t0_percentage:.1f}% vs {t1_percentage:.1f}%"
    )

    # **End of Modified Section**

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(poisoning_rates, accuracies, marker='o', linestyle='--', label='Attack Accuracy')
    plt.xlabel('Poisoning Rate')
    plt.ylabel('Attack Accuracy')
    plt.title('Attack Accuracy vs. Poisoning Rate')
    plt.grid(True)
    plt.legend()

    # **Modified Section for Adding Corner Title**
    # Add the corner title dynamically
    plt.gcf().text(
        0.60, 0.2, corner_title, fontsize=10, bbox=dict(facecolor='white', alpha=0.8)
    )
    # **End of Modified Section**

    plt.show()
    
    