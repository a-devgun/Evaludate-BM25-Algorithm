# EVALUATE SEARCH ENGINE


This script can be used for evaluation of a search engine. To evaluate a search engine, queries for evaluation, relevance judgement and ranking of a search engine algorithm are required.

The result has been provided in a file called 'Output-3-queries.xlsx'

BM25Algo.py file was modified to print the query id as well along with the results.

## SETUP

1. Download the latest version of python - "Python 3.5.0".
2. Install PyCharm.
3. Execute EvaluateSearchEngine.py. 

## ABOUT THE CODE

1. Here in this script the queries should be of the format "<query> (<query_no>)". Code has been build in such a way that it automatically extracts relevance judgement from CACM relevance file from the query number.

2. The result file should be of the following format. It should contain -> query_id,Q0,doc_id,rank,BM25_score,system_name in the same order so that data is extracted in the correct way.

3. On execution, the code first looks for relevance judgement file. The file name has been hard coded in the script.

4. After that it looks for queries file. The file name also has been hard coded here. Here it extracts the queries and their query id. Since I am evaluating the search engine from assignment 3, I have modified the queries in queries1.txt to use the stemmed version of themselves as done in assignment 3.

5. Next the code looks for evaluation result of some search engine. 

6. Output is provided for each query in the files with the query names and is also printed on console.

7. The 3 Precision@K values are printed on console, and have also been provided in the excel file below each query. Mean Average Precision (MAP) is present at the end of the excel file.

## CONTACT

Please contact 'Anirudh Devgun' at 'devgun.a@husky.neu.edu' in case of any issues.