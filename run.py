import os\
from pathlib import Path\
from dotenv import load_dotenv\
import bot as menu_bot\
\
load_dotenv(Path(__file__).parent / ".env")\
\
if __name__ == "__main__":\
    token = os.environ["TELEGRAM_TOKEN"]\
    application = menu_bot.build_application(token)\
    application.run_polling(drop_pending_updates=True)\
```\
}
