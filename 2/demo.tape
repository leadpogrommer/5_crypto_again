Set Shell bash
Output demo.gif

Type "cat lipsum.txt"
Enter
Sleep 1

Type "# Top 10 most frequent letters"
Enter
Type "./main.py freq lipsum.txt | head"
Enter
Sleep 3

Type "# Entropy of lipsum.txt"
Enter
Type "./main.py ent lipsum.txt"
Enter
Sleep 3

Type "# Near zero entropy"
Enter
Type "echo -n '00000000000000001' | ./main.py ent -"
Enter
Sleep 3

Type "# 'RaNdOm' string from alphabet of size 2"
Enter
Type "echo -n '0101010101010' | ./main.py ent -"
Enter
Sleep 3

Type "# 'RaNdOm' string from alphabet of size 4"
Enter
Type "echo -n '123412341234' | ./main.py ent -"
Enter
Sleep 3

Type "# Real random bytestream"
Enter
Type " dd if=/dev/random of=/dev/stdout bs=1k count=1 status=none | ./main.py ent -"
Enter
Sleep 5