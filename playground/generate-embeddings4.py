import numpy as np
import matplotlib.pyplot as plt
import sys

from openai import OpenAI
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

from sklearn.cluster import DBSCAN


import nltk
from transformers import BertTokenizer, BertModel
import torch

nltk.download('punkt')

# Initialize OpenAI client
client = OpenAI(api_key='sk-proj-HnN2Y2wUD26A6oTRQmKgT3BlbkFJ1m6TmmlLe11SMPP2tEKx')

from docx import Document

def read_docx_to_array(file_path):
    # Open the Word document
    doc = Document(file_path)
    
    # Initialize an empty list to store the text
    texts = []

    # Iterate through each paragraph in the document
    for para in doc.paragraphs:
        # Add the paragraph text to the list if it is not empty
        if not para.style.name.startswith('Heading') and para.text.strip():
            texts.append(para.text.strip())
    
    return texts


#for text in texts:
#    print(text)
texts = [
    "Modern data architectures are undergoing significant transformations driven by various technological advancements and evolving business needs.",
    "One major trend is the adoption of cloud-based data solutions, which provide scalability and flexibility.",
    "Cloud providers like AWS, Google Cloud, and Microsoft Azure offer robust platforms for storing and processing large volumes of data.",
    "As businesses generate more data, the demand for efficient data storage solutions has increased.",
    "Data lakes have emerged as a popular choice, allowing organizations to store structured and unstructured data in its raw format.",
    "This approach provides greater flexibility for future data processing and analysis.",
    "AI and ML algorithms can uncover patterns and generate insights that were previously unattainable.",
    "These technologies enable predictive analytics, helping businesses make data-driven decisions.",
    "Another significant trend is the use of real-time data processing frameworks.",
    "Apache Kafka and Apache Flink are popular tools that enable the ingestion and processing of data in real time.",
    "This capability is crucial for applications that require immediate insights, such as fraud detection and monitoring.",
    "Data governance has become increasingly important as organizations strive to ensure data quality and compliance.",
    "Effective data governance frameworks help maintain data accuracy, consistency, and security.",
    "Compliance with regulations such as GDPR and CCPA is a key consideration for modern data architectures.",
    "Data privacy concerns have led to the implementation of robust security measures, including encryption and access controls.",
    "These measures are essential for protecting sensitive information and building trust with customers.",
    "The rise of hybrid and multi-cloud strategies is another notable trend."
    ]

# Example usage
file_path = '/Users/khaas/Library/Mobile Documents/com~apple~CloudDocs/Projects/openai/playground/2024Pentaho+ServicesCatalogTest.docx'
texts = read_docx_to_array(file_path)



# Default value for 'use'
use = 'openai'

# Check if a command-line argument is provided
if len(sys.argv) > 1:
    use = sys.argv[1]

# Generate embeddings
if use == 'openai':
    response = client.embeddings.create(input=texts, model="text-embedding-3-large")
    embeddings = [item.embedding for item in response.data]
    print("OpenAI")
elif use == 'bert':
    def get_bert_embeddings(texts, tokenizer, model):
        embeddings_list = []
        for text in texts:
            inputs = tokenizer(text, return_tensors='pt')
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
            embeddings_list.append(embeddings)
        return embeddings_list

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    bert_embeddings = get_bert_embeddings(texts, tokenizer, model)
    embeddings = np.array(bert_embeddings).reshape(len(bert_embeddings), -1)
    print("BERT")

# Convert embeddings to numpy array and apply PCA
X = np.array(embeddings)
n_components = min(X.shape[0], X.shape[1])
pca = PCA(n_components=n_components)
reduced_embeddings = pca.fit_transform(embeddings)

# Ensure there are enough samples for clustering
if reduced_embeddings.shape[0] < 3:
    raise ValueError("Not enough samples to perform clustering. At least 3 samples are required.")

# Function to calculate the silhouette score for a given number of clusters
def calculate_silhouette_score(reduced_embeddings, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters)
    clusters = kmeans.fit_predict(reduced_embeddings)
    score = silhouette_score(reduced_embeddings, clusters)
    return score, clusters, kmeans.cluster_centers_, kmeans.labels_

# Determine the optimal number of clusters between 3 and 7
best_score = -1
best_num_clusters = 0
best_clusters = None
best_cluster_centers = None
best_labels = None

for n_clusters in range(3, 8):
    score, clusters, cluster_centers, labels = calculate_silhouette_score(reduced_embeddings, n_clusters)
    if score > best_score:
        best_score = score
        best_num_clusters = n_clusters
        best_clusters = clusters
        best_cluster_centers = cluster_centers
        best_labels = labels

print(f'Optimal number of clusters: {best_num_clusters} with Silhouette Score: {best_score}')
clusters = best_clusters
cluster_centers = best_cluster_centers
labels = best_labels

# Turn on interactive mode for non-blocking plot display
plt.ion()

# Plot 1: Cluster Visualization without Centroids
plt.figure(figsize=(10, 7))
unique_labels = np.unique(labels)
colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))

for i, label in enumerate(unique_labels):
    cluster_points = reduced_embeddings[labels == label]
    original_indices = np.where(labels == label)[0]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {label}', color=colors[i])
    for j, point in enumerate(cluster_points):
        plt.annotate(str(original_indices[j]), (point[0], point[1]), textcoords="offset points", xytext=(0, 5), ha='center')

plt.title(f'Cluster Visualization ({use})')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.legend()
# plt.show()

# Plot 2: Cluster Visualization with Centroids
plt.figure(figsize=(10, 7))

for i, label in enumerate(unique_labels):
    cluster_points = reduced_embeddings[labels == label]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {label}', color=colors[i])

# Plotting the cluster centers with matching colors
for i, label in enumerate(unique_labels):
    plt.scatter(cluster_centers[i, 0], cluster_centers[i, 1], s=300, color=colors[i], marker='X', edgecolor='black', linewidth=2, label=f'Centroid {label}')

plt.title(f'Cluster Visualization with Centroids ({use})')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.legend()
plt.show()

# Check if the number of clusters is valid for silhouette score
if len(np.unique(clusters)) > 1:
    score = silhouette_score(reduced_embeddings, clusters)
    print(f'Silhouette Score: {score}')
else:
    print('Silhouette Score: Not enough clusters to calculate silhouette score.')

# Group texts by their cluster label and calculate distance to cluster center
clustered_docs = {label: [] for label in unique_labels}
distances_to_center = {label: [] for label in unique_labels}

for idx, label in enumerate(labels):
    text = texts[idx]
    cluster_center = cluster_centers[label]
    distance = np.linalg.norm(reduced_embeddings[idx] - cluster_center)
    clustered_docs[label].append((text, distance))

# Function to print the top N closest texts to their cluster center
def print_top_n_closest_texts(clustered_docs, distances_to_center, top_n=10):
    for label in clustered_docs:
        # Sort texts by distance to cluster center
        sorted_texts = sorted(clustered_docs[label], key=lambda x: x[1])
        print(f"Cluster {label} Top {top_n} Closest Texts:")
        for i, (text, distance) in enumerate(sorted_texts[:top_n]):
            print(f"{i + 1}. Text: {text}")
            print(f"   Distance to Center: {distance:.4f}")
        print()


# Function to extract key phrases
def extract_key_phrases(docs, top_n=5):
    text = " ".join(docs)
    tfidf = TfidfVectorizer(stop_words='english', max_features=100)
    tfidf_matrix = tfidf.fit_transform([text])
    feature_array = np.array(tfidf.get_feature_names_out())
    tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
    top_n_words = feature_array[tfidf_sorting][:top_n]
    return top_n_words

# Function to extract key sentences using Sumy
def extract_key_sentences(docs, sentence_count=3):
    text = " ".join(docs)
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join([str(sentence) for sentence in summary])

# Extract summaries for each cluster
cluster_summaries_phrases = {}
cluster_summaries_sentences = {}
for label, docs in clustered_docs.items():
    key_phrases = extract_key_phrases([doc[0] for doc in docs])  # Extract only the text part of each tuple
    cluster_summaries_phrases[label] = key_phrases
    summary = extract_key_sentences([doc[0] for doc in docs])  # Extract only the text part of each tuple
    cluster_summaries_sentences[label] = summary

# Example usage
print_top_n_closest_texts(clustered_docs, distances_to_center, top_n=10)

# Print cluster summaries
for label in cluster_summaries_phrases:
    print(f"Cluster {label} Key Phrases: {', '.join(cluster_summaries_phrases[label])}")
    print(f"Cluster {label} Summary using Sumy:\n{cluster_summaries_sentences[label]}")
    # print(f"Cluster {label} Texts:\n{' '.join(clustered_docs[label])}\n")

# Turn off interactive mode to ensure plots display correctly at the end
plt.ioff()
plt.show()