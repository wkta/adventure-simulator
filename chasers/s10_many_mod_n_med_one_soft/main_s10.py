"""
Demo technique se caractéristant par:

 - Plusieurs instances de model
 - plusieurs mediators & comm entre eux via une classe NetworkLayer
 - MAIS un seul programme qui tourne...
 - pas de pygame/GUI pour le moment

Particularité : On ne fait plus bouger l'IA directement dans le model quand le player moves.
Cette update est dorénavant faite dans le code correspondant à la logique serveur
"""
from ClientComponent import ClientComponent
from NetworkLayer import NetworkLayer
from ServerComponent import ServerComponent
from ext_mediators import ServerMediator


# Create network layer
network_layer = NetworkLayer()
# mediators are registered auto within the network layer to SIMULATE a bidirectional connection

# init game,
# les programmes ont volontairement chacun leur modèle. Le défi est qu'ils se sync en jouant...
clients = [
    ClientComponent(network_layer, 'p1'),
    ClientComponent(network_layer, 'p2')
]
server_mediator = ServerMediator(network_layer)
server = ServerComponent(server_mediator)

active_client_rank = 0


# -----------------------------
#  tests
# -----------------------------
def massiv_debug():
    print('>>massiv DEBUG <<')
    for i in range(3):
        tmp[i].disp_model()
    print('|||||||||||')
    print()


tmp = list(clients)
tmp.append(server)
massiv_debug()

# ensure manually that models are sync, right at the start

clients[0]._model.push_changes()  # EXCEPTIONNEL

cpt = None
while cpt is None or cpt > 0:
    cpt = 0
    cpt += clients[0].mediator.update()
    cpt += clients[1].mediator.update()
    cpt += server_mediator.update()
massiv_debug()

ref_active_client = clients[active_client_rank]

while ref_active_client._model.winner == 0:
    # @@@ would work if logic handled client side:

    # wcell = ref_active_client.input_play()
    # ref_active_client.commit_move(wcell)
    # if wcell is None:
    #    print('>> exit prog')
    #    break

    # better do it that way! Authoritatve server
    wcell = ref_active_client.input_play()
    ref_active_client._model.remote_move_pl(*wcell)

    # do the full update
    cpt = None
    while cpt is None or cpt > 0:
        cpt = 0
        cpt += clients[0].mediator.update()
        cpt += clients[1].mediator.update()
        cpt += server_mediator.update()
    massiv_debug()

    active_client_rank = (active_client_rank + 1) % 2  # switch active player
    ref_active_client = clients[active_client_rank]
