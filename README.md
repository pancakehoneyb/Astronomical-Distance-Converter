# 🌌 Astronomical Distance Converter
**v2.0**  

---

## Origin

This tool was born in **2023**, when I was in high school and had just qualified for the **international astronomy olympiad selection rounds** for IOAA (International Olympiad on Astronomy and Astrophysics) and OLAA (Olimpiada Latinoamericana de Astronomía y Astronáutica). During preparation, converting between parsecs, light-years, AU, and other units constantly by hand was slow and error-prone under exam pressure. The solution was to write a converter that could be trusted to get the numbers right, every time.

What started as a few quick functions grew into a full command-line tool with unit conversions, distance modulus, and cosmological redshift covering most of the distance calculations that appear in olympiad problems.

---

## Features 

- **Unit conversion** between any pair of 6 units (parsec, light-year, AU, meter, km, light-second)
- **Reference table** with canonical conversion factors, ready to consult mid-problem
- **Distance modulus** compute μ from distance or distance from μ, in any unit
- **Redshift ↔ Distance** with **three models compared side by side**, including error % vs. ΛCDM reference
- **Session history** with timestamps, exportable to `.txt`
- Bilingual interface: **Portuguese / English**

---

## Installation 

**Requirements:** Python 3.8+  
No external libraries needed, standard library only.

```bash
git clone https://github.com/your-username/astronomical-distance-converter.git
cd astronomical-distance-converter
python astronomical_converter.py
```

---

## Usage

Run the script and navigate the interactive menu:

```
═════════════════════════════════════════════════════════════════
  Conversor de Distâncias Astronômicas
  Astronomical Distance Converter
  Edição Olimpíadas / Olympics Edition  |  IOAA · OLAA
  Programado por Ísis Barbiere  |  v2.0
═════════════════════════════════════════════════════════════════

─────────────────────────────────────────────────────────────────
  MENU PRINCIPAL / MAIN MENU
─────────────────────────────────────────────────────────────────
    1. Conversão de unidades / Unit conversion
    2. Tabela de referência / Reference table
    3. Módulo de distância / Distance modulus
    4. Redshift ↔ Distância / Redshift ↔ Distance
    5. Histórico / History
    0. Sair / Exit
─────────────────────────────────────────────────────────────────
```

---

## Module Details

---

### 1 · Unit Conversion

Converts between any two of the 6 supported units:

| # | Unit / Unidade | Symbol |
|---|---|---|
| 1 | Parsec | pc |
| 2 | Light-year / Ano-luz | ly |
| 3 | Astronomical Unit / UA | AU |
| 4 | Meter / Metro | m |
| 5 | Kilometer / Quilômetro | km |
| 6 | Light-second / Segundo-luz | ls |

All conversions go through **meters as a common base**, so any pair works without hardcoding 30 individual formulas. Example:

```
  Unidade de ORIGEM / FROM unit:  [1] Parsec
  Unidade de DESTINO / TO unit:   [3] AU
  Valor em pc: 1

  ─────────────────────────────────────────────────────────────
  1.000000 pc  =  206,264.81 AU
  ─────────────────────────────────────────────────────────────
```

> 📸 **Screenshot suggestion:** run option 1, convert 1 parsec to AU and 1 ly to km. Two clean examples that show the formatted output well.

---

### 2 · Reference Table

Displays all canonical conversion factors in one screen, useful to check mid-problem without leaving the tool:

```
  1 Parsec                          =  3.0857 × 10¹⁶ m
  1 Parsec                          =  206 264.806 AU
  1 Parsec                          =  3.2616 ly
  1 Ano-luz / Light-year            =  9.4607 × 10¹⁵ m
  1 Ano-luz / Light-year            =  63 240 AU
  1 Ano-luz / Light-year            =  0.30660 pc
  1 UA / AU                         =  1.4960 × 10¹¹ m
  1 UA / AU                         =  1.5813 × 10⁻⁵ ly
  1 UA / AU                         =  4.8481 × 10⁻⁶ pc
  1 km                              =  1 000 m
  1 Segundo-luz / ls                =  2.9979 × 10⁸ m
  1 Segundo-luz / ls                =  0.002004 AU
```

> 📸 **Screenshot suggestion:** just run option 2 and capture the full table. It's self-contained and looks clean.

---

### 3 · Distance Modulus

Implements the standard distance modulus formula:

$$\mu = 5 \cdot \log_{10}\left(\frac{d}{1\,\text{pc}}\right) - 5$$

**Sub-options:**

**3.1 — Distance → Modulus:** accepts the distance in any of the 6 supported units, converts to parsecs internally, and outputs μ in magnitudes.

**3.2 — Modulus → Distance:** given μ, outputs the distance in parsecs, light-years, and AU simultaneously.

Example (Sun → Alpha Centauri, d ≈ 1.34 pc):
```
  d = 1.340000 pc
  μ = 0.632268 mag
```

> 📸 **Screenshot suggestion:** run option 3 → sub-option 1, enter a distance like 10 pc (which gives μ = 0, a good sanity check). Then run sub-option 2 with μ = 0 to show the round-trip.

---

### 4 · Redshift ↔ Distance

This is the most technically detailed module. Three cosmological models are computed and shown **side by side**, with percentage error relative to the ΛCDM reference:

#### The three models

**[1] Linear Hubble — `d = c·z / H₀`**  
The textbook approximation. Only valid for z << 0.1. Error grows quickly with z.

**[2] Relativistic Doppler + Hubble**  
Inverts the special-relativistic Doppler formula to get the recession velocity, then applies Hubble's law:

$$v = c \cdot \frac{(1+z)^2 - 1}{(1+z)^2 + 1}, \quad d = \frac{v}{H_0}$$

Better than linear for 0.1 < z < ~1, but still ignores the expansion of spacetime itself.

**[3] ΛCDM Comoving Distance — numerical integration (reference)**  
The standard of modern cosmology. Integrates numerically with 10,000 steps via the trapezoidal rule:

$$d_C = \frac{c}{H_0} \int_0^z \frac{dz'}{E(z')}, \quad E(z) = \sqrt{\Omega_m(1+z)^3 + \Omega_k(1+z)^2 + \Omega_\Lambda}$$

Valid for any z. Used as the reference against which the other two are measured.

#### Cosmological parameters (Planck 2018)

| Parameter | Value |
|---|---|
| H₀ | 67.4 km/s/Mpc |
| Ω_m | 0.315 |
| Ω_Λ | 0.685 |
| Ω_k | 0.0 (flat universe) |

#### Output also includes 

- **Luminosity distance** d_L = d_C · (1+z) — used in flux/luminosity calculations
- **Angular diameter distance** d_A = d_C / (1+z) — used in angular size calculations
- Result in **pc and ly** as well as Mpc
- Automatic warning about which model is appropriate for the given z

#### Example output for z = 6:

```
  z = 6.000000
  ─────────────────────────────────────────────────────────────
  MODELO / MODEL                            d [Mpc]   erro/error
  ─────────────────────────────────────────────────────────────
  [1] Hubble linear                       26,876.12      67.47%
  [2] Doppler relativístico / relativ.     5,645.54      33.01%
  [3] ΛCDM comóvel (referência)            8,424.08          —
  ─────────────────────────────────────────────────────────────
  Luminosity distance  d_L =  58,968.59 Mpc
  Angular diameter     d_A =   1,203.44 Mpc
  ─────────────────────────────────────────────────────────────
  d_C (ΛCDM) in other units:
    8,424,083,889.44 pc
    27,475,686,869.61 ly
  ─────────────────────────────────────────────────────────────
  ✘  z ≥ 0.3 — use apenas ΛCDM [3] / use only ΛCDM [3].
```

The inversion (Distance → z) uses **bisection** to numerically invert the ΛCDM integral, converging to precision 10⁻⁸.

> 📸 **Screenshot suggestion:** run option 4 → sub-option 1 with z = 0.05 (low z, all three agree, good for showing the green checkmark), then again with z = 2 (large divergence between models, the most visually striking output). Two screenshots side by side would show the full range.

---

### 5 · History

Every calculation performed in the session is logged with a timestamp. At any point you can view the history and optionally export it to a `.txt` file named `historico_YYYYMMDD_HHMMSS.txt`. The program also prompts to save on exit if any operations were performed.

---

## Physical Constants Used 

| Constant | Value | Source |
|---|---|---|
| Speed of light c | 299,792,458 m/s | CODATA 2018 |
| 1 AU | 1.495978707 × 10¹¹ m | IAU 2012 |
| 1 Parsec | 3.085677581491367 × 10¹⁶ m | IAU definition |
| 1 Light-year | 9.4607304725808 × 10¹⁵ m | IAU definition |
| H₀ | 67.4 km/s/Mpc | Planck Collaboration 2018 |
| Ω_m | 0.315 | Planck Collaboration 2018 |
| Ω_Λ | 0.685 | Planck Collaboration 2018 |

---

## Limitations 

- The ΛCDM redshift model uses the **non-relativistic comoving distance** integral, which assumes a flat FLRW metric. This is standard for olympiad-level problems and matches results from tools like the NASA Wright Cosmology Calculator.
- For extremely high redshifts (z > 20), the trapezoidal integration with 10,000 steps may accumulate minor numerical error. Increase `n_steps` in `comoving_distance_mpc()` if needed.
- No k-corrections or peculiar velocities are accounted for.

---

## References 

- Planck Collaboration (2018). *Planck 2018 results. VI. Cosmological parameters*. A&A 641, A6.
- Hogg, D. W. (1999). *Distance measures in cosmology*. arXiv:astro-ph/9905116.
- IAU 2012 Resolution B2 — re-definition of the astronomical unit.
- Wright, E. L. (2006). *A Cosmology Calculator for the World Wide Web*. PASP 118, 1711.

---

## License

Distributed for educational purposes. 
