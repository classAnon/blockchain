import time
from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE

GENESIS_DATA = {
     'timestamp': 1,
     'last_hash': 'genesis_last_hash',
     'hash': 'genesis_hash',
     'data': [],
     'difficulty': 3,
     'nonce': 'genesis_nonce'
}

class Block:
    """
    Block: a unit of storage.
    Store transactions in a block that supports a cryptocurrency.
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )
    '''
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialise the block into a dictionary of its attribute
        """
        return self.__dict__
    '''
    
    
    
    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on thr given last_block and data, until  block hash is found that 
        meets the leading 0's proof of work requirement.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hash[0:difficulty] != '0' * difficulty:
             nonce += 1
             timestamp = time.time_ns()
             difficulty = Block.adjust_difficulty(last_block, timestamp)
             hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)
    
    @staticmethod
    def genesis():
            """
            Generate the genesis block
            """
            #return Block(1, 'genesis_last_hash', 'genesis_hash', [])
            return Block(**GENESIS_DATA)  
    
    '''
    @staticmethod
    def from_json(block_json):
        """
        Deserialise a block's json representation back into a block instance.
        """
        return Block(**block_json)
    '''
    

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
         
         """
         Calculate the adjutsed difficulty according to the MINE_RATE.
         Increase the difficulty for quickly mined blocks.
         Decrease the difficulty for slowly mined blocks.
         """
         if (new_timestamp - last_block.timestamp) < MINE_RATE:
              return last_block.difficulty + 1
         
         if (last_block.difficulty - 1) > 0:
              return last_block.difficulty - 1
         
         return 1

def main():
    gensis_block = Block.genesis()
    block = Block.mine_block(gensis_block, 'foo')
    print(block)

if __name__=='__main__':
    main()