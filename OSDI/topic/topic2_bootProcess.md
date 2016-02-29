# How Computer Boot Up (detail with Linux)

bootstrap processor (BSP) that runs all of the BIOS and kernel initialization code.  

Most registers in the CPU have well-defined values after power up  
instruction pointer (EIP) which holds the memory address for the instruction being 
executed by the CPU.  

`EIP` so that the first instruction executed is at address 0xFFFFFFF0.  
This magical address is called the `reset vector` and is standard for modern Intel CPUs.

The motherboard ensures that the instruction at the reset vector is a jump to the 
memory location mapped to the BIOS entry point.  

`hidden base address`  

The CPU then starts executing BIOS code, which initializes some of the hardware 
in the machine. Afterwards the BIOS kicks off the `Power-on Self Test` `(POST)` 
which tests various components in the computer.  

The CPU then starts executing BIOS code, which initializes some of the hardware 
in the machine.  
Afterwards the BIOS kicks off the Power-on Self Test (POST) which tests various 
components in the computer.  

Lack of a working video card fails the POST and causes the BIOS to halt and emit 
beeps to let you know what's wrong, since messages on the screen aren't an option.  
A working video card takes us to a stage where the computer looks alive:  
manufacturer logos are printed, memory starts to be tested.  

After the POST the BIOS wants to boot up an operating system, which must be found 
somewhere: hard drives, CD-ROM drives, floppy disks, etc.  
The actual order in which the BIOS seeks a boot device is user configurable.  

The BIOS now reads the first 512-byte sector (sector zero) of the hard disk. 
This is called the `Master Boot Record` `(MBR)`:  
The MBR holds the information on how the partitions, containing file systems, 
are organized on that medium. The MBR also contains executable code to function 
as a loader for the installed operating system.

and it normally contains two vital components:   
a tiny OS-specific bootstrapping program at the start of the MBR followed by a partition table for the disk.  

The specific code in the MBR could be a Windows MBR loader, code from Linux 
loaders such as LILO or GRUB, or even a virus.  

1. The MBR itself contains the first stage of the boot loader.
2. Due to its tiny size, the code in the MBR does just enough to load another 
sector from disk that contains additional boostrap code.
3. The MBR code plus code loaded in step 2 then reads a boot configuration file 
(e.g., grub.conf in GRUB, boot.ini in Windows).
4. At this point the boot loader code needs to fire up a kernel. It must know 
enough about file systems to read the kernel from the boot partition.
5. After performing several initializations, `NTDLR` loads the kernel image from 
file c:\Windows\System32\ntoskrnl.exe and, just as GRUB does, jumps to the kernel 
entry point.

## Problems
* How can CPU know the address of first instruction in `EIP`? is EIP init will a 
constant value? (something like `0xFFFFFFF0`)
* What kind of memory BIOS and MBR actually stored? (ROM, flash memory...)
  * I think MBR should be stored in ROM, because partition table can not be volatilized
  * MBR stored in disk, a constant address
* How to stuff the kernel image into memory?







