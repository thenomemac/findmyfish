#!/bin/bash
scrapy crawl clevelandmetroparks_dot_com -o ../data/cle.json
scrapy crawl lakemetroparks_dot_com -o ../data/lake.json
