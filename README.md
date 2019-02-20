# CS172 Assignment 2  
Jialiang Liu

## Environment for Developing  
Python Version: 3.6  
OS: Mac OS 10.14

## File Structure  
|——`data`  
     |——`ap89_collection`  
     |——`query_list.txt`  
     |——`qrels.txt`  
     |——`trec_eval.pl`  
     |——`results_file.txt`  
     |——`eval_results.txt`  
|————`run.sh`  
|————`project.py`  
|————`nltk_download.py`  
|————`README.md`

## To Run the Program  
1. Go inside the project's folder from terminal;
2. Execute `chmod a+x ./run.sh` to give permission to the shell script;
3. Run `run.sh` by command `./run.sh`;
4. The script will check for the environment and install necessary libraries. Manual installation might be asked for, including but not limited to, \\	Python 3\\	numpy\\	nltk.all-corpora. \\	If the script fails to install them, please install them manually.
5. After seeing "ALL-FINISHED" from terminal, results can be checked from `results_file.txt`.
6. `eval_results.txt` is the result I got from trec_eval. It includes non-interpolated average precision and precisions when 10 and 30 documents were retrieved.