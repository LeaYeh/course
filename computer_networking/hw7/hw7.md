## Hands-On Exercises
6. Assume you are an ISP and plan to provide a bandwidth management service for
your business customers on their access links. One of your customers hopes to 
reserve 50% of the downlink bandwidth for the R&D group. Set up a QoS-aware 
ISP-side edge gateway to meet the goal. The classifier in the gateway should 
classify inbound packets into two classes. The first class is for packets sent to the 
PCs in the R&D group, while the other class is for other packets. You can 
demonstrate that the service is workable by showing that the quality of watching 
an online streaming at a PC in the R&D group is total unaffected by the 
overloaded download traffic to the PCs in the other groups.  


## Written Exercises
4. There is a 107 bits/sec link and WRR is used to schedule. Suppose that the link is 
shared by N flows which packet sizes are 125 bytes. Assume we plan to equally 
allocate 8x10^6 bits/sec bandwidth for half number of flows and the residual 
bandwidth for other half. Then, if N-1 flows are backlogged, what is the possible 
worst delay suffered by the first packet of the only non-active flow.  

-----

13. Figure 7.17 illustrates how a token bucket is operated. Assume that r = 1 unit/s, p
= 4 units/s, b = 20 units and no packet arrivals for the first 15 seconds. Then, 
suppose that 4 packets arrive right at the 15th second, with length equal to 2, 2, 
10, and 4 units, respectively. Take the assumption described above and calculate 
the releasing time of the 4 packets.  

