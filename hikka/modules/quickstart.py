import os
from random import choice
import logging

from .. import loader, translations, utils
from ..inline.types import BotInlineCall

logger = logging.getLogger(__name__)

imgs = [
    "https://te.legra.ph/file/bc83ad83a894085f662e4.mp4",

]


@loader.tds
class QuickstartMod(loader.Module):
    """Notifies user about userbot installation"""

    strings = {
        "name": "Quickstart",
        "base": """ππ¬π§ <b>Hello.</b> You've just installed <b>Bampi</b> userbot.

β <b>Need help?</b> Feel free to join our support chat. We help <b>everyone</b>.

π£ <b>Check out community made channels with modules: <a href="https://t.me/Bampiss">show</a></b>

πββοΈ <b>Quickstart:</b>

1οΈβ£ <b>Type </b><code>.help</code> <b>to see modules list</b>
2οΈβ£ <b>Type </b><code>.help &lt;ModuleName/command&gt;</code> <b>to see help of module ModuleName</b>
3οΈβ£ <b>Type </b><code>.dlmod &lt;link&gt;</code> <b>to load module from link</b>
4οΈβ£ <b>Type </b><code>.loadmod</code> <b>with reply to file to install module from it</b>
5οΈβ£ <b>Type </b><code>.unloadmod &lt;ModuleName&gt;</code> <b>to unload module ModuleName</b>

π‘ <b>Bampi supports modules from Friendly-Telegram and GeekTG, as well as its own ones.</b>""",
        "okteto": (
            "βοΈ <b>Your userbot is installed on Okteto</b>. You will get notifications"
            " from @WebpageBot. Do not block him."
        ),
        "railway": (
            "π <b>Your userbot is installed on Railway</b>. This platform has only"
            " <b>500 free hours per month</b>. Once this limit is reached, your"
            " <b>Bampi will be frozen</b>. Next month <b>you will need to go to"
            " https://railway.app and restart it</b>."
        ),
        "language_saved": "π¬π§ Language saved!",
        "language": "π¬π§ English",
        "btn_support": "π₯· Support chat",
    }

    strings_ru = {
        "base": """ππ·πΊ <b>ΠΡΠΈΠ²Π΅Ρ.</b> Π’Π²ΠΎΠΉ ΡΠ·Π΅ΡΠ±ΠΎΡ <b>Bampi</b> ΡΡΡΠ°Π½ΠΎΠ²Π»Π΅Π½.

β <b>ΠΡΠΆΠ½Π° ΠΏΠΎΠΌΠΎΡΡ?</b> ΠΡΡΡΠΏΠ°ΠΉ Π² Π½Π°Ρ ΡΠ°Ρ ΠΏΠΎΠ΄Π΄Π΅ΡΠΆΠΊΠΈ. ΠΡ ΠΏΠΎΠΌΠΎΠ³Π°Π΅ΠΌ <b>Π²ΡΠ΅ΠΌ</b>.

π£ <b>ΠΠ°Π³Π»ΡΠ½ΠΈ Π² ΠΊΠ°Π½Π°Π»Ρ Ρ ΠΌΠΎΠ΄ΡΠ»ΡΠΌΠΈ, ΡΠΎΠ·Π΄Π°Π½Π½ΡΠΌΠΈ ΠΊΠΎΠΌΡΡΠ½ΠΈΡΠΈ: <a href="https://t.me/Bampiss">ΠΏΠΎΠΊΠ°Π·Π°ΡΡ</a></b>

πββοΈ <b>ΠΡΡΡΡΡΠΉ Π³Π°ΠΉΠ΄:</b>

1οΈβ£ <b>ΠΠ°ΠΏΠΈΡΠΈ </b><code>.help</code> <b>ΡΡΠΎΠ±Ρ ΡΠ²ΠΈΠ΄Π΅ΡΡ ΡΠΏΠΈΡΠΎΠΊ ΠΌΠΎΠ΄ΡΠ»Π΅ΠΉ</b>
2οΈβ£ <b>ΠΠ°ΠΏΠΈΡΠΈ </b><code>.help &lt;ΠΠ°Π·Π²Π°Π½ΠΈΠ΅ ΠΌΠΎΠ΄ΡΠ»Ρ/ΠΊΠΎΠΌΠ°Π½Π΄Π°&gt;</code> <b>ΡΡΠΎΠ±Ρ ΡΠ²ΠΈΠ΄Π΅ΡΡ ΠΎΠΏΠΈΡΠ°Π½ΠΈΠ΅ ΠΌΠΎΠ΄ΡΠ»Ρ</b>
3οΈβ£ <b>ΠΠ°ΠΏΠΈΡΠΈ </b><code>.dlmod &lt;ΡΡΡΠ»ΠΊΠ°&gt;</code> <b>ΡΡΠΎΠ±Ρ Π·Π°Π³ΡΡΠ·ΠΈΡΡ ΠΌΠΎΠ΄ΡΠ»Ρ ΠΈΠ· ΡΡΡΠ»ΠΊΠ°</b>
4οΈβ£ <b>ΠΠ°ΠΏΠΈΡΠΈ </b><code>.loadmod</code> <b>ΠΎΡΠ²Π΅ΡΠΎΠΌ Π½Π° ΡΠ°ΠΉΠ», ΡΡΠΎΠ±Ρ Π·Π°Π³ΡΡΠ·ΠΈΡΡ ΠΌΠΎΠ΄ΡΠ»Ρ ΠΈΠ· Π½Π΅Π³ΠΎ</b>
5οΈβ£ <b>ΠΠ°ΠΏΠΈΡΠΈ </b><code>.unloadmod &lt;ΠΠ°Π·Π²Π°Π½ΠΈΠ΅ ΠΌΠΎΠ΄ΡΠ»Ρ&gt;</code> <b>ΡΡΠΎΠ±Ρ Π²ΡΠ³ΡΡΠ·ΠΈΡΡ ΠΌΠΎΠ΄ΡΠ»Ρ</b>

π‘ <b>Bampi ΠΏΠΎΠ΄Π΄Π΅ΡΠΆΠΈΠ²Π°Π΅Ρ ΠΌΠΎΠ΄ΡΠ»ΠΈ ΠΈΠ· Friendly-Telegram, GeekTG, Bampi, Π° ΡΠ°ΠΊΠΆΠ΅ ΡΠ²ΠΎΠΈ ΡΠΎΠ±ΡΡΠ²Π΅Π½Π½ΡΠ΅.</b>
""",
        "okteto": (
            "βοΈ <b>Π’Π²ΠΎΠΉ ΡΠ·Π΅ΡΠ±ΠΎΡ ΡΡΡΠ°Π½ΠΎΠ²Π»Π΅Π½ Π½Π° Okteto</b>. Π’Ρ Π±ΡΠ΄Π΅ΡΡ ΠΏΠΎΠ»ΡΡΠ°ΡΡ"
            " ΡΠ²Π΅Π΄ΠΎΠΌΠ»Π΅Π½ΠΈΡ ΠΎΡ @WebpageBot. ΠΠ΅ Π±Π»ΠΎΠΊΠΈΡΡΠΉ Π΅Π³ΠΎ."
        ),
        "railway": (
            "π <b>Π’Π²ΠΎΠΉ ΡΠ·Π΅ΡΠ±ΠΎΡ ΡΡΡΠ°Π½ΠΎΠ²Π»Π΅Π½ Π½Π° Railway</b>. ΠΠ° ΡΡΠΎΠΉ ΠΏΠ»Π°ΡΡΠΎΡΠΌΠ΅ ΡΡ"
            " ΠΏΠΎΠ»ΡΡΠ°Π΅ΡΡ ΡΠΎΠ»ΡΠΊΠΎ <b>500 Π±Π΅ΡΠΏΠ»Π°ΡΠ½ΡΡ ΡΠ°ΡΠΎΠ² Π² ΠΌΠ΅ΡΡΡ</b>. ΠΠΎΠ³Π΄Π° Π»ΠΈΠΌΠΈΡ Π±ΡΠ΄Π΅Ρ"
            " Π΄ΠΎΡΡΠΈΠ³Π½Π΅Ρ, ΡΠ²ΠΎΠΉ <b>ΡΠ·Π΅ΡΠ±ΠΎΡ Π±ΡΠ΄Π΅Ρ Π·Π°ΠΌΠΎΡΠΎΠΆΠ΅Π½</b>. Π ΡΠ»Π΅Π΄ΡΡΡΠ΅ΠΌ ΠΌΠ΅ΡΡΡΠ΅ <b>ΡΡ"
            " Π΄ΠΎΠ»ΠΆΠ΅Π½ Π±ΡΠ΄Π΅ΡΡ ΠΏΠ΅ΡΠ΅ΠΉΡΠΈ Π½Π° https://railway.app ΠΈ ΠΏΠ΅ΡΠ΅Π·Π°ΠΏΡΡΡΠΈΡΡ Π΅Π³ΠΎ</b>."
        ),
        "language_saved": "π·πΊ Π―Π·ΡΠΊ ΡΠΎΡΡΠ°Π½Π΅Π½!",
        "language": "π·πΊ Π ΡΡΡΠΊΠΈΠΉ",
        "btn_support": "π₯· Π§Π°Ρ ΠΏΠΎΠ΄Π΄Π΅ΡΠΆΠΊΠΈ",
    }

    strings_de = {
        "base": """ππ©πͺ <b>Hallo.</b> Dein Userbot <b>Bampi</b> ist installiert.

β <b>Brauchst du Hilfe?</b> Trete unserem Support-Chat bei. Wir helfen <b>allen</b>.

πΌ <b>Du kannst Module ΓΌber @Bampimods_bot suchen und installieren. Gib einfach einen Suchbegriff ein und drΓΌcke auf β© Install auf dem gewΓΌnschten Modul</b>

π£ <b>Schaue dir die Module-KanΓ€le an, die von der Community erstellt wurden: <a href="https://t.me/Bampi_ub/126">anzeigen</a></b>

πββοΈ <b>Schnellstart:</b>

1οΈβ£ <b>Schreibe </b><code>.help</code> <b>um eine Liste der Module zu sehen</b>
2οΈβ£ <b>Schreibe </b><code>.help &lt;Modulname/Befehl&gt;</code> <b>um die Beschreibung des Moduls zu sehen</b>
3οΈβ£ <b>Schreibe </b><code>.dlmod &lt;Link&gt;</code> <b>um ein Modul aus dem Link zu laden</b>
4οΈβ£ <b>Schreibe </b><code>.loadmod</code> <b>als Antwort auf eine Datei, um ein Modul aus der Datei zu laden</b>
5οΈβ£ <b>Schreibe </b><code>.unloadmod &lt;Modulname&gt;</code> <b>um ein Modul zu entladen</b>

π‘ <b>Bampi unterstΓΌtzt Module von Friendly-Telegram und GeekTG sowie eigene Module.</b>
""",
        "okteto": (
            "βοΈ <b>Dein Userbot ist auf Okteto installiert</b>. Du wirst"
            " Benachrichtigungen von @WebpageBot erhalten. Blockiere ihn nicht."
        ),
        "railway": (
            "π <b>Dein Userbot ist auf Railway installiert</b>. Du erhΓ€ltst nur <b>500"
            " kostenlose Stunden pro Monat</b> auf dieser Plattform. Wenn das Limit"
            " erreicht ist, wird dein <b>Userbot eingefroren</b>. Im nΓ€chsten Monat"
            " musst du zu https://railway.app gehen und ihn neu starten.</b>"
        ),
        "language_saved": "π©πͺ Sprache gespeichert!",
        "language": "π©πͺ Deutsch",
        "btn_support": "π₯· Support-Chat",
    }

    strings_uz = {
        "base": """ππΊπΏ <b>Salom.</b> <b>Bampi</b> Sizning yuzer botingiz sozlandi.

β <b>Yordam kerakmi?</b> Siz bizning qollab quvvatlash guruhimizga qo'shilishingiz mumkin. guruhimzda  <b>barcha savollaringizga javob olasiz</b>.

πΌ <b>Modullar @Bampimods_bot ushbu botimiz orqali siz har qanday yuzerbotga tegishli bo'lgan modullarni o'rnatishingiz mumkun botga kalit so'zni yuboring va  β© O'rnatish tugmasini bosing</b>

π£ <b>Homiylar tomonidan yaratilgan modullar kanalini ko'rish: <a href="https://t.me/Bampi_ub/126">kanalni ko'rish</a></b>

πββοΈ <b>Tez ishga tushurish:</b>

1οΈβ£ <b>Modullar royhatini ko'rish uchun </b><code>.help buyrug'ini</code> <b>yozing</b>
2οΈβ£ <b>Modul haqida ma'lumot olish uchun </b><code>.help &lt;Modul nomi/buyruq&gt;</code> <b>yozing</b>
3οΈβ£ <b>Modulni havola orqali o'rnatish uchun </b><code>.dlmod &lt;Link&gt;</code> <b>yozing</b>
4οΈβ£ <b>Modulni fayl orqali yuklash uchun </b><code>.loadmod</code> <b>faylga javoban yozing</b>
5οΈβ£ <b>Modulni olib tashlash uchun </b><code>.unloadmod &lt;Modul nomi&gt;</code> <b>yozing</b>

π‘ <b>Bampi Friendly-Telegram ve GeekTG O'z Modullarini qollab quvvatlaydi.</b>
""",
        "okteto": (
            "βοΈ <b>Sizning yuzerbotingiz oktetoda o'rnatilgan</b>. @WebpageBot'dan"
            " xabarlar qabul qilasiz uni bloklamang."
        ),
        "railway": (
            "π <b>Sizning yuzerbotingiz Railwayda o'rnatilgan</b>. Bu platforma,"
            " <b>oyiga atigi 500 soat bepul jihati</b> Railway bergan muddat tugagandan"
            " so'ng sizning bo'tingiz  <b>to'xtatiladi</b>. Keyingi oy,"
            " https://railway.app havolasi orqali yuzerbotingizni qayta ishga tushira"
            " olasiz.</b>"
        ),
        "language_saved": "πΊπΏ Til saqlandi!",
        "language": "πΊπΏ O'zbekcha",
        "btn_support": "π₯· Qo'llab-quvvatlash guruhi",
    }

    strings_tr = {
        "base": """ππΉπ· <b>Merhaba.</b> <b>Bampi</b> kullanΔ±cΔ± botunuz kuruldu.

β <b>YardΔ±ma mΔ± ihtiyacΔ±nΔ±z var?</b> YardΔ±m grubumuza katΔ±labilirsin. Herkese <b>yardΔ±m ediyoruz</b>.

πΌ <b>ModΓΌlleri @Bampimods_bot ile arayabilir ve kurabilirsiniz. Sadece anahtar kelimeleri girin ve istediΔiniz modΓΌlΓΌn β© Kur butonuna basΔ±n</b>

π£ <b>Topluluk tarafΔ±ndan oluΕturulan modΓΌl kanallarΔ± gΓΆrΓΌntΓΌleyin: <a href="https://t.me/Bampi_ub/126">gΓΆster</a></b>

πββοΈ <b>HΔ±zlΔ± baΕlangΔ±Γ§:</b>

1οΈβ£ <b>ModΓΌller listesini gΓΆrmek iΓ§in </b><code>.help</code> <b>yazΔ±n</b>
2οΈβ£ <b>ModΓΌl hakkΔ±nda bilgi almak iΓ§in </b><code>.help &lt;Modul adΔ±/Komut&gt;</code> <b>yazΔ±n</b>
3οΈβ£ <b>Bir baΔlantΔ±dan modΓΌl yΓΌklemek iΓ§in </b><code>.dlmod &lt;Link&gt;</code> <b>yazΔ±n</b>
4οΈβ£ <b>Bir modΓΌlΓΌ bir dosyadan yΓΌklemek iΓ§in </b><code>.loadmod</code> <b>bir dosyanΔ±n yanΔ±tΔ±nΔ± yazΔ±n</b>
5οΈβ£ <b>Bir modΓΌlΓΌ kaldΔ±rmak iΓ§in </b><code>.unloadmod &lt;Modul adΔ±&gt;</code> <b>yazΔ±n</b>

π‘ <b>Bampi Friendly-Telegram ve GeekTG modΓΌllerini de dahil olmak ΓΌzere kendi modΓΌllerini destekler.</b>
""",
        "okteto": (
            "βοΈ <b>KullanΔ±cΔ± botunuz Okteto'da kuruldu</b>. @WebpageBot'dan mesajlar"
            " alacaksΔ±nΔ±z. OnlarΔ± engellemeyin."
        ),
        "railway": (
            "π <b>KullanΔ±cΔ± botunuz Railway'de kuruldu</b>. Bu platform, <b>aylΔ±k"
            " sadece 500 saati ΓΌcretsiz olarak</b> saΔlamaktadΔ±r. SΔ±nΔ±rΔ± aΕtΔ±ΔΔ±nΔ±zda,"
            " kullanΔ±cΔ± botunuz <b>durdurulur</b>. Gelecek ay, https://railway.app"
            " adresinden botunuzu yeniden baΕlatmanΔ±z gerekmektedir.</b>"
        ),
        "language_saved": "πΉπ· Dil kaydedildi!",
        "language": "πΉπ· TΓΌrkΓ§e",
        "btn_support": "π₯· Destek grubu",
    }

    strings_hi = {
        "base": """ππ?π³ <b>ΰ€¨ΰ€?ΰ€Έΰ₯ΰ€€ΰ₯.</b> ΰ€ΰ€ͺΰ€ΰ€Ύ <b>Bampi</b> ΰ€ΰ€ͺΰ€―ΰ₯ΰ€ΰ€ΰ€°ΰ₯ΰ€€ΰ€Ύ ΰ€¬ΰ₯ΰ€ ΰ€Έΰ₯ΰ€₯ΰ€Ύΰ€ͺΰ€Ώΰ€€ ΰ€ΰ€Ώΰ€―ΰ€Ύ ΰ€ΰ€―ΰ€Ύ ΰ€Ήΰ₯.

β <b>ΰ€ΰ₯ΰ€―ΰ€Ύ ΰ€ΰ€ͺΰ€ΰ₯ ΰ€?ΰ€¦ΰ€¦ ΰ€ΰ₯ ΰ€ΰ€΅ΰ€Άΰ₯ΰ€―ΰ€ΰ€€ΰ€Ύ ΰ€Ήΰ₯?</b> ΰ€Ήΰ€?ΰ€Ύΰ€°ΰ₯ ΰ€Έΰ€Ύΰ€₯ ΰ€?ΰ€¦ΰ€¦ ΰ€ΰ₯ΰ€°ΰ₯ΰ€ͺ ΰ€?ΰ₯ΰ€ ΰ€Άΰ€Ύΰ€?ΰ€Ώΰ€² ΰ€Ήΰ₯ΰ€. ΰ€Ήΰ€? ΰ€Έΰ€¬ ΰ€ΰ₯ΰ€ ΰ€Έΰ€Ύΰ€ΰ€Ύ ΰ€ΰ€°ΰ₯ΰ€ΰ€ΰ₯.

πΌ <b>ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€²ΰ₯ΰ€Έ ΰ€ΰ₯ @Bampimods_bot ΰ€Έΰ₯ ΰ€ΰ₯ΰ€ΰ₯ΰ€ ΰ€ΰ€° ΰ€ΰ€ΰ€Έΰ₯ΰ€ΰ₯ΰ€² ΰ€ΰ€°ΰ₯ΰ€. ΰ€ΰ₯ΰ€΅ΰ€² ΰ€ΰ€ ΰ€ΰ₯ΰ€ ΰ€Άΰ€¬ΰ₯ΰ€¦ ΰ€¦ΰ€°ΰ₯ΰ€ ΰ€ΰ€°ΰ₯ΰ€ ΰ€ΰ€° ΰ€ΰ€ͺΰ€ΰ₯ ΰ€²ΰ€Ώΰ€ ΰ€ΰ€ͺΰ€²ΰ€¬ΰ₯ΰ€§ ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€ͺΰ€° β© ΰ€ΰ€ΰ€Έΰ₯ΰ€ΰ₯ΰ€² ΰ€¬ΰ€ΰ€¨ ΰ€ͺΰ€° ΰ€ΰ₯ΰ€²ΰ€Ώΰ€ ΰ€ΰ€°ΰ₯ΰ€</b>

π£ <b>ΰ€Έΰ€?ΰ₯ΰ€¦ΰ€Ύΰ€― ΰ€¦ΰ₯ΰ€΅ΰ€Ύΰ€°ΰ€Ύ ΰ€¬ΰ€¨ΰ€Ύΰ€ ΰ€ΰ€ ΰ€ΰ₯ΰ€¨ΰ€² ΰ€¦ΰ₯ΰ€ΰ₯ΰ€: <a href="https://t.me/Bampi_ub/126">ΰ€¦ΰ€Ώΰ€ΰ€Ύΰ€ΰ€</a></b>

πββοΈ <b>ΰ€€ΰ₯ΰ€΅ΰ€°ΰ€Ώΰ€€ ΰ€Άΰ₯ΰ€°ΰ₯ΰ€ΰ€€:</b>

1οΈβ£ <b>ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€²ΰ₯ΰ€ ΰ€ΰ₯ ΰ€Έΰ₯ΰ€ΰ₯ ΰ€¦ΰ₯ΰ€ΰ€¨ΰ₯ ΰ€ΰ₯ ΰ€²ΰ€Ώΰ€ </b><code>.help</code> <b>ΰ€ΰ€Ύΰ€ΰ€ͺ ΰ€ΰ€°ΰ₯ΰ€</b>
2οΈβ£ <b>ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€ΰ₯ ΰ€¬ΰ€Ύΰ€°ΰ₯ ΰ€?ΰ₯ΰ€ ΰ€ΰ€Ύΰ€¨ΰ€ΰ€Ύΰ€°ΰ₯ ΰ€ͺΰ₯ΰ€°ΰ€Ύΰ€ͺΰ₯ΰ€€ ΰ€ΰ€°ΰ€¨ΰ₯ ΰ€ΰ₯ ΰ€²ΰ€Ώΰ€ </b><code>.help &lt;ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€¨ΰ€Ύΰ€?/ΰ€ΰ€?ΰ€Ύΰ€ΰ€‘&gt;</code> <b>ΰ€ΰ€Ύΰ€ΰ€ͺ ΰ€ΰ€°ΰ₯ΰ€</b>
3οΈβ£ <b>ΰ€²ΰ€Ώΰ€ΰ€ ΰ€Έΰ₯ ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€ΰ€ΰ€Έΰ₯ΰ€ΰ₯ΰ€² ΰ€ΰ€°ΰ€¨ΰ₯ ΰ€ΰ₯ ΰ€²ΰ€Ώΰ€ </b><code>.dlmod &lt;ΰ€²ΰ€Ώΰ€ΰ€&gt;</code> <b>ΰ€ΰ€Ύΰ€ΰ€ͺ ΰ€ΰ€°ΰ₯ΰ€</b>
4οΈβ£ <b>ΰ€ΰ€ ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€ΰ₯ ΰ€«ΰ€Ύΰ€ΰ€² ΰ€Έΰ₯ ΰ€²ΰ₯ΰ€‘ ΰ€ΰ€°ΰ€¨ΰ₯ ΰ€ΰ₯ ΰ€²ΰ€Ώΰ€ </b><code>.loadmod</code> <b>ΰ€ΰ€ ΰ€«ΰ€Όΰ€Ύΰ€ΰ€² ΰ€ΰ€Ύ ΰ€ΰ€€ΰ₯ΰ€€ΰ€° ΰ€¦ΰ€°ΰ₯ΰ€ ΰ€ΰ€°ΰ₯ΰ€</b>
5οΈβ£ <b>ΰ€ΰ€ ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€ΰ₯ ΰ€Ήΰ€ΰ€Ύΰ€¨ΰ₯ ΰ€ΰ₯ ΰ€²ΰ€Ώΰ€ </b><code>.unloadmod &lt;ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€¨ΰ€Ύΰ€?&gt;</code> <b>ΰ€ΰ€Ύΰ€ΰ€ͺ ΰ€ΰ€°ΰ₯ΰ€</b>

π‘ <b>ΰ€ΰ€ͺΰ€¨ΰ₯ ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€ΰ₯ ΰ€Έΰ€?ΰ€°ΰ₯ΰ€₯ΰ€Ώΰ€€ ΰ€ΰ€°ΰ€¨ΰ₯ ΰ€ΰ₯ ΰ€²ΰ€Ώΰ€, Bampi Friendly-Telegram ΰ€ΰ€° GeekTG ΰ€?ΰ₯ΰ€‘ΰ₯ΰ€―ΰ₯ΰ€² ΰ€­ΰ₯ ΰ€Άΰ€Ύΰ€?ΰ€Ώΰ€² ΰ€Ήΰ₯ΰ€.</b>
""",
        "okteto": (
            "βοΈ <b>ΰ€ΰ€ͺΰ€ΰ€Ύ ΰ€ΰ€ͺΰ€―ΰ₯ΰ€ΰ€ΰ€°ΰ₯ΰ€€ΰ€Ύ ΰ€¬ΰ₯ΰ€ Okteto ΰ€ͺΰ€° ΰ€¬ΰ€¨ΰ€Ύΰ€―ΰ€Ύ ΰ€ΰ€―ΰ€Ύ ΰ€₯ΰ€Ύ</b>ΰ₯€ @WebpageBot ΰ€Έΰ₯ ΰ€Έΰ€ΰ€¦ΰ₯ΰ€Ά"
            "ΰ€ΰ€ͺ ΰ€ΰ€°ΰ₯ΰ€ΰ€ΰ₯ΰ₯€ ΰ€ΰ€¨ΰ₯ΰ€Ήΰ₯ΰ€ ΰ€¬ΰ₯ΰ€²ΰ₯ΰ€ ΰ€¨ ΰ€ΰ€°ΰ₯ΰ€ΰ₯€"
        ),
        "railway": (
            "π <b>ΰ€ΰ€ͺΰ€ΰ€Ύ ΰ€ΰ€ͺΰ€―ΰ₯ΰ€ΰ€ΰ€°ΰ₯ΰ€€ΰ€Ύ ΰ€¬ΰ₯ΰ€ ΰ€°ΰ₯ΰ€²ΰ€΅ΰ₯ ΰ€?ΰ₯ΰ€ ΰ€Έΰ₯ΰ€₯ΰ€Ύΰ€ͺΰ€Ώΰ€€ ΰ€ΰ€Ώΰ€―ΰ€Ύ ΰ€ΰ€―ΰ€Ύ ΰ€₯ΰ€Ύ</b>ΰ₯€ ΰ€―ΰ€Ή ΰ€?ΰ€ΰ€"
            " <b>ΰ€?ΰ€Ύΰ€Έΰ€Ώΰ€ ΰ€Ήΰ₯ ΰ€ΰ₯ΰ€΅ΰ€² 500 ΰ€ΰ€ΰ€ΰ₯ ΰ€¨ΰ€Ώΰ€ΰ€Άΰ₯ΰ€²ΰ₯ΰ€ ΰ€ͺΰ₯ΰ€°ΰ€¦ΰ€Ύΰ€¨ ΰ€ΰ€°ΰ€€ΰ€Ύ ΰ€Ήΰ₯</b>ΰ₯€ ΰ€ΰ€ ΰ€¬ΰ€Ύΰ€° ΰ€ΰ€¬ ΰ€ΰ€ͺ ΰ€Έΰ₯ΰ€?ΰ€Ύ"
            " ΰ€ͺΰ€Ύΰ€° ΰ€ΰ€° ΰ€²ΰ₯ΰ€€ΰ₯ ΰ€Ήΰ₯ΰ€, ΰ€ΰ€ͺΰ€ΰ€Ύ ΰ€ΰ€ͺΰ€―ΰ₯ΰ€ΰ€ΰ€°ΰ₯ΰ€€ΰ€Ύ ΰ€¬ΰ₯ΰ€ <b>ΰ€°ΰ₯ΰ€ΰ€Ύ ΰ€ΰ€―ΰ€Ύ</b> ΰ€Ήΰ₯ΰ₯€ ΰ€ΰ€ΰ€²ΰ₯ ΰ€?ΰ€Ήΰ₯ΰ€¨ΰ₯,"
            " https://railway.appΰ€ΰ€ͺΰ€ΰ₯ ΰ€ΰ€ͺΰ€¨ΰ₯ ΰ€¬ΰ₯ΰ€ ΰ€ΰ₯ ΰ€Έΰ₯ ΰ€ͺΰ₯ΰ€¨ΰ€ ΰ€ΰ€°ΰ€ΰ€­ ΰ€ΰ€°ΰ€¨ΰ₯ ΰ€ΰ₯ ΰ€ΰ€΅ΰ€Άΰ₯ΰ€―ΰ€ΰ€€ΰ€Ύ ΰ€Ήΰ₯.</b>"
        ),
        "language_saved": "π?π³ ΰ€­ΰ€Ύΰ€·ΰ€Ύ ΰ€Έΰ€Ήΰ₯ΰ€ΰ€Ύ ΰ€ΰ€―ΰ€Ύ!",
        "language": "π?π³ ΰ€Ήΰ€Ώΰ€ΰ€¦ΰ₯",
        "btn_support": "π₯· ΰ€Έΰ€?ΰ€°ΰ₯ΰ€₯ΰ€¨ ΰ€Έΰ€?ΰ₯ΰ€Ή",
    }

    strings_ja = {
        "base": """
πΌ <b>γ’γΈγ₯γΌγ«γζ€η΄’γγ¦γ€γ³γΉγγΌγ«γγγ«γ― @Bampimods_bot γγζ€η΄’γγ¦γγ γγγζ€η΄’γ―γΌγγ1γ€ε₯εγγ¦γγ γγγ</b>

π£ <b>γ³γγ₯γγγ£γ§δ½ζγγγγγ£γ³γγ«γθ¦γγ«γ―γγγ‘γγγ―γͺγγ―γγ¦γγ γγ: <a href="https://t.me/Bampi_ub/126">θ‘¨η€Ί</a></b>

πββοΈ <b>γγγ«ε§γγγ«γ―:</b>

1οΈβ£ <b>γ’γΈγ₯γΌγ«γ?γͺγΉγγθ‘¨η€Ίγγγ«γ― </b><code>.help</code> <b>γε₯εγγΎγ</b>
2οΈβ£ <b>γ’γΈγ₯γΌγ«γ«γ€γγ¦γ?ζε ±γεεΎγγγ«γ― </b><code>.help &lt;γ’γΈγ₯γΌγ«ε/γ³γγ³γ&gt;</code> <b>γε₯εγγΎγ</b>
3οΈβ£ <b>γͺγ³γ―γγγ’γΈγ₯γΌγ«γγ€γ³γΉγγΌγ«γγγ«γ― </b><code>.dlmod &lt;γͺγ³γ―&gt;</code> <b>γε₯εγγΎγ</b>
4οΈβ£ <b>γ’γΈγ₯γΌγ«γγγ‘γ€γ«γγγ­γΌγγγγ«γ― </b><code>.loadmod</code> <b>γγ‘γ€γ«γ?θΏδΏ‘γε₯εγγΎγ</b>
5οΈβ£ <b>γ’γΈγ₯γΌγ«γει€γγγ«γ― </b><code>.unloadmod &lt;γ’γΈγ₯γΌγ«ε&gt;</code> <b>γε₯εγγΎγ</b>

π‘ <b>γ’γΈγ₯γΌγ«γγ΅γγΌγγγγ«γ―γBampi Friendly-Telegram γ¨ GeekTG γ’γΈγ₯γΌγ«γε«γΎγγ¦γγΎγγ</b>
""",
        "okteto": (
            "βοΈ <b>γγͺγγ?γ¦γΌγΆγΌγγγγ― Okteto γ§δ½ζγγγΎγγ</b>γ @WebpageBot γ«γ‘γγ»γΌγΈγιδΏ‘γγΎγγ"
            "γγ­γγ―γγͺγγ§γγ γγγ"
        ),
        "railway": (
            "π <b>γγͺγγ?γ¦γΌγΆγΌγγγγ―γ¬γΌγ«γ¦γ§γ€γ§δ½ζγγγΎγγ</b>γ γγ?γγ©γγγγ©γΌγ γ―"
            " <b>ζιγ§η‘ζγ§500ζιγ?γΏζδΎγγγΎγ</b>γ δΈεΊ¦δΈιγ«ιγγγ¨γ"
            "γγͺγγ?γ¦γΌγΆγΌγγγγ― <b>γγ­γγ―γγγΎγ</b>γ ζ¬‘γ?ζγ«γ"
            " https://railway.app γγͺγγ?γγγγειγγεΏθ¦γγγγΎγγ</b>"
        ),
        "language_saved": "π―π΅ θ¨θͺγδΏε­γγγΎγγ!",
        "language": "π―π΅ ζ₯ζ¬θͺ",
        "btn_support": "π₯· γ΅γγΌγγ°γ«γΌγ",
    }

    strings_kr = {
        "base": """
πΌ <b>λͺ¨λμ κ²μνκ³  μ€μΉνλ €λ©΄ @Bampimods_bot μμ κ²μνμ­μμ€. κ²μμ΄λ₯Ό μλ ₯νμ­μμ€.</b>

π£ <b>μ»€λ?€λν°μμ μμ±λ μ±λμ λ³΄λ €λ©΄ μ¬κΈ°λ₯Ό ν΄λ¦­νμ­μμ€: <a href="https://t.me/Bampi_ub/126">λ³΄κΈ°</a></b>

πββοΈ <b>μ¦μ μμνλ €λ©΄:</b>

1οΈβ£ <b>λͺ¨λ λͺ©λ‘μ νμνλ €λ©΄ </b><code>.help</code> <b>λ₯Ό μλ ₯νμ­μμ€</b>
2οΈβ£ <b>λͺ¨λμ λν μ λ³΄λ₯Ό κ°μ Έ μ€λ €λ©΄ </b><code>.help &lt;λͺ¨λ μ΄λ¦/λͺλ Ή&gt;</code> <b>λ₯Ό μλ ₯νμ­μμ€</b>
3οΈβ£ <b>λ§ν¬μμ λͺ¨λμ μ€μΉνλ €λ©΄ </b><code>.dlmod &lt;λ§ν¬&gt;</code> <b>λ₯Ό μλ ₯νμ­μμ€</b>
4οΈβ£ <b>λͺ¨λμ νμΌμμλ‘λνλ €λ©΄ </b><code>.loadmod</code> <b>νμΌμ μλ΅μ μλ ₯νμ­μμ€</b>
5οΈβ£ <b>λͺ¨λμ μ κ±°νλ €λ©΄ </b><code>.unloadmod &lt;λͺ¨λ μ΄λ¦&gt;</code> <b>λ₯Ό μλ ₯νμ­μμ€</b>

π‘ <b>λͺ¨λμ μ§μνλ €λ©΄ Bampi Friendly-Telegram λ° GeekTG λͺ¨λλ ν¬ν¨λ©λλ€.</b>
""",
        "okteto": (
            "βοΈ <b>μ¬μ©μ λ΄μ Oktetoμμ λ§λ€μ΄μ‘μ΅λλ€</b> @WebpageBot μ λ©μμ§λ₯Ό λ³΄λ΄μ­μμ€.μ°¨λ¨νμ§ λ§μ­μμ€."
        ),
        "railway": (
            "π <b>μ¬μ©μ λ΄μ λ μΌμ¨μ΄μμ λ§λ€μ΄μ‘μ΅λλ€</b> μ΄ νλ«νΌμ"
            " <b>μκ°μΌλ‘ λ¬΄λ£λ‘ 500 μκ°λ§ μ κ³΅λ©λλ€</b> ν λ² μ νμ λλ¬νλ©΄,"
            "μ¬μ©μ λ΄μ <b>μ°¨λ¨λ©λλ€</b> λ€μ λ¬μ,"
            " https://railway.app μ¬μ©μ λ΄μ λ€μ μμν΄μΌν©λλ€.</b>"
        ),
        "language_saved": "π°π· μΈμ΄κ° μ μ₯λμμ΅λλ€!",
        "language": "π°π· νκ΅­μ΄",
        "btn_support": "π₯· μ§μ κ·Έλ£Ή",
    }

    strings_ar = {
        "base": """
πΌ <b>ΩΩΨ¨Ψ­Ψ« ΨΉΩ ΩΨͺΨ«Ψ¨ΩΨͺ Ψ§ΩΩΨ­Ψ―Ψ§ΨͺΨ ΩΨ±Ψ¬Ω Ψ§ΩΨ°ΩΨ§Ψ¨ Ψ₯ΩΩ @Bampimods_bot ΩΨ₯Ψ―Ψ?Ψ§Ω Ψ§ΩΩΩΩΨ§Ψͺ Ψ§ΩΩΩΨͺΨ§Ψ­ΩΨ©.</b>

π£ <b>ΩΩΨ΄Ψ§ΩΨ―Ψ© ΩΩΩΨ§Ψͺ Ψ§ΩΩΨ¬ΨͺΩΨΉ Ψ§ΩΨͺΩ ΨͺΩ Ψ₯ΩΨ΄Ψ§Ψ€ΩΨ§Ψ Ψ§ΩΩΨ± ΩΩΨ§: <a href="https://t.me/Bampi_ub/126">ΨΉΨ±ΨΆ</a></b>

πββοΈ <b>ΩΩΨ¨Ψ―Ψ‘ ΩΩΨ±ΩΨ§:</b>

1οΈβ£ <b>ΩΨΉΨ±ΨΆ ΩΨ§Ψ¦ΩΨ© Ψ§ΩΩΨ­Ψ―Ψ§ΨͺΨ Ψ§ΩΨͺΨ¨ </b><code>.help</code> <b>ΩΨ£Ψ―Ψ?Ω</b>
2οΈβ£ <b>ΩΩΨ­Ψ΅ΩΩ ΨΉΩΩ ΩΨΉΩΩΩΨ§Ψͺ ΨΉΩ Ψ§ΩΩΨ­Ψ―Ψ©Ψ Ψ§ΩΨͺΨ¨ </b><code>.help &lt;Ψ§Ψ³Ω Ψ§ΩΩΨ­Ψ―Ψ©/Ψ§ΩΨ£ΩΨ±&gt;</code> <b>ΩΨ£Ψ―Ψ?Ω</b>
3οΈβ£ <b>ΩΨͺΨ«Ψ¨ΩΨͺ Ψ§ΩΩΨ­Ψ―Ψ© ΩΩ Ψ§ΩΨ±Ψ§Ψ¨Ψ·Ψ Ψ§ΩΨͺΨ¨ </b><code>.dlmod &lt;Ψ§ΩΨ±Ψ§Ψ¨Ψ·&gt;</code> <b>ΩΨ£Ψ―Ψ?Ω</b>
4οΈβ£ <b>ΩΨͺΨ­ΩΩΩ Ψ§ΩΩΨ­Ψ―Ψ© ΩΩ Ψ§ΩΩΩΩΨ Ψ§ΩΨͺΨ¨ </b><code>.loadmod</code> <b>ΩΨ£Ψ±Ψ³Ω Ψ§ΩΩΩΩ Ψ§ΩΩΨ±Ψ§Ψ― ΨͺΨ­ΩΩΩΩ</b>
5οΈβ£ <b>ΩΨ₯Ψ²Ψ§ΩΨ© Ψ§ΩΩΨ­Ψ―Ψ©Ψ Ψ§ΩΨͺΨ¨ </b><code>.unloadmod &lt;Ψ§Ψ³Ω Ψ§ΩΩΨ­Ψ―Ψ©&gt;</code> <b>ΩΨ£Ψ―Ψ?Ω</b>

π‘ <b>ΩΨ―ΨΉΩ Ψ§ΩΩΨ­Ψ―Ψ§ΨͺΨ ΩΨͺΨΆΩΩ Bampi Friendly-Telegram Ω GeekTG Ψ£ΩΨΆΩΨ§.</b>
""",
        "okteto": (
            "βοΈ <b>ΨͺΩ Ψ₯ΩΨ΄Ψ§Ψ‘ Ψ¨ΩΨͺ Ψ§ΩΩΨ³ΨͺΨ?Ψ―Ω ΨΉΩΩ Okteto</b> Ψ§Ψ±Ψ³Ω Ψ±Ψ³Ψ§ΩΨ© Ψ₯ΩΩ @WebpageBot ΩΩΨ§"
            " ΨͺΨ­ΨΈΨ±Ω."
        ),
        "railway": (
            "π <b>ΨͺΩ Ψ₯ΩΨ΄Ψ§Ψ‘ Ψ¨ΩΨͺ Ψ§ΩΩΨ³ΨͺΨ?Ψ―Ω ΨΉΩΩ Railway</b> ΩΨ°Ω Ψ§ΩΩΩΨ΅Ψ© ΨͺΩΨ―Ω"
            " <b>500 Ψ³Ψ§ΨΉΨ© ΩΨ¬Ψ§ΩΩΨ© Ψ΄ΩΨ±ΩΩΨ§</b> Ψ¨ΩΨ¬Ψ±Ψ― Ψ§ΩΩΨ΅ΩΩ Ψ₯ΩΩ Ψ§ΩΨ­Ψ― Ψ§ΩΨ£ΩΨ΅ΩΨ"
            "Ψ³ΩΨͺΩ Ψ­ΨΈΨ± Ψ¨ΩΨͺ Ψ§ΩΩΨ³ΨͺΨ?Ψ―Ω <b>Ψ­ΨͺΩ Ψ§ΩΨ΄ΩΨ± Ψ§ΩΩΨ§Ψ―Ω</b> ΩΨ±Ψ¬Ω Ψ₯ΨΉΨ§Ψ―Ψ© ΨͺΨ΄ΨΊΩΩ"
            " <b>Ψ¨ΩΨͺ Ψ§ΩΩΨ³ΨͺΨ?Ψ―Ω ΩΩ https://railway.app</b>"
        ),
        "language_saved": "πΈπ¦ ΨͺΩ Ψ­ΩΨΈ Ψ§ΩΩΨΊΨ©!",
        "language": "πΈπ¦ Ψ§ΩΨΉΨ±Ψ¨ΩΨ©",
        "btn_support": "π₯· ΩΨ¬ΩΩΨΉΨ© Ψ§ΩΨ―ΨΉΩ",
    }

    strings_es = {
        "base": """
πΌ <b>Para buscar e instalar mΓ³dulos, vaya a @Bampimods_bot y escriba las palabras clave.</b>

π£ <b>Para ver los canales de la comunidad creados, haga clic aquΓ­: <a href="https://t.me/Bampi_ub/126">Ver</a></b>

πββοΈ <b>Para comenzar de inmediato:</b>

1οΈβ£ <b>Para ver la lista de mΓ³dulos, escriba </b><code>.help</code> <b>y presione</b>
2οΈβ£ <b>Para obtener informaciΓ³n sobre el mΓ³dulo, escriba </b><code>.help &lt;nombre del mΓ³dulo/comando&gt;</code> <b>y presione</b>
3οΈβ£ <b>Para instalar el mΓ³dulo desde el enlace, escriba </b><code>.dlmod &lt;enlace&gt;</code> <b>y presione</b>
4οΈβ£ <b>Para cargar el mΓ³dulo desde el archivo, escriba </b><code>.loadmod</code> <b>y responda al archivo que desea cargar</b>
5οΈβ£ <b>Para eliminar el mΓ³dulo, escriba </b><code>.unloadmod &lt;nombre del mΓ³dulo&gt;</code> <b>y presione</b>

π‘ <b>Para admitir mΓ³dulos, tambiΓ©n incluye Bampi Friendly-Telegram y GeekTG.</b>
""",
        "okteto": (
            "βοΈ <b>Se ha creado el bot de usuario en Okteto</b> envΓ­e un mensaje a"
            " @WebpageBot y no lo bloquee."
        ),
        "railway": (
            "π <b>Se ha creado el bot de usuario en Railway</b> esta plataforma ofrece"
            " <b>500 horas gratis al mes</b> una vez que llegue al lΓ­mite, el <b>bot de"
            " usuario serΓ‘ bloqueado hasta el prΓ³ximo mes</b> por favor, reinicie <b>el"
            " bot de usuario en https://railway.app</b>"
        ),
        "language_saved": "πͺπΈ Β‘El idioma se ha guardado!",
        "language": "πͺπΈ EspaΓ±ol",
        "btn_support": "π₯· Grupo de soporte",
    }

    async def client_ready(self):
        if self.get("disable_quickstart"):
            raise loader.SelfUnload

        self.mark = (
            lambda: [
                [
                    {
                        "text": self.strings("btn_support"),
                        "url": "https://t.me/Bampiss",
                    }
                ],
            ]
            + [
                [
                    {
                        "text": "π©ββοΈ Privacy Policy",
                        "url": "https://docs.google.com/document/d/15m6-pb1Eya8Zn4y0_7JEdvMLAo_v050rFMaWrjDjvMs/edit?usp=sharing",
                    },
                    {
                        "text": "π EULA",
                        "url": "https://docs.google.com/document/d/1sZBk24SWLBLoGxcsZHW8yP7yLncToPGUP1FJ4dS6z5I/edit?usp=sharing",
                    },
                ]
            ]
            + utils.chunks(
                [
                    {
                        "text": (
                            getattr(self, f"strings_{lang}")
                            if lang != "en"
                            else self.strings._base_strings
                        )["language"],
                        "callback": self._change_lang,
                        "args": (lang,),
                    }
                    for lang in [
                        "ru",
                        "en",
                        "uz",
                        "tr",
                        "hi",
                        "de",
                        "ja",
                        "kr",
                        "ar",
                        "es",
                    ]
                ],
                2,
            )
        )

        self.text = (
            lambda: self.strings("base")
            + (self.strings("okteto") if "OKTETO" in os.environ else "")
            + (self.strings("railway") if "RAILWAY" in os.environ else "")
        )

        await self.inline.bot.send_animation(self._client.tg_id, animation=choice(imgs))
        await self.inline.bot.send_message(
            self._client.tg_id,
            self.text(),
            reply_markup=self.inline.generate_markup(self.mark()),
            disable_web_page_preview=True,
        )

        self.set("disable_quickstart", True)

    async def _change_lang(self, call: BotInlineCall, lang: str):
        self._db.set(translations.__name__, "lang", lang)
        await self.translator.init()

        for module in self.allmodules.modules:
            try:
                module.config_complete(reload_dynamic_translate=True)
            except Exception as e:
                logger.debug(
                    "Can't complete dynamic translations reload of %s due to %s",
                    module,
                    e,
                )

        await call.answer(self.strings("language_saved"))
        await call.edit(text=self.text(), reply_markup=self.mark())
