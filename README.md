one-time-test-suite
===================
This is one time verison of Ruralnet Test Suite

Usage:
===================
ruralnetOneTime.py --config

Do the Configuration for test suite

ruralnetOneTime.py --loc location_moretext_moretxt --provider provider


Tests:
===================
Throughput Test:
	- Uplink
	- Downlink
Latency Test:
	- RTT to gateway
	- RTT to linode
Traceroute Test:
	- #hops in Infra
	- #hops outside Infra
Ip spoofing Test:
	- Can Ip Spoofing be done in Network
Statefull Firewall:
	-Does the network has statefull firewall
ICSI Netalyzr test:
	- runs the ICSI Netlyzr tests http://netalyzr.icsi.berkeley.edu/index.html
Roaming Tests:
	- tests with a roaming sim
Page Load Time:
	- Tests the page loading time of websites from websites.txt or user specified file
CDN performance Test:
	- Test the improvement of CDN latencies over Origin Latencies.Considers 9 CDN services
Buffer Size Test:
	- Uplink and Downlink Buffer sizes
	- Drain Size: After filling the buffer the buffer drains in chunks of k packets, then Drainsize=k.
	- UDP throughput
Signal Strength:
	- logging of Signal Strength
