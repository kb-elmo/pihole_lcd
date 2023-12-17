# pihole_lcd
### Script for displaying PiHole stats on an i2c 1602 LCD

Stats are displayed on eight different "screens" that are cycled through in 30 sec. intervals.
The first two (version and uptime) are only shown for 15 seconds.

Example screen:
<img align=right width="500" src="https://i.imgur.com/WkKokhu.png">

Currently implemented screens:
- PiHole and FTL version
- Update available (only shown when version is outdated)
- System stats (uptime and load)
- Domains (number of domains on blocklists)
- Queries (amount of queries in the last 24h - total and forwarded)
- Blocked (number and percentage of blocked queries in past 24h)
- Clients (number of known and currently online clients)
- Gravity (age of the gravity database)