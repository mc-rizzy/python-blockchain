# Blockchain Consensus Algorithm Test Log

**Node 1:** `http://localhost:5500`  
**Node 2:** `http://localhost:5501`  
**Target Goal:** Verify consensus algorithm functionality (longest valid chain rule) and conflict resolution between multi-node instances.

---

## Executive Summary

| Step | Action / Endpoint | Node | Result / State |
| :--- | :--- | :--- | :--- |
| **1. Initialization** | Server Spin-up | Node 1 & Node 2 | Both initialized with Genesis Block (`length: 1`) |
| **2. Divergence** | `GET /mine` (x2) | Node 2 | Node 2 forged Blocks 2 & 3 (`length: 3`) |
| **3. Pre-check** | `GET /chain` | Node 1 | Node 1 remained at Genesis Block (`length: 1`) |
| **4. Consensus** | `GET /nodes/resolve` | Node 1 | **Chain Replaced** — Node 1 synced Node 2's longer chain (`length: 3`) |
| **5. Verification** | `GET /nodes/resolve` | Node 1 | **Authoritative** — Node 1 confirmed its chain matches network maximum |

---

## Test Execution Log

### Step 1: Initialize Nodes & Mine on Node 2

Node 2 mined two sequential blocks to construct a longer valid chain (`length: 3`).

* **Command (Mine Block 2):**
  ```bash
  curl -i http://localhost:5501/mine
  ```
* **Response:**
  ```bash
  {
    "index": 2,
    "message": "New Block Forged",
    "previous_hash": "fae762ae2aae8a6e571c7752dc782659c86a109011cda516769139d2de3337ba",
    "proof": 57432,
    "transactions": [
      {
        "amount": 1,
        "recipient": "765bdb955f074dc79a71c76066914b2d",
        "sender": "0"
      }
    ]
  }
  ```
* **Command (Mine Block 3):**
  ```bash
  curl -i http://localhost:5501/mine
  ```
* **Response:**
  ```bash
  {
    "index": 3,
    "message": "New Block Forged",
    "previous_hash": "961bcf0974111955fc2a60cbe4e5e51e5b424559b28996c23a7d78e4a780e30a",
    "proof": 114375,
    "transactions": [
      {
        "amount": 1,
        "recipient": "765bdb955f074dc79a71c76066914b2d",
        "sender": "0"
      }
    ]
  }
  ```


### Step 2: Check Node 1 Initial Chain State
* **Command:**
  ```bash
  curl -i http://localhost:5500/chain
  ```
* **Response:**
  ```bash
    {
    "chain": [
      {
        "index": 1,
        "previous_hash": 1,
        "proof": 100,
        "timestamp": 1784651741.737657,
        "transactions": []
      }
    ],
    "length": 1
  }
  ```

### Step 3: Trigger Consensus Resolution on Node 1

Node 1 evaluated neighbor chains across the network, detected Node 2's longer valid chain, and replaced its own local chain.

* **Command:**
  ```bash
  curl -i http://localhost:5500/nodes/resolve
  ```
* **Response:**
  ```bash
  {
    "chain": [
      {
        "index": 1,
        "previous_hash": 1,
        "proof": 100,
        "timestamp": 1784651777.207683,
        "transactions": []
      },
      {
        "index": 2,
        "previous_hash": "fae762ae2aae8a6e571c7752dc782659c86a109011cda516769139d2de3337ba",
        "proof": 57432,
        "timestamp": 1784651818.621543,
        "transactions": [
          {
            "amount": 1,
            "recipient": "765bdb955f074dc79a71c76066914b2d",
            "sender": "0"
          }
        ]
      },
      {
        "index": 3,
        "previous_hash": "961bcf0974111955fc2a60cbe4e5e51e5b424559b28996c23a7d78e4a780e30a",
        "proof": 114375,
        "timestamp": 1784651833.95809,
        "transactions": [
          {
            "amount": 1,
            "recipient": "765bdb955f074dc79a71c76066914b2d",
            "sender": "0"
          }
        ]
      }
    ],
    "message": "Our chain was replaced"
  }
  ```

### Step 4: Verify Node 2 Chain State
* **Command:**
  ```bash
  curl -i http://localhost:5501/chain
  ```
* **Response:**
  ```bash
  {
    "chain": [
      {
        "index": 1,
        "previous_hash": 1,
        "proof": 100,
        "timestamp": 1784651777.207683,
        "transactions": []
      },
      {
        "index": 2,
        "previous_hash": "fae762ae2aae8a6e571c7752dc782659c86a109011cda516769139d2de3337ba",
        "proof": 57432,
        "timestamp": 1784651818.621543,
        "transactions": [
          {
            "amount": 1,
            "recipient": "765bdb955f074dc79a71c76066914b2d",
            "sender": "0"
          }
        ]
      },
      {
        "index": 3,
        "previous_hash": "961bcf0974111955fc2a60cbe4e5e51e5b424559b28996c23a7d78e4a780e30a",
        "proof": 114375,
        "timestamp": 1784651833.95809,
        "transactions": [
          {
            "amount": 1,
            "recipient": "765bdb955f074dc79a71c76066914b2d",
            "sender": "0"
          }
        ]
      }
    ],
    "length": 3
  }
  ```

### Step 5: Secondary Consensus Check on Node 1

Re-ran consensus on Node 1 to ensure it recognizes its updated chain as authoritative without performing unnecessary replacements.

* **Command:**
  ```bash
  curl -i http://localhost:5500/nodes/resolve
  ```
* **Response:**
  ```bash
  {
    "chain": [
      {
        "index": 1,
        "previous_hash": 1,
        "proof": 100,
        "timestamp": 1784651777.207683,
        "transactions": []
      },
      {
        "index": 2,
        "previous_hash": "fae762ae2aae8a6e571c7752dc782659c86a109011cda516769139d2de3337ba",
        "proof": 57432,
        "timestamp": 1784651818.621543,
        "transactions": [
          {
            "amount": 1,
            "recipient": "765bdb955f074dc79a71c76066914b2d",
            "sender": "0"
          }
        ]
      },
      {
        "index": 3,
        "previous_hash": "961bcf0974111955fc2a60cbe4e5e51e5b424559b28996c23a7d78e4a780e30a",
        "proof": 114375,
        "timestamp": 1784651833.95809,
        "transactions": [
          {
            "amount": 1,
            "recipient": "765bdb955f074dc79a71c76066914b2d",
            "sender": "0"
          }
        ]
      }
    ],
    "message": "Our chain is authoritative"
  }
  ```