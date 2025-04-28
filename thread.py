import threading
import time
import random


safe_sem = threading.Semaphore(2)        # only two tellers can enter the safe at once
manager_sem = threading.Semaphore(1)     # manager can handle one person at once
bank_door_sem = threading.Semaphore(2)   # only two customers can enter the bank at once
teller_ready = [threading.Semaphore(0) for _ in range(3)]   # each tell's ready status
customer_ready = threading.Semaphore(0)  # a customer is ready
transaction_done = threading.Semaphore(0)  # transaction is done
customer_left = threading.Semaphore(0)  # customer leave the teller

bank_open = threading.Event()

teller_locks = [threading.Lock() for _ in range(3)]
teller_available = [True for _ in range(3)]


print_lock = threading.Lock()


def log(thread_type, id, target_id="", msg=""):
    with print_lock:
        if target_id != "":
            print(f"{thread_type} {id} [{target_id}]: {msg}")
        else:
            print(f"{thread_type} {id} []: {msg}")
            
def teller_thread(tid):
    log("Teller", tid, msg="ready to serve")
    bank_open.wait()  # Wait until bank is open
    while True:
        log("Teller", tid, msg="waiting for a customer")
        customer_ready.acquire()
        with teller_locks[tid]:
            teller_available[tid] = False  # This teller is now busy
        log("Teller", tid, msg="serving a customer")
        teller_ready[tid].release()  # Notify a customer to come to this teller

        # Wait a bit for the customer to respond
        time.sleep(0.005)
        log("Teller", tid, msg="asks for transaction")

        # After simulated transaction (including safe or manager access), do:
        transaction_done.release()  # Notify customer that transaction is done
        customer_left.acquire()    # Wait for the customer to leave

        with teller_locks[tid]:
            teller_available[tid] = True
def customer_thread(cid):
    # Decide transaction type
    transaction = random.choice(["deposit", "withdrawal"])
    log("Customer", cid, msg=f"wants to perform a {transaction} transaction")

    # Simulate delay before entering the bank
    time.sleep(random.uniform(0, 0.1))

    bank_door_sem.acquire()
    log("Customer", cid, msg="going to bank.")
    log("Customer", cid, msg="entering bank.")
    bank_door_sem.release()

    # Try to select a teller
    for i in range(3):
        if teller_available[i]:
            log("Customer", cid, f"Teller {i}", "selects teller")
            log("Customer", cid, f"Teller {i}", "introduces itself")
            customer_ready.release()      # Notify teller there's a customer ready
            teller_ready[i].acquire()     # Wait for teller to invite

            log("Customer", cid, f"Teller {i}", f"asks for {transaction} transaction")

            # If it's a withdrawal, go to the manager
            if transaction == "withdrawal":
                log("Teller", i, f"Customer {cid}", "going to the manager")
                manager_sem.acquire()
                log("Teller", i, f"Customer {cid}", "getting manager's permission")
                time.sleep(random.uniform(0.005, 0.03))
                manager_sem.release()

            # Access the safe
            log("Teller", i, f"Customer {cid}", "going to safe")
            safe_sem.acquire()
            log("Teller", i, f"Customer {cid}", "enter safe")
            time.sleep(random.uniform(0.01, 0.05))
            log("Teller", i, f"Customer {cid}", "leaving safe")
            safe_sem.release()

            log("Teller", i, f"Customer {cid}", f"finishes {transaction} transaction.")
            log("Teller", i, f"Customer {cid}", "wait for customer to leave.")

            transaction_done.acquire()
            customer_left.release()

            log("Customer", cid, msg="goes to door")
            log("Customer", cid, msg="leaves the bank")
            return
def main():
    tellers = []
    customers = []

    # Start teller threads
    for i in range(3):
        t = threading.Thread(target=teller_thread, args=(i,))
        tellers.append(t)
        t.start()

    # Bank opens
    bank_open.set()

    # Start customer threads
    for i in range(50):
        c = threading.Thread(target=customer_thread, args=(i,))
        customers.append(c)
        c.start()

    # Wait for all threads to finish
    for c in customers:
        c.join()
    for t in tellers:
        log("Teller", t.name, msg="leaving for the day")

    print("The bank closes for the day.")

if __name__ == "__main__":
    main()
