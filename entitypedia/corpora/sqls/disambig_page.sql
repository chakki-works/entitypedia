CREATE DATABASE wikipedia;
USE wikipedia;
SOURCE jawiki-latest-categorylinks;
SELECT DISTINCT cl_from FROM categorylinks WHERE cl_to LIKE "%曖昧さ回避%" ORDER BY cl_from INTO OUTFILE "/var/lib/mysql-files/disambig_id.csv";