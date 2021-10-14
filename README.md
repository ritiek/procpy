# Procpy

Parses and displays process information from `/proc/<pid>/stat`.
This tool makes use of only the standard library in Python and no external dependencies
should be required to run the program.


## Running

```
$ python3 ./main.py
```

The output should be similar to below and sorted by PID:
```
    PID     NAME                                      PPID     VIRTMEM     UTIME   STIME    OWNER
    ...
    921     kglobalaccel5                             818      276.62MB    1628    0        ritiek
    932     dconf-service                             818      151.87MB    0       0        ritiek
    949     ksmserver                                 1        278.71MB    2380    2362     ritiek
    953     kscreen_backend                           818      214.75MB    1380    0        ritiek
    955     obexd                                     818      45.42MB     0       0        ritiek
    963     krfcommd                                  2        0B          0       0        root
    967     polkit-kde-auth                           1        817.64MB    1372    2        root
    969     org_kde_powerde                           1        802.98MB    2463    0        root
    973     xembedsniproxy                            1        221.36MB    1339    0        ritiek
    977     kaccess                                   1        279.37MB    2617    0        ritiek
    979     plasmashell                               1        6.06GB      144478  511922   ritiek
    982     gmenudbusmenupr                           1        222.41MB    1370    0        ritiek
    987     kdeconnectd                               1        354.9MB     2292    0        ritiek
   ...
```

You can also pipe the output to a pager:

```
$ python3 ./main.py | less
```


## Tests

All the tests are present in `./procpy/tests/` directory. You can run them through:
```
$ python3 -m unittest discover ./procpy
```
