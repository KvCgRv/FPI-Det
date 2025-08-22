#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculate evaluation metrics for model predictions, including accuracy, precision,
recall, F1 score, sensitivity, and specificity.
Ensure required dependencies are installed: pip install pandas scikit-learn
"""

import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


def calculate_metrics():
    # Read CSV files
    label_df = pd.read_csv('label.csv')
    result_df = pd.read_csv('8x.csv')

    # Ensure class_id is integer type
    label_df['class_id'] = label_df['class_id'].astype(int)
    result_df['class_id'] = result_df['class_id'].astype(int)

    # Merge dataframes on image_name
    merged_df = pd.merge(label_df, result_df, on='image_name', suffixes=('_true', '_pred'))

    # Extract true and predicted labels
    y_true = merged_df['class_id_true']
    y_pred = merged_df['class_id_pred']

    # Calculate confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    sensitivity = recall  # Sensitivity equals recall
    specificity = tn / (tn + fp)  # Specificity

    # Print results
    print('Evaluation Metrics:')
    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1 Score: {f1:.4f}')
    print(f'Sensitivity: {sensitivity:.4f}')
    print(f'Specificity: {specificity:.4f}')

    # Return results for further use
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'sensitivity': sensitivity,
        'specificity': specificity
    }


if __name__ == '__main__':
    calculate_metrics()