First i would like to thank those people on this link 
https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/1832

reading them help me a lot to have a better understanding of what nodriver is capable of.
--------------------------------------------------------------------------
This being said let talk about this code.
--------------------------------------------------------------------------

leboncoinf.fr is one of the biggest french website. two or three years ago it was easy to scrap then for they finaly got a WAF ( datadome ). It bacame nearly impossible for some who doesn't have budget to subscribe to proxy service or something like that. Plus it detects easily webdriver like selenium, so complicated to scrap except if you use 'undetected-selenium' which is thd ancestor of nodriver.

with this code which can be improved, you will be able to navigate through pages, clicking on page pagination, grabing data requested.

I- HOW TO USE
First on leboncoin.fr search what you want, copy the link and paste it in
the program (line 97).


II- Limits:
To avoid banishing make sure you subscribe to a proxy service to rotate you ip adress whereas you will be blocked by datadome.
I recommand not to change sleep time, shorted awated is more you increase chances to be block by datadome
