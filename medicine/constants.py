from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()

HEART_PRESSURE_UNIT = _('mm Hg')
GLUCOSE_RATE_UNIT = CHOLESTEROL_RATE_UNIT = _('mmol/l')
TEMPERATURE_UNIT = _('°C')
PROTEIN_RATE_UNIT = ALBUMIN_RATE_UNIT = _('g/l')
MYOGLOBIN_RATE_UNIT = FERRITIN_RATE_UNIT = _('mcg/l')

TEMPERATURE_NORM = 36.6

HEART_PRESSURE = {
    User.MALE: {
        20: {
            'norm_min': 76,
            'norm_max': 123
        },
        30: {
            'norm_min': 79,
            'norm_max': 126
        },
        40: {
            'norm_min': 81,
            'norm_max': 129
        },
        50: {
            'norm_min': 83,
            'norm_max': 135
        },
        60: {
            'norm_min': 85,
            'norm_max': 142
        },
        float('inf'): {
            'norm_min': 80,
            'norm_max': 142
        }
    },
    User.FEMALE: {
        20: {
            'norm_min': 72,
            'norm_max': 116
        },
        30: {
            'norm_min': 75,
            'norm_max': 120
        },
        40: {
            'norm_min': 80,
            'norm_max': 127
        },
        50: {
            'norm_min': 84,
            'norm_max': 137
        },
        60: {
            'norm_min': 85,
            'norm_max': 144
        },
        float('inf'): {
            'norm_min': 85,
            'norm_max': 159
        }
    }

}

GLUCOSE_RATE = {
    14: {
        'norm_min': 3.3,
        'norm_max': 5.6
    },
    60: {
        'norm_min': 4.1,
        'norm_max': 5.9
    },
    90: {
        'norm_min': 4.6,
        'norm_max': 6.4
    },
    float('inf'): {
        'norm_min': 4.2,
        'norm_max': 6.7
    }
}

PROTEIN_RATE = {
    4: {
        'norm_min': 64,
        'norm_max': 75
    },
    7: {
        'norm_min': 52,
        'norm_max': 78
    },
    15: {
        'norm_min': 58,
        'norm_max': 76
    },
    float('inf'): {
        'norm_min': 64,
        'norm_max': 83
    }
}

ALBUMIN_RATE = {
    14: {
        'norm_min': 28,
        'norm_max': 54
    },
    60: {
        'norm_min': 35,
        'norm_max': 50
    },
    float('inf'): {
        'norm_min': 34,
        'norm_max': 48
    }
}

MYOGLOBIN_RATE = {
    User.MALE: {
        'norm_min': 19,
        'norm_max': 92
    },
    User.FEMALE: {
        'norm_min': 12,
        'norm_max': 76
    }
}

FERRITIN_RATE = {
    User.MALE: {
        'norm_min': 25,
        'norm_max': 250
    },
    User.FEMALE: {
        'norm_min': 10,
        'norm_max': 120
    }
}

CHOLESTEROL_RATE = {
    'norm_min': 3,
    'norm_max': 6
}
