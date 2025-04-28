# 4/8/2025 7:53 pm
This is starting time to do this project, let me first understand what to do here.
The goal of the project is:
The goal of this project is to simulate the operation of a bank using multithreading and semaphores for synchronization, demonstrating practical concepts of concurrency in operating systems. The simulation models a bank with three teller threads and fifty customer threads. Customers arrive throughout the day to perform either a deposit or a withdrawal. A teller serves one customer at a time, and additional customers wait in line if all tellers are busy.

The simulation includes coordination for shared resources, such as a safe that only two tellers can access at once, and a bank manager who must approve all withdrawal transactions—only one teller may speak to the manager at a time. Customers also enter the bank through a door with limited capacity (two at a time), and the bank only opens once all three tellers are ready. The simulation ends once all 50 customers have completed their transactions and exited the bank.

This project is an exercise in thread synchronization, critical section handling, and the use of semaphores to manage access to shared resources and control thread behavior in a concurrent environment.

#4/8/2025 9:17 pm
To begin the project, I first focused on setting up the shared resources and synchronization primitives that will be used throughout the bank simulation. Since the simulation relies heavily on coordinating access between multiple threads, using semaphores was critical to prevent race conditions and ensure proper control over the flow of customers and tellers.
I defined several semaphores to manage key constraints:

safe_sem: Limits access to the safe, allowing only two tellers at a time.
manager_sem: Restricts teller interaction with the bank manager to one at a time.
bank_door_sem: Controls how many customers can enter the bank simultaneously (max two).
teller_ready, customer_ready, transaction_done, customer_left: These semaphores coordinate the interaction between tellers and customers, such as when a teller is available, a customer is ready, and when transactions are complete.

In addition to semaphores, I also set up:
An Event called bank_open to ensure that no customers can enter the bank until all tellers are ready.
teller_locks and a teller_available list to help assign customers to tellers and track availability.
A print_lock to prevent log messages from multiple threads from overlapping or interleaving on the console.
This setup lays the foundation for implementing the core teller and customer behaviors with proper synchronization

#4/9/2025 6:25pm
Today is the day Luka back to Dallas.
I am going to cotinus to work on some tekker thread logic
today I am going to let the program knows that when the bank is open? Is this teller busy or not? And tell if tje customer left.

#4/9/2025  8:25pm
Once the core semaphores and shared resources were in place, I moved on to two essential parts of the simulation: setting up the logging system and building the teller thread logic.

First, I created a simple log() function to standardize all output messages. Since this project involves 50 customers and 3 tellers running in parallel, I wanted to avoid chaotic or overlapping console output. To solve that, I used a print_lock to make sure only one thread can print at a time. This should make debugging a lot easier and keep the output readable—especially when trying to match it to the sample output from the professor.

After the logging was ready, I started writing the teller_thread() function. Each teller announces when they are ready and then waits for a customer to approach. Once a customer signals that they are ready, the teller begins the transaction process. I also made sure that a teller marks themselves as “busy” when working with a customer and “available” again after the transaction is complete. I haven’t implemented the full transaction logic yet (like actually talking to the manager or entering the safe), but the framework is there.

This step was pretty satisfying—seeing the tellers spin up, print their status, and wait for customers was the first time the simulation started to feel alive.


#4/12/2025  12:19am
Next up, I’m diving into the customer side of the simulation. Each customer thread will simulate a real person walking into the bank, deciding whether they want to deposit or withdraw, and interacting with the tellers accordingly. I’ll need to implement randomized delays to represent arrival times, manage the flow through the bank entrance (limited to two at a time), and make sure each customer properly syncs up with an available teller.

I’m also planning to make sure withdrawals go through the bank manager and that access to the safe is limited to two tellers, just like in the project spec. The challenge here will be making sure the customer doesn’t jump ahead before the teller is actually ready, and that all steps—from greeting to finishing the transaction—are logged cleanly.

Once this part is working, the full teller-customer interaction loop will be complete, and the simulation should start to feel like an actual functioning bank.

# 4/12/2025 1:35pm

This step was all about bringing the customer side of the simulation to life. I started by defining the behavior of each customer thread—from randomly deciding between a deposit or withdrawal, to waiting before entering the bank, to finding a teller and completing the transaction.

One of the first things I handled was making sure customers didn’t all rush in at once. I used a semaphore (bank_door_sem) to limit the number of customers who can enter the bank at the same time to two. This simulates the real-world constraint mentioned in the spec and adds a nice touch of realism to the simulation flow.

Then came the part where customers have to get in line and wait for a teller. Each customer looks for an available teller and, once one is found, initiates the interaction. I made sure to log each step with clear print statements—when the customer enters, selects a teller, introduces themselves, and states their transaction type.

Withdrawals had to go through the bank manager, so I included that logic too. The customer waits while the teller gets permission from the manager, which is simulated by a short sleep and access controlled by a semaphore (manager_sem). Finally, the teller and customer proceed to the safe (which only allows two tellers at a time) to complete the transaction.

This part of the code was trickier than previous steps because it involved a lot of back-and-forth signaling between customer and teller threads. But once I got the semaphores wired up correctly, everything synced up nicely. Watching the log output now, I can see the full interaction happening in order—from a customer entering the bank to them walking out with their transaction complete.

At this point, the simulation feels almost complete.

#4/12/2025 1:50pm
It is already so late so let me finish the project first.
.
With both the teller and customer threads in place and communicating correctly, the next step is tying everything together in the main function. This final part will handle creating all 50 customer threads and 3 teller threads, ensuring they start in the right order, and waiting for them to complete before closing the simulation.

I’ll also finalize the logic for when the bank opens (making sure customers don’t sneak in early), and add proper cleanup and exit logs for each thread—like tellers saying they’re leaving for the day and the final “bank is closed” message.

The goal here is to make the entire simulation feel like a seamless flow from opening to closing, with all events properly logged and synchronized.

Once this step is done, the bank simulation will be fully functional. 

#4/12/2025 2:45pm
In the final step of the project, I put all the pieces into motion. With the teller and customer logic implemented and tested individually, the focus shifted to orchestrating the full simulation flow from start to finish.

I started by creating three teller threads and launched them first. These threads immediately printed that they were “ready to serve” and began waiting for customers. To make sure the bank didn’t open before the tellers were ready, I used an Event (bank_open) to delay customer access until all teller threads were up and running.

Once the tellers were in place, I launched all 50 customer threads. Each customer followed the logic I’d already built—waiting a random amount of time, entering the bank (respecting the entrance limit), selecting a teller, and going through the transaction process. Thanks to the synchronization I added earlier, everything ran smoothly: no race conditions, clean logs, and proper sequencing of interactions between threads.

At the end of the simulation, I used join() to wait for all customer threads to finish. Then, each teller thread printed a final message saying they were “leaving for the day.” The simulation concluded with the message: “The bank closes for the day.”

This step tied everything together and marked the point where the simulation truly felt complete. Seeing the output mirror the sample provided by the professor was super satisfying—and also a huge relief that all the semaphore juggling paid off.
