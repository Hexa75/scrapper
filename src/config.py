input_url = "https://fr.trustpilot.com/review/"
extension = '.eu'

scrap_tag = {'card': 'div', 'title': 'h2', 'rating': 'div', 'review': 'p', 'date': 'p', 'reply': 'p'}
scrap_class = {'card': "styles_cardWrapper__LcCPA", 'title': 'typography_heading-s__f7029',
               'rating': 'styles_reviewHeader__iU9Px', 'review': 'typography_body-l__KUYFJ',
               'date': 'typography_body-m__xgxZ_', 'reply': 'typography_body-m__xgxZ_'}

matching_rule = {'1': '.\nJe ne suis pas content du tout.\n',
                 '2': '.\nJe ne suis pas content.\n',
                 '3': '.\nJe suis partagé.\n',
                 '4': '.\nJe suis content.\n',
                 '5': '.\nJe suis très content.\n'}

reactivity = ['réactivité', 'rapidité', 'disponibilité', 'joindre', 'joignable', 'disponible', 'instantané',
              'instantanément', 'rapidement', 'répond', 'réponse', 'compliqué', 'difficulté', 'difficile', 'long',
              'pénible', 'simple', 'sérieux',
              'facile', 'efficace', 'fluide', 'procédure', 'toujours pas']
price = ['compétitif', 'cher', 'prix', 'tarif']
offer = ['remboursement', 'règlement', 'sinistre', 'vol', 'déclaration']
labels = reactivity + price + offer
