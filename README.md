# emCompound és emPreverb

Programkód az MSZNY2022 konferenciára benyújtott
_Igekötő-kapcsolás_ című cikkhez a bírálók számára.


## használat

A következő parancs segítségével egy kis tesztfájlon futtathatja le
az igekötő-kapcsoló eljárást.

```bash
make
```

Majd hasonlítsa össze
az `in/before` és az `out/after` fájlt a cikkben leírtak alapján.

A futtatáshoz linux + python környezet szükséges,
a futási idő néhány másodperc.


## kiértékelési eredmények

A cikk _Az igekötő-kapcsolás teljesítménye_ c. részében lévő,
eredményekről szóló táblázatok tartalma a

```bash
evaluation/general_test_results.txt
evaluation/difficult_test_results.txt
```

fájlokban található.

A felhasznált kézzel annotált gold _teszt_korpuszok hozzáférhetők itt:

```bash
evaluation/general_test.txt
evaluation/difficult_test.txt
```


## a kiértékelés reprodukálása

Ennek a folyamatnak jelentős az erőforrásigénye.

Először szerezzük be az `e-magyar` rendszert.
A docker image-hez 4 GB szabad hely szükséges.

```bash
docker pull mtaril/emtsv:latest
```

Ez után a 

```bash
make evaluate
```

a teljes kiértékelés újra lefut
és a tesztkorpuszok alapján újragenerálódnak az eredményfájlok,
melyek azonosak lesznek az eredetileg a repóban lévőkkel.
Ez hosszabb időt, akár egy órát igényel.

