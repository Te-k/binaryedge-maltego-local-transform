# Maltego Local Transform for BinaryEdge

## Transforms implemented

The following transforms have been implemented :

* `Get Subdomains` that returns subdomains of a domain
* `Get Domains` that returns domains hosted on an IP
* `Get IP Info` that returns anything interesting on an IP from the last scan
* `Get DNS Entries` that returns DNS information on a domain

## Installation

To install this package, you need to install canari and generate a mtz file :

```
pip install canari3 pybinaryedge
git clone https://github.com/Te-k/binaryedge-maltego-local-transform.git
cd binaryedge-maltego-local-transform/
canari create-profile
```

Then import the file `binaryedge.mtz` in your Maltego. You need to add your BinaryEdge API key to the canari configuration file `vim ~/.canari/binaryedge.conf`


