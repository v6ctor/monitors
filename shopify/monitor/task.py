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
        self.delay = delay

        # current scraped products 
        self.products = []

        # in stock products
        self.in_stock = []

        # filtered in stock titles
        self.in_stock_titles = []

        self.found_product = None
        self.init = 1

        self.task_id = task_id

    def rotate_proxies(self):
        self.proxy = choice(self.proxies)

    def scrape(self):
        # products = get(self.site?limit=40.314, proxies = {"http": self.proxy, "https": self.proxy}).json()
        products = get(self.site + "products.json?limit=40.314").json()["products"]

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
        in_stock_titles = {product[0] for product in self.in_stock}

        for product in self.products:
            if self.init == 1 and product[0] not in in_stock_titles:
                self.in_stock.append(product)
            elif product[0] not in in_stock_titles:
                self.found_product = product
                print("%s [%s] NEW - %s" % (str(datetime.datetime.now()), self.site, self.found_product[0]))
                self.in_stock.append(product)
                self.send_webhook(False)
            elif product[0] in in_stock_titles:
                for index in range(len(self.in_stock)):
                    if product[0] == self.in_stock[index][0] and product[3] != self.in_stock[index][3]:
                        self.in_stock[index][3] = product[3]
                        self.send_webhook(True)

    def send_webhook(self, is_restock):
        webhook = DiscordWebhook(url=self.webhook)

        embed = DiscordEmbed(title=self.found_product[0], url=self.found_product[1])
        embed.set_thumbnail(url=self.found_product[2])
        embed.set_footer(text="Shopify Monitor - @v6ctor")
        embed.set_timestamp()

        embed.add_embed_field(name="Price", value=self.found_product[3][0][3], inline=False)

        if (is_restock):
            embed.add_embed_field(name="Type", value="Restock", inline=False)
        else:
            embed.add_embed_field(name="Type", value="New Product", inline=False)

        for index in range(len(self.found_product[3])):
            if (self.found_product[3][index][0]):
                embed.add_embed_field(name=self.found_product[3][index][2], value="[ATC](%scart/%s:1)" % (self.site, self.found_product[3][index][1]))

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

  
