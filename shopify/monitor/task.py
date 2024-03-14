from time import sleep
from random import choice
from requests import get
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime

class Task:
    def __init__(self, proxies, site, webhook, delay, task_id):
        self.proxies = proxies
        self.proxy = choice(self.proxies)
        self.site = site
        self.webhook = webhook
        self.delay = delay[0]

        self.products = []
        self.in_stock = []
        self.found_product = None
        self.init = 1

        self.task_id = task_id

    def rotate_proxies(self):
        self.proxy = choice(self.proxies)

    def scrape(self):
        # products = get(self.site, proxies = {"http": self.proxy, "https": self.proxy}).json()
        products = get(self.site + "products.json").json()["products"]

        if products is None:
            self.rotate_proxies(self.proxies)
            sleep(self.delay)
            scrape()
        for product in products:
            variants = []
            for variant in product["variants"]:
                variants.append([
                    variant["available"],
                    variant["id"],
                    variant["title"],
                    variant["price"],
                    variant["sku"],
                ])
            
            self.products.append([
                product["title"],
                self.site + "products/" + product["handle"],
                product["images"][0]["src"],
                variants, 
            ])

    def compare(self):
        for product in self.products:
            if product not in self.in_stock and self.init == 1:
                self.in_stock.append(product)
            elif product not in self.in_stock:
                self.found_product = product
                print("%s [%s] NEW - %s" % (str(datetime.datetime.now()), self.site, self.found_product[0]))
                self.in_stock.append(product)
                self.send_webhook()

    def send_webhook(self):
        webhook = DiscordWebhook(url=self.webhook)

        embed = DiscordEmbed(title=self.found_product[0])
        embed.set_thumbnail(url=self.found_product[2])
        embed.set_footer(text="Shopify Monitor - @v6ctor")
        embed.set_timestamp()

        embed.add_embed_field(name="Price", value=self.found_product[3][0][3], inline=False)

        for index in range(len(self.found_product[3])):
            embed.add_embed_field(name=self.found_product[3][index][2], value="[ATC](%scart/add.js?id=%s)" % (self.site, self.found_product[3][index][1]))

        webhook.add_embed(embed)

        webhook.execute()

    def monitor(self):
        while True:
            self.scrape()
            self.compare()
            self.rotate_proxies()
            print("scraped")
            self.init = 0
            sleep(self.delay)

  
