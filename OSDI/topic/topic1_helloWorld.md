# Topic 1: Behind helloWorld programmer

### How does a computer load/run/debug "hello world"?

#### How to compile hello.c

```shell
$ gcc -Wall hello.c -o hello
```

其中 `hello` 為 `executable file`/`機械碼`  

* 參數
  * `-Wall`: 開啟所有 warning
    * 當 source code 未產生任何 warning 時稱之為 `compile cleanly`
  * `-o`: 指定檔案名稱，default 為 `a.out`


* Compilation: 將 `source code` 轉換為 `機械碼` 的過程
* Compiler 分為 `front end` & `back end`
  * `front end`: 處理語言本身，包括 `scanning`, `parsing`, build `parse-tree`
  * `back end`: Code Generation, 產生對應目標系統的 target code
* portable compiler: 設計 compiler 時我們不需要對於每一個語言每個作業系統分別設計
front end & back end 而是 same front-end with multiple backends, one per target.
  * MxN problem: you don't want to have to write MxN compilers where you have M 
languages and N target systems. The idea is to only have to write M+N compilers.


[=====> COMPILATION PROCESS <======](http://stackoverflow.com/questions/3996651/what-is-compiler-linker-loader)

                     |
                     |---->  Input is Source file(.c)
                     |
                     V
            +=================+
            |                 |
            | C Preprocessor  | 將 define, include, macros 展開
            |                 |
            +=================+
                     |
                     | ---> Pure C file ( comd:cc -E <file.name> )
                     |
                     V
            +=================+
            |                 |
            | Lexical Analyzer|
            |                 |
            +-----------------+
            |                 |
            | Syntax Analyzer |
            |                 |
            +-----------------+
            |                 |
            | Semantic Analize|
            |                 |
            +-----------------+
            |                 |
            | Pre Optimization|
            |                 |
            +-----------------+
            |                 |
            | Code generation |
            |                 |
            +-----------------+
            |                 |
            | Post Optimize   |
            |                 |
            +=================+
                     |
                     |--->  Assembly code (comd: cc -S <file.name> )
                     |
                     V
            +=================+
            |                 | 產生 assembly code，並將出現頻率高的 variable 存入 registers
            |   Assembler     |
            |                 |
            +=================+
                     |
                     |--->  Object file (.obj) (comd: cc -c <file.name>)
                     |
                     V
            +=================+
            |     Linker      |
            |      and        |
            |     loader      |
            +=================+
                     |
                     |--->  Executable (.Exe/a.out) (com:cc <file.name> ) 
                     |
                     V
            Executable file(a.out)



(待補充/修正...)

-----

#### How to load a program

假設我們已經先有了第一個 shell，並由其呼叫 `fork`

* `fork()` 系統呼叫：用來建立 child process。
  * fork 是為了要一份記憶體
* `exec` 系列系統呼叫：以一個「外部程式」來取代自己（current process）的執行空間
* parent process、child process 與 Linux process tree
  * 建立 parent process、child process 之間的關係，parent 有權限控制 child
* `copy on write`: 但實際上 `fork` 並沒有真的複製一份 parent，其中資料段則與 parent 
共用
  * 大部分的狀況下child process並不會去對資料段作寫入的動作
  * 執行exec()後，之前的資料段就沒用了

> 在 child process 尚未對資料段作寫入的動作之前，parent 與 child process 共用資料段；
當 child process 對資料段記憶體作出寫入的要求時，系統會配置一塊實體記憶體﹙一個 page﹚
給 child process，並將原本資料段中被要求寫入之 page 的內容複製到這塊新的 page；
接著系統會更改 child process 的 page table，使要被寫入資料的虛擬位址可以對應到上
述新配置的實體記憶體位址。

> 此時 child process 與 parent process 的資料段大部分都還是功用的，不同的地方只
是這次要被寫入的 page；這種演算法的好處很多，在最節省記憶體的前提下使得 parent 與 
child process 不致互相影響。要達到這種效果，CPU 沒有支援 MMU 是做不到的，所以 
uClinux 無法直接支援 fork() 這個系統功能。

Read more: http://tw.tonytuan.org/2009/04/vforkuclinux.html#ixzz416zHQ5e3

-----

#### Why distinguish .text and .data in memory

* data 可讀寫，而 text/code(指令) 是 read-only
  * 而在 memory 中將其區分開來(.text 和 .data 的記憶體不連續)可以防止成是在執行
時被惡意改寫
* 為了提高 cache hit
  * 把指令和資料分開，有效的利用space locality(for data)和time locality(for 
instruction)有助於提高 cache hit
* 方便進行 fork
  * 指令只要保存一份，不同的資料保存很多份 -> 省記憶體









fork -> int 0x80
signal trap
x86-INF


[v] why text not contact with data in mem?

fork is lib
  static linking:
    already in mem, fast
  dynamic linking:
    in disk, slow but more space

fork need to parsing a.out(elf format) and load the needed info

is stack necessary? when?
who maintain code stack?
  each program own/maintain its code stack
    if exec a.out, but sp->b.out = vitous

who assign pc the first instruction's address?


compiling
  front
  IR
  backend

loading
  shell fork program from disk, 
  exec mmap(virturl to real) hello to ram

exec


