#!/usr/bin/env python3

# /* +-----------------------------------------------------------+ */
# /* | Ergo Mainnet P2S Address to Testnet P2S Address Converter | */
# /* |                      p2s2testnet.py                       | */
# /* |                (c)copyright nitram147 2021                | */
# /* +-----------------------------------------------------------+ */

import sys
import base58
import hashlib

mainnet_prefix = 0x00
testnet_prefix = 0x10
p2s_address_type = 0x03

checksum_length = 4

def print_usage(binary_name):
	print("python ./" + binary_name + " [address]")
	print("\tWhere [address] is mainnet P2S adress such as 4MQyML64GnzMxZgm")

if len(sys.argv) != 2:
	print_usage(sys.argv[0])
	sys.exit(1)

input = sys.argv[1]

#decode base58 address representation into bytearray
input_decoded = bytearray(base58.b58decode(input))

if input_decoded[0] != (mainnet_prefix + p2s_address_type):
	print("Input should be Mainnet P2S address")
	sys.exit(1)

#change prefix from mainnet to testnet
input_decoded[0] -= mainnet_prefix
input_decoded[0] += testnet_prefix

prefix_and_content_bytes = input_decoded[0:-checksum_length]

#recalculate checksum from prefix + content bytes
blake2b256 = hashlib.blake2b(digest_size=32)
blake2b256.update(prefix_and_content_bytes)
checksum = bytearray(blake2b256.digest())[0:checksum_length]

#replace checksum with new one
input_len = len(input_decoded)
for i in range(0, len(checksum)):
	input_decoded[ input_len - checksum_length + i] = checksum[i]

#encode back to base58
output = base58.b58encode(input_decoded)

#print result
print(output.decode("utf-8"))

sys.exit(0)
