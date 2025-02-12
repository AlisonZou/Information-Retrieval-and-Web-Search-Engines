import os
import re
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor


def default_dict_int():
    return defaultdict(int)


def clean_and_separate_words(text):
    # Convert to lowercase
    text = text.lower()
    # Replace all punctuation and numerals with space
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Insert space before capital letters (for cases like "aaccepted")
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def separate_joined_words(word):
    # List of common prefixes that might be incorrectly joined
    prefixes = ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag']
    for prefix in prefixes:
        if word.startswith(prefix) and len(word) > len(prefix):
            return f"{prefix} {word[len(prefix):]}"
    return word


def normalize_word(word):
    # Remove repeated characters (more than 2 in a row)
    word = re.sub(r'(.)\1{2,}', r'\1\1', word)
    # Remove single character words except 'a' and 'i'
    if len(word) == 1 and word not in ['a', 'i']:
        return ''
    return word


def map_file(file_path):
    unigram_index = defaultdict(default_dict_int)

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split('\t', 1)
            if len(parts) != 2:
                continue

            docID, content = parts

            # Clean and separate words in the content
            content = clean_and_separate_words(content)

            # Process words
            for word in content.split():
                # Separate joined words
                separated_words = separate_joined_words(word).split()
                for w in separated_words:
                    normalized_word = normalize_word(w)
                    if normalized_word:
                        unigram_index[normalized_word][docID] += 1

    return unigram_index


def shuffle_indices(indices):
    merged_index = defaultdict(list)
    for index in indices:
        for word, doc_dict in index.items():
            for docID, count in doc_dict.items():
                merged_index[word].append(f"{docID}:{count}")
    return merged_index


def reduce_to_file(merged_index, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, postings in sorted(merged_index.items()):
            f.write(f"{word}\t{' '.join(postings)}\n")


def process_fulldata_directory(directory):
    all_indices = []
    txt_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]

    with ProcessPoolExecutor() as executor:
        all_indices = list(executor.map(map_file, txt_files))

    merged_index = shuffle_indices(all_indices)
    reduce_to_file(merged_index, 'unigram_index.txt')


if __name__ == "__main__":
    fulldata_directory = 'fulldata'  # Update this to your fulldata directory path
    process_fulldata_directory(fulldata_directory)