

def change_url(company_search_name):
    # return f"https://www.google.com/search?q=%22{company_search_name.replace(' ','+')}%22+-unimedia+-autoblog+" \
    #        "-noi.md+-TVR+-TV8+-zugo.md+-telegraph.md+-Pro&lr=lang_ro&cr=countryMD&sca_esv=9fc63cc73e9e59b8&tbs=" \
    #        "lr:lang_1ro,ctr:countryMD,qdr:m&tbm=nws&sxsrf=ACQVn08MkeYFl8L0oH1_iVIg7ywcbNAszg:1711955038244&source=" \
    #        "lnt&sa=X&ved=2ahUKEwiQ2bO_uaCFAxWHgv0HHUJhDjQQpwV6BAgBEA8&biw=1124&bih=901&dpr=1.5"
    #
    # return f"https://www.google.com/search?q={company_search_name.replace(' ','+')}+-unimedia+-autoblog+-noi.md+-" \
    #        f"TVR+-TV8+-zugo.md+-telegraph.md+-Pro+-horoscop+-zodii+-observatorul.md&lr=lang_ro&cr=countryMD&sca_es" \
    #        f"v=92f3b3f3bf62a3d6&sca_upv=1&biw=1707&bih=906&tbs=qdr%3Am%2Clr%3Alang_1ro%2Cctr%3AcountryMD&tbm=nws&" \
    #        f"sxsrf=ACQVn0-B-5a6CxdBUj8gO_mMMmjN3e8ZZg%3A1711963088562&ei=0HsKZtjiIej87_UPsuKWmAw&udm=&ved=0ahUKE" \
    #        f"wjYioy-16CFAxVo_rsIHTKxBcMQ4dUDCA0&uact=5&oq={company_search_name.replace(' ','+')}+-unimedia+-auto" \
    #        f"blog+-noi.md+-TVR+-TV8+-zugo.md+-telegraph.md+-Pro+-horoscop+-zodii+-observatorul.md&gs_lp=Egxnd3Mt" \
    #        f"d2l6LW5ld3MibkdlbWVuaWkgU0EgLXVuaW1lZGlhIC1hdXRvYmxvZyAtbm9pLm1kIC1UVlIgLVRWOCAtenVnby5tZCAtdGVsZWdy" \
    #        f"YXBoLm1kIC1Qcm8gLWhvcm9zY29wIC16b2RpaSAtb2JzZXJ2YXRvcnVsLm1kSABQAFgAcAB4AJABAJgBAKABAKoBALgBA8gBAPgB" \
    #        f"AfgBApgCAKACAJgDAJIHAKAHAA&sclient=gws-wiz-news"

    return f"https://www.google.com/search?q=%22{company_search_name.replace(' ','+')}%22+-unimedia+-autoblog+" \
           f"-noi.md+-TVR+-TV8+-zugo.md+-telegraph.md+-Pro+-horoscop+-zodii+-observatorul.md&lr=lang_ro&cr=" \
           f"countryMD&sca_esv=2fadc5c1139010e7&sca_upv=1&tbs=qdr:m,lr:lang_1ro,ctr:countryMD,sbd:1&tbm=nw" \
           f"s&prmd=isvnbtz&sxsrf=ACQVn09EyiIRJSNaTxBBzHtp4BT19xgKhw:1711965993607&source=lnt&sa=X&ved=2ahUKEwjN" \
           f"jKqn4qCFAxXUgf0HHeGPD2UQpwV6BAgCEBk&biw=1707&bih=906&dpr=1.5"