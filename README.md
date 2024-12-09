# CE 397 Infrastructure Systems Optimization Course Project
Authors: Kyle Bathgate, Matthew Friar, Qianqian Tong

Dec 9, 2024

This repository contains Python scripts for the container stacking problem (CSP) conducted as a course project for Dr. Guo at UT Austin.

We create a rule-based heuristic and a dynamic program (DP) to stack containers in a terminal yard bay such that the number of reshuffles is minimal.

To run the heuristic, execute the file `heuristic_analysis.py`. Change the variables $n$, $N$, $H$, and $B$ in the file to run different instances. In-code comments provide a description of the variables and code structure and logic used.

To run the DP, execute the file `DP_analysis.py`. This instance will only work for $B = 2$ and $n = 4$, for a maximum of $N = 24$ unique input permutations.

Running both of the scripts will output different summary statistics and plots for analysis.

The file `helpers.py` contains functions used for sorting lists, computing swaps in bubble sort to count reshuffles, etc.