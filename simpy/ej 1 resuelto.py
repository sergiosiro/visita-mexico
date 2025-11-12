import simpy

personasAtendidas = 0
personasEsperando = 0
personasQueLlegaron = 0

def persona(env, nombre, maquina):
  global personasEsperando
  global personasAtendidas
  personasEsperando += 1
  print('Llega la persona',nombre)
  with maquina.request() as req:
    yield req
    personasEsperando -= 1
    personasAtendidas += 1
    yield env.timeout(3)
    
#Si se toma el recurso con un with, se libera en forma automática luego de finalizado el with
#Si no se toma con un with, se debe liberar mediante el release() una vez que se terminó de utilizar

def sistema(env, maquina):
    print('Sistema')
    global personasQueLlegaron
    i=0
    while True:
      yield env.timeout(random.expovariate(1/4))
      print('Generando persona',i)
      i+=1
      personasQueLlegaron+=1
      env.process(persona(env, i, maquina))

print('Inicio')
  
env = simpy.Environment()
maquina = simpy.Resource(env, capacity=1)
env.process(sistema(env,maquina))

env.run(until=60)
print('Personas que llegaron:', personasQueLlegaron)   
print('Personas atendidas:', personasAtendidas)
print('Personas esperando:', personasEsperando)