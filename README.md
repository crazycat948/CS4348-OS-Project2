# CS4348 Project 2: Bank Simulation with Threads and Semaphores

## Project Overview
This project simulates a small bank using multithreading and semaphores for synchronization. The simulation includes:

- **Three Teller Threads**
- **Fifty Customer Threads**

Customers arrive at the bank to perform either deposits or withdrawals. Tellers interact with the customers, manage access to the safe and bank manager, and complete customer transactions in a synchronized manner.

The program is implemented in **Python** using the `threading` module and `threading.Semaphore` for thread synchronization.

---

## File Structure

- `bank_simulation.py`  
  Main program that contains the Teller and Customer thread logic, shared resource management, and program execution flow.

- `devlog.md`  
  Development log documenting session plans, progress, problems, and thoughts.

- `README.md`  
  Project description, file descriptions, and instructions for running the program.

---

## How to Compile and Run

### Prerequisites:
- Python 3.8 or higher installed
- No external libraries needed (only standard Python libraries)

### Running the Program:
Navigate to the project folder and run:

```bash
python bank_simulation.py
