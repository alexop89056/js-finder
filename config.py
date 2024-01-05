FILE_PATTERNS = {
    'js': r'(["\'])(https?://[^"\']*?\.js\??[^"\']*?)\1',
    'xml': r'(["\'])(https?://[^"\']*?\.xml\??[^"\']*?)\1',
    'php': r'(["\'])(https?://[^"\']*?\.php\??[^"\']*?)\1',
}

URL_REGEX = '^https?://(?:www\.)?[\w-]+\.[a-z]{2,3}(?:/\S*)?$'
USER_AGENT = {'User-Agent': 'Mozilla/5.0'}
DELAY_DEFAULT = 0.2

APP_LOGO = """
    
 .----------------. .----------------. .----------------. .----------------. 
| .--------------. | .--------------. | .--------------. | .--------------. |
| | ____    ____ | | |   _    _     | | | _____  _____ | | |     __       | |
| ||_   \  /   _|| | |  | |  | |    | | ||_   _||_   _|| | |    /  |      | |
| |  |   \/   |  | | |  | |__| |_   | | |  | | /\ | |  | | |    `| |      | |
| |  | |\  /| |  | | |  |____   _|  | | |  | |/  \| |  | | |     | |      | |
| | _| |_\/_| |_ | | |      _| |_   | | |  |   /\   |  | | |    _| |_     | |
| ||_____||_____|| | |     |_____|  | | |  |__/  \__|  | | |   |_____|    | |
| |              | | |              | | |              | | |              | |
| '--------------' | '--------------' | '--------------' | '--------------' |
 '----------------' '----------------' '----------------' '----------------' 

"""