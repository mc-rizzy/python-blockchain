# Blockchain API Test Log

**Base URL:** `http://localhost:5500`  
**Target Goal:** Verify `/mine`, `/transactions/new`, and `/chain` endpoints and resolve infinite loop in Proof of Work.

---

## Executive Summary

| Test Phase | Endpoint / Action | Status | Notes |
| :--- | :--- | :--- | :--- |
| **Initial Mining** | `GET /mine` | Failed | Infinite loop due to indexing bug |
| **Bug Fix** | `valid_proof()` logic | Fixed | Corrected string slice indexing |
| **Mining Test** | `GET /mine` | Passed | Successfully forged Block 2 (`proof: 57432`) |
| **New Transaction** | `POST /transactions/new` | Passed | Queued 5 coins to `someone-other-address` |
| **Block Inclusion** | `GET /mine` | Passed | Mined Block 3 containing posted transaction |
| **Chain Verification**| `GET /chain` | Passed | Confirmed linear history across 4 blocks |

---

## Root Cause Analysis & Resolution

During initial test runs on the `/mine` endpoint, requests hung indefinitely without returning a response.

* **Symptom:** The server process entered an infinite loop during `proof_of_work()`.
* **Investigation Steps:**
  1. Reduced difficulty target from trailing `1234` down to `000`, and finally `0`.
  2. Inspected `valid_proof()` function execution with debug print statements.
* **Root Cause:** An incorrect indexing slice inside `valid_proof()` prevented valid hashes from evaluating to `True`. Because the success condition was unreachable, the mining loop continued infinitely.
* **Fix Applied:** Corrected hash indexing logic in `valid_proof()`. Reverted difficulty target back to `1234`.

---

## Test Execution Timeline

#### Attempt 1
* **Command:**
  ```bash
  curl http://localhost:5500/mine
  ```
* **Result:**
  Command hung indefinitely. No HTTP headers or response body returned.

#### Attempt 2
* **Commands:**
  ```bash
  curl -v http://localhost:5500/mine
  curl -i http://localhost:5500/mine
  ```
* **Result:**
  Request timed out / process remained stuck in `proof_of_work()`.

#### Attempt 3
* **Action:** Lowered hash target from 1234 to 000.
* **Commands:**
  ```bash
  curl -i http://localhost:5500/mine
  ```
* **Result:**
  Still hung. Debugged `proof_of_work()` and `valid_proof()`. Identified and patched indexing error.

#### Attempt 4 (Validation with Target 0)
* **Action:** Lowered hash target from 000 to 0.
* **Commands:**
  ```bash
  curl -i http://localhost:5500/mine
  ```
* **Result:**
  Success (HTTP/1.1 200 OK).
* **Response:**
```bash
{
  "index": 2,
  "message": "New Block Forged",
  "previous_hash": "e0e90ef098543ad236e363c1fc6a97affdd7fd8a215d9256700e93ec6f5e8bef",
  "proof": 16,
  "transactions": [
    {
      "amount": 1,
      "recipient": "b779c1ab52f2428f96b7cccd4458231c",
      "sender": "0"
    }
  ]
}
```

#### Attempt 5 (Validation with Target 0)
* **Action:** Restored hash target from 0 to 1234.
* **Commands:**
  ```bash
  curl -i http://localhost:5500/mine
  ```
* **Response:**
```bash
{
  "index": 2,
  "message": "New Block Forged",
  "previous_hash": "5f7150b78acdc94afc480d1ceda02f607def38855c755b4fd5fb4148942b6158",
  "proof": 57432,
  "transactions": [
    {
      "amount": 1,
      "recipient": "9a1a61b33dad4eb0a2905a7a0a9439b1",
      "sender": "0"
    }
  ]
}
```


* **Commands:**
  ```bash
    curl -X POST -H "Content-Type: application/json" -d '{
    "sender": "d4ee26eee15148ee92c6cd394edd974e",
    "recipient": "someone-other-address",
    "amount": 5
    }' "http://localhost:5500/transactions/new"
  ```
* **Message:**
```bash
{"message":"Transaction will be added to Block 3"}
```
* **Response:**
```bash
{
  "index": 2,
  "message": "New Block Forged",
  "previous_hash": "5f7150b78acdc94afc480d1ceda02f607def38855c755b4fd5fb4148942b6158",
  "proof": 57432,
  "transactions": [
    {
      "amount": 1,
      "recipient": "9a1a61b33dad4eb0a2905a7a0a9439b1",
      "sender": "0"
    }
  ]
}
```


* **Commands:**
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
      "timestamp": 1784645067.9718442,
      "transactions": []
    },
    {
      "index": 2,
      "previous_hash": "5f7150b78acdc94afc480d1ceda02f607def38855c755b4fd5fb4148942b6158",
      "proof": 57432,
      "timestamp": 1784645071.023669,
      "transactions": [
        {
          "amount": 1,
          "recipient": "9a1a61b33dad4eb0a2905a7a0a9439b1",
          "sender": "0"
        }
      ]
    }
  ],
  "length": 2
}
```


* **Commands:**
  ```bash
    curl -i http://localhost:5500/mine
  ```
* **Response:**
```bash
{
  "index": 3,
  "message": "New Block Forged",
  "previous_hash": "0d46c3f000b9beaf3d6f4070152196d77b96f0d53200bd6d457c8a8cdc84c1cc",
  "proof": 114375,
  "transactions": [
    {
      "amount": 5,
      "recipient": "someone-other-address",
      "sender": "d4ee26eee15148ee92c6cd394edd974e"
    },
    {
      "amount": 1,
      "recipient": "9a1a61b33dad4eb0a2905a7a0a9439b1",
      "sender": "0"
    }
  ]
}
```


* **Commands:**
  ```bash
    curl -i http://localhost:5500/mine
  ```
* **Response:**
```bash
{
  "index": 4,
  "message": "New Block Forged",
  "previous_hash": "7999bdf07ab00316b014f433d64bb523f194a4cdd322990d87e593ad85a0cc8e",
  "proof": 48982,
  "transactions": [
    {
      "amount": 1,
      "recipient": "9a1a61b33dad4eb0a2905a7a0a9439b1",
      "sender": "0"
    }
  ]
}
```


* **Commands:**
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
      "timestamp": 1784645067.9718442,
      "transactions": []
    },
    {
      "index": 2,
      "previous_hash": "5f7150b78acdc94afc480d1ceda02f607def38855c755b4fd5fb4148942b6158",
      "proof": 57432,
      "timestamp": 1784645071.023669,
      "transactions": [
        {
          "amount": 1,
          "recipient": "9a1a61b33dad4eb0a2905a7a0a9439b1",
          "sender": "0"
        }
      ]
    },
    {
      "index": 3,
      "previous_hash": "0d46c3f000b9beaf3d6f4070152196d77b96f0d53200bd6d457c8a8cdc84c1cc",
      "proof": 114375,
      "timestamp": 1784645267.217002,
      "transactions": [
        {
          "amount": 5,
          "recipient": "someone-other-address",
          "sender": "d4ee26eee15148ee92c6cd394edd974e"
        },
        {
          "amount": 1,
          "recipient": "9a1a61b33dad4eb0a2905a7a0a9439b1",
          "sender": "0"
        }
      ]
    },
    {
      "index": 4,
      "previous_hash": "7999bdf07ab00316b014f433d64bb523f194a4cdd322990d87e593ad85a0cc8e",
      "proof": 48982,
      "timestamp": 1784645295.2191648,
      "transactions": [
        {
          "amount": 1,
          "recipient": "9a1a61b33dad4eb0a2905a7a0a9439b1",
          "sender": "0"
        }
      ]
    }
  ],
  "length": 4
}
```