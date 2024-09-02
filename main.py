# Import in our libraries
import datetime as dt
import hashlib as hasher
import json
import os

# An array that will store our local JSON data, this is for verifying the blockchain
jarr = []
coins_amount = int(input("How many coins? "))
p=input("Set your password to whatever you want! ")

# Set the number of coins
def set_coins(n):
  coins_amount=n
  return coins_amount

def set_password(password):
  p=password
  return p

def read_blockchain():
  with open("blockchain.json", 'r', encoding='utf-8')as f:
    jsonarr=json.loads(f.read())
    return jsonarr

# Create the base block
class Block:

  def __init__(self, index: int, timestamp: dt.date, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()

  def hash_block(self):
    sha = hasher.sha256()
    new_index, new_timestamp, new_data, prev_hash = (str(
        self.index).encode(), str(self.timestamp).encode(), str(
            self.data).encode(), str(self.previous_hash).encode())
    sha.update(new_index + new_timestamp + new_data + prev_hash)
    return sha.hexdigest()


# Add attributes of the block to the array, which will then be added to the JSON file.
def update_blockchain(b: Block):
  with open("blockchain.json", 'w', encoding='utf-8') as feedjson:
    entry = {
        'index': b.index,
        'timestamp': b.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
        'data': b.data,
        'hash': b.hash,
        'previous_hash': b.previous_hash,
    }
    jarr.append(entry)
    json.dump(jarr, feedjson, indent=4)


# Simply create a new block, and add it to the blockchain.
def create_genesis_block():
  genesis_data={
    'to': None,
    'from': None,
    'amount': 0
  }
  return Block(
    0, 
    dt.datetime.now(), 
    genesis_data, 
    "0000"
  )


# Create a new block, and add it to the blockchain based on the previous one.
def create_next_block(last_block):
  new_index = last_block.index + 1
  new_timestamp = dt.datetime.now()
  new_data = {
    'to': input(f"Block {new_index}\nWho would you like to send this to? "),
    'from': str(input("Enter your password(a 2-digit number): ")),
    'amount': input("How much would you like to send? "),
  }
  if new_data['from'] != p:
    print("Not authorized user")
    print(new_data['from'], " is not", p)
    exit()
  new_hash = last_block.hash

  return Block(new_index, new_timestamp, new_data, new_hash)


# See if the blockchain is valid.
def verify_chain():
  with open("blockchain.json", 'r', encoding='utf-8') as feedjson:
    j = json.load(feedjson)
    for i in range(1, len(j)):
      block = j[i]
      B = Block(block['index'],
                dt.datetime.strptime(block['timestamp'], "%m/%d/%Y, %H:%M:%S"),
                block['data'], block['previous_hash'])
      prev_block = j[i - 1]
      PB = Block(
          prev_block['index'],
          dt.datetime.strptime(block['timestamp'], "%m/%d/%Y, %H:%M:%S"),
          block['data'],
          block['hash'],
      )
      if B.hash != B.hash_block():
        print("Invalid block hash")
        return False
      if block['previous_hash'] != prev_block['hash']:
        print("Invalid block hash becasue block prev_hash is not pb hash")
        return False
      PB = B

    print("The blockchain is valid!")
    return True

def mine_add_block():
  if len(jarr)>1:
    print(jarr[-1])

# Create a demonstration of the blockchain.
def demo():
  jsonarr=[]
  #Read jsonarr
  if os.path.getsize("blockchain.json")==0:
    pass
  else:
    jsonarr=read_blockchain()
  # Create a genesis block
  if len(jsonarr)>1:
    previous_block=Block(
      jsonarr[-1]['index'],
      dt.datetime.strptime(jsonarr[-1]['timestamp'], "%m/%d/%Y, %H:%M:%S"),
      jsonarr[-1]['data'],
      jsonarr[-1]['hash'],
    )
  else:
    previous_block = create_genesis_block()
  
  update_blockchain(previous_block)
  

  #How many transactions?
  blocks_to_make = int(input("How many transactions do you want to make? "))
  
  for _ in range(blocks_to_make):
    new_block = create_next_block(previous_block)
    update_blockchain(new_block)
    previous_block = new_block

    # Print out new block
    print(f"\nBlock #{new_block.index} has been added")
    print(f"Timestamp: {new_block.timestamp}")
    print(f"Data: {new_block.data}")
    print("Hash: " + new_block.hash)
    print("Previous Hash " + new_block.previous_hash)
    print("\n\n")

  print(f"{blocks_to_make} blocks have been added to the blockchain")
  verify_chain()
demo()
