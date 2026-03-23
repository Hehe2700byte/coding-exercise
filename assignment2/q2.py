# Import anything here from the Python Standard Library if you see fit.
import math

class NaiveBayesClassifier:
    def __init__(self):
        self.class_priors = {}
        self.word_counts = {}
        self.vocabulary = set()

    def fit(self, X: list[str], y: list[str]) -> None:
        """
        Train the classifier using the provided data.

        Parameters:
            X: list of text documents (list of strings)
            y: list of class labels corresponding to X
        """
        N = len(X)
        label_counts = {}
        for text, label in zip(X, y):
            text = text.lower()
            label = label.lower()
            words = text.split(" ")
            self.vocabulary.update(words)
            label_counts[label] = label_counts.get(label, 0) + 1
            for word in words:
                if label not in self.word_counts:
                    self.word_counts[label] = {}
                self.word_counts[label][word] = self.word_counts[label].get(word, 0) + 1
        
        self.class_priors = {class_name: label_counts[class_name]/N for class_name in y}
    

    def predict(self, text: str) -> tuple[str, dict[str, float]]:
        """
        Predict the class of a given document.

        Parameters:
            text: string, the document to classify

        Returns:
            string: predicted class label
        """
        text = text.lower()
        words = text.split()
        scores = {}
        for label in self.class_priors.keys():
            p = [math.log10((self.word_counts[label].get(word, 0) + 1)/(sum(self.word_counts[label].values()) + len(self.vocabulary))) for word in words]
            scores[label] = math.log10(self.class_priors[label]) + sum(p)
        
        label_max = max(scores, key = scores.get)
        return label_max, scores

    @staticmethod
    def load_data(filename: str) -> tuple[list[str], list[str]]:
        """
        Load training data from a CSV file.

        Parameters:
        filename: string, file path to the CSV file

        Returns:
        tuple: (X, y) where X is a list of documents and y is a list of labels
        """
        # TODO: Add your code (and remove this line)
        X = []
        y = []

        
# Example usage
if __name__ == "__main__":
    # Small training dataset
    train_set = [
        ("tech", "I love programming in Python"),
        ("tech", "Python is great for data science"),
        ("outdoors", "I enjoy hiking and outdoor activities"),
        ("tech", "Data science is my passion"),
        ("fashion", "LV and Gucci are top fashion brands"),
    ]
    y_train, X_train = map(list, zip(*train_set))

    # Create and train the classifier
    classifier = NaiveBayesClassifier()
    classifier.fit(X_train, y_train)
    print(f"class_priors:\n{classifier.class_priors}\n")
    print(f"word_counts:\n{classifier.word_counts}\n")
    print(f"vocabulary:\n{classifier.vocabulary}\n")

    # Predict new text
    text_to_predict = "I like Python coding"
    predicted_class, scores = classifier.predict(text_to_predict)
    print(f"scores:\n{scores}")
    print(f"Predicted class for '{text_to_predict}': {predicted_class}")

    # Predict new text
    text_to_predict = "I love outdoor adventures"
    predicted_class, _ = classifier.predict(text_to_predict)
    print(f"Predicted class for '{text_to_predict}': {predicted_class}\n")

    # Load a large training dataset from a CSV file
    y_train, X_train = NaiveBayesClassifier.load_data('q2_tweets.csv')

    # Create and train the classifier
    tweets_classifier = NaiveBayesClassifier()
    tweets_classifier.fit(X_train, y_train)

    # Predict new texts in a test set
    test_set = [
        ("negative", "I am angry at the flight delay"),
        ("negative", "I will complain the staff"),
        ("neutral", "What time will we arrive at Hong Kong"),
        ("positive", "I am happy about the free upgrade"),
        ("positive", "What a happy fun trip with this airline"),
    ]

    print("Batch testing results:")
    correct_predictions = 0
    for true_label, text_to_predict in test_set:
        predicted_class, _ = tweets_classifier.predict(text_to_predict)
        correct = (predicted_class == true_label)
        correct_predictions += correct
        print(predicted_class, correct)
    print(f"Accuracy: {correct_predictions / len(test_set):.2%}")
