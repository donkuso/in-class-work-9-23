import csv
import string

def load_messages(filepath):
    """
    prints each line in the file provided in param
    filepath: str representing the path to the file to read in
    returns: dictionary of {word: occurrence}
    """
    # with block
    # handles opening and closing of file automatically. 
    # file is only open in indented block.
    '''
    If the integrity of the message should be saved:
        use a list data structure (below)
    '''
    # data = []
    # with open(filepath, newline='', mode='r', encoding='utf-8-sig') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',')
    #     for row in reader:
    #         label, message = row[0], row[1]
    #         data.append((label, message))
    # return data
    """
    Dictionaries are better in this case
    (quick lookups!)
    """
    ham_counts = {}
    spam_counts = {}
    with open(filepath, newline='', mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) # skips header row
        for row in reader:
            label, message = row[0], row[1] # we still need this actually

            message = message.lower()
            translator = str.maketrans("", "", string.punctuation)
            message = message.translate(translator)

            for word in message.split(): # do i need to do more to the message?
                                            # like remove punctuation? capitilzation? 
                
                word_counts = ham_counts if label == "ham" else spam_counts
                if word not in word_counts:
                    word_counts[word] = 1
                else:
                    word_counts[word] += 1
    return ham_counts, spam_counts 

def probability(word, ham_counts, spam_counts):
    
    total_ham = sum(ham_counts.values())
    total_spam = sum(spam_counts.values())

    # calculate probabilities
    p_ham = ham_counts.get(word, 0) / total_ham if total_ham > 0 else 0
    p_spam = spam_counts.get(word, 0) / total_spam if total_spam > 0 else 0

    return p_ham, p_spam

def export_word(ham_counts, spam_counts, outpath):
    total_ham = sum(ham_counts.values())
    total_spam = sum(spam_counts.values())

    all_words = set(ham_counts.keys()) | set(spam_counts.keys())

    with open(outpath, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "ham_prob", "spam_prob"])  # header

        for word in all_words:
            p_ham = ham_counts.get(word, 0) / total_ham if total_ham > 0 else 0
            p_spam = spam_counts.get(word, 0) / total_spam if total_spam > 0 else 0
            writer.writerow([word, p_ham, p_spam])


ham_counts, spam_counts = load_messages("/Users/oliviadonkus/Desktop/DS5010/TEST/in class/Week-3/SMSSpamCollectionFull.csv")
export_word(ham_counts, spam_counts, "word_probs.csv")
