from googletrans import Translator
translator = Translator()
# 未提供源语言以及翻译的最终语言,会自动翻译成英文
translator.translate('안녕하세요.')
# 告诉它翻译成什么语言
translator.translate('안녕하세요.', dest='ja')
# 告诉它源语言是什么
translator.translate('极客飞兔', src='zh-cn')
# 语言检测
t = ttranslator.detect('이 문장은 한글로 쓰여졌습니다.')
t.lang
