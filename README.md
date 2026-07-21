# Python Blockchain

A lightweight Python implementation of a decentralized blockchain, featuring a Proof of Work (PoW) consensus algorithm and a Flask REST API for multi-node interaction.

---

## Overview

* **`blockchain.py`**: Core architecture containing the main `Blockchain` class and structural definitions for blocks, transaction management, and hashing routines.
* **`proof_of_work_concept.py`**: A standalone demonstration of Proof of Work mechanics using basic trailing-zero difficulty rules.
* **Flask Server (`main.py`)**: An interactive API layer built to simulate a distributed network.

> **Note on Implementation:** While `proof_of_work_concept.py` demonstrates simple trailing zeros, the actual API implementation validates blocks against a target prefix rule (`1234`).

---

## Key Features & Endpoints

The Flask server handles multi-node consensus, mining rewards, and transaction queuing across three primary workflows:

| Action | Endpoint | Method | Description |
| :--- | :--- | :--- | :--- |
| **Mine Block** | `/mine` | `GET` | Solves the Proof of Work puzzle, forges a new block, and issues a mining reward. |
| **New Transaction** | `/transactions/new` | `POST` | Adds a new transaction payload to the pool of unconfirmed transactions for the next block. |
| **View Chain** | `/chain` | `GET` | Returns the full block ledger and current chain length. |
| **Register Nodes** | `/nodes/register` | `POST` | Adds peer node URLs to the network state. |
| **Consensus** | `/nodes/resolve` | `GET` | Executes the longest-valid-chain rule across registered peers to resolve conflicting states. |

---

## Quickstart

1. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
    ```

2. **Install dependencies:**
    ```bash
    pip install flask
    ```

3. **Start a local node:**
    ```bash
    python main.py
    ```
    
4. **Mine a block via curl:**
    ```bash
    curl -i http://localhost:5500/mine
    ```

> **Refer to testing log for more curl and implemenation visualization:** Observe `testing blockchain.md` for simple blockchain logic and `testing consensus.md` for network logic