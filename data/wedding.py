WEDDING = {
    'names': 'Sofia & Marcos',
    'initials': 'S & M',
    'bride': {
        'name': 'Sofia',
        'title': 'Princesa del Alba',
    },
    'groom': {
        'name': 'Marcos',
        'title': 'Príncipe de la Noche',
    },
    'date': '20 de septiembre de 2026',
    'date_iso': '2026-09-20T17:00:00',
    'ceremony': {
        'time': '17:00 h',
        'venue': 'Iglesia de San Juan',
        'address': 'Calle Mayor 12, Madrid',
    },
    'reception': {
        'time': '19:30 h',
        'venue': 'Palacio de los Jardines',
        'address': 'Av. del Parque 45, Madrid',
    },
    'rsvp_deadline': '1 de agosto de 2026',
    'map_embed_url': (
        'https://maps.google.com/maps'
        '?q=Calle+Mayor+12,+Madrid'
        '&z=16&output=embed'
    ),
    'transport': [
        {
            'title': 'Metro',
            'desc': (
                'Línea 1 (azul), parada <strong>Sol</strong>. '
                'A 5 minutos a pie de la iglesia.'
            ),
        },
        {
            'title': 'En coche',
            'desc': (
                'Parking público en <strong>Plaza Mayor</strong> a 200 metros. '
                'Recomendamos llegar con algo de antelación.'
            ),
        },
        {
            'title': 'Taxi / VTC',
            'desc': (
                'Indica <strong>Calle Mayor 12</strong> como destino. '
                'Amplia zona de bajada frente a la iglesia.'
            ),
        },
    ],
    'dress_code': {
        'label': 'Etiqueta',
        'description': (
            'Os pedimos que vengáis elegantes para acompañar la ocasión. '
            'Esmoquin o traje oscuro para ellos; vestido largo o de cóctel para ellas.'
        ),
        'note': 'Por favor, evitad el blanco y el negro riguroso.',
        'palette': [
            {'name': 'Champán',     'hex': '#F5E6C8'},
            {'name': 'Malva',       'hex': '#C9A8C0'},
            {'name': 'Azul noche',  'hex': '#1B2A4A'},
            {'name': 'Verde salvia','hex': '#8A9E7E'},
            {'name': 'Tierra',      'hex': '#A07858'},
        ],
    },
    'hotels': [
        {
            'name': 'Hotel Palacio Real',
            'stars': 5,
            'distance': 'A 5 min a pie',
            'description': (
                'Ubicado en el corazón de Madrid, frente al Palacio Real. '
                'Descuento especial para invitados con el código BODASM26.'
            ),
        },
        {
            'name': 'Hotel Metrópolis',
            'stars': 4,
            'distance': 'A 8 min a pie',
            'description': (
                'Elegante hotel boutique en la Gran Vía con vistas '
                'inigualables a la ciudad.'
            ),
        },
        {
            'name': 'Hotel Sol Centro',
            'stars': 3,
            'distance': 'A 10 min a pie',
            'description': (
                'Opción céntrica y económica, perfecta si buscas '
                'comodidad sin salir del centro.'
            ),
        },
    ],
}

GIFTS = [
    {
        'id': 1,
        'name': 'Fondo de luna de miel',
        'description': 'Ayúdanos a crear recuerdos inolvidables en nuestra luna de miel por Italia.',
        'category': 'Experiencia',
        'claimed': False,
    },
    {
        'id': 2,
        'name': 'Vajilla completa',
        'description': 'Un juego de vajilla de porcelana para nuestro nuevo hogar.',
        'category': 'Hogar',
        'claimed': False,
    },
    {
        'id': 3,
        'name': 'Robot de cocina',
        'description': 'Batidora KitchenAid para los domingos de repostería en casa.',
        'category': 'Cocina',
        'claimed': True,
    },
    {
        'id': 4,
        'name': 'Ropa de cama',
        'description': 'Juego de sábanas de lino premium, talla king, en blanco marfil.',
        'category': 'Hogar',
        'claimed': False,
    },
    {
        'id': 5,
        'name': 'Copas de cristal',
        'description': 'Set de 8 copas de cristal soplado a mano.',
        'category': 'Cocina',
        'claimed': False,
    },
    {
        'id': 6,
        'name': 'Escapada de fin de semana',
        'description': 'Una contribución para una futura escapada romántica de dos.',
        'category': 'Experiencia',
        'claimed': False,
    },
]
