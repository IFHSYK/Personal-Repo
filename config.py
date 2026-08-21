# ---- Welcome screen -----------------------------------------------------\
WELCOME_TEXT = "Start the bot by sending /start or click on the button!"\
\
# Set to a filename in the ./images folder, or None for no logo.\
LOGO = "logo.png"\
\
# Short line shown just above the menu buttons.\
MENU_PROMPT = "Please choose an option below \uc0\u55357 \u56391 "\
\
\
# ---- Button map ---------------------------------------------------------\
MENU = \{\
    "main": \{\
        "text": MENU_PROMPT,\
        "buttons": [\
            [\
                \{"label": "\uc0\u55356 \u57104  Website", "action": "link", "url": "https://example.com"\},\
            ],\
            [\
                \{"label": "\uc0\u8505 \u65039  Info", "action": "text",\
                 "text": "Here's how it works \'97 replace this text in config.py "\
                         "with anything you like. It can span multiple lines."\},\
            ],\
            [\
                \{"label": "\uc0\u55357 \u56764 \u65039  Promotions", "action": "image", "image": "promo.png",\
                 "caption": "Check out our latest promotion! (edit this caption in config.py)"\},\
            ],\
            [\
                \{"label": "\uc0\u55357 \u56514  More", "action": "submenu", "target": "more"\},\
                \{"label": "\uc0\u55357 \u56542  Contact Us", "action": "link", "url": "https://t.me/telegram"\},\
            ],\
        ],\
    \},\
\
    "more": \{\
        "text": "More options:",\
        "buttons": [\
            [\
                \{"label": "\uc0\u10067  FAQ", "action": "text",\
                 "text": "Frequently asked questions go here. Edit in config.py."\},\
            ],\
            [\
                \{"label": "\uc0\u55357 \u56540  Terms", "action": "text",\
                 "text": "Your terms / disclaimer text goes here."\},\
            ],\
            [\
                \{"label": "\uc0\u11013 \u65039  Back", "action": "submenu", "target": "main"\},\
            ],\
        ],\
    \},\
\}\
```\
\
}
