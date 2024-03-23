from OpenSSL import crypto
from cryptography import x509
from cryptography.hazmat.backends import default_backend

rb = ["country01.pfx", "country02.pfx", "country03.pfx", "country04.pfx", "country05.pfx", "country06.pfx"]

passwords = [
    'afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'antigua and barbuda',
    'argentina', 'armenia', 'australia', 'austria', 'azerbaijan', 'bahamas',
    'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize',
    'benin', 'bhutan', 'bolivia', 'bosnia and herzegovina', 'botswana', 'brazil',
    'brunei', 'bulgaria', 'burkina faso', 'burundi', 'cabo verde', 'cambodia',
    'cameroon', 'canada', 'central african republic', 'chad', 'chile', 'china',
    'colombia', 'comoros', 'congo', 'costa rica', 'croatia', 'cuba', 'cyprus',
    'czech republic', 'denmark', 'djibouti', 'dominica', 'dominican republic',
    'east timor', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea',
    'estonia', 'eswatini', 'ethiopia', 'fiji', 'finland', 'france', 'gabon', 'gambia',
    'georgia', 'ghana', 'greece', 'grenada', 'guatemala', 'guinea',
    'guinea-bissau', 'guyana', 'haiti', 'honduras', 'hungary', 'india',
    'indonesia', 'iran', 'iraq', 'ire', 'georgia', 'germany', 'ghana', 'greece', 'grenada', 'guatemala', 'guinea',
    'guinea-bissau', 'guyana', 'haiti', 'honduras', 'hungary', 'iceland', 'india',
    'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan',
    'jordan', 'kazakhstan', 'kenya', 'kiribati', 'north korea', 'south korea',
    'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho',
    'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'madagascar',
    'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands',
    'mauritania', 'mauritius', 'mexico', 'micronesia', 'moldova', 'monaco',
    'mongolia', 'montenegro', 'morocco', 'mozambique', 'myanmar', 'namibia',
    'nauru', 'nepal', 'netherlands', 'new zealand', 'nicaragua', 'niger', 'nigeria',
    'north macedonia', 'norway', 'oman', 'pakistan', 'palau', 'palestine', 'panama',
    'papua new guinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal',
    'qatar', 'romania', 'russia', 'rwanda', 'saint kitts and nevis', 'saint lucia',
    'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe',
    'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore',
    'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south sudan',
    'spain', 'sri lanka', 'sudan', 'suriname', 'sweden', 'switzerland', 'syria',
    'taiwan', 'tajikistan', 'tanzania', 'thailand', 'togo', 'tonga', 'trinidad and tobago',
    'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates',
    'united kingdom', 'united states', 'uruguay', 'uzbekistan', 'vanuatu', 'vatican city',
    'venezuela', 'vietnam', 'yemen', 'zambia', 'zimbabwe'
]

for file in rb:
    for password in passwords:

        try:
            pfx = open(file, 'rb').read()
            
            p12 = crypto.load_pkcs12(pfx, password)
            
            print (f"- **{file}**: {password}")

        except:
            continue