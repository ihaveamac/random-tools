rm seeddb.bin
rm -rf 0004*/
rm -rf xmls/
cd files
wget -O json_dec https://{tkey_site}/json_dec
wget -O seeddb.bin https://{tkey_site}/seeddb
rm -rf 9.6-dbgen-xmls
git clone https://github.com/ihaveamac/9.6-dbgen-xmls.git
cd ..
