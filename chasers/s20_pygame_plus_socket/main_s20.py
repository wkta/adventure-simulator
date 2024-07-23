"""
Demo technique se caractéristant par:

 - pygame & GUI
 - le fait d'avoir un vrai serveur & une vraie classe NetworkLayer mais 100% basée sur 'socket'
 - plusieurs programmes qui tournent

 - donc plusieurs instances de model
 - bien sûr plusieurs mediators & comm entre eux via les methodes statiques de NetworkLayer

Particularité : On  fait bouger l'IA directement dans le model, c'est implémenté
dans le code correspondant à la logique serveur
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

# server.process_move((1, 0, 'O'))
# server.flag_winner()
# print('---')
#
# client_a.play_move(2, 2, 'X')
# client_b.kill_player()

# ------- test model changes pushing mechanism ------
# Create a Point3D instance and push changes
# point_mediator = client_a_mediator
# point = Point3D(1, 2, 3, point_mediator)
# client_a.point = point

# Manually update mediators to process event queues
# print(client_a_mediator.update())
# print(client_b_mediator.update())
# print(server_mediator.update())
#
# print('...')
# print(client_a_mediator.update())
# print(client_b_mediator.update())
# print(server_mediator.update())
#
# print('...')
# print(client_a_mediator.update())
# print(client_b_mediator.update())
# print(server_mediator.update())

# print('>>»')
# print(point.components)
# print('server-side: ', server.three_d_point.components)
# print()
#
# print('post point3d components is now set client side...')
# point.components = (87, 1.0, -3.0)
# print(client_a_mediator.update())
# print(client_b_mediator.update())
# print(server_mediator.update())
#
# print('>>»')
# print(point.components)
# print('server-side: ', server.three_d_point.components)

#
# print(' Je FAIS EVOLVE vec manuellement')
# server.evolve_vector()
# print('...')
#
# print('...')
# print(client_a_mediator.update())
# print(client_b_mediator.update())
# print(server_mediator.update())
# print('...')
# print(client_a_mediator.update())
# print(client_b_mediator.update())
# print(server_mediator.update())

# print('>>»')
# print(point.components)
# print('server-side: ', server.three_d_point.components)
