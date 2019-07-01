import bitcoin
import requests
import ast
from fractions import gcd
import random
import time


blockcypher_tr = 'https://api.blockcypher.com/v1/btc/main/txs/'
blockcypher_blocks = 'https://api.blockcypher.com/v1/btc/main/blocks/'
blockcypher_addr = 'https://api.blockcypher.com/v1/btc/main/addrs/'
scripttype_str = '"script_type": "null-data"'
datahex_str = '"data_hex"'
datastring_str = '"data_string"'
blockhash_str = '"block_hash"'


#
# VDF
#

x = 645789320567980453421435467548039214534796082
mod = 2**256 - 351 * 2**32 + 1
n = 1000

#
# WE SHOULD AGREE ON A k_vec
#

k_vec = [479625, 287888, 504535, 569984, 11640, 117590, 194157, 403260, 651355, 363798, 357841, 804185, 651119, 36290, 240296, 960156, 562663, 510041, 544004, 848436]


def VDFback(input, vec):
    out = input
    time0 = time.time()
    for i in range(n):
        out = (pow(out,3,mod) + vec[i % len(vec)])%mod
    #    print(time.time() - time0)
    return out

exponent =  (2*mod-1)/3

def VDFfor(input, vec):
    out = input
    time0 = time.time()
    for i in range(n):
        out = pow(out - vec[- (i % len(vec))-1],exponent,mod)
    #   print(time.time() - time0)
    return out



def search_for_transaction(tr):
    r = requests.get(blockcypher_tr+tr)
    rjson = r.json()
    sec = rjson["outputs"]
    number_outputs = len(sec)
    for i in range(number_outputs):
        a = dict(sec[i])
        #    print a["script_type"]
        if a["script_type"] == "null-data":
            #           print "DATA STRING:", a["data_string"]
            TXID = tr
            #         print "TXID", TXID
            BLOCK = rjson["block_hash"]
            #          print "BLOCK HASH", BLOCK
            return int(TXID+BLOCK, 16)
    return 0


def search_for_address(addr):
    cand = []
    r = requests.get(blockcypher_addr+addr)
    rjson = r.json()
    sec = rjson["txrefs"]
    for i in range(len(sec)):
        a = dict(sec[i])
        aux = a["tx_hash"]
        if search_for_transaction(aux) > 0:
            cand.append(search_for_transaction(aux))
    #    print a["tx_hash"]
    return cand




SEARCH_TYPE = 2


#
# SEARCH BY TRANSACTION ID
#
if SEARCH_TYPE == 1:
    tr = '142e03e3000348a883bb30d8f67a4c70783d9b7dedc337c328e40156a61dee72'
    result = search_for_transaction(tr)
    if result==0:
        print 'no data found'
    else:
        print 'calculating VDF:'
    print 'res', result





#
# SEARCH BY ADDRESS
#

if SEARCH_TYPE == 2:
    addr = '15ATtUdMik5gvYK2e2Dkc1DoBGLDHHbzAC'
    result = search_for_address('15ATtUdMik5gvYK2e2Dkc1DoBGLDHHbzAC')[0]
    





y  = VDFfor(result, k_vec)
#print y
#print VDFback(y, k_vec)-Random_input%mod


seed = str(y)[:15]
jumpahead = str(y)[15:]
print "SEED:", seed
print "JUMPAHEAD:", jumpahead

