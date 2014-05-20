one-time-test-suite
===================
This is one time verison of Ruralnet Test Suite

Usage:
===================
usage: sudo python ruralnetOneTime.py [-h] [-t] [-l] [-T] [-i] [-s] [-n] [-r [R [R ...]]]
                          [-p] [-c] [-b] -L L [L ...] -P P [P ...] -C C
                          [C ...] [-re RE [RE ...]]

process ruralnetOneTime arguments

optional arguments:
  -h, --help       show this help message and exit
  -t               Run Throughput Test
  -l               Run Latency Test
  -T               Run Traceroute Test
  -i               Run Ip spoofing Test
  -s               Run Statefull Firewall Test
  -n               Run ICSI Netalyzr Test
  -r [R [R ...]]   Run Roaming Test
  -p               Run Page Load Time Test
  -c               Run CDN performance Test
  -b               Run Buffer Size Test
  -L L [L ...]     Locaton of Test being conducted
  -P P [P ...]     Provider of Test being conducted
  -C C [C ...]     Connection type of Test being conducted umts/edge/evdo
  -re RE [RE ...]  Resume the tests that did not complete due to
                   disconnections


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

