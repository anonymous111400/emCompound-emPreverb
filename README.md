# preverb

Programkód az MSZNY2022 konferenciára benyújtott
_Igekötő-kapcsolás_ című cikkhez a bírálók számára.


## használat

A futtatáshoz linux + python környezet szükséges. 

```bash
make
```

Majd hasonlítsa össze
az `in/before` és az `out/after` fájlt a cikkben leírtak alapján.


## kiértékelési eredmények

A cikk _Az igekötő-kapcsolás teljesítménye_ c. részében lévő,
eredményekről szóló táblázatok tartalma a

```bash
eval/general_test_results.txt
eval/difficult_test_results.txt
```

fájlokban található.


## a kiértékelés reprodukálása

Először be kell szereztünk az `e-magyar` rendszert.
A docker image-hez 4 GB szabad hely szükséges.

```bash
docker pull mtaril/emtsv:latest
```

Ez után a 

```bash
make eval
```

hatására hosszabb, akár egy órás futás során
a teljes kiértékelés újra lefut
és újragenerálódnak az eredményfájlok.

