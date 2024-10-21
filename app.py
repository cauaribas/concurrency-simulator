import threading
import time
import random

lockX = threading.Lock()
lockY = threading.Lock()
counter_lock = threading.Lock()
timestamp_lock = threading.Lock()

thread_counter = 0 # item x
number = 0 # item y
increment_success = 0
deadlock_count = 0
thread_timestamps = {}


def run():
    global thread_counter
    t = threading.current_thread()

    print(f"{t.name} entrou em execução.")
    
    time.sleep(random.uniform(0.1, 2.0))

    with timestamp_lock:
        thread_timestamps[t.name] = time.time()

    with counter_lock:
        thread_counter += 1
        
    transaction(thread_counter, t)
        
    print(f"{t.name} finalizou sua execução.")

def check_deadlock(lock, t):
    global deadlock_count
    start_time = time.time()

    while True:
        if lock.acquire(blocking = False):
            print(f"{t.name} obteve o bloqueio do recurso.")
            return True # Lock acquired

        print(f"{t.name} está esperando por um recurso.")

        with timestamp_lock:
            for thread_name, timestamp in thread_timestamps.items():
                if thread_name != t.name and lock.locked():
                    if timestamp > thread_timestamps[t.name]:
                        print(f"{t.name} finalizou {thread_name} para evitar deadlock.")
                        return False # Thread nova morre
                    else:
                        print(f"{t.name} aguardando {thread_name} (thread mais antiga).")
                        time.sleep(1)
        
        if time.time() - start_time > 5:
            print(f"{t.name} foi finalizada devido a deadlock.")
            with counter_lock:
                deadlock_count += 1 
            return False

def transaction(thread_counter, t):
    global number, increment_success
    
    if thread_counter % 2 == 0:
        if check_deadlock(lockX, t):
            # print(f"{t.name} alocou a lock X")
            time.sleep(random.uniform(0.1, 2.0))

            if check_deadlock(lockY, t):
                number += 5
                increment_success += 1
                print(f"{t.name} incrementou o número para {number}.")
                print(f"{t.name} liberou o bloqueio do recurso Y.")
                lockY.release()
            print(f"{t.name} liberou o bloqueio do recurso X.")
            lockX.release()
    else:
        if check_deadlock(lockY, t):
            # print(f"{t.name} alocou a lock Y")
            time.sleep(random.uniform(0.1, 2.0))
            
            if check_deadlock(lockX, t):
                number += 5   
                increment_success += 1   
                print(f"{t.name} incrementou o número para {number}.")
                print(f"{t.name} liberou o bloqueio do recurso X.")
                lockX.release()
            print(f"{t.name} liberou o bloqueio do recurso Y.")
            lockY.release()     

def main():
    global number, increment_success, deadlock_count
    threads = []

    for i in range(5):
        t = threading.Thread(target=run, name=f"Thread-{i}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Main concluido")
    print("Numbero final: ", number)
    print(f"Incrementos bem-sucedidos: {increment_success}")
    print(f"Threads finalizadas por deadlock: {deadlock_count}")

if __name__ == "__main__":
    main()