# STATES THAT BELONG TO EACH REGION OF BRAZIL
dict_regions = {
    "North": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "Northeast":["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centerwest":["DF", "GO", "MT", "MS"],
    "South":["PR", "RS", "SC"],
    "Southeast":["ES", "MG", "RJ", "SP"]
}

# TIME TO TRAVEL FROM A STATE TO ANOTHER
dict_travel_time = {

    # SP to other ditribution centers
    ("SP","AM"): 235,
    ("SP","CE"): 207,
    ("SP","MS"): 78,
    ("SP","SC"): 42,

    # Region North  "AC", "AP", "AM", "PA", "RO", "RR", "TO"
    ("AC", "AP"): 234,
    ("AC", "AM"): 249,
    ("AC", "PA"): 203,
    ("AC", "RO"): 42,
    ("AC", "RR"): 148,
    ("AC", "TO"): 189,

    ("AP", "AM"): 92,
    ("AP", "PA"): 29,
    ("AP", "RO"): 150,
    ("AP", "RR"): 97,
    ("AP", "TO"): 102,

    ("AM", "PA"): 113,
    ("AM", "RO"): 66,
    ("AM", "RR"): 61,
    ("AM", "TO"): 132,

    ("PA", "RO"): 165,
    ("PA", "RR"): 126,
    ("PA", "TO"): 84,

    ("RO", "RR"): 120,
    ("RO", "TO"): 149,

    ("RR", "TO"): 175,

    # Region Northeast  "AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"
    ("AL", "BA"): 41,
    ("AL", "CE"): 63,
    ("AL", "MA"): 107,
    ("AL", "PB"): 26,
    ("AL", "PE"): 17,
    ("AL", "PI"): 81,
    ("AL", "RN"): 37,
    ("AL", "SE"): 17,

    ("BA", "CE"): 89,
    ("BA", "MA"): 115,
    ("BA", "PB"): 66,
    ("BA", "PE"): 59,
    ("BA", "PI"): 86,
    ("BA", "RN"): 76,
    ("BA", "SE"): 24,

    ("CE", "MA"): 57,
    ("CE", "PB"): 48,
    ("CE", "PE"): 54,
    ("CE", "PI"): 43,
    ("CE", "RN"): 37,
    ("CE", "SE"): 71,

    ("MA", "PB"): 101,
    ("MA", "PE"): 105,
    ("MA", "PI"): 28,
    ("MA", "RN"): 93,
    ("MA", "SE"): 107,

    ("PB", "PE"): 9,
    ("PB", "PI"): 79,
    ("PB", "RN"): 13,
    ("PB", "SE"): 42,

    ("PE", "PI"): 81,
    ("PE", "RN"): 22,
    ("PE", "SE"): 34,

    ("PI", "RN"): 73,
    ("PI", "SE"): 79,

    ("RN", "SE"): 52,

    # Region Centerwest  "DF", "GO", "MT", "MS"
    ("DF", "GO"): 15,
    ("DF", "MT"): 76,
    ("DF", "MS"): 76,

    ("GO", "MT"): 64,
    ("GO", "MS"): 61,

    ("MT", "MS"): 49,

    # Region South "PR", "RS", "SC"
    ("PR", "RS"): 47,
    ("PR", "SC"): 21,
    ("RS", "SC"): 32,

    # Region Southeast  "ES", "MG", "RJ", "SP"
    ("ES", "MG"): 33,
    ("ES", "RJ"): 36,
    ("ES", "SP"): 65,

    ("MG", "RJ"): 29,
    ("MG", "SP"): 42,

    ("RJ", "SP"): 31,
}

# DEFINE WHICH CITY IS THE DISTRIBUTION CENTER OF EACH REGION
distribution_center = {
    "North": "AM",
    "Northeast": "CE",
    "Centerwest": "MS",
    "South": "SC",
    "Southeast": "SP"
}

dict_state_capital = {
    "SP": "São Paulo",
    "RJ": "Rio de Janeiro",
    "MG": "Belo Horizonte",
    "DF": "Brasília",
    "BA": "Salvador",
    "CE": "Fortaleza",
    "PR": "Curitiba",
    "AM": "Manaus",
    "ES": "Vitória",
    "PE": "Recife",
    "RS": "Porto Alegre",
    "GO": "Goiânia",
    "PA": "Belém",
    "MA": "São Luís",
    "AL": "Maceió",
    "RN": "Natal",
    "MS": "Campo Grande",
    "PI": "Teresina",
    "PB": "João Pessoa",
    "SE": "Aracaju",
    "MT": "Cuiabá",
    "SC": "Florianópolis",
    "AP": "Macapá",
    "AC": "Rio Branco",
    "RR": "Boa Vista",
    "RO": "Porto Velho",
    "TO": "Palmas",
}
