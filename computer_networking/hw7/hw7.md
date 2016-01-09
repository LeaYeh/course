## Hands-On Exercises
6) Assume you are an ISP and plan to provide a bandwidth management service for
your business customers on their access links. One of your customers hopes to 
reserve 50% of the downlink bandwidth for the R&D group. Set up a QoS-aware 
ISP-side edge gateway to meet the goal. The classifier in the gateway should 
classify inbound packets into two classes. The first class is for packets sent to the 
PCs in the R&D group, while the other class is for other packets. You can 
demonstrate that the service is workable by showing that the quality of watching 
an online streaming at a PC in the R&D group is total unaffected by the 
overloaded download traffic to the PCs in the other groups.  

**[ans]**  
```sh
tc qdisc add dev PC root handle 10:0 cbq bandwidth 5Mbit
tc qdisc add dev RD root handle 10:0 cbq bandwidth 5Mbit
```
qdisc: queure rule  
cbq: bit unit  
htb: byte unit, and more effective  


## Written Exercises
4) There is a 10^7 bits/sec link and WRR is used to schedule. Suppose that the link is 
shared by N flows which packet sizes are 125 bytes. Assume we plan to equally 
allocate 8x10^6 bits/sec bandwidth for half number of flows and the residual 
bandwidth for other half. Then, if N-1 flows are backlogged, what is the possible 
worst delay suffered by the first packet of the only non-active flow.  

**[ans]**  
> In WRR, the flows with high bandwidth allocation can send 4 packets in one round 
while the other flow can send one packet.  
> in the worst case, when the first packet arrives, the server may just begin to 
serve the first flow.  
> ((N/2)x4 + (N/2-1)) = 5N/2 - 1  
> transmission time of each packet,  
> 10^7 (bits/sec) / 125x8 (bits/packet) = 10^4 (packets/sec) = 10^-4 (sec/packet)  
> delay time = (5N/2 - 1) x 10^-4 sec

-----

13) Figure 7.17 illustrates how a token bucket is operated. Assume that r = 1 unit/s, p
= 4 units/s, b = 20 units and no packet arrivals for the first 15 seconds. Then, 
suppose that 4 packets arrive right at the 15th second, with length equal to 2, 2, 
10, and 4 units, respectively. Take the assumption described above and calculate 
the releasing time of the 4 packets.  

**[ans]**  
> 15 token will be accumulated in first 15 sec  
> assume first packet arrive in 15th sec, it will release at 15.5th sec  
> second packet will release at 16th sec  
> third packet will release at 18.5th sec  
> final packet will release at 19.5th sec
