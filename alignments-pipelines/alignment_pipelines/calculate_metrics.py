class AlignmentMetrics:
    """
    A class to calculate alignment metrics (precision, recall, F1 score, and AER)
    from precomputed alignment files.
    """

    def __init__(self, predicted_file, reference_file):
        """
        Initializes with paths to the predicted and reference alignment files.
        
        :param predicted_file: Path to the file containing predicted alignments.
        :param reference_file: Path to the file containing reference alignments.
        """
        self.predicted_file = predicted_file
        self.reference_file = reference_file
        self.predicted_alignments = self.load_alignments(predicted_file)
        self.reference_alignments = self.load_alignments(reference_file)

    def load_alignments(self, file_path):
        """
        Load alignments from a file. Each line in the file should represent a sentence pair's
        alignments in the format "source_index-target_index", separated by spaces.
        
        Example line: "0-0 1-1 2-2" represents alignments for a sentence pair.
        
        :param file_path: Path to the alignment file.
        :return: List of sets of alignment pairs for each sentence pair.
        """
        alignments = []
        with open(file_path, 'r') as file:
            for line in file:
                # Parse each alignment pair in the line as a tuple of integers
                alignment_set = {tuple(map(int, pair.split('-'))) for pair in line.strip().split()}
                alignments.append(alignment_set)
        return alignments

    def calculate_precision(self, predicted, reference):
        """Calculate precision for alignments."""
        true_positives = len(predicted & reference)
        false_positives = len(predicted - reference)
        return true_positives / len(predicted) if len(predicted) > 0 else 0.0 

    def calculate_recall(self, predicted, reference):
        """Calculate recall for alignments."""
        true_positives = len(predicted & reference)
        false_negatives = len(reference - predicted)
        return true_positives / len(reference) if len(reference) > 0 else 0.0

    def calculate_f1_score(self, precision, recall):
        """Calculate F1 score from precision and recall."""
        return (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    def calculate_aer(self, predicted, reference):
        """Calculate Alignment Error Rate (AER)."""
        true_positives = len(predicted & reference)
        total_predicted = len(predicted)
        total_reference = len(reference)
        return 1 - (2 * true_positives) / (total_predicted + total_reference) if (total_predicted + total_reference) > 0 else 1.0

    def evaluate(self):
        """
        Evaluate the precision, recall, F1 score, and AER across all sentence pairs.
        
        :return: Dictionary containing the average precision, recall, F1 score, and AER.
        """
        total_precision, total_recall, total_f1, total_aer = 0.0, 0.0, 0.0, 0.0
        num_sentences = len(self.predicted_alignments)

        for predicted, reference in zip(self.predicted_alignments, self.reference_alignments):
            # Calculate metrics for each sentence pair
            precision = self.calculate_precision(predicted, reference)
            recall = self.calculate_recall(predicted, reference)
            f1_score = self.calculate_f1_score(precision, recall)
            aer = self.calculate_aer(predicted, reference)

            # Accumulate metrics
            total_precision += precision
            total_recall += recall
            total_f1 += f1_score
            total_aer += aer

        # Calculate average metrics across all sentence pairs
        return {
            "precision": total_precision / num_sentences,
            "recall": total_recall / num_sentences,
            "f1_score": total_f1 / num_sentences,
            "aer": total_aer / num_sentences
        }

