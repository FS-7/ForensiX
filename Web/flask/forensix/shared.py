from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_core.documents import Document
#from langchain_community import 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from typing import Any, List
from flask import Flask, Blueprint, request, make_response, session
from flask_cors import CORS, cross_origin
from mysql import connector
from datetime import datetime
from collections import defaultdict

import pandas as pd 
import numpy as np
import chromadb
import os
import uuid
import hashlib, uuid, json, os, random
import sqlite3

'''
cnx = connector.connect(
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)
'''

DB_LOCATION = "../db/Forensix.db"
conn = None

def init_db():
    conn = sqlite3.connect(DB_LOCATION)
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS CRIME_CASES(
            CASE_ID VARCHAR(32) NOT NULL PRIMARY KEY,
            TITLE VARCHAR(50) NOT NULL,
            DESCRIPTION VARCHAR(255) NOT NULL,
            TYPE VARCHAR(20) NOT NULL,
            STATUS INT NOT NULL,
            SEVERITY INT NOT NULL,
            LOCATION VARCHAR(255) NOT NULL,
            DATE_OCCURED DATETIME NOT NULL,
            DATE_REPORTED DATETIME NOT NULL,
            ASSIGNED_OFFICER VARCHAR(32),
            WITNESSES INT,
            NOTES VARCHAR(100)
        );
        '''    
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS EVIDENCES(
            CASE_ID VARCHAR(32) NOT NULL REFERENCES CRIME_CASES(CASE_ID),
            TITLE VARCHAR(50) NOT NULL,
            REFERENCE VARCHAR(512) NOT NULL
        );
        '''
    )
    conn.commit()
    
def get_conn():
    return sqlite3.connect(DB_LOCATION)


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into smaller chunks for better RAG performance"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(split_docs)} chunks")
    
    # Show example of a chunk
    if split_docs:
        print(f"\nExample chunk:")
        print(f"Content: {split_docs[0].page_content[:200]}...")
        print(f"Metadata: {split_docs[0].metadata}")
    
    return split_docs

class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            raise

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        if not self.model:
            raise ValueError("Model not loaded")
    
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

class VectorStore:
    def __init__(self, collection_name: str, persist_directory: str):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={
                    "description": "Document embeddings for RAG"
                }
            )
            print(f"Vector store initialized. Collection: {self.collection_name}")
            print(f"Existing documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise

    def add_documents(self, documents: List[Any], embeddings: np.ndarray):
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        print(f"Adding {len(documents)} documents to vector store...")
        
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []
        
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
            
            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)
            
            documents_text.append(doc.page_content)
            
            embeddings_list.append(embedding.tolist())
        
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                metadatas=metadatas,
                documents=documents_text
            )
            print(f"Successfully added {len(documents)} documents to vector store")
            print(f"Total documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise

class RAGRetriever:    
    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.0):
        print(f"Retrieving documents for query: '{query}'")
        print(f"Top K: {top_k}, Score threshold: {score_threshold}")
        
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]
        
        try:
            results = self.vector_store.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            
            # Process results
            retrieved_docs = []
            
            if results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                ids = results['ids'][0]
                
                for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
                    similarity_score = 1 - distance
                    
                    if similarity_score >= score_threshold:
                        retrieved_docs.append({
                            'id': doc_id,
                            'content': document,
                            'metadata': metadata,
                            'similarity_score': similarity_score,
                            'distance': distance,
                            'rank': i + 1
                        })
                
                print(f"Retrieved {len(retrieved_docs)} documents (after filtering)")
            else:
                print("No documents found")
            
            return retrieved_docs
            
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []