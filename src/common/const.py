"""Generate random headers to avoid 403 forbidden error"""
HEADERS = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

user_agents_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0)\
 Gecko/20100101 Firefox/124.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0)\
 Gecko/20100101 Firefox/124.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1)\
 AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
 Chrome/123.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux i686; rv:124.0)\
 Gecko/20100101 Firefox/124.0"
]
