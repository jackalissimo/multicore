"""
1-file task. No architecture.

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
"""

import asyncio
import csv
import shutil
from os import unlink, path, mkdir
import string
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import random
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from collections import deque


MAX_WORKERS = 4
ZIPS_DIR = path.join(path.realpath('.'), 'race-zips')


def get_zip_batches(dir_: str = ZIPS_DIR, batch_num: int = 4):
    assert path.isdir(dir_)
    batches = deque()
    for i in range(batch_num):
        batches.append([])

    for pf in Path(dir_).glob("*.zip".format(dir_)):
        zip_realpath = path.join(dir_, pf.name)
        batches[0].append(zip_realpath)
        batches.rotate()


    return list(batches)


def write_results(levels, object_names, csv1_realpath, csv2_realpath):
    with open(csv1_realpath, 'a') as csv1, \
         open(csv2_realpath, 'a') as csv2:
        writer1 = csv.writer(csv1, delimiter=';')
        writer2 = csv.writer(csv2, delimiter=';')
        for level in levels:
            writer1.writerow(level)
        for names_line in object_names:
            writer2.writerow(names_line)


def process_zips(zips: list, csv1_realpath: str, csv2_realpath: str):
    """
    multi CPU, same files output
    """
    c = 0

    try:
        for zip_realpath in zips:
            print(zip_realpath)
            levels = []
            object_names = []
            with ZipFile(zip_realpath, 'r') as zip_obj:
                filenames = [f.filename for f in zip_obj.filelist]
                for filename in filenames:
                    xml_content = zip_obj.read(filename)
                    doc = etree.fromstring(xml_content)
                    id_els = doc.findall('var[@name="id"]')
                    level_els = doc.findall('var[@name="level"]')
                    object_els = doc.findall('objects/object')
                    assert len(id_els) > 0
                    assert len(level_els) > 0
                    id = id_els[0].attrib.get('value')
                    level = level_els[0].attrib.get('value')
                    levels.append((id, level,))
                    # print('--', id, level, len(object_els))
                    for obj in object_els:
                        obj_name = obj.attrib.get('name')
                        object_names.append((id, obj_name,))

                write_results(levels, object_names, csv1_realpath, csv2_realpath)

    except Exception as e:
        # print('ERROR! ', type(e), str(e))
        raise e




async def make_csv_few_cores():
    zip_batches = get_zip_batches(batch_num=MAX_WORKERS)

    csv1_realpath = path.join(ZIPS_DIR, 'csv1.csv')
    csv2_realpath = path.join(ZIPS_DIR, 'csv2.csv')
    with open(csv1_realpath, 'w'), \
         open(csv2_realpath, 'w'):
        # cleaning output files, if needed
        pass

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                process_zips,
                *(zips, csv1_realpath, csv2_realpath)
            )
            for zips in zip_batches
        ]

        for resp in await asyncio.gather(*tasks):
            pass
    print('all zips parsed')


def random_word(length=20):
    symbols = string.ascii_lowercase
    return ''.join(random.choice(symbols) for i in range(length))


class UniqAlgoMilleniumEventException(Exception):
    pass


def random_id(ids_used: set):
    """
    plz don't ask what if 1000000000000000 ids here
    no uuids :P
    """
    for i in range(3):
        id = random_word(length=15)
        if id in ids_used:
            if i >=2:
                raise UniqAlgoMilleniumEventException('today')
        else:
            break
    ids_used.add(id)
    return id


def prepare_dir(dir_):
    """
    clean it up
    """
    if not path.isdir(dir_):
        mkdir(dir_)
    assert path.isdir(dir_)
    for pf in Path(dir_).glob("**/*"):
        if pf.is_file():
            pf.unlink()
        elif pf.is_dir():
            shutil.rmtree(pf)


def generate_zips(zips_num=50, xmls_per_zip=100, dir_=ZIPS_DIR):
    prepare_dir(dir_)

    ids_used = set()
    for z in range(1, zips_num + 1):
        zip_name = "{0}.zip".format(z)
        zip_realpath = path.join(dir_, zip_name)
        xml_realpaths = []
        with ZipFile(zip_realpath, 'w') as zip_obj:
            for x in range(1, xmls_per_zip + 1):
                root = etree.Element('root')
                doc = etree.ElementTree(root)
                xml_name = "{0}.xml".format(x)
                xml_realpath = path.join(dir_, xml_name)
                xml_realpaths.append(xml_realpath)
                obj_num = random.randint(1, 10)
                id = random_id(ids_used)
                level = random.randint(1, 100)
                etree.SubElement(root, 'var', name='id', value=id)
                etree.SubElement(root, 'var', name='level', value=str(level))
                objects = etree.SubElement(root, 'objects')

                for o in range(1, obj_num+1):
                    obj_name = random_word(33)
                    etree.SubElement(objects, 'object', name=obj_name)

                with open(xml_realpath, 'wb') as xml_file:
                    doc.write(xml_file, xml_declaration=True, encoding='utf-8')
                assert path.isfile(xml_realpath)
                zip_obj.write(xml_realpath, arcname=xml_name)
                unlink(xml_realpath)
                assert not path.isfile(xml_realpath)
    print('zips generated')


def part_one():
    generate_zips(50, 100)


def part_two():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(make_csv_few_cores())
    loop.run_until_complete(future)


def main():
    part_one()
    part_two()


if __name__ == '__main__':
    main()
