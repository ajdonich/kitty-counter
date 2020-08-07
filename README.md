## Project: kitty-counter

[CryptoKitties](https://www.cryptokitties.co/catalogue) is an Ethereum blockchain game; here is its [Smart Contract](https://etherscan.io/address/0x06012c8cf97bead5deae237070f9587f8e7a266d#code), which also provides its ABIs. This [kittycounter.py](https://github.com/ajdonich/kitty-counter/blob/master/kittycounter.py) Python script interacts with the this smart contract through the [Infura API](https://infura.io/).

The script takes commandline args **start_blk** and **end_blk**, and it counts all kittens born within that block range (it does this by querying for Birth Events in the Ethereum logs). The script prints this and a few other data metrics, as well as some stats on the maternal/matron kitty who gave birth to the most kittens in that range (which it finds using the getKitty Function provided by the contract).

___

### Installation:

Running the script requires a valid **mainnet** Infura project (which you can create from here: https://infura.io/register), and for the **WEB3_INFURA_PROJECT_ID** environment variable to be set to that project_id. The only dependancy is [web3py](https://web3py.readthedocs.io/en/stable/) which may be installed with the miniconda [kitty-counter.yml](https://github.com/ajdonich/kitty-counter/blob/master/kitty-counter.yml) env file or with the pip [requirements.txt](https://github.com/ajdonich/kitty-counter/blob/master/requirements.txt) file. Miniconda can be downloaded and installed here: [Miniconda Installation Instructions](https://docs.conda.io/en/latest/miniconda.html), then from a terminal execute:

```
$ git clone https://github.com/ajdonich/kitty-counter.git
$ cd kitty-counter
$ conda env create -f kitty-counter.yml
```

___


### Execution:

Example execution with corresponding output using block range 6607985 to 7028323:  
Note: gen0 kitties were "inserted" by CryptoKitties admin, they have no official matron/sire parents

```
$ python3 kittycounter.py 6607985 7028323
Beginning kitty count for block range: [6607985, 7028323]
Querying range: [6607985, 6621119] (13135 blocks)
Querying range: [6621120, 6634254] (13135 blocks)
Querying range: [6634255, 6647389] (13135 blocks)
Querying range: [6647390, 6660524] (13135 blocks)
Querying range: [6660525, 6673659] (13135 blocks)
Querying range: [6673660, 6686794] (13135 blocks)
Querying range: [6686795, 6699929] (13135 blocks)
Querying range: [6699930, 6713064] (13135 blocks)
  query returned more than 10000 results : subdividing range...
Querying range: [6699930, 6706496] (6567 blocks)
Querying range: [6706497, 6713064] (6568 blocks)
Querying range: [6713065, 6726199] (13135 blocks)
Querying range: [6726200, 6739334] (13135 blocks)
Querying range: [6739335, 6752469] (13135 blocks)
Querying range: [6752470, 6765604] (13135 blocks)
Querying range: [6765605, 6778739] (13135 blocks)
Querying range: [6778740, 6791874] (13135 blocks)
Querying range: [6791875, 6805009] (13135 blocks)
Querying range: [6805010, 6818144] (13135 blocks)
  query returned more than 10000 results : subdividing range...
Querying range: [6805010, 6811576] (6567 blocks)
Querying range: [6811577, 6818144] (6568 blocks)
Querying range: [6818145, 6831279] (13135 blocks)
  query returned more than 10000 results : subdividing range...
Querying range: [6818145, 6824711] (6567 blocks)
Querying range: [6824712, 6831279] (6568 blocks)
Querying range: [6831280, 6844414] (13135 blocks)
Querying range: [6844415, 6857549] (13135 blocks)
Querying range: [6857550, 6870684] (13135 blocks)
Querying range: [6870685, 6883819] (13135 blocks)
Querying range: [6883820, 6896954] (13135 blocks)
Querying range: [6896955, 6910089] (13135 blocks)
Querying range: [6910090, 6923224] (13135 blocks)
Querying range: [6923225, 6936359] (13135 blocks)
Querying range: [6936360, 6949494] (13135 blocks)
Querying range: [6949495, 6962629] (13135 blocks)
Querying range: [6962630, 6975764] (13135 blocks)
Querying range: [6975765, 6988899] (13135 blocks)
Querying range: [6988900, 7002034] (13135 blocks)
Querying range: [7002035, 7015169] (13135 blocks)
Querying range: [7015170, 7028304] (13135 blocks)
Querying range: [7028305, 7028323] (19 blocks)
Completed kitty count (420339 blocks) in 218.373 sec

Total kitties born in range: 131344
Number of gen0 matrons born/inserted: 3099
Number of gen0 sires born/inserted: 3099

Max maternal birther matronId: 1083637 with 22 kittens
Max paternal birther sireId: 1083433 with 22 kittens

Avg births/matron: 2.659807558543937
Avg births/sire: 2.944588827926974

Max maternal birther matronId: 1083637
  born at birth time: 1539134711
  in generation: 0
  with genes: 467882257905024579446667743955452078189962217938379332103542434935342116

1083637 22 1539134711 0 467882257905024579446667743955452078189962217938379332103542434935342116

```