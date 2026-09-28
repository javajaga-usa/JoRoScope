"""JoRoScope Comprehensive Life Prediction Engine
Assembles the bilingual (English and Tamil) life prediction report from the reading modules in
`joroscope.core.readings`: the birth star and Lagna, the twelve bhavas, grahas in houses, the
running Dasa-Bhukti, transits, lucky factors, Jaimini, double transit, career and health,
kakshya transits, Shadbala, KP, Bhrigu Nandi Nadi, avasthas, pada, sahams, Panchanga Phala,
the Sudarshana Chakra and the Dasa-Bhukti timeline.

The names other modules and the tests use are re-exported here, so `from .predictions import X`
keeps working.
"""
from .timeline import calculate_timeline_predictions
from .readings.common import (
    SIGNS, TAMIL_SIGNS, SIGN_LORDS, PLANET_TAMIL, STARS, TAMIL_STARS, DASA_LORDS, VIMSHOTTARI_YEARS,
    DIGNITY_SCORE, DIGNITY_PHRASE, HOUSE_THEMES, _functional_role, _house_list, _ordinal
)
from .readings.life import (
    NAKSHATRA_PREDICTIONS, LAGNA_PREDICTIONS, generate_bhava_predictions, generate_planet_house_predictions,
    generate_dasa_forecast, generate_transit_forecast, generate_lucky_factors
)
from .readings.jaimini import calculate_jaimini_karakas, jaimini_arudhas, _jaimini_lord, _rasi_drishti
from .readings.timing import calculate_double_transit, calculate_kakshya_transits
from .readings.career_health import calculate_career_vocation_d10, calculate_ayur_jyotish
from .readings.strength_kp import get_kp_sublord, calculate_shadbala, calculate_kp_system
from .readings.numerology import calculate_numerology
from .readings.remedies import calculate_remedies
from .readings.life_reports import calculate_marriage_report, calculate_career_report
from .readings.classical import (
    calculate_bhrigu_nandi_nadi, calculate_planetary_avasthas, calculate_nakshatra_pada_reading, calculate_sahams,
    generate_panchanga_phala, calculate_sudarshana_chakra, lajjitadi_avasthas, _bnn_link, _saham
)

# Re-exported for callers of this module and the tests
__all__ = [
    'generate_comprehensive_predictions', 'calculate_timeline_predictions', 'calculate_numerology', 'calculate_remedies', 'calculate_marriage_report', 'calculate_career_report', 'SIGNS', 'TAMIL_SIGNS',
    'SIGN_LORDS', 'PLANET_TAMIL', 'STARS', 'TAMIL_STARS', 'DASA_LORDS', 'VIMSHOTTARI_YEARS',
    'DIGNITY_SCORE', 'DIGNITY_PHRASE', 'HOUSE_THEMES', '_functional_role', '_house_list',
    '_ordinal', 'NAKSHATRA_PREDICTIONS', 'LAGNA_PREDICTIONS', 'generate_bhava_predictions',
    'generate_planet_house_predictions', 'generate_dasa_forecast', 'generate_transit_forecast',
    'generate_lucky_factors', 'calculate_jaimini_karakas', 'jaimini_arudhas', '_jaimini_lord',
    '_rasi_drishti', 'calculate_double_transit', 'calculate_kakshya_transits',
    'calculate_career_vocation_d10', 'calculate_ayur_jyotish', 'get_kp_sublord',
    'calculate_shadbala', 'calculate_kp_system', 'calculate_bhrigu_nandi_nadi',
    'calculate_planetary_avasthas', 'calculate_nakshatra_pada_reading', 'calculate_sahams',
    'generate_panchanga_phala', 'calculate_sudarshana_chakra', 'lajjitadi_avasthas', '_bnn_link',
    '_saham'
]


def generate_comprehensive_predictions(chart):
    # Modules that need the ephemeris import the engine, which imports this module
    from .monthly import calculate_monthly_transits
    from .varshaphal import calculate_varshaphal

    planets = chart['planets']
    asc = planets['Ascendant']
    moon = planets['Moon']
    panch = chart['panchanga']
    active_dasa = chart.get('active_dasha')
    dasha_rows = chart.get('dasha', [])
    house_details = chart.get('house_details', [])
    vargas = chart.get('vargas', {})

    star_pred = NAKSHATRA_PREDICTIONS.get(moon['nakshatra'], NAKSHATRA_PREDICTIONS['Ashwini'])
    lagna_pred = LAGNA_PREDICTIONS.get(asc['sign'], LAGNA_PREDICTIONS['Aries'])
    bhavas = generate_bhava_predictions(house_details, planets, bhava_bala=chart.get('bhava_bala'))
    planets_in_houses = generate_planet_house_predictions(planets)
    dasa_forecast = generate_dasa_forecast(active_dasa, dasha_rows, planets, chart.get('timezone') or 'UTC')
    transits = generate_transit_forecast(moon['sign_index'], chart['gochara'])
    luck = generate_lucky_factors(asc['sign_index'])

    # 5 Advanced Approved Astrological Research Modules
    jaimini_karakas = calculate_jaimini_karakas(planets, vargas)
    double_transit = calculate_double_transit(chart)
    career_d10 = calculate_career_vocation_d10(chart)
    ayur_jyotish = calculate_ayur_jyotish(chart)
    kakshya_transits = calculate_kakshya_transits(chart)

    # 6 New Advanced Calculation & Predictive Modules
    shadbala = calculate_shadbala(chart)
    kp_system = calculate_kp_system(chart)
    bnn = calculate_bhrigu_nandi_nadi(chart)
    avasthas = calculate_planetary_avasthas(chart)
    pada_reading = calculate_nakshatra_pada_reading(chart)
    sahams = calculate_sahams(chart)

    # 7 Chronological Life Timeline & 10-Year Projections (81 Dasa-Bhukti periods)
    timeline_predictions = calculate_timeline_predictions(chart)

    return {
        'overview': {
            'nakshatra': moon['nakshatra'],
            'tamil_nakshatra': moon['tamil_nakshatra'],
            'nakshatra_pred_en': star_pred['en'],
            'nakshatra_pred_ta': star_pred['ta'],
            'lagna': asc['sign'],
            'tamil_lagna': asc['tamil'],
            'lagna_pred_en': lagna_pred['en'],
            'lagna_pred_ta': lagna_pred['ta'],
            'moon_sign': moon['sign'],
            'tamil_moon_sign': moon['tamil'],
            'tithi_name': panch['tithi_name'],
            'yoga_name': panch['yoga_name']
        },
        'panchanga_phala': generate_panchanga_phala(chart),
        'sudarshana': calculate_sudarshana_chakra(chart),
        'bhavas': bhavas,
        'planets_in_houses': planets_in_houses,
        'dasa_forecast': dasa_forecast,
        'transits': transits,
        'lucky_factors': luck,
        'jaimini_karakas': jaimini_karakas,
        'double_transit': double_transit,
        'career_d10': career_d10,
        'ayur_jyotish': ayur_jyotish,
        'kakshya_transits': kakshya_transits,
        'shadbala': shadbala,
        'kp_system': kp_system,
        'bhrigu_nandi_nadi': bnn,
        'avasthas': avasthas,
        'pada_reading': pada_reading,
        'sahams': sahams,
        'timeline_predictions': timeline_predictions,
        'numerology': calculate_numerology(chart),
        'remedies': calculate_remedies(chart),
        'monthly': calculate_monthly_transits(chart),
        'varshaphal': calculate_varshaphal(chart),
        'marriage': calculate_marriage_report(chart, jaimini_karakas, double_transit),
        'career_report': calculate_career_report(chart, jaimini_karakas, career_d10, double_transit)
    }
