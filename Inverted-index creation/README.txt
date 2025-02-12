Inverted Index Creation
This project creates inverted indexes for unigrams and selected bigrams using Python.

Code Explanation
The project consists of two main Python scripts:
unigram.py: Creates a unigram inverted index
bigram.py: Creates an inverted index for selected bigrams

Libraries Used
os: For file and directory operations
re: For text cleaning and processing using regular expressions
collections: For using defaultdict data structure
concurrent.futures: For parallel processing in unigram indexing

Execution Instructions
Ensure you have Python 3.x installed
Place the input files in directories named fulldata (for unigrams) and devdata (for bigrams)

Run the scripts:

python unigram.py
python bigram.py

Output Structure
The scripts generate two output files:
unigram_index.txt: Contains the unigram inverted index
selected_bigram_index.txt: Contains the inverted index for selected bigrams

Output File Format
Both output files follow this format:
term    docID1:count1 docID2:count2 ...
Where:
term is either a unigram or a bigram
docID is the document identifier
count is the number of occurrences of the term in that document

Output Generation Process
1. Unigram Index:
·Reads all .txt files in the fulldata directory
·Cleans and processes text, including handling joined words and normalizing terms
·Uses parallel processing to map terms to documents
·Shuffles and reduces the results to create the final index
·Writes the index to unigram_index.txt
2. Bigram Index:
·Reads all .txt files in the devdata directory
·Processes text to extract only the specified bigrams
·Maps bigrams to documents
·Reduces the results to create the final index for selected bigrams
·Writes the index to selected_bigram_index.txt
Both processes implement a simplified version of the MapReduce paradigm to efficiently process the data and create the inverted indexes.