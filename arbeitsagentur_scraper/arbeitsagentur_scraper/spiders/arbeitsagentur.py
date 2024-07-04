import base64
import json

import scrapy
from scrapy import FormRequest
from scrapy.utils.response import open_in_browser


class ArbeitsagenturSpider(scrapy.Spider):
    name = 'arbeitsagentur'
    start_urls = ['http://www.arbeitsagentur.de/']
    url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs?berufsfeld=Elektrotechnik&angebotsart=1&befristung=2&externestellenboersen=false&zeitarbeit=false&page=1&size=25&pav=false&facetten=false "
    captcha_url = "https://rest.arbeitsagentur.de/idaas/id-aas-service/pc/v1/assignment"

    payload = {
        "formId": "ARBEITGEBERDATEN",
        "formProtectionLevel": "JB_JOBSUCHE_20",
        'sessionId': '021FEE84-51D8-402E-9D01-57B707B6A264'
    }
    info_url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v3/jobs/{}/bewerbung"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9,ur-PK;q=0.8,ur;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Origin': 'https://www.arbeitsagentur.de',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'X-API-Key': 'jobboerse-jobsuche',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Cookie': 'rest=024dae17b4-4300-4526_V9yA_NNRBk3GoBGOIor-hHppDQr1vvjOs-3x4uO2wR8R7Nkg6PVweO4yxDGyjtsw'
    }
    custom_settings = {
        # 'FEED_URI': f'ah_output.json',
        # 'FEED_FORMAT': 'json',
        # 'FEED_EXPORT_ENCODING': 'utf-8-sig',
        # "ZYTE_API_TRANSPARENT_MODE": True,
        'ZYTE_SMARTPROXY_ENABLED': False,
        'ZYTE_SMARTPROXY_APIKEY': '',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610
        },
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse,
                             meta={'dont_proxy': False})

    def parse(self, response):
        self.headers['Cookie'] = '; '.join([i.decode('utf-8') for i in response.headers.getlist('Set-Cookie')])
        self.headers['Correlation-Id'] = '; '.join([i.decode('utf-8') for i in response.headers.getlist('Correlation-Id')])
        json_data = json.loads(response.text)
        results = json_data.get('stellenangebote')
        for result in results[:1]:
            company_code = self.encode_to_base64(result.get('refnr'))
            url = f"https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v3/jobdetails/{company_code}"
            yield scrapy.Request(url=url, callback=self.parse_details, headers=self.headers,
                                 meta={'company_code': company_code, 'dont_proxy': False, 'dont_merge_cookies': True})

    def encode_to_base64(self, original_string):
        encoded_bytes = original_string.encode('utf-8')
        encoded_string = base64.b64encode(encoded_bytes)
        return encoded_string.decode('utf-8')

    def parse_details(self, response):
        # self.headers['Cookie'] = '; '.join([i.decode('utf-8') for i in response.headers.getlist('Set-Cookie')])
        self.headers['Correlation-Id'] = '; '.join(
            [i.decode('utf-8') for i in response.headers.getlist('Correlation-Id')])
        company_code = response.meta.get('company_code')
        json_data = json.loads(response.text)
        item = dict()
        item['company_name'] = json_data.get('firma')
        item['job_Title'] = json_data.get('stellenangebotsTitel')
        item['Detail_url'] = f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{json_data.get('referenznummer')}"
        yield scrapy.Request(url=self.captcha_url,
                             method="POST",
                             body=json.dumps(self.payload),
                             headers=self.headers,
                             callback=self.parse_captcha,
                             meta={'item': item, 'company_code': company_code, 'dont_merge_cookies': True})
                             # callback=self.parse_captcha, meta={'item': item, 'company_code': company_code})

    def parse_captcha(self, response):
        company_code = response.meta.get('company_code')
        item = response.meta.get('item')
        json_data = json.loads(response.text)
        session_id = json_data.get('sessionId')
        challenge_id = json_data.get('challengeId')
        self.headers['Aas-Answer'] = '5yCkKG'
        # self.headers['X-Api-Key'] = 'jobboerse-jobsuche'
        self.headers['Aas-info'] = f"sessionId={session_id},challengeId={challenge_id}"
        # self.headers['Cookie'] = '; '.join([i.decode('utf-8') for i in response.headers.getlist('Set-Cookie')])
        self.headers['Correlation-Id'] = '; '.join(
            [i.decode('utf-8') for i in response.headers.getlist('X-Correlationid')])
        # self.headers['Cookie'] = 'rest=024dae17b4-4300-45VE-2_8QYQDai1I5jiv3MxkIw8TgSi6NH-BRKkaB8PAEwpMfEIEtn40jE27K_dJPXc64; cookie_consent=accepted; personalization_consent=accepted; marketing_consent=accepted; _pk_id.1000.cfae=5cc94b27c1e723be.1714650702.; _pk_ses.1000.cfae=1; DS_VARY_ML=_unknown; context-profile-id=aff78478-aff3-4e76-8331-ed3a17415648; _pk_id.35.cfae=5af795de2105e55c.1714651208.; _pk_ses.35.cfae=1; LANG=en; dropsolidCapture=%7B%22uuid%22%3A%22b18da63b-35d0-42dd-bf53-8a611e3891d0%22%2C%22domain%22%3A%22www.arbeitsagentur.de%22%2C%22hostName%22%3A%22www.arbeitsagentur.de%22%2C%22created%22%3A%222024-05-02T12%3A03%3A26.189Z%22%2C%22cdpUuid%22%3A%22c1871227-7704-4522-b950-46b0dc12a0db%22%7D'
        yield scrapy.Request(url=self.info_url.format(company_code),
                             headers=self.headers,
                             callback=self.parse_info, meta={'item': item, 'dont_merge_cookies': True})

    def parse_info(self, response):
        item = response.meta.get('item')
        json_data = json.loads(response.text)
        details = json_data.get('angebotskontakt')
        item['First Name'] = details.get('name').get('vorname')
        item['Last Name'] = details.get('name').get('nachname')
        item['Gender'] = details.get('anrede')
        address = details.get('postadresse')
        item['address'] = f"{address.get('strasse')} {address.get('hausnummer')}, {address.get('plz')} {address.get('ort')}"
        item['Email'] = details.get('emailadresse')
        telephone = details.get('telefonnummer')
        item['Contact_number'] = f"{telephone.get('laendervorwahl')} {telephone.get('vorwahl')} {telephone.get('rufnummer')}"
