## Hands-On Exercises
2. Setup iptables to block the outgoing connection to a certain IP address, and try to
see whether the blocking work.  

**[ans]**  
!(iptables)[images/iptables.png]  

-----

4. Use Nessus ( http://www.nessus.org/nessus ) to find the services running on the
hosts in your subnet, and indicate what they are. Are there any services not 
running on well-known ports, e.g., a Web service not on port 80?  

**[ans]**  
!(nessus)[images/nessus.png]  

-----

7. Find out how many rules are in your current Snort rule set.  

**[ans]**  
!(snort)[images/snort.png]  

> awk '條件類型1{動作1} 條件類型2{動作2} ...' filename


## Written Exercises
4. Is it efficient to implement the DES (or 3DES) algorithm in software? Why is the
implementation a target for hardware acceleration?  

**[ans]**  
> No, the DES alg use many bitwise operations and harware is good than software 
on bit operations.

-----

11. What are possible reasons of false positives from NIDS alerts?  

**[ans]**  
> The detection rules are too general, so a normal context may be detected that 
imply an attack.

-----

14. ClamAV claims a very large signature set (larger than 500,000). Are there really
so many viruses in the wild, i.e., on the Internet? What are possible reasons that so 
many signatures are needed?  

**[ans]**  
> not so many, but also need to concern old viruses.


