#!/usr/bin/env python3

# ticker per le regionali sarde 2014.

import xml.etree.ElementTree as ET
import urllib.request
import time

yellow = lambda x: "\x1b[33m{}\x1b[0m".format(x)
green = lambda x: "\x1b[32m{}\x1b[0m".format(x)
cyan = lambda x: "\x1b[36m{}\x1b[0m".format(x)

err = lambda n, N: (1*(1-n/N)/N)**0.5

u = "http://www.regione.sardegna.it/xml/elezioni2014/risultati_riassuntivi.xml"

while(True):
    req = urllib.request.Request(url=u)
    rob = {}
    with urllib.request.urlopen(req) as f:
        s = f.read().decode("utf-8")
        tree = ET.fromstring(s)
        r = tree.findall("risultati_riassuntivi")[0]

        reg = int(r.attrib["sezioni_regionali"])
        circ = int(r.attrib["sezioni_circoscrizionali"])
        tot = int(r.attrib["sezioni_totali"])

        rreg = reg/tot
        rcirc = circ/tot

        print("## Sezioni regionali scrutinate: {}/{} ({})".format(reg, tot, cyan("{:.2%}".format(rreg))))
        print("## Sezioni circoscrizionali scrutinate: {}/{} ({})".format(circ, tot, cyan("{:.2%}".format(rcirc))))

        for coal in r.findall("coalizioni"):
            pr = coal.attrib["presidente"]
            rob[pr] = {"voti": int(coal.attrib["voti"].replace(".", "")), "liste": [{"lista": i.attrib["nome"], "voti": int(i.attrib["voti"].replace(".", ""))} for i in coal.findall("liste")]}

        totc = sum([rob[pr]["voti"] for pr in rob])
        totp = sum([i["voti"] for pr in rob for i in rob[pr]["liste"]])

        print("")

        for x in sorted([(d, rob[d]["voti"]) for d in rob], key=lambda x: -x[1]):
            pr = x[0]
            v = rob[pr]["voti"]
            perc = rob[pr]["voti"]/totc
            print(">> Candidato presidente: {}, {} voti ({} ± {}: [{}, {}])".format(yellow(pr), green(v), cyan("{:.2%}".format(perc)), cyan("{:.2%}".format(2*err(v, totc))), cyan("{:.2%}".format(perc - 2*err(v, totc))), cyan("{:.2%}".format(perc + 2*err(v, totc)))))
            for lista in rob[pr]["liste"]:
                print("-- {}: {} voti ({:.2%})".format(lista["lista"], green(lista["voti"]), lista["voti"]/totp))
            print("")

        time.sleep(15)
