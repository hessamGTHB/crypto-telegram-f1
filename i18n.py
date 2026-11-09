"""
Internationalization for the bot.

Six languages are supported out of the box:
    fa (فارسی), en (English), zh (中文), ja (日本語), ko (한국어), hi (हिन्दी)

To add a new language:
    1. Add its code and display name (with flag) to `LANGUAGES`.
    2. Copy the `TEXTS["en"]` dictionary, rename it to the new code and
       translate every value. Keep the `{placeholders}` untouched.
    3. Add the language code to `SUPPORTED_LANGUAGES` in `config.py`.
    4. Optionally extend `COIN_NAMES` / `COIN_SYMBOLS` / `COIN_EMOJI`.
"""
from __future__ import annotations

LANGUAGES = {
    "fa": "🇮🇷 فارسی",
    "en": "🇺🇸 English",
    "zh": "🇨🇳 中文",
    "ja": "🇯🇵 日本語",
    "ko": "🇰🇷 한국어",
    "hi": "🇮🇳 हिन्दी",
}

DEFAULT_LANGUAGE = "fa"

TEXTS: dict[str, dict[str, str]] = {
    # =====================================================================
    "fa": {
        "welcome": (
            "👋 سلام {name}!\n"
            "من ربات قیمت ارز دیجیتال هستم و به‌صورت خودکار قیمت لحظه‌ای "
            "ارزها را در کانال شما منتشر می‌کنم.\n\n{choose}"
        ),
        "choose_language": "🌐 زبان خود را انتخاب کنید:",
        "lang_changed": "✅ زبان شما تنظیم شد: {lang}",
        "channel_lang_updated": "📢 زبان پست‌های کانال هم روی {lang} تنظیم شد.",
        "help_user": (
            "ℹ️ دستورهای موجود:\n"
            "/start — شروع و انتخاب زبان\n"
            "/help — همین راهنما\n"
            "/lang — تغییر زبان\n\n"
            "دستورهای مدیریت کانال فقط برای مدیران ربات فعال است."
        ),
        "help_admin": (
            "ℹ️ دستورهای مدیر:\n"
            "/post — ارسال فوری پست قیمت به کانال\n"
            "/coins — نمایش لیست ارزها\n"
            "/addcoin <نام یا نماد> — افزودن ارز (مثال: /addcoin bitcoin یا /addcoin BTC)\n"
            "/delcoin <نام یا نماد> — حذف ارز از لیست\n"
            "/channel @name — تنظیم کانال مقصد\n"
            "/interval <دقیقه> — تنظیم فاصله ارسال خودکار\n"
            "/lang — تغییر زبان\n"
            "/status — وضعیت ربات"
        ),
        "post_title": "قیمت لحظه‌ای ارزهای دیجیتال",
        "market_cap_total": "مارکت کپ کل",
        "source": "منبع داده",
        "msg_only_admin": "⛔ این دستور فقط برای مدیران ربات است.",
        "msg_no_channel": (
            "⚠️ هنوز کانالی تنظیم نشده است.\n"
            "با دستور /channel @ChannelName کانال مقصد را مشخص کنید.\n"
            "(ربات باید اول ادمین کانال با دسترسی ارسال پست شود)"
        ),
        "msg_channel_set": "✅ کانال {channel} تنظیم شد؛ ربات آماده ارسال است.",
        "msg_channel_fail": "❌ تنظیم کانال ناموفق بود: {error}\nمطمئن شوید ربات ادمین کانال باشد و دسترسی ارسال پست داشته باشد.",
        "msg_usage_channel": "🖊 استفاده: /channel @ChannelName",
        "msg_posted": "✅ پست قیمت با موفقیت در {channel} منتشر شد.",
        "msg_post_failed": "❌ ارسال پست ناموفق بود: {error}",
        "msg_usage_addcoin": "🖊 استفاده: /addcoin bitcoin یا /addcoin BTC",
        "msg_coin_added": "✅ {coin} به لیست اضافه شد.",
        "msg_coin_removed": "🗑 {coin} از لیست حذف شد.",
        "msg_coin_not_found": "❌ ارزی با عبارت «{query}» پیدا نشد.",
        "msg_already_added": "⚠️ این ارز از قبل در لیست هست.",
        "msg_not_in_list": "⚠️ «{query}» در لیست نیست. لیست را با /coins ببینید.",
        "msg_empty_list": "📭 لیست ارزها خالی است. با /addcoin ارز اضافه کنید.",
        "pick_coin": "🔍 چند ارز پیدا شد؛ کدام را اضافه کنم؟",
        "current_coins": "📌 ارزهای فعلی ({count}):",
        "msg_usage_interval": "🖊 استفاده: /interval 60 (بین ۱۰ تا ۱۴۴۰ دقیقه)",
        "msg_interval_set": "⏱ فاصله ارسال روی هر {minutes} دقیقه تنظیم شد؛ پست بعدی به‌زودی ارسال می‌شود.",
        "msg_usage_delcoin": "🖊 استفاده: /delcoin bitcoin",
        "max_coins_reached": "⚠️ حداکثر {max} ارز می‌توان در لیست داشت.",
        "status_title": "⚙️ وضعیت ربات:",
        "status_channel": "📢 کانال: {value}",
        "status_language": "🌐 زبان پست کانال: {value}",
        "status_interval": "⏱ فاصله ارسال: {value} دقیقه",
        "status_coins": "🪙 تعداد ارزها: {count}",
        "status_not_set": "تنظیم نشده",
        "error_generic": "😢 خطایی پیش آمد؛ لطفاً دوباره تلاش کنید.",
    },
    # =====================================================================
    "en": {
        "welcome": (
            "👋 Hi {name}!\n"
            "I'm a crypto price bot and I automatically publish live "
            "cryptocurrency prices to your Telegram channel.\n\n{choose}"
        ),
        "choose_language": "🌐 Choose your language:",
        "lang_changed": "✅ Your language is now: {lang}",
        "channel_lang_updated": "📢 The channel post language was updated to {lang} as well.",
        "help_user": (
            "ℹ️ Available commands:\n"
            "/start — start & pick a language\n"
            "/help — this help\n"
            "/lang — change language\n\n"
            "Channel management commands are available to bot admins only."
        ),
        "help_admin": (
            "ℹ️ Admin commands:\n"
            "/post — publish a price post to the channel right now\n"
            "/coins — show the coin list\n"
            "/addcoin <name or ticker> — add a coin (e.g. /addcoin bitcoin or /addcoin BTC)\n"
            "/delcoin <name or ticker> — remove a coin\n"
            "/channel @name — set the target channel\n"
            "/interval <minutes> — auto-posting interval\n"
            "/lang — change language\n"
            "/status — bot status"
        ),
        "post_title": "Live Crypto Prices",
        "market_cap_total": "Total Market Cap",
        "source": "Data",
        "msg_only_admin": "⛔ This command is for bot admins only.",
        "msg_no_channel": (
            "⚠️ No channel is set yet.\n"
            "Use /channel @ChannelName to set the target channel.\n"
            "(the bot must first be added as a channel admin with post permission)"
        ),
        "msg_channel_set": "✅ Channel {channel} is set — the bot is ready to post.",
        "msg_channel_fail": "❌ Could not set the channel: {error}\nMake sure the bot is a channel admin with post permission.",
        "msg_usage_channel": "🖊 Usage: /channel @ChannelName",
        "msg_posted": "✅ Price post published to {channel}.",
        "msg_post_failed": "❌ Failed to post: {error}",
        "msg_usage_addcoin": "🖊 Usage: /addcoin bitcoin or /addcoin BTC",
        "msg_coin_added": "✅ {coin} added to the list.",
        "msg_coin_removed": "🗑 {coin} removed from the list.",
        "msg_coin_not_found": "❌ No coin found for “{query}”.",
        "msg_already_added": "⚠️ This coin is already in the list.",
        "msg_not_in_list": "⚠️ “{query}” is not in the list. See /coins.",
        "msg_empty_list": "📭 The coin list is empty. Add coins with /addcoin.",
        "pick_coin": "🔍 Several coins found — which one should I add?",
        "current_coins": "📌 Current coins ({count}):",
        "msg_usage_interval": "🖊 Usage: /interval 60 (10–1440 minutes)",
        "msg_interval_set": "⏱ Posting interval set to {minutes} minutes. The next post is coming shortly.",
        "msg_usage_delcoin": "🖊 Usage: /delcoin bitcoin",
        "max_coins_reached": "⚠️ The list can hold at most {max} coins.",
        "status_title": "⚙️ Bot status:",
        "status_channel": "📢 Channel: {value}",
        "status_language": "🌐 Channel post language: {value}",
        "status_interval": "⏱ Posting interval: {value} min",
        "status_coins": "🪙 Coins: {count}",
        "status_not_set": "not set",
        "error_generic": "😢 Something went wrong. Please try again.",
    },
    # =====================================================================
    "zh": {
        "welcome": (
            "👋 你好 {name}！\n"
            "我是加密货币价格机器人，会自动向你的 Telegram 频道发布实时价格。\n\n{choose}"
        ),
        "choose_language": "🌐 请选择你的语言：",
        "lang_changed": "✅ 你的语言已设置为：{lang}",
        "channel_lang_updated": "📢 频道帖子的语言也已更新为 {lang}。",
        "help_user": (
            "ℹ️ 可用命令：\n"
            "/start — 启动并选择语言\n"
            "/help — 帮助\n"
            "/lang — 更改语言\n\n"
            "频道管理命令仅限机器人管理员使用。"
        ),
        "help_admin": (
            "ℹ️ 管理员命令：\n"
            "/post — 立即向频道发布价格\n"
            "/coins — 查看币种列表\n"
            "/addcoin <名称或代码> — 添加币种（例：/addcoin bitcoin）\n"
            "/delcoin <名称或代码> — 删除币种\n"
            "/channel @name — 设置目标频道\n"
            "/interval <分钟> — 设置发布间隔\n"
            "/lang — 更改语言\n"
            "/status — 机器人状态"
        ),
        "post_title": "加密货币实时价格",
        "market_cap_total": "总市值",
        "source": "数据来源",
        "msg_only_admin": "⛔ 该命令仅限管理员使用。",
        "msg_no_channel": (
            "⚠️ 尚未设置频道。\n"
            "请使用 /channel @频道名称 设置目标频道。\n"
            "（机器人必须是频道管理员并拥有发帖权限）"
        ),
        "msg_channel_set": "✅ 频道 {channel} 设置成功，机器人已准备就绪。",
        "msg_channel_fail": "❌ 频道设置失败：{error}\n请确保机器人是频道管理员并拥有发帖权限。",
        "msg_usage_channel": "🖊 用法：/channel @频道名称",
        "msg_posted": "✅ 价格帖已发布到 {channel}。",
        "msg_post_failed": "❌ 发布失败：{error}",
        "msg_usage_addcoin": "🖊 用法：/addcoin bitcoin 或 /addcoin BTC",
        "msg_coin_added": "✅ 已添加 {coin}。",
        "msg_coin_removed": "🗑 已移除 {coin}。",
        "msg_coin_not_found": "❌ 未找到“{query}”对应的币种。",
        "msg_already_added": "⚠️ 该币种已在列表中。",
        "msg_not_in_list": "⚠️ “{query}”不在列表中。请查看 /coins。",
        "msg_empty_list": "📭 币种列表为空。请使用 /addcoin 添加。",
        "pick_coin": "🔍 找到多个币种，请选择要添加的：",
        "current_coins": "📌 当前币种（{count}）：",
        "msg_usage_interval": "🖊 用法：/interval 60（10–1440 分钟）",
        "msg_interval_set": "⏱ 发布间隔已设置为 {minutes} 分钟，稍后将立即发布一帖。",
        "msg_usage_delcoin": "🖊 用法：/delcoin bitcoin",
        "max_coins_reached": "⚠️ 列表最多可容纳 {max} 个币种。",
        "status_title": "⚙️ 机器人状态：",
        "status_channel": "📢 频道：{value}",
        "status_language": "🌐 频道帖子语言：{value}",
        "status_interval": "⏱ 发布间隔：{value} 分钟",
        "status_coins": "🪙 币种数量：{count}",
        "status_not_set": "未设置",
        "error_generic": "😢 出错了，请重试。",
    },
    # =====================================================================
    "ja": {
        "welcome": (
            "👋 こんにちは {name}！\n"
            "私は暗号資産価格ボットです。あなたのTelegramチャンネルへ"
            "リアルタイムの価格を自動投稿します。\n\n{choose}"
        ),
        "choose_language": "🌐 言語を選んでください：",
        "lang_changed": "✅ 言語を設定しました：{lang}",
        "channel_lang_updated": "📢 チャンネル投稿の言語も {lang} に更新されました。",
        "help_user": (
            "ℹ️ 使えるコマンド：\n"
            "/start — 開始と言語選択\n"
            "/help — ヘルプ\n"
            "/lang — 言語変更\n\n"
            "チャンネル管理コマンドは管理者のみ使用できます。"
        ),
        "help_admin": (
            "ℹ️ 管理者コマンド：\n"
            "/post — 価格を今すぐ投稿\n"
            "/coins — コイン一覧を表示\n"
            "/addcoin <名前/ティッカー> — コインを追加（例：/addcoin bitcoin）\n"
            "/delcoin <名前/ティッカー> — コインを削除\n"
            "/channel @name — 投稿先チャンネルを設定\n"
            "/interval <分> — 投稿間隔を設定\n"
            "/lang — 言語変更\n"
            "/status — ボットの状態"
        ),
        "post_title": "暗号資産のリアルタイム価格",
        "market_cap_total": "総時価総額",
        "source": "データ",
        "msg_only_admin": "⛔ このコマンドは管理者専用です。",
        "msg_no_channel": (
            "⚠️ チャンネルが未設定です。\n"
            "/channel @チャンネル名 で設定してください。\n"
            "（ボットをチャンネルの管理者にして投稿権限を与えてください）"
        ),
        "msg_channel_set": "✅ チャンネル {channel} を設定しました。投稿準備完了です。",
        "msg_channel_fail": "❌ チャンネルを設定できません：{error}\nボットがチャンネルの管理者で投稿権限を持っているか確認してください。",
        "msg_usage_channel": "🖊 使い方：/channel @チャンネル名",
        "msg_posted": "✅ 価格ポストを {channel} に投稿しました。",
        "msg_post_failed": "❌ 投稿に失敗しました：{error}",
        "msg_usage_addcoin": "🖊 使い方：/addcoin bitcoin または /addcoin BTC",
        "msg_coin_added": "✅ {coin} を追加しました。",
        "msg_coin_removed": "🗑 {coin} を削除しました。",
        "msg_coin_not_found": "❌「{query}」に一致するコインが見つかりません。",
        "msg_already_added": "⚠️ このコインは既にリストに入っています。",
        "msg_not_in_list": "⚠️「{query}」はリストにありません。/coins をご覧ください。",
        "msg_empty_list": "📭 コインリストが空です。/addcoin で追加してください。",
        "pick_coin": "🔍 複数見つかりました。どれを追加しますか？",
        "current_coins": "📌 現在のコイン（{count}）：",
        "msg_usage_interval": "🖊 使い方：/interval 60（10〜1440 分）",
        "msg_interval_set": "⏱ 投稿間隔を {minutes} 分に設定しました。まもなく投稿します。",
        "msg_usage_delcoin": "🖊 使い方：/delcoin bitcoin",
        "max_coins_reached": "⚠️ リストには最大 {max} コインまで登録できます。",
        "status_title": "⚙️ ボットの状態：",
        "status_channel": "📢 チャンネル：{value}",
        "status_language": "🌐 投稿の言語：{value}",
        "status_interval": "⏱ 投稿間隔：{value} 分",
        "status_coins": "🪙 コイン数：{count}",
        "status_not_set": "未設定",
        "error_generic": "😢 エラーが発生しました。もう一度お試しください。",
    },
    # =====================================================================
    "ko": {
        "welcome": (
            "👋 안녕하세요 {name}님!\n"
            "저는 암호화폐 시세 봇입니다. 텔레그램 채널에 실시간 가격을 "
            "자동으로 게시합니다.\n\n{choose}"
        ),
        "choose_language": "🌐 언어를 선택하세요:",
        "lang_changed": "✅ 언어가 설정되었습니다: {lang}",
        "channel_lang_updated": "📢 채널 게시물 언어도 {lang}(으)로 변경되었습니다.",
        "help_user": (
            "ℹ️ 사용 가능한 명령어:\n"
            "/start — 시작 및 언어 선택\n"
            "/help — 도움말\n"
            "/lang — 언어 변경\n\n"
            "채널 관리 명령어는 봇 관리자만 사용할 수 있습니다."
        ),
        "help_admin": (
            "ℹ️ 관리자 명령어:\n"
            "/post — 지금 시세 게시\n"
            "/coins — 코인 목록 보기\n"
            "/addcoin <이름/티커> — 코인 추가 (예: /addcoin bitcoin)\n"
            "/delcoin <이름/티커> — 코인 삭제\n"
            "/channel @name — 대상 채널 설정\n"
            "/interval <분> — 게시 간격 설정\n"
            "/lang — 언어 변경\n"
            "/status — 봇 상태"
        ),
        "post_title": "암호화폐 실시간 시세",
        "market_cap_total": "총 시가총액",
        "source": "데이터",
        "msg_only_admin": "⛔ 이 명령어는 관리자 전용입니다.",
        "msg_no_channel": (
            "⚠️ 아직 채널이 설정되지 않았습니다.\n"
            "/channel @채널명 으로 대상 채널을 설정해 주세요.\n"
            "(봇이 채널 관리자이며 게시 권한이 있어야 합니다)"
        ),
        "msg_channel_set": "✅ 채널 {channel} 이(가) 설정되었습니다. 게시할 준비가 완료되었습니다.",
        "msg_channel_fail": "❌ 채널 설정 실패: {error}\n봇이 채널 관리자이며 게시 권한이 있는지 확인해 주세요.",
        "msg_usage_channel": "🖊 사용법: /channel @채널명",
        "msg_posted": "✅ 시세 게시물을 {channel} 에 게시했습니다.",
        "msg_post_failed": "❌ 게시 실패: {error}",
        "msg_usage_addcoin": "🖊 사용법: /addcoin bitcoin 또는 /addcoin BTC",
        "msg_coin_added": "✅ {coin} 을(를) 추가했습니다.",
        "msg_coin_removed": "🗑 {coin} 을(를) 삭제했습니다.",
        "msg_coin_not_found": "❌ “{query}”에 해당하는 코인을 찾을 수 없습니다.",
        "msg_already_added": "⚠️ 이 코인은 이미 목록에 있습니다.",
        "msg_not_in_list": "⚠️ “{query}”은(는) 목록에 없습니다. /coins 를 확인하세요.",
        "msg_empty_list": "📭 코인 목록이 비어 있습니다. /addcoin 으로 추가하세요.",
        "pick_coin": "🔍 여러 개가 검색되었습니다. 어떤 것을 추가할까요?",
        "current_coins": "📌 현재 코인 ({count}):",
        "msg_usage_interval": "🖊 사용법: /interval 60 (10–1440분)",
        "msg_interval_set": "⏱ 게시 간격이 {minutes}분으로 설정되었습니다. 곧 게시됩니다.",
        "msg_usage_delcoin": "🖊 사용법: /delcoin bitcoin",
        "max_coins_reached": "⚠️ 목록에는 최대 {max}개의 코인을 등록할 수 있습니다.",
        "status_title": "⚙️ 봇 상태:",
        "status_channel": "📢 채널: {value}",
        "status_language": "🌐 게시 언어: {value}",
        "status_interval": "⏱ 게시 간격: {value}분",
        "status_coins": "🪙 코인 수: {count}",
        "status_not_set": "설정 안 됨",
        "error_generic": "😢 오류가 발생했습니다. 다시 시도해 주세요.",
    },
    # =====================================================================
    "hi": {
        "welcome": (
            "👋 नमस्ते {name}!\n"
            "मैं क्रिप्टो कीमत बॉट हूँ और आपके Telegram चैनल पर लाइव "
            "कीमतें अपने आप पोस्ट करता हूँ।\n\n{choose}"
        ),
        "choose_language": "🌐 अपनी भाषा चुनें:",
        "lang_changed": "✅ आपकी भाषा अब: {lang}",
        "channel_lang_updated": "📢 चैनल पोस्ट की भाषा भी {lang} कर दी गई है।",
        "help_user": (
            "ℹ️ उपलब्ध कमांड:\n"
            "/start — शुरू करें और भाषा चुनें\n"
            "/help — सहायता\n"
            "/lang — भाषा बदलें\n\n"
            "चैनल प्रबंधन कमांड केवल बॉट एडमिन के लिए हैं।"
        ),
        "help_admin": (
            "ℹ️ एडमिन कमांड:\n"
            "/post — अभी कीमतें पोस्ट करें\n"
            "/coins — कॉइन सूची देखें\n"
            "/addcoin <नाम/टिकर> — कॉइन जोड़ें (जैसे: /addcoin bitcoin)\n"
            "/delcoin <नाम/टिकر> — कॉइन हटाएँ\n"
            "/channel @name — लक्ष्य चैनल सेट करें\n"
            "/interval <मिनट> — पोस्ट अंतराल सेट करें\n"
            "/lang — भाषा बदलें\n"
            "/status — बॉट स्थिति"
        ),
        "post_title": "क्रिप्टो लाइव कीमतें",
        "market_cap_total": "कुल बाज़ार पूँजी",
        "source": "डेटा",
        "msg_only_admin": "⛔ यह कमांड केवल एडमिन के लिए है।",
        "msg_no_channel": (
            "⚠️ अभी कोई चैनल सेट नहीं है।\n"
            "/channel @चैनलनाम से लक्ष्य चैनल सेट करें।\n"
            "(बॉट को चैनल एडमिन और पोस्ट अनुमति की आवश्यकता है)"
        ),
        "msg_channel_set": "✅ चैनल {channel} सेट हो गया — बॉट पोस्ट के लिए तैयार है।",
        "msg_channel_fail": "❌ चैनल सेट नहीं हो सका: {error}\nसुनिश्चित करें कि बॉट चैनल का एडमिन है और उसे पोस्ट की अनुमति है।",
        "msg_usage_channel": "🖊 उपयोग: /channel @चैनलनाम",
        "msg_posted": "✅ कीमत पोस्ट {channel} पर प्रकाशित हुई।",
        "msg_post_failed": "❌ पोस्ट विफल: {error}",
        "msg_usage_addcoin": "🖊 उपयोग: /addcoin bitcoin या /addcoin BTC",
        "msg_coin_added": "✅ {coin} सूची में जोड़ा गया।",
        "msg_coin_removed": "🗑 {coin} सूची से हटाया गया।",
        "msg_coin_not_found": "❌ “{query}” से मेल खाता कोई कॉइन नहीं मिला।",
        "msg_already_added": "⚠️ यह कॉइन पहले से सूची में है।",
        "msg_not_in_list": "⚠️ “{query}” सूची में नहीं है। /coins देखें।",
        "msg_empty_list": "📭 कॉइन सूची खाली है। /addcoin से जोड़ें।",
        "pick_coin": "🔍 कई कॉइन मिले — कौन सा जोड़ूँ?",
        "current_coins": "📌 वर्तमान कॉइन ({count}):",
        "msg_usage_interval": "🖊 उपयोग: /interval 60 (10–1440 मिनट)",
        "msg_interval_set": "⏱ पोस्ट अंतराल {minutes} मिनट सेट हुआ। पोस्ट जल्दी आएगी।",
        "msg_usage_delcoin": "🖊 उपयोग: /delcoin bitcoin",
        "max_coins_reached": "⚠️ सूची में अधिकतम {max} कॉइन रखे जा सकते हैं।",
        "status_title": "⚙️ बॉट स्थिति:",
        "status_channel": "📢 चैनल: {value}",
        "status_language": "🌐 चैनल पोस्ट भाषा: {value}",
        "status_interval": "⏱ पोस्ट अंतराल: {value} मिनट",
        "status_coins": "🪙 कॉइन: {count}",
        "status_not_set": "सेट नहीं",
        "error_generic": "😢 कुछ गड़बड़ हुई। कृपया फिर कोशिश करें।",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Translate `key` into `lang` (English fallback), applying placeholders."""
    text = TEXTS.get(lang, TEXTS[DEFAULT_LANGUAGE]).get(key)
    if not text:
        text = TEXTS[DEFAULT_LANGUAGE][key]
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


# ---------------------------------------------------------------------------
# Coin metadata (localized names for popular coins; English fallback)
# ---------------------------------------------------------------------------

COIN_NAMES: dict[str, dict[str, str]] = {
    "bitcoin":     {"fa": "بیت‌کوین",     "en": "Bitcoin",   "zh": "比特币",     "ja": "ビットコイン",     "ko": "비트코인",   "hi": "बिटकॉइन"},
    "ethereum":    {"fa": "اتریوم",       "en": "Ethereum",  "zh": "以太坊",     "ja": "イーサリアム",     "ko": "이더리움",   "hi": "इथीरियम"},
    "tether":      {"fa": "تتر",          "en": "Tether",    "zh": "泰达币",     "ja": "テザー",           "ko": "테더",       "hi": "टेथर"},
    "binancecoin": {"fa": "بایننس کوین",  "en": "BNB",       "zh": "币安币",     "ja": "BNB",              "ko": "BNB",        "hi": "BNB"},
    "solana":      {"fa": "سولانا",       "en": "Solana",    "zh": "Solana",     "ja": "Solana",           "ko": "솔라나",     "hi": "सोलाना"},
    "ripple":      {"fa": "ریپل",         "en": "XRP",       "zh": "瑞波币",     "ja": "XRP",              "ko": "리플",       "hi": "रिपल"},
    "cardano":     {"fa": "کاردانو",      "en": "Cardano",   "zh": "卡尔达诺",   "ja": "カルダノ",         "ko": "카르다노",   "hi": "कार्डानो"},
    "dogecoin":    {"fa": "دوج‌کوین",     "en": "Dogecoin",  "zh": "狗狗币",     "ja": "ドージコイン",     "ko": "도지코인",   "hi": "डॉजकॉइन"},
    "tron":        {"fa": "ترون",          "en": "TRON",      "zh": "波场",       "ja": "トロン",           "ko": "트론",       "hi": "ट्रॉन"},
    "shiba-inu":   {"fa": "شیبا اینو",    "en": "Shiba Inu", "zh": "柴犬币",     "ja": "シバ・イヌ",       "ko": "시바이누",   "hi": "शिबा इनु"},
    "toncoin":     {"fa": "تون‌کوین",     "en": "Toncoin",   "zh": "Toncoin",    "ja": "Toncoin",          "ko": "탱코인",     "hi": "टॉनकॉइन"},
    "chainlink":   {"fa": "چین‌لینک",     "en": "Chainlink", "zh": "Chainlink",  "ja": "チェーンリンク",   "ko": "체인링크",   "hi": "चेनलिंक"},
    "litecoin":    {"fa": "لایت‌کوین",    "en": "Litecoin",  "zh": "莱特币",     "ja": "ライトコイン",     "ko": "라이트코인", "hi": "लाइटकॉइन"},
    "polkadot":    {"fa": "پولکادات",     "en": "Polkadot",  "zh": "波卡",       "ja": "ポルカドット",     "ko": "폴카닷",     "hi": "पोलकाडॉट"},
    "avalanche-2": {"fa": "آوالانچ",      "en": "Avalanche", "zh": "雪崩协议",   "ja": "アバランチ",       "ko": "아발란체",   "hi": "अवालांच"},
    "usd-coin":    {"fa": "یو‌اس‌دی کوین","en": "USDC",      "zh": "USDC",       "ja": "USDC",             "ko": "USDC",       "hi": "USDC"},
    "near":        {"fa": "نیر پروتکل",   "en": "NEAR",      "zh": "NEAR",       "ja": "NEAR",             "ko": "니어",       "hi": "नियर"},
    "uniswap":     {"fa": "یونی‌سواپ",    "en": "Uniswap",   "zh": "Uniswap",    "ja": "Uniswap",          "ko": "유니스왑",   "hi": "यूनिस्वैप"},
    "aptos":       {"fa": "اپتوس",        "en": "Aptos",     "zh": "Aptos",      "ja": "Aptos",            "ko": "아프토스",   "hi": "एप्टोस"},
    "stellar":     {"fa": "استلار",       "en": "Stellar",   "zh": "恒星币",     "ja": "ステラー",         "ko": "스텔라",     "hi": "स्टेलर"},
}

COIN_SYMBOLS: dict[str, str] = {
    "bitcoin": "BTC", "ethereum": "ETH", "tether": "USDT", "binancecoin": "BNB",
    "solana": "SOL", "ripple": "XRP", "cardano": "ADA", "dogecoin": "DOGE",
    "tron": "TRX", "shiba-inu": "SHIB", "toncoin": "TON", "chainlink": "LINK",
    "litecoin": "LTC", "polkadot": "DOT", "avalanche-2": "AVAX", "usd-coin": "USDC",
    "near": "NEAR", "uniswap": "UNI", "aptos": "APT", "stellar": "XLM",
}

COIN_EMOJI: dict[str, str] = {
    "btc": "₿", "eth": "Ξ", "bnb": "🟡", "sol": "◎", "xrp": "✕", "doge": "Ð",
    "ada": "₳", "ltc": "Ł", "dot": "●", "trx": "🔺", "ton": "💎", "link": "🔗",
    "shib": "🐶", "usdt": "💵", "usdc": "💵", "avax": "🔺", "near": "🌙",
    "uni": "🦄", "apt": "🟪", "xlm": "★",
}


def coin_name(coin_id: str, lang: str, fallback: str | None = None) -> str:
    """Localized coin display name; falls back to English name or the id."""
    entry = COIN_NAMES.get(coin_id)
    if entry:
        return entry.get(lang) or entry["en"]
    return fallback or coin_id
