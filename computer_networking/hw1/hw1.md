**Linux Distribution: ubuntu 15.04**

## Hands-On Exercises ##

### [2-2] Things inside the distribution ###
> **basic editor**         *vim*

> **Shell**                *bash*

> **Browser**              *firefox*

> **desktop environment**  *gnome*

> **office solfware**      *LibreOffice*

### [3]   Summarize and categorize what is inside that directory ###
**in this distribution sorce files reside in `/usr/src`** </br>
And observed on http://lxr.free-electrons.com/source/?v=3.19

#### arch/ ####
> contains all of the architecture specific kernel code. In further 
> subdirectories, one per supported architecture, for example i386.

#### arch/\*/kernel/ ####
> The main kernel code. (e.g. `arch/arm/kernel/*`)

#### init/ ####
> It contains the initialization code for the kernel.

#### mm/ ####
> It contains all of the memory management code.

#### drivers/ ####
> It contains of the system's device drivers.

#### ipc/ ####
> It contains the kernels inter-process communications code.

#### fs/ ####
> It contains all of the file system code. 
> In further subdirectories, one per supported file system, 
> for example `vfat` and `ext2`.

#### net/ ####
> The kernel's networking code.

#### lib/ ####
> It contains the kernel's library code.

#### script/  ####
> It contains the scripts that are used when the kernel is configured.

### Trace Linux Kernel code to find: ###
> **ubuntu 15.04 use kernel 3.19**

**(a) Which function calls `alloc_skb()` to allocate `sk_buffer` for request and the response?**

> NIC alert driver to move the packet into the memory space which is allocated 
> from the `sk_buff` pool.

```c
/* in source code drivers/net/ethernet/netx-eth.c */

139 static void netx_eth_receive(struct net_device *ndev)
140 {
...
152         skb = netdev_alloc_skb(ndev, len);
...
158         data = skb_put(skb, len);
159 
160         memcpy_fromio(data, priv->sram_base + frameno * 1560, len);
...
169 }
```
</br>
> After **path. A** recv the data, then TCP mudule builds the ACK packet, then 
> trans along **path. B**

```c
/* in source code /net/ipv4/tcp_output.c */

3264 static int tcp_xmit_probe_skb(struct sock *sk, int urgent)
3265 {
3266         struct tcp_sock *tp = tcp_sk(sk);
3267         struct sk_buff *skb;
3268 
3269         /* We don't queue it, tcp_transmit_skb() sets ownership. */
3270         skb = alloc_skb(MAX_TCP_HEADER, sk_gfp_atomic(sk, GFP_ATOMIC));
...
3282         return tcp_transmit_skb(sk, skb, 0, GFP_ATOMIC);
3283 }

3220 void tcp_send_ack(struct sock *sk)
3221 {
3222         struct sk_buff *buff;
...
3234         buff = alloc_skb(MAX_TCP_HEADER, sk_gfp_atomic(sk, GFP_ATOMIC));
...
3250 }
```
**(b) Which function calls `kfree_skb()` to release `sk_buffer` for request and the response?** 

> After **path. B** warp the respone data and IP header to the packet, then 
> return space(released `sk_buff` pool) after trans.

> **Collapse contiguous sequence of skbs** head..tail with sequence numbers start..end.

```c
/* in source code net/ipv4/tcp_input.c */

4531 tcp_collapse(struct sock *sk, struct sk_buff_head *list,
4532              struct sk_buff *head, struct sk_buff *tail,
4533              u32 start, u32 end)
4534 {
...
4548                         skb = tcp_collapse_one(sk, skb, list);
...
4610                                 skb = tcp_collapse_one(sk, skb, list);
...
4618 }
```

```c
849 static netdev_tx_t ethoc_start_xmit(struct sk_buff *skb, struct net_device *dev)
850 {
...
856         if (unlikely(skb->len > ETHOC_BUFSIZ)) {
857                 dev->stats.tx_errors++;
858                 goto out;
859         }
...
888 out:
889         dev_kfree_skb(skb);
890         return NETDEV_TX_OK;
891 }
```


**(c) Which function calls `alloc_skb()` to allocate `sk_buffer`?**
```c
/* in source code net/ipv4/route.c */

2391 static int inet_rtm_getroute(struct sk_buff *in_skb, struct nlmsghdr *nlh)
2392 {
...
2411         skb = alloc_skb(NLMSG_GOODSIZE, GFP_KERNEL);
...
2486 }
```

**(d) Which function calls `kfree_skb()` to release  `sk_buffer`?**
> Also in **net/ipv4/route.c inet_rtm_getroute**, 

```c
2391 static int inet_rtm_getroute(struct sk_buff *in_skb, struct nlmsghdr *nlh)
2392 {
...
2484         kfree_skb(skb);
...
2486 }
```

**(e) How you trace these dynamically or statically?**

statically, inferred possible source code file by fig. 1.19 1.21 and find the key 
words and function then crossed reference.


## Written Exercises ##

**[Ans 1]**
> a. bit width = 1 / (40 * 10^9) = 0.025 ns/b
> bit length = 0.025 * 10^-9 * 2 * 10^8 = 5 * 10^-3 m

> b. 5000 * 1.6 * 10^3 / (5 * 10^-3) = 1.6 * 10^9 = 1.6 Gb

> c. 1500 * 8 / (40 * 10^9) = 300 * 10^-9 = 300 ns/b

> d. 1.6 Gb * 0.025 ns/b = 40 ms

**[Ans 3]**
> a. 
> 
> Mean latency = 1 / (1000 – 500) = 2 * 10^-9 = 2 ns
> 
> Mean queuing time = Mean latency – 1 = 1 ns
> 
> Mean occupancy = 500 * 10^6 * 2 * 10^-9 = 1

> b.
>  
> Mean latency = 1 / (10 – 5) (Gb/s) = 0.2 ns
> 
> Mean queuing time = Mean latency – 0.1 = 0.1 ns
> 
> Mean occupancy = 1

**[Ans 5]**
> (3 * 10^6) phone * 6 hop * 5 mins = 90 * 10^6 memory entries

**[Ans 17]**
> put the routing task as a daemon in the user space, is because that
> this computation executed occasionally and avoid wasting CPU times.

> keeping the routing table lookup in the kernel, is because that 
> it is required fast and routing table lookup is very stable.

> put table in kernel and implement in user space because if </br>
> **both in kernel:** when the implemention crash, kernel will be crashed too.
> kernel need almost bug free. </br>
> **both in user space:** it's will handle kernel in few hundary sec.

**[Ans 20]**
> a. registers and IRQ

> b. The driver asks register with an address then controller interrupts CPU 
> with an IRQ number to call driver.

> c. The controller interrupts CPU and look up the IRQ number.


