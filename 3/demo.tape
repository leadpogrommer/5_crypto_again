Set Shell bash
Output demo.gif

Type "dd if=/dev/random count=1  bs=6 of=key.bin"
Enter
Sleep 1

Type "cat plain.txt"
Enter
Sleep 1

Type "./main.py xor plain.txt key.bin enc.bin"
Enter
Sleep 1
Type "hexdump -C enc.bin"
Enter
Sleep 1
Type "./main.py xor enc.bin key.bin -"
Enter
Sleep 5

Type "./main.py rc4 lipsum.txt key.bin lipsum.enc"
Enter
Sleep 1
Type "hexdump -C lipsum.enc"
Enter
Sleep 1
Type "./main.py rc4 lipsum.enc key.bin -"
Enter
Sleep 5