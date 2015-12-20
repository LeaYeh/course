## Hands-On Exercises ##
(1) NS-2 is the most popular simulator for TCP research. It includes a package 
called NAM that can visually replay the whole simulation at all timescales. Many 
websites that introduce ns-2 can be found at [13]. Use NAM to observe a TCP running 
from a source to its destination, with and without buffer overflow at one intermediate 
router.  

-----

(4) Linux Packet Socket is a useful tool when you want to generate arbitrary types 
of packets. Find and modify an example program to generate a packet and sniff the 
packet with the same program.  

-----

(8) What transport protocols are used in MS Media Player or RealMedia? Please 
use Wireshark to observe and find out the answer.  


## Written Exercises ##

(4) Consider that a mobile TCP receiver is receiving data from its TCP sender, 
what will the smoothed RTT and the RTO evolve when the receiver gets farer and 
then nearer? Assume the moving speed is very fast such that the propagation delay 
ranges from 100 ms to 300 ms within 1 second.  

**[ans]**  

```
R': a new RTT
SRRT: smoothed round-trip time
RTTVAR: round-trip time variation
alpha = 0.125
beta = 0.25

RTTVAR <- (1 - beta) * RTTVAR + beta * |SRTT - R'|
SRTT <- (1 - alpha) * SRTT + alpha * R'
RTO <- SRTT + max (G, K*RTTVAR)
```
> The difference(RTTVAR) between SRTT and R' will increase,  
> so RTO will increase too

-----
(6) Given that the throughput of a TCP connection is inversely proportional to 
its RTT, connections with heterogeneous RTTs sharing the **same queue will get 
different bandwidth** shares. What will be the eventual proportion of the bandwidth 
sharing among three connections if their propagation delays are 10 ms, 100 ms, 
150 ms, and the service rate of the shared queue is 200 kbps? Assume that the 
queue size is infinite without buffer overflow (no packet loss), and the max 
window of the TCP sender is 20 packets, with each packet having 400 bytes. (1k=1000)   

**[ans]**  
> Assume heterogeneous RTTs sharing the same queue: **q**  
> q / 10(ms) + q / 100(ms) + q / 150(ms) = 200 * 1000 byte/sec = 200 byte/ms  
> q = 1714.2857143836734 ~= 1714.3 
> => 171.43, 17.143, 11.43 (byte/ms)

-----

(8) If the smoothed RTT kept by the TCP sender is currently 30 msec and the 
following measured RTT are 26, 32, and 24 msec, respectively. What is the new 
RTT estimate?  

**[ans]**  
`SRTT <- (1 - alpha) * SRTT + alpha * R'`
> after 26, SRTT = (1 - 0.125) * 30 + 0.125 * 26 = 29.5  
> after 32, SRTT = (1 - 0.125) * 29.5 + 0.125 * 32 = 29.8125  
> after 24, SRTT = (1 - 0.125) * 29.8125 + 0.125 * 24 = 29.0859375

-----

(13) Suppose you are going to design a real-time streaming application over the 
Internet that employs RTP on top of TCP instead of UDP, what situations will the 
sender and the receiver encounter in each TCP congestion control state shown in 
Figure 5.21? Compare your expected situations with those designed on top of UDP 
in a table format.  

**[ans]**  
> * **TCP**:
>   * **Slow Start**
>     * The sender increases `cwnd` exponentially by adding one packet
to `cwnd` each time it receives an ACK, so `cwnd` is doubled.
>   * **Congestion Avoidance**
>     * This state begins when `cwnd` >= `ssth`
>     * `cwnd` will grow linearly(slowly) by add `1 / cwnd` packet each time
>   * **Fast Retransmission**
>     * `cwnd` will reset to 1, then go back to **Slow Start**
>   * **Retransmission Timeout**
>     * `cwnd` will reset to 1, then go back to **Slow Start**

> * **UDP**:
>   * **Slow Start**
>     * only limited by bandwidth and hardware's capability
>   * **Congestion Avoidance**
>     * only limited by bandwidth and hardware's capability
>   * **Fast Retransmission**
>     * no retransmission mechanism
>   * **Retransmission Timeout**
>     * no retransmission mechanism


-----

(16) The text spends a great amount of pages introducing the different versions 
of TCP. Identify three more TCP versions by searching Itemize them and highlight 
their contributions within three lines of words with each TCP version.  

**[ans]**  
> * **FAST TCP (also written FastTCP)**: long-distance, high latency links
> * **TCP Vegas**: emphasizes packet delay, rather than packet loss, as a signal 
to help determine the rate at which to send packets.
> * **TCP Hybla**: eliminate penalization of TCP connections that incorporate a 
high-latency terrestrial or satellite radio link.


