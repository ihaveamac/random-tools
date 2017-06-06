#!/usr/bin/env python3
import binascii
import json
import os
import ssl
import urllib.request, urllib.error, urllib.parse

# stolen fron PlaiCDN and heavily edited
def getTitleInfo(title_id):
    # create new SSL context to load decrypted CLCert-A off directory, key and cert are in PEM format
    # see https://github.com/SciresM/ccrypt
    ctr_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctr_context.load_cert_chain('ctr-common-1.crt', keyfile='ctr-common-1.key')

    # ninja handles handles actions that require authentication, in addition to converting title ID to internal the CDN content ID
    ninja_url = 'https://ninja.ctr.shop.nintendo.net/ninja/ws/'

    # use GET request with parameter "title_id[]=mytitle_id" with SSL context
    # use header "Accept: application/json" to retrieve JSON instead of XML
    try:
        shop_request = urllib.request.Request(ninja_url + 'titles/id_pair' + '?title_id[]=' + title_id)
        shop_request.get_method = lambda: 'GET'
        shop_request.headers['Accept'] = 'application/json'
        response = urllib.request.urlopen(shop_request, context=ctr_context)
        json_response = json.loads((response.read()).decode('UTF-8', 'replace'))
        print(json_response)
    except urllib.error.URLError as e:
        raise

    # set ns_uid (the internal content ID) to field from JSON
    ns_uid = json_response['title_id_pairs']['title_id_pair'][0]['ns_uid']

    # samurai handles metadata actions, including getting a title's info
    # URL regions are by country instead of geographical regions... for some reason
    samurai_url = 'https://samurai.ctr.shop.nintendo.net/samurai/ws/'
    region_dict = [
        ('US', 'USA'),
        ('GB', 'EUR'),
        ('JP', 'JPN'),
        ('ES', 'EUR'),
        ('DE', 'EUR'),
        ('IT', 'EUR'),
        ('FR', 'EUR'),
        ('NL', 'EUR'),
        ('KR', 'KOR'),
        ('TW', 'TWN'),
        ('HK', 'HKG'),
    ]

    # try loop to figure out which region the title is from; there is no easy way to do this other than try them all
    for country_code, region in region_dict:
        try:
            title_request = urllib.request.Request(samurai_url + country_code + '/title/' + str(ns_uid))
            title_request.headers['Accept'] = 'application/json'
            response = urllib.request.urlopen(title_request, context=ctr_context)
            title_response = json.loads((response.read()).decode('UTF-8', 'replace'))
            break
        except urllib.error.URLError as e:
            print(e.read())
            pass

    # get info from the returned JSON from the URL
    try:
        title_name = (title_response['title'].get('formal_name', '-eShop Content-'))
        publisher = title_response['title']['publisher'].get('name', '------')
        product_code = title_response['title'].get('product_code', '------')
        if product_code[9] == "A":
            region = 'ALL'

        return([title_name, region, product_code, publisher, title_id])
    except UnboundLocalError:
        return None

os.makedirs("info", exist_ok=True)
os.makedirs("info_unknown", exist_ok=True)
with open("seeddb.bin", "rb") as seeddb:
    total = int.from_bytes(seeddb.read(2),'little')
    print(total)
    for i in range(0, total):
        seeddb.seek((i * 32) + 16)
        tid = binascii.hexlify(seeddb.read(8)[::-1]).decode('UTF-8')
        print(tid, end='')
        if os.path.isfile("info/%s.txt" % tid):
            print(" - already exists")
        else:
            print(" - getting info")
            titleinfo = getTitleInfo(tid)
            if titleinfo != None:
                with open("info/%s.txt" % tid, "w") as f:
                    json.dump(titleinfo, f)
            else:
                with open("info_unknown/%s.txt" % tid, "w") as f:
                    f.write("for some reason we have the seed for this title but no info on it...")
