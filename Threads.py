from threading import Thread
import Collector


class minhaThread (Thread):
    def __init__(self, threadID, nome, id):
        Thread.__init__(self)
        self.threadID = threadID
        self.nome = nome
        self.id = id


    def run(self):
        print "Iniciando thread %s " % (self.name)
        Collector.MainBoot(self.nome, self.id)
        print "Finalizando " + self.nome


# Criando as threads
thread1 = minhaThread(1, "Senador",0)
thread2 = minhaThread(2, "Dep_Estadual",0)
thread3 = minhaThread(3, "Vereador", 0)
thread4 = minhaThread(4, "Dep_Federal", 0)


 
# Comecando novas Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()


threads = []
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)
threads.append(thread4)

for t in threads:
    t.join()
 
print "Saindo da main"