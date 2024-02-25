# Decoupled Blockchain
This is an open-sourced Python-based blockchain.
<br>
<br>
Note, this code is untested and very much unfinished. The purpose is
to demonstrate a blockchain built in Python for my [Meetup group](https://www.meetup.com/florida-python-ninjas/).

### Why the Name Decoupled?
This blockchain will be decoupled from
the fiat system. More on this to come...

------------------

### How to Run
#### Install Requirements
    pip install -r requirements.txt

#### Create Flat Database Files
    touch master_node/block_db.json master_node/state_db.json

#### Run Blockchain Server
    python master_node/blockchain_server.py

------------------

### References
While working on this, I read upon previous Python-based blockchain tutorials
to gain an understanding of the fundamentals.
* https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/
* https://www.geeksforgeeks.org/create-simple-blockchain-using-python/