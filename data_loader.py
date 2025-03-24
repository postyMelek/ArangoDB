import networkx as nx
from arango import ArangoClient
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

ARANGO_HOST = os.getenv("ARANGO_HOST")
ARANGO_USERNAME = os.getenv("ARANGO_USERNAME")
ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD")
ARANGO_DB_NAME = os.getenv("ARANGO_DB_NAME")

# Init client
client = ArangoClient(hosts=ARANGO_HOST)

# Always connect first to _system to manage DBs
sys_db = client.db('_system', username=ARANGO_USERNAME, password=ARANGO_PASSWORD)

# Cek & buat database jika belum ada
if not sys_db.has_database(ARANGO_DB_NAME):
    sys_db.create_database(ARANGO_DB_NAME)
    print(f"✅ Database {ARANGO_DB_NAME} telah dibuat!")

# Now connect ke database tujuan
db = client.db(ARANGO_DB_NAME, username=ARANGO_USERNAME, password=ARANGO_PASSWORD)

# Load dataset amazon0302
G = nx.read_edgelist("amazon0302.txt", create_using=nx.DiGraph())

# RESET KOLEKSI
if db.has_collection("products"):
    db.delete_collection("products")
if db.has_collection("co_purchases"):
    db.delete_collection("co_purchases")

# BUAT KOLEKSI ULANG
db.create_collection("products")
db.create_collection("co_purchases", edge=True)

print("✅ Koleksi products dan co_purchases sudah dibuat ulang.")

# INSERT PRODUCTS
products = [{"_key": str(node)} for node in G.nodes()]
db.collection("products").insert_many(products, overwrite=True)

print(f"✅ {len(products)} produk berhasil dimasukkan!")

# INSERT EDGES DENGAN BATCHING
edges = [{"_from": f"products/{u}", "_to": f"products/{v}"} for u, v in G.edges()]

batch_size = 10000
edges_collection = db.collection("co_purchases")

for i in range(0, len(edges), batch_size):
    batch = edges[i:i + batch_size]
    edges_collection.insert_many(batch, overwrite=True)
    print(f"✅ Batch {i // batch_size + 1} selesai. ({len(batch)} edges)")

print("✅ Semua data produk dan co-purchases berhasil di-insert ke ArangoDB!")
