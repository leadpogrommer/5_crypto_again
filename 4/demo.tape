Set Shell bash
Set Padding 0
Output demo.gif

Type "dd if=/dev/random count=1  bs=16 of=key.bin"
Enter
Sleep 1

Type "dd if=/dev/random count=1  bs=16 of=iv.bin"
Enter
Sleep 1


Type "./main.py encrypt key.bin iv.bin lipsum.txt lipsum.enc"
Enter
Sleep 3

Type "hexdump -C lipsum.enc"
Enter
Sleep 5

Type "./main.py decrypt key.bin iv.bin lipsum.enc -"
Enter
Sleep 5