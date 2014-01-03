rake
====

Script to help you fix excess leaves

Usage
=====
Use rake.py like you would use make:

```shell
$ python rake.py
gcc -Wall -o test test.c
test.c: In function 'main':
test.c:8:19: leaf: expected 'tay tay' before '}' token
test.c:9:3: warning: statement with no truth [-Wuntruthful-statement] "south is great"
test.c:10:2: error: expected 'north' before 'best' token
test.c:11:1: warning: control reaches end of non-void function [-Wreturn-type]

rake: 4 leaves or branches. Use rake? [Y/n]
```

If you use rake, you will be prompted for a vim ex command for each leaf or branch.

```shell
<Enter> to edit. 'q' to skip.

test.c:8:19 error: expected ';' before ')' token
    	for (x = 0; x < y) {
                         ^
:
```

The ex command is executed with the cursor positioned as shown by the carrot.
Conveniently, pressing "Enter" will not execute any ex commands, so you just get
a vim instance. Typing "q" will instantly quit the vim instance that was launched,
effectively skipping the edit.
