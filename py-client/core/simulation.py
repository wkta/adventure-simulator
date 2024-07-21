from ClientComponent import ClientComponent
from ServerComponent import ServerComponent
from game_objects import Point3D
from mediators import NetworkLayer, ClientMediator, ServerMediator


# Create network layer
network_layer = NetworkLayer()

# Create mediator + component, three times
client_a_mediator = ClientMediator('Client A', network_layer)
client_a = ClientComponent(client_a_mediator)

client_b_mediator = ClientMediator('Client B', network_layer)
client_b = ClientComponent(client_b_mediator)

server_mediator = ServerMediator(network_layer)
server = ServerComponent(server_mediator)

# Register mediators with the network layer
network_layer.mediators.extend([
    client_a_mediator, client_b_mediator, server_mediator
])


# -----------------------------
#  tests
# -----------------------------
client_a.play_move(0, 0, 'X')
client_b.play_move(1, 1, 'O')

server.process_move((1, 0, 'O'))
server.flag_winner()
print('---')

client_a.play_move(2, 2, 'X')
client_b.kill_player()

# ------- test model changes pushing mechanism ------
# Create a Point3D instance and push changes
point_mediator = client_a_mediator
point = Point3D(1, 2, 3, point_mediator)
client_a.point = point

# Manually update mediators to process event queues
print(client_a_mediator.update())
print(client_b_mediator.update())
print(server_mediator.update())

print('...')
print(client_a_mediator.update())
print(client_b_mediator.update())
print(server_mediator.update())

print('...')
print(client_a_mediator.update())
print(client_b_mediator.update())
print(server_mediator.update())



print('>>»')
print(point.components)
print('server-side: ', server.three_d_point.components)
print()

print('post point3d components is now set client side...')
point.components = (87, 1.0, -3.0)
print(client_a_mediator.update())
print(client_b_mediator.update())
print(server_mediator.update())

print('>>»')
print(point.components)
print('server-side: ', server.three_d_point.components)


print( ' Je FAIS EVOLVE vec manuellement')
server.evolve_vector()
print('...')

print('...')
print(client_a_mediator.update())
print(client_b_mediator.update())
print(server_mediator.update())
print('...')
print(client_a_mediator.update())
print(client_b_mediator.update())
print(server_mediator.update())

print('>>»')
print(point.components)
print('server-side: ', server.three_d_point.components)
