import csv
import random
from os import path
from zipfile import ZipFile

from lxml import etree

ZIPS_DIR = path.join(path.realpath('.'), 'race-zips')
zips_num = 50
xmls_per_zip = 100


def test_csv1():
    total_ids_expected = zips_num * xmls_per_zip
    csv1_realpath = path.join(ZIPS_DIR, 'csv1.csv')
    ids = set()
    with open(csv1_realpath, 'r') as csv1:
        reader1 = csv.reader(csv1)
        for row in reader1:
            ids.add(row[0])
    assert len(ids) == total_ids_expected


def test_csv2():
    csv2_realpath = path.join(ZIPS_DIR, 'csv2.csv')
    with open(csv2_realpath, 'r') as csv2:
        lines = csv2.readlines()
        # print('---', len(lines), lines[:3])
        object_names = []
        find_lines = set()
        for i in range(3):
            # lets test few
            zipnum = random.randint(1,zips_num)
            zip_realpath = path.join(ZIPS_DIR, '{0}.zip'.format(zipnum))
            with ZipFile(zip_realpath, 'r') as zip_obj:
                j = 0
                filenames = [f.filename for f in zip_obj.filelist]
                assert len(filenames) == xmls_per_zip
                for x in zip(filenames, range(3)):
                    xml_content = zip_obj.read(x[0])
                    doc = etree.fromstring(xml_content)
                    id_els = doc.findall('var[@name="id"]')
                    object_els = doc.findall('objects/object')
                    assert len(id_els) > 0
                    assert len(object_els) > 0
                    id = id_els[0].attrib.get('value')
                    for obj in object_els:
                        obj_name = obj.attrib.get('name')
                        find_lines.add('{0};{1}\n'.format(id, obj_name))
        assert len(find_lines) > 0
        for line in lines:
            if line in find_lines:
                find_lines.remove(line)
        assert len(find_lines) == 0
