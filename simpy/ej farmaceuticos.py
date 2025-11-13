import random
import simpy

#subsistema de generación de pedidos
def sistema(env, farmaceuticos,store):
    while True:
        yield env.timeout(random.uniform(4,6))
        env.process(pedido(env, farmaceuticos,store))
        
#subsistema del pedido
def pedido(env, farmaceuticos,store):
    with farmaceuticos.request() as req:
        yield req 
        yield env.timeout(random.uniform(3,5))
        yield store.put('pedido')
        print('el farmaceutico dejó 1 remedio')

def repartidor(env,store):
  while True:
      yield env.timeout(random.uniform(15,30))
      n = 0
      while len(store.items) > 0:
        n+=1
        yield store.get()
      print(f'Sacados {n} remedios')

env = simpy.Environment()
store = simpy.Store(env)
farmaceuticos = simpy.Resource(env, capacity=2)
env.process(sistema(env, farmaceuticos,store))
env.process(repartidor(env, store))
env.run(until=480)