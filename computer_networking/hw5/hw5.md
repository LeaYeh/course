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

-----

(6) Given that the throughput of a TCP connection is inversely proportional to 
its RTT, connections with heterogeneous RTTs sharing the same queue will get 
different bandwidth shares. What will be the eventual proportion of the bandwidth 
sharing among three connections if their propagation delays are 10 ms, 100 ms, 
150 ms, and the service rate of the shared queue is 200 kbps? Assume that the 
queue size is infinite without buffer overflow (no packet loss), and the max 
window of the TCP sender is 20 packets, with each packet having 400 bytes. (1k=1000)   

-----

(8) If the smoothed RTT kept by the TCP sender is currently 30 msec and the 
following measured RTT are 26, 32, and 24 msec, respectively. What is the new 
RTT estimate?  

-----

(13) Suppose you are going to design a real-time streaming application over the 
Internet that employs RTP on top of TCP instead of UDP, what situations will the 
sender and the receiver encounter in each TCP congestion control state shown in 
Figure 4.9? Compare your expected situations with those designed on top of UDP 
in a table format.  

-----

(16) The text spends a great amount of pages introducing the different versions 
of TCP. Identify three more TCP versions by searching 
http://www.lib.nctu.edu.tw/n_service/abi.html. 
Itemize them and highlight their contributions within three lines of words with 
each TCP version.  

