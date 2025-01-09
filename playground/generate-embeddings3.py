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

import nltk
from transformers import BertTokenizer, BertModel
import torch

nltk.download('punkt')

# Initialize OpenAI client
client = OpenAI(api_key='sk-proj-HnN2Y2wUD26A6oTRQmKgT3BlbkFJ1m6TmmlLe11SMPP2tEKx')

# Sample texts
texts = ["We have one cat", "She owns two dogs", "Eggs are for breakfast"]

texts = ["hello"]

texts = [
    "Modern data architectures are undergoing significant transformations driven by various technological advancements and evolving business needs.",
    "One major trend is the adoption of cloud-based data solutions, which provide scalability and flexibility.",
    "Cloud providers like AWS, Google Cloud, and Microsoft Azure offer robust platforms for storing and processing large volumes of data.",
    "As businesses generate more data, the demand for efficient data storage solutions has increased.",
    "Data lakes have emerged as a popular choice, allowing organizations to store structured and unstructured data in its raw format.",
    "This approach provides greater flexibility for future data processing and analysis.",
    "The integration of artificial intelligence (AI) and machine learning (ML) into data architectures is revolutionizing data analytics.",
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
    "The rise of hybrid and multi-cloud strategies is another notable trend.",
    "Organizations are leveraging multiple cloud providers to avoid vendor lock-in and ensure data portability.",
    "This approach provides flexibility and resilience, enabling businesses to adapt to changing requirements.",
    "Edge computing is gaining traction as a means to process data closer to its source.",
    "This reduces latency and bandwidth usage, supporting applications like autonomous vehicles and industrial IoT.",
    "Microservices architecture is transforming how data services are designed and deployed.",
    "By breaking down monolithic applications into smaller, independent services, microservices enable more agile development and scalability.",
    "Containerization technologies like Docker and Kubernetes are widely used to deploy and manage microservices.",
    "Containers provide a lightweight and portable way to run applications, simplifying the management of data processing workloads.",
    "Data integration platforms play a crucial role in modern data architectures.",
    "Tools like Apache NiFi and Talend facilitate the seamless combination of data from various sources.",
    "This improves data consistency and usability, enabling better decision-making.",
    "The concept of a data fabric is gaining popularity as organizations seek to create a unified data environment.",
    "A data fabric integrates various data management technologies, providing a cohesive architecture for data discovery and governance.",
    "Data democratization aims to make data accessible to all employees, regardless of their technical expertise.",
    "Self-service analytics platforms and user-friendly data tools are essential for achieving this goal.",
    "These tools empower users to explore and analyze data independently, driving innovation and productivity.",
    "Data catalogs are becoming more prevalent as organizations look to improve data utilization.",
    "By providing a centralized repository for metadata, data catalogs help users discover and trust the data available within the organization.",
    "The use of graph databases is on the rise, particularly for managing complex relationships between data points.",
    "Graph databases like Neo4j use nodes, edges, and properties to represent and store data.",
    "This makes them ideal for applications like social networks and fraud detection.",
    "Another emerging trend is the use of serverless computing models.",
    "Serverless architectures abstract away the underlying infrastructure, simplifying the deployment of data processing workflows.",
    "As data volumes continue to grow, efficient data storage solutions are critical.",
    "Technologies like columnar storage, data compression, and deduplication help optimize storage utilization.",
    "These techniques reduce costs and improve performance in modern data architectures.",
    "The integration of metadata management solutions is also essential.",
    "Metadata provides insights into data lineage, usage, and quality, helping organizations manage their data assets more effectively.",
    "Event-driven architectures are becoming more common in modern data systems.",
    "These architectures respond to changes in real time, enabling quick reactions to new data.",
    "This is particularly useful for applications that require immediate processing and integration with other systems.",
    "The importance of data quality management cannot be overstated.",
    "Ensuring data is accurate, complete, and reliable is crucial for making informed decisions.",
    "Flexible data models and schema-less databases, such as NoSQL databases, are gaining popularity.",
    "These databases can handle diverse data types and adapt to changes without extensive re-engineering.",
    "This flexibility is essential for dynamic and evolving data environments.",
    "Real-time analytics is a growing demand in various industries.",
    "Businesses need to analyze data as it is generated to gain timely insights and remain competitive.",
    "Data visualization tools are critical for making data insights accessible and actionable.",
    "Tools like Tableau and Power BI allow users to create interactive dashboards and visualizations.",
    "These tools make it easier for decision-makers to understand and act on data insights.",
    "The integration of AI and ML into data architectures is driving new capabilities in data processing and analysis.",
    "These technologies enable advanced analytics and automation, transforming how businesses operate.",
    "The concept of a unified data platform is gaining traction.",
    "Unified platforms integrate various data management and analytics tools into a single environment.",
    "This approach simplifies data operations and enhances collaboration across teams.",
    "Data lineage tracking is becoming increasingly important for ensuring data integrity and compliance.",
    "Understanding the origins and transformations of data helps organizations maintain trust and accountability.",
    "Data-driven decision-making is now a core aspect of business strategy.",
    "Organizations are leveraging data to gain competitive advantages and drive innovation.",
    "The need for scalable and efficient data processing solutions is more critical than ever.",
    "Technologies like distributed computing frameworks are essential for handling large-scale data processing tasks.",
    "Apache Spark and Hadoop are widely used to distribute data processing across multiple nodes.",
    "As the volume and complexity of data grow, the role of data architects is becoming more important.",
    "Data architects design and oversee the implementation of data architectures, ensuring they meet business requirements.",
    "The integration of AI and ML is also influencing the role of data engineers.",
    "Data engineers are responsible for building and maintaining the infrastructure needed for AI and ML applications.",
    "Data security remains a top priority for modern data architectures.",
    "Organizations must implement robust security measures to protect data from breaches and cyberattacks.",
    "This includes encryption, access controls, and regular security audits.",
    "The rise of data-centric business models is driving the need for advanced data management solutions.",
    "Businesses are increasingly relying on data to create value and drive growth.",
    "The evolution of data architectures is closely tied to advancements in hardware and infrastructure.",
    "Innovations in storage technology, such as NVMe drives, are improving data access speeds and reliability.",
    "Network advancements, including the rollout of 5G, are enabling faster and more reliable data transmission.",
    "These infrastructure improvements support the demands of modern data-intensive applications.",
    "Data ethics is becoming a significant consideration in data management practices.",
    "Organizations must ensure they handle data responsibly and transparently.",
    "This includes addressing issues related to data privacy, consent, and bias.",
    "The rise of ethical AI is driving efforts to ensure AI systems are fair and unbiased.",
    "This is crucial for maintaining trust and ensuring equitable outcomes in AI-driven decision-making.",
    "In conclusion, modern data architectures are evolving rapidly to meet the demands of today's data-driven world.",
    "The integration of cloud solutions, AI, real-time processing, and robust security measures are key trends shaping the future of data management.",
    "As technology continues to advance, data architectures will need to adapt and innovate to remain effective and efficient.",
    "The future of data architecture is bright, with endless possibilities for leveraging data to drive business success and innovation."
]


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
plt.show()

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

# Group texts by their cluster label
clustered_docs = {label: [] for label in unique_labels}
for idx, label in enumerate(labels):
    clustered_docs[label].append(texts[idx])

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
    key_phrases = extract_key_phrases(docs)
    cluster_summaries_phrases[label] = key_phrases
    summary = extract_key_sentences(docs)
    cluster_summaries_sentences[label] = summary

# Print cluster summaries
for label in cluster_summaries_phrases:
    print(f"Cluster {label} Key Phrases: {', '.join(cluster_summaries_phrases[label])}")
    print(f"Cluster {label} Summary using Sumy:\n{cluster_summaries_sentences[label]}")
    print(f"Cluster {label} Texts:\n{' '.join(clustered_docs[label])}\n")

# Turn off interactive mode to ensure plots display correctly at the end
plt.ioff()
plt.show()