### Project stages

We understand that there's a steep lerning curve for most of the folk working
on this project, and that's OK. This is an inflection point for the Dogecoin 
community: moving from a tiny dev team to a wider #dogeDevArmy is great for 
derisking the bus-factor aspect of Dogecoin. The process of creating libdogecoin 
is an important step toward a broader and more sustainable community of devs.

With that in mind we're suggesting a staged approach to this project. Starting
with the basics and delivering working vertical slices of functionality 
as a useful C library with a handfull of higher level language wrappers early,
should force us to solve fundamental concerns such as language wrappers, testing
and other issues before getting too far down a rabbit hole.

![Stage 1 Diagram](/doc/diagrams/libdogecoin-stage1.png)

Stage one lets us learn and understand the lowest level building blocks of Dogecoin
as we build each slice of functionality and deliver incremental releases with full
tests, doc and perhaps even commandline utilities that exercise them. We expect 
that this approach will gain momentum after the first and second 'slice' as we face
and solve the problems of library design, building effective language wrappers etc.


![Stage 2 Diagram](/doc/diagrams/libdogecoin-stage2.png)

Stage two makes use of the low level building blocks we've delivered by combinging
them into higher level components that are needed to build wallets and nodes. This
is where we deliver the parts needed for other members of the community to cobble 
together operational doge projects.


![Stage 3a Diagram](/doc/diagrams/libdogecoin-stage3.png)

Stage three A takes what we've built and uses it to create a new Dogecoin Node 
service (in C) capable of joining the network and participating in the blockchain. 
The plan is to make this new DogeNode available for Windows, Linux, MacOS etc. in 
a simple-to-setup manner that will encourage new users to support the network.

This DogeNode should be far simpler to maintain, being abstracted from the many
'and the kitchen sink' additions that encumber the Dogecoin Core daemon.

![Stage 3b Diagram](/doc/diagrams/libdogecoin-stage3b.png)

At the same time, GigaWallet which is being built around the Dogecoin Core APIs
can be easily ported to libdogecoin so it can operate directly on L1 to transact
dogecoin. This will be the first major project using libdogecoin via a language
binding, and prove the ability for libdogecoin to enable greater flexibility in
how the community can get involved in development.

### Current features
----------------
* Generating and storing private and public keys
* ECDSA secp256k1 signing and verification (through [libsecp256k1](https://github.com/bitcoin-core/secp256k1) included as git subtree)
* Generate recoverable signatures (and recover pubkey from signatures)
* BIP32 hierarchical deterministic key derivation
* Transaction generation, manipulation, signing and ser-/deserialization including P2PKH, P2SH, multisig
* Address generation
* Base58check encoding
* Native implementation of SHA256, SHA512, SHA512_HMAC, RIPEMD-160 including NIST testvectors
* Native constant time AES (+256CBC) cipher implementation including NIST testvectors
* Keystore (wallet) databases (through logdb https://github.com/liblogdb/liblogdb)
* Event based dogecoin P2P client capable of connecting to multiple nodes in a single thread (requires [libevent](https://github.com/libevent/libevent))
