import winreg


def get_system_proxy():
    proxy = {}
    try:
        # accesam registrul din setarile windows
        internet_settings = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                           r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')

        # luam valorile din refistru setarilor
        proxy_enable = winreg.QueryValueEx(internet_settings, 'ProxyEnable')[0]
        proxy_server = winreg.QueryValueEx(internet_settings, 'ProxyServer')[0]

        if proxy_enable:
            # verificam daca sunt specifice pentru hhtp si https
            if '=' in proxy_server:
                for p in proxy_server.split(';'):
                    if p.startswith('http='):
                        proxy['http'] = 'http://' + p.split('=')[1]
                    elif p.startswith('https='):
                        proxy['https'] = 'https://' + p.split('=')[1]
            else:
                proxy_address = 'http://' + proxy_server
                proxy['http'] = proxy_address
                proxy['https'] = proxy_address
    except Exception as e:
        print(f"Could not get proxy settings: {e}")

    return proxy


# # TEST
# system_proxies = get_system_proxy()
# print(system_proxies)
