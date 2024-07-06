import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

import tensorflow as tf
import tensorflow_hub as hub

# Load the Universal Sentence Encoder model from TensorFlow Hub
model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(model_url)

print("Universal Sentence Encoder model loaded successfully.")

df1 = pd.read_csv(r"Zerodha_Varsity.csv")
df2 = pd.read_csv(r"Copy_of_Finance_With_Sharan.csv")
df1 = df1.fillna('')
df2 = df2.fillna('')
df2.head()

df = pd.concat([df1, df2], ignore_index=True)
df.head()

df = df[['Title','Description','ids']]
df['Title_Description'] = df['Title'] + df['Description']
# df = df[['Name', 'City']]
df.head()

def embed(texts):
    return model(texts)

titles = df['Title_Description']
titles[0]

embeddings = embed(titles)
embeddings.shape

pca = PCA(n_components=2)
pca_result = pca.fit_transform(embeddings)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
plt.scatter(pca_result[:, 0], pca_result[:, 1])
plt.show()

nn = NearestNeighbors(n_neighbors=10)
nn.fit(embeddings)

yt_url = "https://www.youtube.com/watch?v="
def process(url):
  return yt_url + url

def recommend(text):
    emd = embed([text])
    # idx = df[df['Title'] == title].index[0]
    neighbours = nn.kneighbors(emd, return_distance=False)[0]

    urls = df['ids'].iloc[neighbours].tolist()

    return [process(url) for url in urls]

recommend('different types of mutual funds')