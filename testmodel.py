from model import fermata
from model.fermata import Fermata
from model.model import Model

model= Model()
# model.buildGraph()
model.buildGraphPesato()
print("Num nodi: ", model.get_num_nodi())
print("Num archi: ", model.get_num_archi())
fermata= Fermata(2,"Abbesses", 2.33855, 48.8843)
nodiBfs= model.getBFSNodesFromEdges(fermata)
nodiDfs= model.getDFSNodesFromEdges(fermata)

print(len(nodiBfs))
for i in range (0,10):
    print(nodiBfs[i])
print(len(nodiDfs))
for i in range (0,10):
    print(nodiDfs[i])
nodiDfs= model.getDFSNodesFromEdges(fermata)

print("===========================================")
print("Archi con peso 2")
arcMaggiori= model.getArchiPesoMaggiore()
for a in arcMaggiori:
    print(f"{a[0]}-->{a[1]} : {a[2]["weight"]}")

