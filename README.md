# Decoupled Blockchain
This is an open-sourced Python-based blockchain.
<br>
<br>
Note, this code is untested and very much unfinished. The purpose is
to demonstrate a blockchain built in Python for my [Meetup group](https://www.meetup.com/florida-python-ninjas/).

In the future, I will probably make a closed-source version of this
code which is maintained and more feature-complete.

### Why the Name Decoupled?
The closed-source version will be a blockchain that is decoupled from
the fiat system. More on this to come...

### How to Run
#### Install Requirements
    pip install -r requirements.txt

#### Create Flat Database Files
    touch master_node/block_db.json master_node/state_db.json

#### Run Blockchain Server
    python master_node/main.py
