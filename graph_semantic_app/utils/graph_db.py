import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from .embedding_utils import cosine_similarity

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

class GraphDB:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def insert_text_with_embedding(self, text, embedding):
        with self.driver.session() as session:
            session.write_transaction(self._create_node, text, embedding)

    @staticmethod
    def _create_node(tx, text, embedding):
        tx.run(
            "CREATE (n:Text {text: $text, embedding: $embedding, timestamp: datetime()})",
            text=text,
            embedding=embedding,
        )

    def create_similarity_relationships(self, threshold=0.85):
        with self.driver.session() as session:
            nodes = session.run("MATCH (n:Text) RETURN id(n) as id, n.embedding as emb").data()
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    sim = cosine_similarity(nodes[i]['emb'], nodes[j]['emb'])
                    if sim >= threshold:
                        session.write_transaction(self._create_relation, nodes[i]['id'], nodes[j]['id'], sim)

    @staticmethod
    def _create_relation(tx, id1, id2, weight):
        tx.run(
            "MATCH (a),(b) WHERE id(a)=$id1 AND id(b)=$id2 CREATE (a)-[r:SIMILAR {weight:$w}]->(b)",
            id1=id1,
            id2=id2,
            w=weight,
        )

    def search_similar_embeddings(self, query_emb, top_k=5):
        with self.driver.session() as session:
            nodes = session.run("MATCH (n:Text) RETURN id(n) as id, n.text as text, n.embedding as emb").data()
            scored = []
            for node in nodes:
                score = cosine_similarity(query_emb, node['emb'])
                scored.append({'id': node['id'], 'text': node['text'], 'distance': 1 - score})
            scored.sort(key=lambda x: x['distance'])
            return scored[:top_k]

    def get_subgraph(self, node_id, depth=1):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n)-[r:SIMILAR*1..$d]-(m) WHERE id(n)=$id RETURN n,r,m",
                id=node_id,
                d=depth
            )
            nodes = []
            edges = []
            for record in result:
                n = record['n']
                m = record['m']
                rels = record['r']
                nodes.append({'id': n.id, 'label': n['text']})
                nodes.append({'id': m.id, 'label': m['text']})
                for rel in rels:
                    edges.append({'source': rel.start_node.id, 'target': rel.end_node.id, 'weight': rel['weight']})
            # remove duplicates
            unique_nodes = {node['id']: node for node in nodes}
            return {'nodes': list(unique_nodes.values()), 'edges': edges}
