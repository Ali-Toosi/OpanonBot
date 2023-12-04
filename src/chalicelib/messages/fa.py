from textwrap import dedent

from . import en


class Messages(en.Messages):
    start_message = dedent(
        """\
        *دریافت پیام ناشناس*
        روی /my\\_link کلیک کن، لینک ناشناست رو بگیر و بده به بقیه!

        هر وقت خسته شدی میتونی با /delete\\_link لینکت رو پاک کنی یا با /new\\_link یه لینک جدید بگیری.

        *راهنما*
        روی /help بزن تا یه سری نکته کمکی بگیری.

        *درخواست امکانات بیشتر*
        امکان دیگه‌ای هست که باید به ربات اضافه بشه؟ روی /feature بزن و بهمون بگو چی تا اضافه‌ش کنیم.
    """
    )

    help_message = (
        "*ادمین ربات پیام‌های من رو می‌بینه؟*" + "\n"
        "نه. همه چیز ناشناس و کد این ربات هم متن بازه. می‌تونین کد ربات رو اینجا ببینین:"
        + "\n"
        "[کد در گیت‌هاب](https://github.com/Ali-Toosi/OpanonBot) "
        "\n\n"
        "*چطوری یکی رو آنبلاک کنم؟*" + "\n"
        "متاسفانه وقتی یکی رو بلاک کنی دیگه نمی‌تونی آنبلاکش کنی."
        "\n\n"
        "*چطوری میشه درخواست فیچر جدید کرد؟*" + "\n"
        "با کلیک روی /feature. اگه هم برنامه‌نویس هستین و مشتاق مشارکت، لینک گیت‌هاب بالاست."
    )

    feature_request = "دوست داری چه امکانی به ربات اضافه بشه؟" + " (یا /cancel)"
    why_feature = "گرفتم. میشه یه ذره هم توضیح بدی چرا به نظرت این امکان باید اضافه بشه؟ اضافه شدنش چه کمکی می‌کنه؟"
    feature_reason_explained = "تو پیام قبلی توضیح دادم."
    empty_feature = "پیامت به نظر خالی بود. دوباره امتحان کن یا کنسل کن /cancel:"
    thank_you = "ممنون."

    all_cancelled = "کنسل شد! حالا چی؟ 👈 /start؟"

    show_link = dedent(
        """\
        هر کسی این لینک رو داشته باشه می‌تونه بهت پیام بده مگه اینکه بلاک باشه.

        می‌تونی لینکت رو با /delete\\_link پاک کنی یا با /new\\_link یه لینک جدید بگیری.

        👇 لینک ناشناس شما 👇
    """
    )

    delete_link_no_link = (
        "لینک ناشناسی برای پاک کردن نداری. میتونی با "
        + "/my\\_link"
        + " یه لینک ناشناس برای خودت بگیری"
    )
    delete_link_confirmation = (
        "مطمئنی می‌خوای لینکت رو پاک کنی؟ هیچ کس دیگه نمیتونه با این لینک بهت پیام بده"
    )
    delete_link_deleted = (
        "لینک ناشناست پاک شد! اگر خواستی می‌تونی با "
        + "/my\\_link"
        + " یه لینک جدید بگیری."
    )
    delete_link_cancelled = "حله."

    new_link_confirmation = dedent(
        """\
        درست کردن لینک جدید، لینک قبلیت رو حذف می‌کنه و دیگه ازش پیامی نمی‌گیری.

        مطمئنی می‌خوای لینک جدید درست کنی؟
    """
    )
    new_link_created = "اینم لینک جدیدت:"

    send_link_not_found = "این لینک وجود نداره."
    send_blocked = "متاسفانه بلاک شدی و نمی‌تونی به این آدم پیام بدی 😞"
    send_ask_message = "پیام ناشناست رو بفرست تا بفرستم..." + " (یا /cancel)"
    send_successful = "فرستادم براش! هر وقت جواب بده بهت خبر میدم"
    send_failed = (
        "پیامت ارسال نشد! با یه پیام دیگه امتحان کن. اگه بازم ارسال نشد یعنی احتمالا دیگه از این ربات استفاده نمیکنه"
        " و نمی‌تونه پیامی دریافت کنه."
    )

    no_self_messaging = "نمیشه به خودت پیام بفرستی! اونطوری خیلی ناشناس نمی‌مونی."
    new_anonymous_chat = "چت ناشناس حدید!"

    block_confirmation = "مطمئنی می‌خوای بلاک کنی؟ دیگه هیچ پیامی ازش نمی‌گیری!"
    user_blocked = "بلاک شد! تمام!"
    block_cancelled = "ردیفه. بلاک نمی‌کنم : )"

    unknown_message = "نمی‌دونم این پیام چیه 🤷‍♀️"
    confirmation_keyboard_ignored = "نفهمیدم! بی‌زحمت از کیبورد استفاده کن:"

    yes_delete = "آره پاک کن"
    no_cancel = "نه! لغو"
    yes_do_it = "آره!"
    yes_block = "قطعا بلاک!"
