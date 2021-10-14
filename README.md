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
    PID     NAME                                      PPID          VIRTMEM
    ...
    963     krfcommd                                  2             0B
    967     polkit-kde-auth                           1             817.64MB
    969     org_kde_powerde                           1             802.98MB
    973     xembedsniproxy                            1             221.36MB
    977     kaccess                                   1             279.37MB
    979     plasmashell                               1             5.94GB
    982     gmenudbusmenupr                           1             222.41MB
    987     kdeconnectd                               1             354.9MB
    992     agent                                     1             230.53MB
    996     pulseaudio                                818           2.37GB
    999     msm_kde_notifie                           1             464.63MB
   1004     pamac-tray-plas                           1             432.64MB
   1009     rtkit-daemon                              1             150.67MB
   1019     kactivitymanage                           818           534.17MB
   1067     gvfsd                                     818           230.71MB
   1076     gvfsd-fuse                                818           370.24MB
   1096     gsettings-helpe                           996           231.88MB
   1112     ksystemstats                              818           242.68MB
   1226     kio_http_cache_                           1             157.13MB
   1603     kioslave5                                 1             84.75MB
   1605     kioslave5                                 1             84.75MB
   ...
```


## Tests

All the tests are present in `./procpy/tests/` directory. You can run them through:
```
$ python3 -m unittest discover ./procpy
```
