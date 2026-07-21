

Mine block by making GET request to http://localhost:5500/mine

Command: curl http://localhost:5500/mine
Result: Nothing happened.


Attempt 2:
Command: curl -v http://localhost:5500/mine
Command: curl -i http://localhost:5500/mine
Result: The server is mining indefinetely.


Changed proof from looking for a hash ending in 1234 to ending in 000.
    
Attempt 3:
Command: curl -i http://localhost:5500/mine
Result: The server is still mining indefinetely.

Changed proof from looking for a hash ending in 000 to ending in 0.
Debugged ```proof_of_work()``` and ```valid_proof()```.
Found that ```valid_proof()``` does not return true when a correct hash is found due to incorrect indicing.

Fixed indicing.

Attempt 4:
Command: curl -i http://localhost:5500/mine
Received: 
```
{"index":2,"message":"New Block Forged","previous_hash":"e0e90ef098543ad236e363c1fc6a97affdd7fd8a215d9256700e93ec6f5e8bef","proof":16,"transactions":[{"amount":1,"recipient":"b779c1ab52f2428f96b7cccd4458231c","sender":"0"}]}
```

Changed proof from looking for a hash ending in 0 back to looking for a hash ending in 1234.

Attempt 5:
Command: curl -i http://localhost:5500/mine
Received:
```
{"index":2,"message":"New Block Forged","previous_hash":"5f7150b78acdc94afc480d1ceda02f607def38855c755b4fd5fb4148942b6158","proof":57432,"transactions":[{"amount":1,"recipient":"9a1a61b33dad4eb0a2905a7a0a9439b1","sender":"0"}]}
```

Command: 
```
curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "d4ee26eee15148ee92c6cd394edd974e",
 "recipient": "someone-other-address",
 "amount": 5
}' "http://localhost:5500/transactions/new"
```
Received: ```{"message":"Transaction will be added to Block 3"}```


Command: curl -i http://localhost:5500/chain
Received:
```
{"chain":[{"index":1,"previous_hash":1,"proof":100,"timestamp":1784645067.9718442,"transactions":[]},{"index":2,"previous_hash":"5f7150b78acdc94afc480d1ceda02f607def38855c755b4fd5fb4148942b6158","proof":57432,"timestamp":1784645071.023669,"transactions":[{"amount":1,"recipient":"9a1a61b33dad4eb0a2905a7a0a9439b1","sender":"0"}]}],"length":2}
```

Command: curl -i http://localhost:5500/mine
Received:
```
{"index":3,"message":"New Block Forged","previous_hash":"0d46c3f000b9beaf3d6f4070152196d77b96f0d53200bd6d457c8a8cdc84c1cc","proof":114375,"transactions":[{"amount":5,"recipient":"someone-other-address","sender":"d4ee26eee15148ee92c6cd394edd974e"},{"amount":1,"recipient":"9a1a61b33dad4eb0a2905a7a0a9439b1","sender":"0"}]}
```

Command: curl -i http://localhost:5500/mine
Received:
```
{"index":4,"message":"New Block Forged","previous_hash":"7999bdf07ab00316b014f433d64bb523f194a4cdd322990d87e593ad85a0cc8e","proof":48982,"transactions":[{"amount":1,"recipient":"9a1a61b33dad4eb0a2905a7a0a9439b1","sender":"0"}]}
```

Command: curl -i http://localhost:5500/chain
Received:
```
{"chain":[{"index":1,"previous_hash":1,"proof":100,"timestamp":1784645067.9718442,"transactions":[]},{"index":2,"previous_hash":"5f7150b78acdc94afc480d1ceda02f607def38855c755b4fd5fb4148942b6158","proof":57432,"timestamp":1784645071.023669,"transactions":[{"amount":1,"recipient":"9a1a61b33dad4eb0a2905a7a0a9439b1","sender":"0"}]},{"index":3,"previous_hash":"0d46c3f000b9beaf3d6f4070152196d77b96f0d53200bd6d457c8a8cdc84c1cc","proof":114375,"timestamp":1784645267.217002,"transactions":[{"amount":5,"recipient":"someone-other-address","sender":"d4ee26eee15148ee92c6cd394edd974e"},{"amount":1,"recipient":"9a1a61b33dad4eb0a2905a7a0a9439b1","sender":"0"}]},{"index":4,"previous_hash":"7999bdf07ab00316b014f433d64bb523f194a4cdd322990d87e593ad85a0cc8e","proof":48982,"timestamp":1784645295.2191648,"transactions":[{"amount":1,"recipient":"9a1a61b33dad4eb0a2905a7a0a9439b1","sender":"0"}]}],"length":4}
```