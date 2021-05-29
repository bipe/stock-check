# stock-check
Web scrapping python app to check item availability in some retail sellers
#### *Until now, works for Kabum, Amazon and FastShop links.

## Try it:
 - Put the URLs in a __urls.txt__ file, in the same directory as the program. One url per line.
 - The first command-line argument (optional) defines the cooldown between every round of checks. Default is 300s = 5 minutes.


### Don't rush me:
- Organize code
- Let manually changing user-agent of requests

### Don't even hold your breath:
- Integration to web app
- SPA retailer sites scrapping


* The sad fact about web scrapping this kind of sites is that they can change at anytime (html elements ids/classes etc). Also, if you check in small intervals, they may send a recaptcha verification.
