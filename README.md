# Monitors
Includes a bundle of product monitoring scripts for popular retail sites like Shopify. 
May not work on all sites and (at the moment) does not support Cloudflare protected domains.

## Disclaimer
For educational purposes only. The maintainers do not endorse, support, or promote the use of this code for any activities that violate the terms of service of any websites or applications.

## Getting Started
1. Clone the repository with `git clone https://github.com/v6ctor/monitors`
2. Navigate into the cloned directory
3. Install dependencies with `pip install requirements.txt` or `pip3 install requirements.txt`
4. Add sites, webhooks, delay to config.json 
    - One webhook per site
    - Delay is used globally

## To Do
- [x] Support product restock alerts
- [ ] Simplify config.json user readability
- [ ] Improve error logging and handling
- [ ] Node JS refactor with accompanying user dashboard
