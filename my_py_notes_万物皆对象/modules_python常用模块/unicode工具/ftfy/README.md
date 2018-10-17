# ftfy
超级强大的Unicode文本工具

[docs](https://ftfy.readthedocs.io/en/latest/)

## simple use
```bash
>>> print(fix_text('uÌˆnicode'))
ünicode

>>> print(fix_text('Broken text&hellip; it&#x2019;s ﬂubberiﬁc!',
...                normalization='NFKC'))
Broken text... it's flubberific!

>>> print(fix_text('HTML entities &lt;3'))
HTML entities <3

>> print(fix_text('<em>HTML entities &lt;3</em>'))
<em>HTML entities &lt;3</em>

>>> print(fix_text("&macr;\\_(ã\x83\x84)_/&macr;"))
¯\_(ツ)_/¯

>>> # This example string starts with a byte-order mark, even if
>>> # you can't see it on the Web.
>>> print(fix_text('\ufeffParty like\nit&rsquo;s 1999!'))
Party like
it's 1999!

>>> print(fix_text('ＬＯＵＤ　ＮＯＩＳＥＳ'))
LOUD NOISES

>>> len(fix_text('ﬁ' * 100000))
200000

>>> len(fix_text(''))
0
```