import numpy as np
import skfuzzy as fuzz

# 1. Universe
x_income = np.arange(0, 10.1, 0.1)
x_family = np.arange(0, 8.1, 0.1)
x_house = np.arange(1, 5.1, 0.1)

# 2. Membership Functions
# Pendapatan
inc_low  = fuzz.trapmf(x_income, [0, 0, 2, 4])
inc_mid  = fuzz.trimf(x_income, [2, 5, 8])
inc_high = fuzz.trapmf(x_income, [6, 8, 10, 10])

# Tanggungan
fam_few  = fuzz.trapmf(x_family, [0, 0, 1, 3])
fam_mid  = fuzz.trimf(x_family, [2, 4, 6])
fam_many = fuzz.trapmf(x_family, [4, 6, 8, 8])

# Kondisi Rumah
house_good = fuzz.trapmf(x_house, [1, 1, 2, 3])
house_mid  = fuzz.trimf(x_house, [2, 3, 4])
house_bad  = fuzz.trapmf(x_house, [3, 4, 5, 5.1])

# Output
x_output = np.arange(0, 101, 1)
out_low  = fuzz.trapmf(x_output, [0, 0, 20, 40])
out_mid  = fuzz.trimf(x_output, [30, 50, 70])
out_high = fuzz.trapmf(x_output, [60, 80, 100, 100])


# 3. Output Singleton (0–100)
# Dalam Sugeno, output setiap rule bukan fuzzy set, tapi angka. angka ini disebut singleton.
M = [
    [   # Income Low
        [90, 80, 70],  
        [80, 70, 60],
        [75, 65, 55]
    ],
    [   # Income Mid
        [70, 60, 50],
        [60, 50, 40],
        [55, 45, 35]
    ],
    [   # Income High
        [40, 30, 20],
        [35, 25, 15],
        [30, 20, 10]
    ]
]

# 4. Fungsi Sugeno
def sugeno(income_value, family_value, house_value):

    # --- Fuzzification ---
    in_1 = [
        fuzz.interp_membership(x_income, inc_low, income_value),
        fuzz.interp_membership(x_income, inc_mid, income_value),
        fuzz.interp_membership(x_income, inc_high, income_value)
    ]

    in_2 = [
        fuzz.interp_membership(x_family, fam_few, family_value),
        fuzz.interp_membership(x_family, fam_mid, family_value),
        fuzz.interp_membership(x_family, fam_many, family_value)
    ]

    in_3 = [
        fuzz.interp_membership(x_house, house_good, house_value),
        fuzz.interp_membership(x_house, house_mid, house_value),
        fuzz.interp_membership(x_house, house_bad, house_value)
    ]

    # Untuk nampilin di UI
    input_miu_detail = {
        "income": in_1,
        "family": in_2,
        "house": in_3
    }

    # --- Sugeno Inference ---
    rules_detail = []  #  nampilin μ tiap rule
    firing = []
    weighted = []

    for i in range(3):
        for j in range(3):
            for k in range(3):

                μ = np.min([in_1[i], in_2[j], in_3[k]])
                z = M[i][j][k] # singleton output
                w = μ * z   # weighted output

                firing.append(μ)
                weighted.append(w)

                # Simpan detail rule untuk ditampilkan
                rules_detail.append({
                    "rule": f"R({i},{j},{k})",
                    "μ_income": in_1[i],
                    "μ_family": in_2[j],
                    "μ_house": in_3[k],
                    "μ_rule": μ,
                    "z": z,
                    "weighted": w
                })

    # --- Defuzzification ---
    pembilang = np.sum(weighted)
    penyebut = np.sum(firing)
    result = pembilang / penyebut if penyebut != 0 else 0

    # --- Kategori Output ---
    if result < 40:
        kategori = "Tidak Layak"
    elif result < 60:
        kategori = "Dipertimbangkan"
    else:
        kategori = "Layak"

    return {
        "hasil": result,
        "kategori": kategori,
        "input_miu": input_miu_detail,
        "rules": rules_detail,
        "sum_weighted": pembilang,
        "sum_miu": penyebut
    }