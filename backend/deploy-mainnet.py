import json
import os
import subprocess
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
RPC = 'https://ethereum.publicnode.com'
EXPECTED_OWNER = '0x806918b917a89956b8af1a2897940c475973e2d3'
RESULT = ROOT / 'deployment-mainnet.json'


def rpc(method, params):
    response = requests.post(RPC, json={'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}, timeout=30)
    response.raise_for_status()
    data = response.json()
    if 'error' in data:
        raise RuntimeError(data['error']['message'])
    return data['result']


def main():
    if RESULT.exists():
        raise RuntimeError('Deployment record exists; inspect it before sending another transaction')
    artifact = json.loads((ROOT / 'build/deployment-artifact.json').read_text(encoding='utf-8'))
    bytecode = '0x' + artifact['contract']['evm']['bytecode']['object']
    assert int(rpc('eth_chainId', []), 16) == 1
    balance = int(rpc('eth_getBalance', [EXPECTED_OWNER, 'latest']), 16)
    nonce = int(rpc('eth_getTransactionCount', [EXPECTED_OWNER, 'pending']), 16)
    gas = int(rpc('eth_estimateGas', [{'from': EXPECTED_OWNER, 'data': bytecode, 'value': '0x0'}]), 16)
    gas_limit = gas * 120 // 100
    gas_price = int(rpc('eth_gasPrice', []), 16) * 125 // 100
    maximum_cost = gas_limit * gas_price
    print(json.dumps({'owner': EXPECTED_OWNER, 'balanceETH': balance / 10**18, 'estimatedGas': gas, 'maximumCostETH': maximum_cost / 10**18}), flush=True)
    if maximum_cost > balance or maximum_cost > 100_000_000_000_000:
        raise RuntimeError('Deployment cost exceeds balance or 0.0001 ETH cap')
    tx = {'chainId': 1, 'nonce': nonce, 'gasLimit': gas_limit, 'gasPrice': str(gas_price), 'data': bytecode, 'value': 0}
    signer = "const {ethers}=require('../frontend/node_modules/ethers');let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',async()=>{try{const w=new ethers.Wallet(process.env.DIARY_DEPLOY_KEY);if(w.address.toLowerCase()!==process.env.DIARY_EXPECTED_OWNER)process.exit(2);process.stdout.write(await w.signTransaction(JSON.parse(s)));}catch{process.stderr.write('Signing failed');process.exit(1)}});"
    env = dict(os.environ, DIARY_EXPECTED_OWNER=EXPECTED_OWNER)
    signed = subprocess.run(['node', '-e', signer], input=json.dumps(tx), text=True, capture_output=True, cwd=ROOT, env=env, check=True).stdout
    tx_hash = rpc('eth_sendRawTransaction', [signed])
    result = {'chainId': 1, 'owner': EXPECTED_OWNER, 'transactionHash': tx_hash, 'compiler': artifact['compiler'], 'status': 'pending'}
    RESULT.write_text(json.dumps(result, indent=2) + '\n')
    print('Transaction submitted:', tx_hash, flush=True)
    for _ in range(60):
        receipt = rpc('eth_getTransactionReceipt', [tx_hash])
        if receipt:
            if int(receipt['status'], 16) != 1:
                raise RuntimeError('Deployment transaction reverted')
            result.update(status='confirmed', contractAddress=receipt['contractAddress'], blockNumber=int(receipt['blockNumber'], 16), gasUsed=int(receipt['gasUsed'], 16))
            RESULT.write_text(json.dumps(result, indent=2) + '\n')
            assert rpc('eth_getCode', [result['contractAddress'], 'latest']) == '0x' + artifact['contract']['evm']['deployedBytecode']['object']
            assert rpc('eth_call', [{'to': result['contractAddress'], 'data': '0x8da5cb5b'}, 'latest'])[-40:].lower() == EXPECTED_OWNER[2:]
            print(json.dumps(result), flush=True)
            return
        time.sleep(5)
    raise RuntimeError('Transaction still pending; inspect recorded hash without redeploying')


if __name__ == '__main__':
    main()

