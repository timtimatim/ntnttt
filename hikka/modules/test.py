import inspect
import logging
import os
import random
import time
from io import BytesIO
import typing

from telethon.tl.types import Message

from .. import loader, main, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

DEBUG_MODS_DIR = os.path.join(utils.get_base_dir(), "debug_modules")

if not os.path.isdir(DEBUG_MODS_DIR):
    os.mkdir(DEBUG_MODS_DIR, mode=0o755)

for mod in os.scandir(DEBUG_MODS_DIR):
    os.remove(mod.path)


@loader.tds
class TestMod(loader.Module):
    """Perform operations based on userbot self-testing"""

    _memory = {}

    strings = {
        "name": "Tester",
        "set_loglevel": "đĢ <b>Please specify verbosity as an integer or string</b>",
        "no_logs": "âšī¸ <b>You don't have any logs at verbosity {}.</b>",
        "logs_filename": "Bampi-logs.txt",
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Bampi logs with"
            " verbosity </b><code>{}</code>\n\n<emoji"
            " document_id=5454390891466726015>đ</emoji> <b>Bampi version:"
            " {}.{}.{}</b>{}\n<emoji document_id=6321050180095313397>âą</emoji>"
            " <b>Uptime: {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{}"
            " InlineLogs</b>"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>Invalid time to"
            " suspend</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot suspended"
            " for</b> <code>{}</code> <b>seconds</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>Telegram ping:</b>"
            " <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>Uptime: {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>Telegram ping mostly"
            " depends on Telegram servers latency and other external factors and has"
            " nothing to do with the parameters of server on which userbot is"
            " installed</i>"
        ),
        "confidential": (
            "â ī¸ <b>Log level </b><code>{}</code><b> may reveal your confidential info,"
            " be careful</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Log level </b><code>{0}</code><b> may reveal your confidential info,"
            " be careful</b>\n<b>Type </b><code>.logs {0} force_insecure</code><b> to"
            " ignore this warning</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Choose log level</b>",
        "bad_module": "đĢ <b>Module not found</b>",
        "debugging_enabled": (
            "đ§âđģ <b>Debugging mode enabled for module </b><code>{0}</code>\n<i>Go to"
            " directory named `debug_modules`, edit file named `{0}.py` and see changes"
            " in real time</i>"
        ),
        "debugging_disabled": "â <b>Debugging disabled</b>",
        "send_anyway": "đ¤ Send anyway",
        "cancel": "đĢ Cancel",
    }

    strings_ru = {
        "set_loglevel": "đĢ <b>ĐŖĐēĐ°ĐļĐ¸ ŅŅĐžĐ˛ĐĩĐŊŅ ĐģĐžĐŗĐžĐ˛ ŅĐ¸ŅĐģĐžĐŧ Đ¸ĐģĐ¸ ŅŅŅĐžĐēĐžĐš</b>",
        "no_logs": "âšī¸ <b>ĐŖ ŅĐĩĐąŅ ĐŊĐĩŅ ĐģĐžĐŗĐžĐ˛ ŅŅĐžĐ˛ĐŊŅ {}.</b>",
        "logs_filename": "Bampi-logs.txt",
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>ĐĐžĐŗĐ¸ Bampi ŅŅĐžĐ˛ĐŊŅ"
            " </b><code>{}</code>\n\n<emoji document_id=5454390891466726015>đ</emoji>"
            " <b>ĐĐĩŅŅĐ¸Ņ Bampi: {}.{}.{}</b>{}\n<emoji"
            " document_id=6321050180095313397>âą</emoji> <b>Uptime:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{}"
            " InlineLogs</b>"
        ),
        "bad_module": "đĢ <b>ĐĐžĐ´ŅĐģŅ ĐŊĐĩ ĐŊĐ°ĐšĐ´ĐĩĐŊ</b>",
        "debugging_enabled": (
            "đ§âđģ <b>Đ ĐĩĐļĐ¸Đŧ ŅĐ°ĐˇŅĐ°ĐąĐžŅŅĐ¸ĐēĐ° Đ˛ĐēĐģŅŅĐĩĐŊ Đ´ĐģŅ ĐŧĐžĐ´ŅĐģŅ"
            " </b><code>{0}</code>\n<i>ĐŅĐŋŅĐ°Đ˛ĐģŅĐšŅŅ Đ˛ Đ´Đ¸ŅĐĩĐēŅĐžŅĐ¸Ņ `debug_modules`,"
            " Đ¸ĐˇĐŧĐĩĐŊŅĐš ŅĐ°ĐšĐģ `{0}.py`, Đ¸ ŅĐŧĐžŅŅĐ¸ Đ¸ĐˇĐŧĐĩĐŊĐĩĐŊĐ¸Ņ Đ˛ ŅĐĩĐļĐ¸ĐŧĐĩ ŅĐĩĐ°ĐģŅĐŊĐžĐŗĐž Đ˛ŅĐĩĐŧĐĩĐŊĐ¸</i>"
        ),
        "debugging_disabled": "â <b>Đ ĐĩĐļĐ¸Đŧ ŅĐ°ĐˇŅĐ°ĐąĐžŅŅĐ¸ĐēĐ° Đ˛ŅĐēĐģŅŅĐĩĐŊ</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>ĐĐĩĐ˛ĐĩŅĐŊĐžĐĩ Đ˛ŅĐĩĐŧŅ"
            " ĐˇĐ°ĐŧĐžŅĐžĐˇĐēĐ¸</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>ĐĐžŅ ĐˇĐ°ĐŧĐžŅĐžĐļĐĩĐŊ ĐŊĐ°</b>"
            " <code>{}</code> <b>ŅĐĩĐēŅĐŊĐ´</b>"
        ),
        "results_ping": (
            "<emoji document_id=5370869711888194012>đž</emoji><b>Bampi ĐŋĐ¸ĐŊĐŗ:</b> <code>"
            "</b> <code>{}</code> <b>ms</b>\n<emoji"
            "</b><emoji document_id=5469741319330996757>đĢ</emoji><b>ĐĐŋŅĐ°ĐšĐŧ:"
            " {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>ĐĄĐēĐžŅĐžŅŅŅ ĐžŅĐēĐģĐ¸ĐēĐ°"
            " Telegram Đ˛ ĐąĐžĐģŅŅĐĩĐš ŅŅĐĩĐŋĐĩĐŊĐ¸ ĐˇĐ°Đ˛Đ¸ŅĐ¸Ņ ĐžŅ ĐˇĐ°ĐŗŅŅĐļĐĩĐŊĐŊĐžŅŅĐ¸ ŅĐĩŅĐ˛ĐĩŅĐžĐ˛ Telegram Đ¸"
            " Đ´ŅŅĐŗĐ¸Ņ Đ˛ĐŊĐĩŅĐŊĐ¸Ņ ŅĐ°ĐēŅĐžŅĐžĐ˛ Đ¸ ĐŊĐ¸ĐēĐ°Đē ĐŊĐĩ ŅĐ˛ŅĐˇĐ°ĐŊĐ° Ņ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐ°ĐŧĐ¸ ŅĐĩŅĐ˛ĐĩŅĐ°, ĐŊĐ°"
            " ĐēĐžŅĐžŅŅĐš ŅŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊ ŅĐˇĐĩŅĐąĐžŅ</i>"
        ),
        "confidential": (
            "â ī¸ <b>ĐŖŅĐžĐ˛ĐĩĐŊŅ ĐģĐžĐŗĐžĐ˛ </b><code>{}</code><b> ĐŧĐžĐļĐĩŅ ŅĐžĐ´ĐĩŅĐļĐ°ŅŅ ĐģĐ¸ŅĐŊŅŅ"
            " Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ, ĐąŅĐ´Ņ ĐžŅŅĐžŅĐžĐļĐĩĐŊ</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>ĐŖŅĐžĐ˛ĐĩĐŊŅ ĐģĐžĐŗĐžĐ˛ </b><code>{0}</code><b> ĐŧĐžĐļĐĩŅ ŅĐžĐ´ĐĩŅĐļĐ°ŅŅ ĐģĐ¸ŅĐŊŅŅ"
            " Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ, ĐąŅĐ´Ņ ĐžŅŅĐžŅĐžĐļĐĩĐŊ</b>\n<b>ĐĐ°ĐŋĐ¸ŅĐ¸ </b><code>.logs {0}"
            " force_insecure</code><b>, ŅŅĐžĐąŅ ĐžŅĐŋŅĐ°Đ˛Đ¸ŅŅ ĐģĐžĐŗĐ¸ Đ¸ĐŗĐŊĐžŅĐ¸ŅŅŅ"
            " ĐŋŅĐĩĐ´ŅĐŋŅĐĩĐļĐ´ĐĩĐŊĐ¸Đĩ</b>"
        ),
        "choose_loglevel": "đââī¸ <b>ĐŅĐąĐĩŅĐ¸ ŅŅĐžĐ˛ĐĩĐŊŅ ĐģĐžĐŗĐžĐ˛</b>",
        "_cmd_doc_dump": "ĐĐžĐēĐ°ĐˇĐ°ŅŅ Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ Đž ŅĐžĐžĐąŅĐĩĐŊĐ¸Đ¸",
        "_cmd_doc_logs": (
            "<ŅŅĐžĐ˛ĐĩĐŊŅ> - ĐŅĐŋŅĐ°Đ˛ĐģŅĐĩŅ ĐģĐžĐŗ-ŅĐ°ĐšĐģ. ĐŖŅĐžĐ˛ĐŊĐ¸ ĐŊĐ¸ĐļĐĩ WARNING ĐŧĐžĐŗŅŅ ŅĐžĐ´ĐĩŅĐļĐ°ŅŅ"
            " ĐģĐ¸ŅĐŊŅŅ Đ¸ĐŊŅĐžĐŧŅĐ°ŅĐ¸Ņ."
        ),
        "_cmd_doc_suspend": "<Đ˛ŅĐĩĐŧŅ> - ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅŅ ĐąĐžŅĐ° ĐŊĐ° ĐŊĐĩĐēĐžŅĐžŅĐžĐĩ Đ˛ŅĐĩĐŧŅ",
        "_cmd_doc_ping": "ĐŅĐžĐ˛ĐĩŅŅĐĩŅ ŅĐēĐžŅĐžŅŅŅ ĐžŅĐēĐģĐ¸ĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°",
        "_cls_doc": "ĐĐŋĐĩŅĐ°ŅĐ¸Đ¸, ŅĐ˛ŅĐˇĐ°ĐŊĐŊŅĐĩ Ņ ŅĐ°ĐŧĐžŅĐĩŅŅĐ¸ŅĐžĐ˛Đ°ĐŊĐ¸ĐĩĐŧ",
        "send_anyway": "đ¤ ĐŅĐĩ ŅĐ°Đ˛ĐŊĐž ĐžŅĐŋŅĐ°Đ˛Đ¸ŅŅ",
        "cancel": "đĢ ĐŅĐŧĐĩĐŊĐ°",
    }

    strings_de = {
        "set_loglevel": (
            "đĢ <b>Geben Sie die Protokollebene als Zahl oder Zeichenfolge an</b>"
        ),
        "no_logs": "âšī¸ <b>Du hast kein Protokollnachrichten des {} Ebene.</b>",
        "logs_filename": "Bampi-logs.txt",
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Bampi-Level-Protokolle"
            " </b><code>{}</code>\n\n<emoji document_id=5454390891466726015>đ</emoji>"
            " <b>Bampi-Version: {}.{}.{}</b>{}\n<Emoji"
            "document_id=6321050180095313397>âą</emoji> <b>VerfÃŧgbarkeit:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "bad_module": "đĢ <b>Modul nicht gefunden</b>",
        "debugging_enabled": (
            (
                "đ§âđģ <b>Entwicklermodus fÃŧr Modul aktiviert"
                " </b><code>{0}</code>\n<i>Gehe zum Verzeichnis `debug_modules`"
            ),
            (
                "Ãndern Sie die `{0}.py`-Datei und sehen Sie sich die Ãnderungen in"
                " Echtzeit an</i>"
            ),
        ),
        "debugging_disabled": "â <b>Entwicklermodus deaktiviert</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>Falsche Zeit"
            "einfrieren</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot ist"
            " eingefroren</b> <code>{}</code> <b>Sekunden</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>Reaktionszeit des"
            " Telegram:</b> <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>Zeit seit dem letzten"
            " Neustart: {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji>"
            " <i>ReaktionsfÃ¤higkeitTelegram ist stÃ¤rker abhÃ¤ngig von der Auslastung der"
            " Telegram-Server undAndere externe Faktoren und steht in keinem"
            " Zusammenhang mit den Servereinstellungen welcher Userbot installiert"
            " ist</i>"
        ),
        "confidential": (
            "â ī¸ <b>Protokollebene </b><code>{}</code><b> kann privat enthalten"
            "Informationen, seien Sie vorsichtig</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Protokollebene </b><code>{0}</code><b> kann privat"
            " enthaltenInformationen, seien Sie vorsichtig</b>\n<b>Schreiben Sie"
            " </b><code>.logs {0} force_insecure</code><b> um Protokolle zu"
            " ignorierenWarnung</b>"
        ),
        "choose_loglevel": "đââī¸ <b>WÃ¤hle eine Protokollebene</b>",
        "_cmd_doc_dump": "Nachrichteninformationen anzeigen",
        "_cmd_doc_logs": (
            "<Ebene> - Sendet eine Protokolldatei. Ebenen unterhalb von WARNUNG kÃļnnen"
            " enthaltenpersÃļnliche Informationen."
        ),
        "_cmd_doc_suspend": "<Zeit> - Bot fÃŧr eine Weile einfrieren",
        "_cmd_doc_ping": "ÃberprÃŧft die Antwortgeschwindigkeit des Userbots",
        "_cls_doc": "Selbsttestbezogene Operationen",
        "send_anyway": "đ¤ Trotzdem senden",
        "cancel": "đĢ Abbrechen",
    }

    strings_uz = {
        "set_loglevel": "đĢ <b>Log darajasini raqam yoki satr sifatida ko'rsating</b>",
        "no_logs": "âšī¸ <b>Siz {} darajadagi hech qanday loglaringiz yo'q.</b>",
        "logs_filename": "Bampi-logs.txt",
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Bampi Loglari"
            " </b><code>{}</code>\n\n<emoji document_id=5454390891466726015>đ</emoji>"
            " <b>Bampi-versiyasi: {}.{}.{}</b>{}\n<Emoji"
            "document_id=6321050180095313397>âą</emoji> <b>Mavjudligi:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "bad_module": "đĢ <b>Modul topilmadi</b>",
        "debugging_enabled": (
            (
                "đ§âđģ <b>Modul uchun ishlab chiqarish rejimi yoqildi"
                " </b><code>{0}</code>\n<i>`debug_modules` papkasiga o'ting"
            ),
            "`{0}.py` faylini o'zgartiring va o'zgarishlarni reallaqam ko'ring</i>",
        ),
        "debugging_disabled": "â <b>Ishtirok rejimi o'chirildi</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>Noto'g'ri vaqt"
            "qo'ymoq</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot chiqarildi</b>"
            " <code>{}</code> <b>Soniyalar</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>Telegram tezligi:</b>"
            " <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>SoĘģngi marotaba qayta ishga"
            " tushirilgan vaqti:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>Telegram"
            " tezligiTelegram serverlarining ishga tushishi va boshqa tashqi"
            " faktorlariga bog'liq va Userbot o'rnatilgan serverlarining sozlamalari"
            " bilan bog'liq emas</i>"
        ),
        "confidential": (
            "â ī¸ <b>Log darajasi </b><code>{}</code><b> shaxsiy ma'lumotlarga ega"
            " bo'lishi mumkinO'zingizni xavfsizligi uchun</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Log darajasi </b><code>{0}</code><b> shaxsiy ma'lumotlarga ega"
            " bo'lishi mumkinO'zingizni xavfsizligi uchun</b>\n<b>Yozing"
            " </b><code>.logs {0} force_insecure</code><b> loglarniOgohlantirish</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Log darajasini tanlang</b>",
        "_cmd_doc_dump": "Xabar haqida ma'lumotlarni ko'rsatish",
        "_cmd_doc_logs": (
            "<Ebene> - Log faylini yuboradi. O'rin darajalari xavfsizlikma'lumotlar."
        ),
        "_cmd_doc_suspend": "<Vaqt> - Botni bir necha vaqtga o'chirish",
        "_cmd_doc_ping": "Userbotning javob berish tezligini tekshirish",
        "_cls_doc": "O'z testi bilan bog'liq operatsiyalar",
        "send_anyway": "đ¤ Baribir yuborish",
        "cancel": "đĢ Bekor qilish",
    }

    strings_tr = {
        "set_loglevel": (
            "đĢ <b>LÃŧtfen gÃŧnlÃŧk seviyesini sayÄą veya dize olarak belirtin</b>"
        ),
        "no_logs": "âšī¸ <b>HiÃ§bir {} seviyesindeki gÃŧnlÃŧk bulunmuyor.</b>",
        "logs_filename": "Bampi-logs.txt",
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Bampi GÃŧnlÃŧkleri"
            " </b><code>{}</code>\n\n<emoji document_id=5454390891466726015>đ</emoji>"
            " <b>Bampi versiyasÄą: {}.{}.{}</b>{}\n<Emoji"
            "document_id=6321050180095313397>âą</emoji> <b>SÃŧre:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "bad_module": "đĢ <b>ModÃŧl bulunamadÄą</b>",
        "debugging_enabled": (
            (
                "đ§âđģ <b>GeliÅtirme modu modÃŧl iÃ§in etkinleÅtirildi"
                " </b><code>{0}</code>\n<i>`debug_modules` klasÃļrÃŧne gidin"
            ),
            (
                "`{0}.py` dosyasÄąnÄą dÃŧzenleyin ve deÄiÅiklikleri gerÃ§ekleÅtirmek iÃ§in"
                " kaydedin</i>"
            ),
        ),
        "debugging_disabled": "â <b>GeliÅtirme modu devre dÄąÅÄą bÄąrakÄąldÄą</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>GeÃ§ersiz zaman"
            "girdiniz</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot donduruldu</b>"
            " <code>{}</code> <b>saniye</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>TelegramhÄązÄą:</b>"
            " <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>Son gÃŧncellemeden"
            " sonra:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>Telegram hÄązÄą"
            "Telegram sunucularÄąnÄąn baÅlatÄąlmasÄą ve diÄer dÄąÅ faktÃļrler ile alakalÄądÄąr"
            "ve Userbot kurulumunuzun sunucu ayarlarÄąyla alakalÄą deÄildir</i>"
        ),
        "confidential": (
            "â ī¸ <b>GÃŧnlÃŧk seviyesi </b><code>{}</code><b> gizli bilgilere sahip"
            " olabilirKendi gÃŧvenliÄiniz iÃ§in</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>GÃŧnlÃŧk seviyesi </b><code>{0}</code><b> gizli bilgilere sahip"
            " olabilirKendi gÃŧvenliÄiniz iÃ§in</b>\n<b>YazÄąn </b><code>.logs {0}"
            " force_insecure</code><b> gÃŧnlÃŧkleriuyarÄą</b>"
        ),
        "choose_loglevel": "đââī¸ <b>LÃŧtfen gÃŧnlÃŧk seviyesini seÃ§in</b>",
        "_cmd_doc_dump": "Mesaj hakkÄąnda bilgi gÃļster",
        "_cmd_doc_logs": (
            "<Ebene> - GÃŧnlÃŧk dosyasÄąnÄą gÃļnderir. Seviyeler gizlibilgiler."
        ),
        "_cmd_doc_suspend": "<Zaman> - Botu bir sÃŧreliÄine dondurun",
        "_cmd_doc_ping": "Userbotun yanÄąt verme hÄązÄąnÄą kontrol edin",
        "_cls_doc": "Ä°lgili testlerle ilgili iÅlemler",
        "send_anyway": "đ¤ GÃļnder",
        "cancel": "đĢ Ä°ptal",
    }

    strings_hi = {
        "set_loglevel": (
            "đĢ <b>ā¤āĨā¤Ēā¤¯ā¤ž ā¤˛āĨā¤ ā¤¸āĨā¤¤ā¤° ā¤āĨ ā¤¸ā¤ā¤āĨā¤¯ā¤ž ā¤¯ā¤ž ā¤¸āĨā¤āĨā¤°ā¤ŋā¤ā¤ ā¤āĨ ā¤°āĨā¤Ē ā¤ŽāĨā¤ ā¤¨ā¤ŋā¤°āĨā¤Ļā¤ŋā¤ˇāĨā¤ ā¤ā¤°āĨā¤</b>"
        ),
        "no_logs": "âšī¸ <b>ā¤āĨā¤ {} ā¤¸āĨā¤¤ā¤° ā¤āĨ ā¤˛āĨā¤ ā¤¨ā¤šāĨā¤ ā¤Žā¤ŋā¤˛ā¤žāĨ¤</b>",
        "logs_filename": "Bampi-logs.txt",
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Bampi ā¤˛āĨā¤</b>"
            " </code>\n\n<emoji document_id=5454390891466726015>đ</emoji>"
            " <b>Bampi ā¤¸ā¤ā¤¸āĨā¤ā¤°ā¤Ŗ: {}.{}.{}</b>{}\n<Emoji"
            "document_id=6321050180095313397>âą</emoji> <b>ā¤ĩāĨā¤ŗ:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "bad_module": "đĢ <b>ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤¨ā¤šāĨā¤ ā¤Žā¤ŋā¤˛ā¤ž</b>",
        "debugging_enabled": (
            (
                "đ§âđģ <b>ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤āĨ ā¤˛ā¤ŋā¤ ā¤Ąā¤ŋā¤Ŧā¤ā¤ŋā¤ā¤ ā¤¸ā¤āĨā¤ˇā¤Ž ā¤ā¤° ā¤Ļā¤ŋā¤¯ā¤ž ā¤ā¤¯ā¤ž ā¤šāĨ"
                " </b><code>{0}</code>\n<i>`debug_modules` ā¤Ģā¤ŧāĨā¤˛āĨā¤Ąā¤° ā¤ŽāĨā¤ ā¤ā¤žā¤ā¤"
            ),
            "`{0}.py` ā¤Ģā¤ŧā¤žā¤ā¤˛ ā¤āĨ ā¤¸ā¤ā¤Ēā¤žā¤Ļā¤ŋā¤¤ ā¤ā¤°āĨā¤ ā¤ā¤° ā¤Ēā¤°ā¤ŋā¤ĩā¤°āĨā¤¤ā¤¨āĨā¤ ā¤āĨ ā¤¸ā¤šāĨā¤āĨā¤</i>",
        ),
        "debugging_disabled": "â <b>ā¤Ąā¤ŋā¤Ŧā¤ā¤ŋā¤ā¤ ā¤Ąā¤ŋā¤¸āĨā¤Ŧā¤˛ ā¤ā¤° ā¤Ļā¤ŋā¤¯ā¤ž ā¤ā¤¯ā¤ž ā¤šāĨ</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>ā¤ā¤Žā¤žā¤¨āĨā¤¯ ā¤¸ā¤Žā¤¯"
            "ā¤Ļā¤°āĨā¤ ā¤ā¤ŋā¤¯ā¤ž ā¤ā¤¯ā¤žāĨ¤</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>ā¤ŦāĨā¤ ā¤¨ā¤ŋā¤˛ā¤ā¤Ŧā¤ŋā¤¤ ā¤ā¤° ā¤Ļā¤ŋā¤¯ā¤ž"
            " ā¤ā¤¯ā¤ž ā¤šāĨ</b> <code>{}</code> <b>ā¤¸āĨā¤ā¤ā¤Ą</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>ā¤āĨā¤˛āĨā¤āĨā¤°ā¤žā¤Ž"
            "ā¤ā¤¤ā¤ŋ:</b> <code>{}</code> <b>ā¤Žā¤ŋā¤˛āĨā¤¸āĨā¤ā¤ā¤Ą</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>ā¤ā¤ā¤¤ā¤ŋā¤Ž ā¤ā¤Ēā¤ĄāĨā¤ ā¤¸āĨ ā¤Ŧā¤žā¤Ļ:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>ā¤āĨā¤˛āĨā¤āĨā¤°ā¤žā¤Ž ā¤ā¤¤ā¤ŋ"
            "ā¤āĨā¤˛āĨā¤āĨā¤°ā¤žā¤Ž ā¤¸ā¤°āĨā¤ĩā¤° ā¤āĨ ā¤ļāĨā¤°āĨ ā¤ā¤°ā¤¨āĨ ā¤ā¤° ā¤ā¤¨āĨā¤¯ ā¤Ŧā¤žā¤šā¤°āĨ ā¤ĩā¤ā¤šāĨā¤ ā¤¸āĨ ā¤āĨā¤Ąā¤ŧā¤ž ā¤šāĨ"
            "ā¤ā¤° ā¤ā¤Ēā¤āĨ ā¤ā¤Ēā¤¯āĨā¤ā¤ā¤°āĨā¤¤ā¤ž ā¤ŦāĨā¤ ā¤¸āĨā¤Ĩā¤žā¤Ēā¤¨ā¤ž ā¤āĨ ā¤¸ā¤°āĨā¤ĩā¤° ā¤¸āĨā¤ā¤ŋā¤ā¤āĨā¤¸ ā¤¸āĨ ā¤¸ā¤ā¤Ŧā¤ā¤§ā¤ŋā¤¤ ā¤¨ā¤šāĨā¤ ā¤šāĨ</i>"
        ),
        "confidential": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>ā¤ĩāĨā¤ŗ:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>ā¤˛āĨā¤ ā¤¸āĨā¤¤ā¤° </b><code>{0}</code><b> ā¤ŽāĨā¤ ā¤āĨā¤Ēā¤¨āĨā¤¯ ā¤ā¤žā¤¨ā¤ā¤žā¤°āĨ ā¤šāĨ ā¤¸ā¤ā¤¤āĨ ā¤šāĨ"
            "ā¤ā¤Ēā¤¨āĨ ā¤¸āĨā¤°ā¤āĨā¤ˇā¤ž ā¤āĨ ā¤˛ā¤ŋā¤</b>\n<b>ā¤˛ā¤ŋā¤āĨā¤ </b><code>.logs {0}"
            "force_insecure</code><b> ā¤˛āĨā¤"
            "ā¤āĨā¤¤ā¤žā¤ĩā¤¨āĨ</b>"
        ),
        "choose_loglevel": "đââī¸ <b>ā¤āĨā¤Ēā¤¯ā¤ž ā¤˛āĨā¤ ā¤˛āĨā¤ĩā¤˛ ā¤āĨā¤¨āĨā¤</b>",
        "_cmd_doc_dump": "ā¤¸ā¤ā¤ĻāĨā¤ļ ā¤āĨ ā¤Ŧā¤žā¤°āĨ ā¤ŽāĨā¤ ā¤ā¤žā¤¨ā¤ā¤žā¤°āĨ ā¤Ļā¤ŋā¤ā¤žā¤ā¤",
        "_cmd_doc_logs": "<Ebene> - ā¤˛āĨā¤ ā¤Ģā¤ŧā¤žā¤ā¤˛ ā¤­āĨā¤ā¤¤ā¤ž ā¤šāĨāĨ¤ ā¤¸āĨā¤¤ā¤° ā¤ā¤ŋā¤ĒāĨ ā¤šāĨā¤ ā¤šāĨā¤ā¤¸āĨā¤ā¤¨ā¤žā¤ā¤āĨ¤",
        "_cmd_doc_suspend": "<ā¤¸ā¤Žā¤¯> - ā¤ŦāĨā¤ ā¤āĨ ā¤ĨāĨā¤Ąā¤ŧāĨ ā¤ĻāĨā¤° ā¤āĨ ā¤˛ā¤ŋā¤ ā¤Ģā¤ŧāĨā¤°āĨā¤ā¤ŧ ā¤ā¤°āĨā¤",
        "_cmd_doc_ping": "ā¤¯āĨā¤ā¤°ā¤ŦāĨā¤ ā¤°ā¤ŋā¤¸āĨā¤ĒāĨā¤¨āĨā¤¸ā¤ŋā¤Ŧā¤ŋā¤˛ā¤ŋā¤āĨ ā¤āĨā¤ ā¤ā¤°āĨā¤",
        "_cls_doc": "ā¤¸ā¤ā¤Ŧā¤ā¤§ā¤ŋā¤¤ ā¤Ēā¤°āĨā¤āĨā¤ˇā¤Ŗ ā¤¸ā¤ā¤¸ā¤žā¤§ā¤ŋā¤¤ ā¤ā¤ŋā¤ ā¤ā¤ž ā¤°ā¤šāĨ ā¤šāĨā¤",
        "send_anyway": "đ¤ ā¤Ģā¤ŋā¤° ā¤­āĨ ā¤­āĨā¤āĨā¤",
        "cancel": "đĢ ā¤°ā¤ĻāĨā¤Ļ ā¤ā¤°āĨā¤",
    }

    strings_ja = {
        "debugging_enabled": "â <b>ãããã°ãæåšãĢãĒããžãã</b>",
        "debugging_disabled": "â <b>ãããã°ãįĄåšãĢãĒããžãã</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>įĄåšãĒæéåĨåãããžããã</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>ãããã"
            "ä¸æåæ­ĸãããžãã</b> <code>{}</code> <b>į§</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>ããŦã°ãŠã "
            "éåēĻ:</b> <code>{}</code> <b>ããĒį§</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>æåžãŽæ´æ°ãããŽįĩéæé:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>ããŦã°ãŠã éåēĻ"
            "ããŦã°ãŠã ãĩãŧããŧãčĩˇåããäģãŽå¤é¨čĻå ãĢãã"
            "ããĒããŽãĻãŧãļãŧããããŽãģãããĸããã¨ã¯éĸäŋããããžãã</i>"
        ),
        "confidential": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>æé:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>ã­ã°ãŦããĢ </b><code>{0}</code><b>ãĢã¯æŠå¯æå ąãåĢãžããĻããå¯čŊæ§ããããžã"
            "ãģã­ãĨãĒããŖä¸ãŽįįąã§</b>\n<b>æ¸ãčžŧãŋ</b><code>.logs {0}"
            "force_insecure</code><b>ã­ã°"
            "č­Ļå</b>"
        ),
        "choose_loglevel": "đââī¸ <b>ã­ã°ãŦããĢãé¸æããĻãã ãã</b>",
        "_cmd_doc_dump": "ãĄããģãŧã¸ãĢéĸããæå ąãčĄ¨į¤ēããžã",
        "_cmd_doc_logs": "<ãŦããĢ> - ã­ã°ããĄã¤ãĢãéäŋĄããžããé ããããŦããĢã¯éįĨãããžããã",
        "_cmd_doc_suspend": "<æé> - ããããä¸æåæ­ĸããžã",
        "_cmd_doc_ping": "ãĻãŧãļãŧããããŽãŦãšããŗãščŊåããã§ãã¯ããžã",
        "_cls_doc": "éĸéŖããããšããåŽčĄãããĻããžã",
        "send_anyway": "đ¤ ããã§ãéäŋĄãã",
        "cancel": "đĢ ã­ãŖãŗãģãĢ",
    }

    strings_kr = {
        "debugging_enabled": "â <b>ëë˛ęšė´ íėąíëėėĩëë¤</b>",
        "debugging_disabled": "â <b>ëë˛ęšė´ ëšíėąíëėėĩëë¤</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>ėëĒģë ėę°ėë Ĩëėėĩëë¤</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>ë´ė´"
            "ėŧė ė¤ė§ëėėĩëë¤</b> <code>{}</code> <b>ė´</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>íë ęˇ¸ë¨"
            "ėë:</b> <code>{}</code> <b>ë°ëĻŦ ė´</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>ë§ė§ë§ ėë°ė´í¸ ė´í ę˛Ŋęŗŧ ėę°:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>íë ęˇ¸ë¨ ėë"
            "íë ęˇ¸ë¨ ėë˛ëĨŧ ėėíęŗ  ë¤ëĨ¸ ė¸ëļ ėė¸ė ėí´"
            "ëšė ė ėŦėŠė ë´ė ė¤ė ęŗŧë ę´ë ¨ė´ ėėĩëë¤</i>"
        ),
        "confidential": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>ėę°:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>ëĄęˇ¸ ë ë˛¨ </b><code>{0}</code><b>ėë ę¸°ë° ė ëŗ´ę° íŦí¨ë  ė ėėŧë¯ëĄ"
            "ëŗ´ėėė ė´ė ëĄ</b>\n<b>ėėą</b><code>.logs {0}"
            "force_insecure</code><b>ëĄęˇ¸"
            "ę˛Ŋęŗ </b>"
        ),
        "choose_loglevel": "đââī¸ <b>ëĄęˇ¸ ë ë˛¨ė ė ííė¸ė</b>",
        "_cmd_doc_dump": "ëŠėė§ė ëí ė ëŗ´ëĨŧ íėíŠëë¤",
        "_cmd_doc_logs": "<ë ë˛¨> - ëĄęˇ¸ íėŧė ëŗ´ëëë¤. ė¨ę˛¨ė§ ë ë˛¨ė ėëĻŧëė§ ėėĩëë¤.",
        "_cmd_doc_suspend": "<ėę°> - ë´ė ėŧė ė¤ė§íŠëë¤",
        "_cmd_doc_ping": "ėŦėŠė ë´ė ėëĩ ëĨë Ĩė íė¸íŠëë¤",
        "_cls_doc": "ę´ë ¨ë íė¤í¸ę° ė¤í ė¤ėëë¤",
        "send_anyway": "đ¤ ęˇ¸ëë ëŗ´ë´ę¸°",
        "cancel": "đĢ ėˇ¨ė",
    }

    strings_ar = {
        "debugging_enabled": "â <b>ØĒŲ ØĒŲŲŲŲ Ø§ŲØĒØĩØ­ŲØ­</b>",
        "debugging_disabled": "â <b>ØĒŲ ØĒØšØˇŲŲ Ø§ŲØĒØĩØ­ŲØ­</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>ØŖØ¯ØŽŲØ§ŲŲŲØĒ Ø§ŲØĩØ­ŲØ­</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>ØĒŲ ØĨŲŲØ§Ų"
            "Ø§ŲØ¨ŲØĒ</b> <code>{}</code> <b>ØĢŲØ§ŲŲ</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>ØŗØąØšØŠØĒŲŲŲØŦØąØ§Ų:</b>"
            " <code>{}</code> <b>ŲŲŲŲ ØĢØ§ŲŲØŠ</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>ŲØ¯ØŠ Ø§ŲŲŲØĒ ŲŲØ° ØĸØŽØą"
            " ØĒØ­Ø¯ŲØĢ:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>ØŗØąØšØŠ"
            "ØĒŲŲŲØŦØąØ§Ų ŲŲØŗØĒ ØšØ¨Ø§ØąØŠ ØšŲ Ø§ŲŲŲØĒ Ø§ŲØ°Ų ŲØŗØĒØēØąŲŲ Ø§ŲØ¨ŲØĒ ŲŲØąØ¯ ØšŲŲ Ø§ŲØąØŗØ§ØĻŲ"
            "ŲŲŲŲØ§ ŲŲ Ø§ŲŲŲØĒ Ø§ŲØ°Ų ŲØŗØĒØēØąŲŲ Ø§ŲØ¨ŲØĒ ŲŲØąØ¯ ØšŲŲ Ø§ŲØąØŗØ§ØĻŲ Ø§ŲØŽØ§ØĩØŠ Ø¨Ų ŲŲ"
            "Ø¨Ø¯ØĄ ØĒØ´ØēŲŲ Ø§ŲØ¨ŲØĒ ŲŲŲØŗ Ø¨ØŗØ¨Ø¨ ØŖŲ ØšŲØ§ŲŲ ØŽØ§ØąØŦŲØŠ ØŖØŽØąŲ"
            "ŲØĢŲ ØĨØšØ¯Ø§Ø¯Ø§ØĒ Ø§ŲØ¨ŲØĒ Ø§ŲØŽØ§Øĩ Ø¨Ų</i>"
        ),
        "confidential": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>Ø§ŲŲŲØĒ:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>ŲØ­ØĒŲŲ ŲØŗØĒŲŲ Ø§ŲØŗØŦŲØ§ØĒ </b><code>{0}</code><b>ØšŲŲ ŲØšŲŲŲØ§ØĒ"
            "ØŗØąŲØŠ ŲŲØ°ŲŲ</b>\n<b>Ø§ŲØĒØ¨</b><code>.logs {0}"
            "force_insecure</code><b>ŲØĨØąØŗØ§Ų Ø§ŲØŗØŦŲØ§ØĒ"
            "ŲØšŲŲŲØ§ØĒ ØŗØąŲØŠ</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Ø§ØŽØĒØą ŲØŗØĒŲŲ Ø§ŲØŗØŦŲØ§ØĒ</b>",
        "_cmd_doc_dump": "ØšØąØļ ŲØšŲŲŲØ§ØĒ Ø§ŲØąØŗØ§ŲØŠ",
        "_cmd_doc_logs": (
            "<ŲØŗØĒŲŲ> - ØĨØąØŗØ§Ų ŲŲŲØ§ØĒ Ø§ŲØŗØŦŲØ§ØĒ. Ø§ŲŲØŗØĒŲŲØ§ØĒ Ø§ŲŲØŽŲŲØŠ ŲØ§ ŲØĒŲ ØĨØŽØˇØ§ØąŲ ØšŲŲØ§."
        ),
        "_cmd_doc_suspend": "<ŲŲØĒ> - ØĨŲŲØ§Ų Ø§ŲØ¨ŲØĒ ŲØ¤ŲØĒŲØ§",
        "_cmd_doc_ping": "ØĒØ­ŲŲ ŲŲ ØŗØąØšØŠ Ø§ŲØ¨ŲØĒ",
        "_cls_doc": "ØĒŲ ØĒØ´ØēŲŲ Ø§ØŽØĒØ¨Ø§ØąØ§ØĒ Ø°Ø§ØĒ ØĩŲØŠ",
        "send_anyway": "đ¤ ØĨØąØŗØ§ŲŲØ§ ØšŲŲ ØŖŲØŠ Ø­Ø§Ų",
        "cancel": "đĢ ØĨŲØēØ§ØĄ",
    }

    strings_es = {
        "debugging_enabled": "â <b>DepuraciÃŗn habilitada</b>",
        "debugging_disabled": "â <b>DepuraciÃŗn deshabilitada</b>",
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>Ingrese"
            "el tiempo correcto</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot"
            "suspendido</b> <code>{}</code> <b>segundos</b>"
        ),
        "results_ping": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>Velocidad"
            "de Telegram:</b> <code>{}</code> <b>milisegundos</b>\n<emoji"
            " document_id=5377371691078916778>đ</emoji> <b>Desde el Ãēltimo"
            "actualizaciÃŗn:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>La velocidad"
            "de Telegram no es el tiempo que toma en responder el bot a los mensajes"
            "pero es el tiempo que toma en responder a tus mensajes desde que"
            "el bot se iniciÃŗ y no por cualquier otra razÃŗn externa"
            "como la configuraciÃŗn de tu bot</i>"
        ),
        "confidential": (
            "<emoji document_id=6321050180095313397>âą</emoji> <b>Tiempo:"
            " {}</b>\n<b>{}</b>\n\n<b>{} NoNick</b>\n<b>{} Grep</b>\n<b>{ }"
            "InlineLogs</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>El nivel de registro </b><code>{0}</code><b>contiene"
            "informaciÃŗn confidencial y por lo tanto</b>\n<b>escribe</b><code>.logs {0}"
            "force_insecure</code><b>para enviar los registros"
            "informaciÃŗn confidencial</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Elige el nivel de registro</b>",
        "_cmd_doc_dump": "Mostrar informaciÃŗn del mensaje",
        "_cmd_doc_logs": (
            "<nivel> - EnvÃ­a archivos de registro. Los niveles ocultos no se"
            " notificarÃĄn."
        ),
        "_cmd_doc_suspend": "<tiempo> - Suspende el bot temporalmente",
        "_cmd_doc_ping": "Verifique la velocidad del bot",
        "_cls_doc": "Se ejecutaron pruebas relacionadas",
        "send_anyway": "đ¤ Enviar de todos modos",
        "cancel": "đĢ Cancelar",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "force_send_all",
                False,
                "â ī¸ Do not touch, if you don't know what it does!\nBy default, Bampi"
                " will try to determine, which client caused logs. E.g. there is a"
                " module TestModule installed on Client1 and TestModule2 on Client2. By"
                " default, Client2 will get logs from TestModule2, and Client1 will get"
                " logs from TestModule. If this option is enabled, Bampi will send all"
                " logs to Client1 and Client2, even if it is not the one that caused"
                " the log.",
                validator=loader.validators.Boolean(),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "tglog_level",
                "INFO",
                "â ī¸ Do not touch, if you don't know what it does!\n"
                "Minimal loglevel for records to be sent in Telegram.",
                validator=loader.validators.Choice(
                    ["INFO", "WARNING", "ERROR", "CRITICAL"]
                ),
                on_change=self._pass_config_to_logger,
            ),
        )

    def _pass_config_to_logger(self):
        logging.getLogger().handlers[0].force_send_all = self.config["force_send_all"]
        logging.getLogger().handlers[0].tg_level = {
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50,
        }[self.config["tglog_level"]]

    @loader.command(
        ru_doc="ĐŅĐ˛ĐĩŅŅ ĐŊĐ° ŅĐžĐžĐąŅĐĩĐŊĐ¸Đĩ, ŅŅĐžĐąŅ ĐŋĐžĐēĐ°ĐˇĐ°ŅŅ ĐĩĐŗĐž Đ´Đ°ĐŧĐŋ",
        de_doc="Antworten Sie auf eine Nachricht, um ihren Dump anzuzeigen",
        tr_doc="DÃļkÃŧmÃŧnÃŧ gÃļstermek iÃ§in bir iletiyi yanÄątlayÄąn",
        hi_doc="ā¤ā¤ŋā¤¸āĨ ā¤¸ā¤ā¤ĻāĨā¤ļ ā¤ā¤ž ā¤ā¤¤āĨā¤¤ā¤° ā¤ā¤¸ā¤āĨ ā¤Ąā¤ā¤Ē ā¤āĨ ā¤Ļā¤ŋā¤ā¤žā¤¨āĨ ā¤āĨ ā¤˛ā¤ŋā¤ ā¤ĻāĨā¤",
        uz_doc="Xabarning axlatini ko'rsatish uchun unga javob bering",
        ja_doc="ãĄããģãŧã¸ãĢčŋäŋĄããĻããŽããŗããčĄ¨į¤ēããžã",
        kr_doc="ëŠėė§ė ëĩėĨíėŦ ęˇ¸ ë¤íëĨŧ íėíŠëë¤",
        ar_doc="ØŖØąØŗŲ ØąØŗØ§ŲØŠ ŲØšØąØļ ŲØŗØŽØŠ ŲŲŲØ§",
        es_doc="Responde a un mensaje para mostrar su volcado",
    )
    async def dump(self, message: Message):
        """Use in reply to get a dump of a message"""
        if not message.is_reply:
            return

        await utils.answer(
            message,
            "<code>"
            + utils.escape_html((await message.get_reply_message()).stringify())
            + "</code>",
        )

    @loader.loop(interval=1)
    async def watchdog(self):
        if not os.path.isdir(DEBUG_MODS_DIR):
            return

        try:
            for module in os.scandir(DEBUG_MODS_DIR):
                last_modified = os.stat(module.path).st_mtime
                cls_ = module.path.split("/")[-1].split(".py")[0]

                if cls_ not in self._memory:
                    self._memory[cls_] = last_modified
                    continue

                if self._memory[cls_] == last_modified:
                    continue

                self._memory[cls_] = last_modified
                logger.debug("Reloading debug module %s", cls_)
                with open(module.path, "r") as f:
                    try:
                        await next(
                            module
                            for module in self.allmodules.modules
                            if module.__class__.__name__ == "LoaderMod"
                        ).load_module(
                            f.read(),
                            None,
                            save_fs=False,
                        )
                    except Exception:
                        logger.exception("Failed to reload module in watchdog")
        except Exception:
            logger.exception("Failed debugging watchdog")
            return

    @loader.command(
        ru_doc=(
            "[ĐŧĐžĐ´ŅĐģŅ] - ĐĐģŅ ŅĐ°ĐˇŅĐ°ĐąĐžŅŅĐ¸ĐēĐžĐ˛: ĐžŅĐēŅŅŅŅ ĐŧĐžĐ´ŅĐģŅ Đ˛ ŅĐĩĐļĐ¸ĐŧĐĩ Đ´ĐĩĐąĐ°ĐŗĐ° Đ¸ ĐŋŅĐ¸ĐŧĐĩĐŊŅŅŅ"
            " Đ¸ĐˇĐŧĐĩĐŊĐĩĐŊĐ¸Ņ Đ¸Đˇ ĐŊĐĩĐŗĐž Đ˛ ŅĐĩĐļĐ¸ĐŧĐĩ ŅĐĩĐ°ĐģŅĐŊĐžĐŗĐž Đ˛ŅĐĩĐŧĐĩĐŊĐ¸"
        ),
        de_doc=(
            "[Modul] - FÃŧr Entwickler: Ãffnet ein Modul im Debug-Modus und"
            " wendet Ãnderungen aus ihm in Echtzeit an"
        ),
        uz_doc=(
            "[modul] - Dasturchaklar uchun: modulni debug rejimida ochib, va uni"
            " real vaqtda ishga tushirish"
        ),
        tr_doc=(
            "[modul] - GeliÅtiriciler iÃ§in: Bir modÃŧlÃŧ debug modunda aÃ§ar ve"
            " deÄiÅiklikleri gerÃ§ek zamanlÄą uygular"
        ),
        hi_doc=(
            "[ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛] - ā¤ĄāĨā¤ĩā¤˛ā¤Ēā¤°āĨā¤¸ ā¤āĨ ā¤˛ā¤ŋā¤: ā¤ā¤ ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤āĨ ā¤Ąā¤ŋā¤Ŧā¤ ā¤ŽāĨā¤Ą ā¤ŽāĨā¤ ā¤āĨā¤˛āĨā¤ ā¤ā¤°"
            " ā¤ĩā¤žā¤¸āĨā¤¤ā¤ĩā¤ŋā¤ ā¤¸ā¤Žā¤¯ ā¤ŽāĨā¤ ā¤ā¤¸ā¤āĨ ā¤Ēā¤°ā¤ŋā¤ĩā¤°āĨā¤¤ā¤¨āĨā¤ ā¤āĨ ā¤˛ā¤žā¤āĨ ā¤ā¤°āĨā¤"
        ),
        ja_doc="[ãĸã¸ãĨãŧãĢ] - éįēčåãīŧãĸã¸ãĨãŧãĢããããã°ãĸãŧãã§éããå¤æ´ããĒãĸãĢãŋã¤ã ã§éŠį¨ããžã",
        kr_doc="[ëĒ¨ë] - ę°ë°ėėŠ: ëĒ¨ëė ëë˛ęˇ¸ ëĒ¨ëëĄ ė´ęŗ  ė¤ėę°ėŧëĄ ëŗę˛Ŋė ė ėŠíŠëë¤",
        ar_doc=(
            "[ŲØ­Ø¯ØŠ] - ŲŲŲØˇŲØąŲŲ: ŲØĒØ­ ŲØ­Ø¯ØŠ ŲŲ ŲØļØš ØĒØĩØ­ŲØ­ Ø§ŲØŖØŽØˇØ§ØĄ ŲØĒØˇØ¨ŲŲ"
            " Ø§ŲØĒØēŲŲØąØ§ØĒ ŲŲŲ ŲŲ Ø§ŲŲŲØĒ Ø§ŲØ­ŲŲŲŲ"
        ),
        es_doc=(
            "[mÃŗdulo] - Para desarrolladores: abre un mÃŗdulo en modo de depuraciÃŗn y"
            " aplica los cambios de ÃŠl en tiempo real"
        ),
    )
    async def debugmod(self, message: Message):
        """[module] - For developers: Open module for debugging
        You will be able to track changes in real-time"""
        args = utils.get_args_raw(message)
        instance = None
        for module in self.allmodules.modules:
            if (
                module.__class__.__name__.lower() == args.lower()
                or module.strings["name"].lower() == args.lower()
            ):
                if os.path.isfile(
                    os.path.join(
                        DEBUG_MODS_DIR,
                        f"{module.__class__.__name__}.py",
                    )
                ):
                    os.remove(
                        os.path.join(
                            DEBUG_MODS_DIR,
                            f"{module.__class__.__name__}.py",
                        )
                    )

                    try:
                        delattr(module, "Bampi_debug")
                    except AttributeError:
                        pass

                    await utils.answer(message, self.strings("debugging_disabled"))
                    return

                module.Bampi_debug = True
                instance = module
                break

        if not instance:
            await utils.answer(message, self.strings("bad_module"))
            return

        with open(
            os.path.join(
                DEBUG_MODS_DIR,
                f"{instance.__class__.__name__}.py",
            ),
            "wb",
        ) as f:
            f.write(inspect.getmodule(instance).__loader__.data)

        await utils.answer(
            message,
            self.strings("debugging_enabled").format(instance.__class__.__name__),
        )

    @loader.command(
        ru_doc="<ŅŅĐžĐ˛ĐĩĐŊŅ> - ĐĐžĐēĐ°ĐˇĐ°ŅŅ ĐģĐžĐŗĐ¸",
        de_doc="<Level> - Zeige Logs",
        uz_doc="<daraja> - Loglarni ko'rsatish",
        tr_doc="<seviye> - GÃŧnlÃŧkleri gÃļster",
        hi_doc="<ā¤¸āĨā¤¤ā¤°> - ā¤˛āĨā¤ ā¤Ļā¤ŋā¤ā¤žā¤ā¤",
        ja_doc="<ãŦããĢ> - ã­ã°ãčĄ¨į¤ēããžã",
        kr_doc="<ë ë˛¨> - ëĄęˇ¸ íė",
        ar_doc="<ŲØŗØĒŲŲ> - ØĨØ¸ŲØ§Øą Ø§ŲØŗØŦŲØ§ØĒ",
        es_doc="<nivel> - Mostrar registros",
    )
    async def logs(
        self,
        message: typing.Union[Message, InlineCall],
        force: bool = False,
        lvl: typing.Union[int, None] = None,
    ):
        """<level> - Dump logs"""
        if not isinstance(lvl, int):
            args = utils.get_args_raw(message)
            try:
                try:
                    lvl = int(args.split()[0])
                except ValueError:
                    lvl = getattr(logging, args.split()[0].upper(), None)
            except IndexError:
                lvl = None

        if not isinstance(lvl, int):
            try:
                if not self.inline.init_complete or not await self.inline.form(
                    text=self.strings("choose_loglevel"),
                    reply_markup=[
                        [
                            {
                                "text": "đ¨ Critical",
                                "callback": self.logs,
                                "args": (False, 50),
                            },
                            {
                                "text": "đĢ Error",
                                "callback": self.logs,
                                "args": (False, 40),
                            },
                        ],
                        [
                            {
                                "text": "â ī¸ Warning",
                                "callback": self.logs,
                                "args": (False, 30),
                            },
                            {
                                "text": "âšī¸ Info",
                                "callback": self.logs,
                                "args": (False, 20),
                            },
                        ],
                        [
                            {
                                "text": "đ§âđģ Debug",
                                "callback": self.logs,
                                "args": (False, 10),
                            },
                            {
                                "text": "đ All",
                                "callback": self.logs,
                                "args": (False, 0),
                            },
                        ],
                        [{"text": "đĢ Cancel", "action": "close"}],
                    ],
                    message=message,
                ):
                    raise
            except Exception:
                await utils.answer(message, self.strings("set_loglevel"))

            return

        logs = "\n\n".join(
            [
                "\n".join(
                    handler.dumps(lvl, client_id=self._client.tg_id)
                    if "client_id" in inspect.signature(handler.dumps).parameters
                    else handler.dumps(lvl)
                )
                for handler in logging.getLogger().handlers
            ]
        )

        named_lvl = (
            lvl
            if lvl not in logging._levelToName
            else logging._levelToName[lvl]  # skipcq: PYL-W0212
        )

        if (
            lvl < logging.WARNING
            and not force
            and (
                not isinstance(message, Message)
                or "force_insecure" not in message.raw_text.lower()
            )
        ):
            try:
                if not self.inline.init_complete:
                    raise

                cfg = {
                    "text": self.strings("confidential").format(named_lvl),
                    "reply_markup": [
                        {
                            "text": self.strings("send_anyway"),
                            "callback": self.logs,
                            "args": [True, lvl],
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                }
                if isinstance(message, Message):
                    if not await self.inline.form(**cfg, message=message):
                        raise
                else:
                    await message.edit(**cfg)
            except Exception:
                await utils.answer(
                    message,
                    self.strings("confidential_text").format(named_lvl),
                )

            return

        if len(logs) <= 2:
            if isinstance(message, Message):
                await utils.answer(message, self.strings("no_logs").format(named_lvl))
            else:
                await message.edit(self.strings("no_logs").format(named_lvl))
                await message.unload()

            return

        if btoken := self._db.get("Bampi.inline", "bot_token", False):
            logs = logs.replace(
                btoken,
                f'{btoken.split(":")[0]}:***************************',
            )

        if Bampi_token := self._db.get("BampiDL", "token", False):
            logs = logs.replace(
                Bampi_token,
                f'{Bampi_token.split("_")[0]}_********************************',
            )

        if Bampi_token := self._db.get("Kirito", "token", False):
            logs = logs.replace(
                Bampi_token,
                f'{Bampi_token.split("_")[0]}_********************************',
            )

        if os.environ.get("DATABASE_URL"):
            logs = logs.replace(
                os.environ.get("DATABASE_URL"),
                "postgre://**************************",
            )

        if os.environ.get("REDIS_URL"):
            logs = logs.replace(
                os.environ.get("REDIS_URL"),
                "postgre://**************************",
            )

        if os.environ.get("Bampi_session"):
            logs = logs.replace(
                os.environ.get("Bampi_session"),
                "StringSession(**************************)",
            )

        logs = BytesIO(logs.encode("utf-16"))
        logs.name = self.strings("logs_filename")

        ghash = utils.get_git_hash()

        other = (
            *main.__version__,
            " <i><a"
            f' href="https://github.com/hikariatama/Bampi/commit/{ghash}">({ghash[:8]})</a></i>'
            if ghash
            else "",
            utils.formatted_uptime(),
            utils.get_named_platform(),
            "â" if self._db.get(main.__name__, "no_nickname", False) else "đĢ",
            "â" if self._db.get(main.__name__, "grep", False) else "đĢ",
            "â" if self._db.get(main.__name__, "inlinelogs", False) else "đĢ",
        )

        if getattr(message, "out", True):
            await message.delete()

        if isinstance(message, Message):
            await utils.answer(
                message,
                logs,
                caption=self.strings("logs_caption").format(named_lvl, *other),
            )
        else:
            await self._client.send_file(
                message.form["chat"],
                logs,
                caption=self.strings("logs_caption").format(named_lvl, *other),
            )

    @loader.owner
    @loader.command(
        ru_doc="<Đ˛ŅĐĩĐŧŅ> - ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅŅ ĐąĐžŅĐ° ĐŊĐ° N ŅĐĩĐēŅĐŊĐ´",
        de_doc="<Zeit> - Stoppe den Bot fÃŧr N Sekunden",
        tr_doc="<sÃŧre> - Botu N saniye boyunca durdur",
        uz_doc="<vaqt> - Botni N soniya davomida to'xtatish",
        hi_doc="<ā¤¸ā¤Žā¤¯> - ā¤ŦāĨā¤ ā¤āĨ N ā¤¸āĨā¤ā¤ā¤Ą ā¤¤ā¤ ā¤ ā¤šā¤°ā¤žā¤ā¤",
        ja_doc="<æé> - ããããNį§éåæ­ĸããžã",
        kr_doc="<ėę°> - ë´ė N ė´ ëė ė ė§",
        ar_doc="<Ø§ŲŲŲØĒ> - ØĒØŦŲŲØ¯ Ø§ŲØ¨ŲØĒ ŲŲØ¯ØŠ N ØĢØ§ŲŲØŠ",
        es_doc="<tiempo> - Congela el bot durante N segundos",
    )
    async def suspend(self, message: Message):
        """<time> - Suspends the bot for N seconds"""
        try:
            time_sleep = float(utils.get_args_raw(message))
            await utils.answer(
                message,
                self.strings("suspended").format(time_sleep),
            )
            time.sleep(time_sleep)
        except ValueError:
            await utils.answer(message, self.strings("suspend_invalid_time"))

    @loader.command(
        ru_doc="ĐŅĐžĐ˛ĐĩŅĐ¸ŅŅ ŅĐēĐžŅĐžŅŅŅ ĐžŅĐēĐģĐ¸ĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°",
        de_doc="ÃberprÃŧfe die Antwortgeschwindigkeit des Userbots",
        tr_doc="KullanÄącÄą botunun yanÄąt hÄązÄąnÄą kontrol edin",
        uz_doc="Foydalanuvchi botining javob tezligini tekshiring",
        hi_doc="ā¤ā¤Ēā¤¯āĨā¤ā¤ā¤°āĨā¤¤ā¤ž ā¤ŦāĨā¤ ā¤āĨ ā¤ĒāĨā¤°ā¤¤ā¤ŋā¤āĨā¤°ā¤ŋā¤¯ā¤ž ā¤ā¤¤ā¤ŋ ā¤āĨ ā¤ā¤žā¤ā¤ ā¤ā¤°āĨā¤",
        ja_doc="ãĻãŧãļãŧããããŽåŋį­éåēĻãįĸēčĒããžã",
        kr_doc="ėŦėŠė ë´ė ėëĩ ėëëĨŧ íė¸íė­ėė¤",
        ar_doc="ØĒØ­ŲŲ ŲŲ ØŗØąØšØŠ Ø§ØŗØĒØŦØ§Ø¨ØŠ Ø¨ŲØĒ Ø§ŲŲØŗØĒØŽØ¯Ų",
        es_doc="Comprueba la velocidad de respuesta del bot de usuario",
    )
    async def ping(self, message: Message):
        """Test your userbot ping"""
        start = time.perf_counter_ns()
        message = await utils.answer(message, "<code>đģ Nofin...</code>")

        await utils.answer(
            message,
            self.strings("results_ping").format(
                round((time.perf_counter_ns() - start) / 10**6, 3),
                utils.formatted_uptime(),
            )
            + (
                ("\n\n" + self.strings("ping_hint"))
                if random.choice([0, 0, 2]) == 1
                else ""
            ),
        )

    async def client_ready(self):
        chat, _ = await utils.asset_channel(
            self._client,
            "Bampi-logs",
            "đ Your Bampi logs will appear in this chat",
            silent=True,
            invite_bot=True,
            avatar="https://github.com/hikariatama/assets/raw/master/Bampi-logs.png",
        )

        self._logchat = int(f"-100{chat.id}")

        self.watchdog.start()

        logging.getLogger().handlers[0].install_tg_log(self)
        logger.debug("Bot logging installed for %s", self._logchat)

        self._pass_config_to_logger()
