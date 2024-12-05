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

    def calculate_micro_average(self, predicted_alignments, reference_alignments):
        """Calculate micro average precision, recall, F1 score, and AER."""
        total_true_positives = total_false_positives = total_false_negatives = 0
        total_predicted = total_reference = 0

        for predicted, reference in zip(predicted_alignments, reference_alignments):
            true_positives = len(predicted & reference)
            false_positives = len(predicted - reference)
            false_negatives = len(reference - predicted)

            total_true_positives += true_positives
            total_false_positives += false_positives
            total_false_negatives += false_negatives
            total_predicted += len(predicted)
            total_reference += len(reference)

        precision = total_true_positives / total_predicted if total_predicted > 0 else 0.0
        recall = total_true_positives / total_reference if total_reference > 0 else 0.0
        f1_score = self.calculate_f1_score(precision, recall)
        aer = self.calculate_aer(
            set(pair for alignment in predicted_alignments for pair in alignment),
            set(pair for alignment in reference_alignments for pair in alignment)
        )

        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "aer": aer
        }

    def calculate_macro_average(self, predicted_alignments, reference_alignments):
        """Calculate macro average precision, recall, F1 score, and AER."""
        total_precision, total_recall, total_f1, total_aer = 0.0, 0.0, 0.0, 0.0
        num_sentences = len(predicted_alignments)

        for predicted, reference in zip(predicted_alignments, reference_alignments):
            precision = self.calculate_precision(predicted, reference)
            recall = self.calculate_recall(predicted, reference)
            f1_score = self.calculate_f1_score(precision, recall)
            aer = self.calculate_aer(predicted, reference)

            total_precision += precision
            total_recall += recall
            total_f1 += f1_score
            total_aer += aer

        return {
            "precision": total_precision / num_sentences,
            "recall": total_recall / num_sentences,
            "f1_score": total_f1 / num_sentences,
            "aer": total_aer / num_sentences
        }

    def evaluate(self):
        """
        Evaluate the precision, recall, F1 score, and AER across all sentence pairs.
        
        :return: Dictionary containing the micro and macro averages of precision, recall, F1 score, and AER.
        """
        # Calculate micro average
        micro_avg = self.calculate_micro_average(self.predicted_alignments, self.reference_alignments)

        # Calculate macro average
        macro_avg = self.calculate_macro_average(self.predicted_alignments, self.reference_alignments)

        return {
            "micro_average": micro_avg,
            "macro_average": macro_avg
        }

