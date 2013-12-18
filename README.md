vake
====

Script to help you fix compiler errors using vim

Usage
=====
Run vake.py like you would run make:

```shell
$ python vake.py
gcc -Wall -o test test.c
test.c: In function 'main':
test.c:8:19: error: expected ';' before ')' token
test.c:9:3: warning: statement with no effect [-Wunused-value]
test.c:10:2: error: expected ';' before '}' token
test.c:11:1: warning: control reaches end of non-void function [-Wreturn-type]

vake: 4 errors or warnings. Run vake? [Y/n]
```

If you run vake, you will be prompted for a vim ex command for each error or warning.

```shell
<Enter> to edit. 'q' to skip.

test.c:8:19 error: expected ';' before ')' token
    	for (x = 0; x < y) {
                         ^
:
```

The ex command is executed with the cursor positioned as shown by the caret.
Conveniently, pressing "Enter" will not execute any ex commands, so you just get
a vim instance. Typing "q" will instantly quit the vim instance that was launched,
effectively skipping the edit.