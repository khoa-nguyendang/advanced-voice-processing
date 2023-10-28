import re
import os
import torch
import pickle
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class RobertaQA(metaclass=Singleton):
    def __init__(self):
        self.embedder = None
        self.corpus = None
        self.qa_model = None
        self.corpus_embeddings = None
        self.corona_dataset_with_paper_info = None
        self.base_path = "./checkpoint"

        self.initialize()

    def initialize(self):
        self.embedder = SentenceTransformer('paraphrase-distilroberta-base-v1', device='cpu')

        corpus_embeddings_path = os.path.join(self.base_path, "/corpus_embeddings_roberta_9000.pt")
        with open(corpus_embeddings_path, 'rb') as f:
            self.corpus_embeddings = torch.load(f, map_location="cpu")

        model_name = "deepset/roberta-base-squad2"
        self.qa_model = pipeline('question-answering', model=model_name, tokenizer=model_name)

        CORD19_data_path = os.path.join(self.base_path, "/CORD19_SentenceMap_9000.pkl")
        with open(CORD19_data_path, 'rb') as drivef:
            self.corona_dataset_with_paper_info = pickle.load(drivef)

        self.corpus = list(self.corona_dataset_with_paper_info.keys())


    def document_filter(self, question: str, top_k=5):
        query_embedding = self.embedder.encode(question, convert_to_tensor=True, device='cpu')
        cos_scores = util.pytorch_cos_sim(query_embedding, self.corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        sentences_info = []
        for iter, score, idx in zip(range(0, top_k),top_results[0], top_results[1]):
            answer = ' '.join([re.sub(r"^\[.*\]", "", x) for x in self.corpus[idx].split()])
            paper_info = self.corona_dataset_with_paper_info[self.corpus[idx]]
            sentences_info.append({
                "answer": answer,
                "paper_id": paper_info[0],
                "paper_title": paper_info[1],
                "score": score
            })
        
        return sentences_info

    def __call__(self, question: str):
        list_answer_info = self.document_filter(question, top_k=20)
        context_sentence = "".join([info["answer"] for info in list_answer_info])
        QA_input = {
            'question': question,
            'context': context_sentence
        }
        res = self.qa_model(QA_input)
        res["question"] = question

        return res
    