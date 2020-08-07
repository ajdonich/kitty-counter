import argparse, time, os
from collections import deque, defaultdict
from web3 import Web3


class KittyCounter:
#{
    ABI_BIRTH_EVENT = [
        {"anonymous":False,
        "inputs":[{"indexed":False,"name":"owner","type":"address"},
                {"indexed":False,"name":"kittyId","type":"uint256"},
                {"indexed":False,"name":"matronId","type":"uint256"},
                {"indexed":False,"name":"sireId","type":"uint256"},
                {"indexed":False,"name":"genes","type":"uint256"}],
        "name":"Birth",
        "type":"event"}]

    ABI_GET_KITTY_FCN = [
        {"constant":True,
        "inputs":[{"name":"_id","type":"uint256"}],
        "name":"getKitty",
        "outputs":[{"name":"isGestating","type":"bool"},
                    {"name":"isReady","type":"bool"},
                    {"name":"cooldownIndex","type":"uint256"},
                    {"name":"nextActionAt","type":"uint256"},
                    {"name":"siringWithId","type":"uint256"},
                    {"name":"birthTime","type":"uint256"},
                    {"name":"matronId","type":"uint256"},
                    {"name":"sireId","type":"uint256"},
                    {"name":"generation","type":"uint256"},
                    {"name":"genes","type":"uint256"}],
        "payable":False,
        "stateMutability":"view",
        "type":"function"}]

    def __init__(self, start_blk, end_blk):
        self.start_blk = start_blk
        self.end_blk = end_blk

    def kitty_contract_handle(self, abi_fragment):
    #{  
        # Init websocket connection (w/unlimited max_size) (Infura stateless HTTP doesn't support filters)
        infura_proj_url = f"wss://mainnet.infura.io/ws/v3/{os.environ['WEB3_INFURA_PROJECT_ID']}"
        web3_handle = Web3(Web3.WebsocketProvider(infura_proj_url, websocket_kwargs={'max_size':None}))
        
        # Contract params
        cryptokitty_addr = "0x06012c8cf97BEaD5deAe237070F9587f8E7A266d"    
        return web3_handle.eth.contract(address=cryptokitty_addr, abi=abi_fragment)
    #}

    def count_kitties(self, contract_handle, qblock_queue, sirecnts, matroncnts):
    #{  
        # Execute event log queries
        while qblock_queue:
            start_blk, end_blk = qblock_queue[0]
            print(f"Querying range: [{start_blk}, {end_blk}] ({end_blk - start_blk + 1} blocks)")
            event_filter = contract_handle.events.Birth.createFilter(fromBlock=start_blk, toBlock=end_blk)
            
            # Raises ValueError if payload > 128MB
            for log in event_filter.get_all_entries():
                matroncnts[log['args']['matronId']] += 1
                sirecnts[log['args']['sireId']] += 1

            qblock_queue.popleft()
    #}

    # Iteratively subdivide query range for Infura payload overloads
    # Default qbatchsz=13135 gives empirically descent query success
    # Set qbatchsz=None to begin querying from the full block range 
    def kitty_count_batch(self, qbatchsz=13135):
    #{
        initial = time.time()

        # Kitty counters
        sirecnts = defaultdict(int)
        matroncnts = defaultdict(int)
        
        # Init contract and block ranges
        qblock_queue = deque()
        contract_handle = self.kitty_contract_handle(KittyCounter.ABI_BIRTH_EVENT)
        if qbatchsz is None: qblock_queue.append((self.start_blk, self.end_blk))
        else:
            for bi in range(self.start_blk, self.end_blk+1, qbatchsz):
                qblock_queue.append((bi, min(bi+qbatchsz-1, self.end_blk)))
        
        # Subdivide and conquer
        while qblock_queue:
        #{
            try: self.count_kitties(contract_handle, qblock_queue, sirecnts, matroncnts)
            except ValueError as verror:
            #{        
                # Assert this ValueError is a payload too big error
                if verror.args[0]['code'] != -32005: raise verror
                print(f"  {verror.args[0]['message']} : subdividing range...")
                
                sblk, eblk = qblock_queue.popleft()
                midblk = (eblk - sblk)//2
                qblock_queue.appendleft((sblk+midblk, eblk))
                qblock_queue.appendleft((sblk, sblk+midblk-1))
            #}  
        #}
        
        print((f"Completed kitty count ({self.end_blk - self.start_blk + 1} "
               f"blocks) in {time.time()-initial:.3f} sec\n"))
            
        return sirecnts, matroncnts
    #}

    def get_max_matron(self):
    #{
        print(f"Beginning kitty count for block range: [{self.start_blk}, {self.end_blk}]")
        sirecnts, matroncnts = self.kitty_count_batch()
        
        print(f'Total kitties born in range: {len(sirecnts) + len(matroncnts)}')
        print(f'Number of gen0 matrons born/inserted: {matroncnts[0]}'); del matroncnts[0]
        print(f'Number of gen0 sires born/inserted: {sirecnts[0]}'); del sirecnts[0]

        total = len(sirecnts) + len(matroncnts)
        if total == 0: return None, None, None, None, None
        maxmatron = max(matroncnts.items(), key=lambda tup: tup[1])
        maxsire = max(sirecnts.items(), key=lambda tup: tup[1])

        print(f"\nMax maternal birther matronId: {maxmatron[0]} with {maxmatron[1]} kittens")
        print(f"Max paternal birther sireId: {maxsire[0]} with {maxsire[1]} kittens")
        print("\nAvg births/matron:", sum(matroncnts.values())/len(matroncnts))
        print("Avg births/sire:", sum(sirecnts.values())/len(sirecnts))
        
        contract_handle = self.kitty_contract_handle(KittyCounter.ABI_GET_KITTY_FCN)
        kitty = contract_handle.functions.getKitty(maxmatron[0]).call()
        birth_time, generation, genes = kitty[5], kitty[8], kitty[9]

        print((f"\nMax maternal birther matronId: {maxmatron[0]}\n"
            f"  born at birth time: {birth_time}\n"
            f"  in generation: {generation}\n"
            f"  with genes: {genes}\n"))
        
        return maxmatron[0], maxmatron[1], birth_time, generation, genes
    #}
#}

if __name__ == "__main__":
#{
    if 'WEB3_INFURA_PROJECT_ID' not in os.environ:
        print("ERROR: env variable 'WEB3_INFURA_PROJECT_ID' is not set:")
        print("  Please assure you have a valid Infura Mainnet project.")
        print("  You can create one here: https://infura.io/register")
        print("  Then set WEB3_INFURA_PROJECT_ID to your project_id\n")
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('start_blk')
    parser.add_argument('end_blk')
    args = parser.parse_args()
    
    kcounter = KittyCounter(int(args.start_blk), int(args.end_blk))
    matron_id, nbirths, birth_time, generation, genes = kcounter.get_max_matron()
    if matron_id is not None: print(matron_id, nbirths, birth_time, generation, genes)
#}
