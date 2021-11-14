```
part 1:
    generate 50 zips with 100 xmls in each
        <root>
            <var name="id" value="<rnd_str>"/>
            <var name="level" value="<rnd_int:1...100>"/>
            <objects>
                <object name="<rnd_str>"/>
                ... 1...10
            </objects>
        </root>
    may use 1 thread only

part 2:
    make 2 csv files from zip archives, use few CPUs:
        1:
            id, level
        2:
            id, object_name
```

```
python race_csv.py
python -m pytest -s tests
```
