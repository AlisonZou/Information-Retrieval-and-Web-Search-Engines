import os
import re
from collections import defaultdict

SELECTED_BIGRAMS = [
    "computer science",
    "information retrieval",
    "power politics",
    "los angeles",
    "bruce willis"
]


def read_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                yield filename, file.read()


def clean_text(text):
    return re.sub(r'[^\w\s]', ' ', text.lower())


def get_bigrams(words):
    return zip(words, words[1:])


def map_function(doc_id, text):
    words = clean_text(text).split()
    for bigram in get_bigrams(words):
        bigram_str = " ".join(bigram)
        if bigram_str in SELECTED_BIGRAMS:
            yield bigram_str, doc_id


def reduce_function(bigram, doc_ids):
    count = defaultdict(int)
    for doc_id in doc_ids:
        count[doc_id] += 1
    return bigram, count


def process_selected_bigrams(directory):
    intermediate = defaultdict(list)
    for doc_id, text in read_files(directory):
        for bigram, doc_id in map_function(doc_id, text):
            intermediate[bigram].append(doc_id)

    results = []
    for bigram, doc_ids in intermediate.items():
        results.append(reduce_function(bigram, doc_ids))

    return sorted(results)


def main():
    directory = "devdata"
    results = process_selected_bigrams(directory)

    with open("selected_bigram_index.txt", "w", encoding="utf-8") as f:
        for bigram, counts in results:
            count_str = " ".join([f"{doc_id}:{count}" for doc_id, count in counts.items()])
            f.write(f"{bigram}\t{count_str}\n")


if __name__ == "__main__":
    main()