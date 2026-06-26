# =============================================================================
#  Astronomical Distance Converter / Conversor de Distâncias Astronômicas
#  Programado por Ísis Barbiere
#  Versão 2.0 — Edição Olimpíadas (IOAA/OLAA)
# =============================================================================

from datetime import datetime

# =============================================================================
#  CONSTANTS / CONSTANTES
#  All values in meters / Todos os valores em metros
# =============================================================================

METER       = 1.0
KM          = 1e3
LIGHT_SEC   = 299_792_458.0               # meters per light-second / metros por segundo-luz
LIGHT_YEAR  = 9.4607304725808e15          # meters per light-year / metros por ano-luz
AU          = 1.495978707e11              # meters per AU / metros por UA
PARSEC      = 3.085677581491367e16        # meters per parsec / metros por parsec

# Hubble constant for redshift (km/s/Mpc) — standard ΛCDM
# Constante de Hubble para redshift (km/s/Mpc) — ΛCDM padrão
H0_KM_S_MPC = 67.4
H0           = H0_KM_S_MPC * 1e3 / (1e6 * PARSEC)  # in s⁻¹

SPEED_OF_LIGHT = 299_792_458.0  # m/s

# =============================================================================
#  UNIT REGISTRY / REGISTRO DE UNIDADES
# =============================================================================

UNITS = {
    "1":  ("Parsec",        "pc",     PARSEC),
    "2":  ("Ano-luz / Light-year",  "ly",  LIGHT_YEAR),
    "3":  ("UA / AU",       "AU",     AU),
    "4":  ("Metro / Meter", "m",      METER),
    "5":  ("Quilômetro / Kilometer", "km", KM),
    "6":  ("Segundo-luz / Light-second", "ls", LIGHT_SEC),
}

# =============================================================================
#  CONVERSION ENGINE / MOTOR DE CONVERSÃO
# =============================================================================

def convert(value: float, from_meters: float, to_meters: float) -> float:
    """Convert a value between two units via meters as common base."""
    return value * (from_meters / to_meters)

# =============================================================================
#  DISTANCE MODULUS / MÓDULO DE DISTÂNCIA
# =============================================================================

def distance_to_modulus(distance_pc: float) -> float:
    """μ = 5·log₁₀(d/pc) − 5"""
    if distance_pc <= 0:
        raise ValueError("Distance must be positive / Distância deve ser positiva.")
    import math
    return 5 * math.log10(distance_pc) - 5

def modulus_to_distance(mu: float) -> float:
    """d = 10^((μ+5)/5)  [parsecs]"""
    return 10 ** ((mu + 5) / 5)

# =============================================================================
#  REDSHIFT — THREE MODELS / TRÊS MODELOS
#
#  Model 1 — Linear Hubble (non-relativistic):
#    d = c·z / H₀
#    Valid only for z << 0.1. Breaks down quickly.
#
#  Model 2 — Special Relativity correction (no expansion):
#    Uses the relativistic Doppler formula to get recession velocity,
#    then applies Hubble law. Better for 0.1 < z < ~1, but still
#    ignores spacetime expansion.
#    v = c · [(1+z)² - 1] / [(1+z)² + 1]
#    d = v / H₀
#
#  Model 3 — ΛCDM Comoving Distance (numerical integration):
#    d_C = (c / H₀) · ∫₀ᶻ dz' / E(z')
#    E(z) = sqrt(Ω_m·(1+z)³ + Ω_k·(1+z)² + Ω_Λ)
#    Parameters: Planck 2018
#      H₀ = 67.4 km/s/Mpc,  Ω_m = 0.315,  Ω_Λ = 0.685,  Ω_k = 0
#    Valid for all z. This is the standard used in modern cosmology.
#
# =============================================================================

import math

# ΛCDM Planck 2018 parameters
OMEGA_M   = 0.315
OMEGA_L   = 0.685
OMEGA_K   = 0.0   # flat universe / universo plano

def _E(z: float) -> float:
    """Dimensionless Hubble parameter E(z) = H(z)/H0."""
    return math.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_K * (1 + z)**2 + OMEGA_L)

def comoving_distance_mpc(z: float, n_steps: int = 10_000) -> float:
    """
    ΛCDM comoving distance via trapezoidal integration [Mpc].
    d_C = (c/H0) · ∫₀ᶻ dz'/E(z')
    """
    if z < 0:
        raise ValueError("Redshift must be non-negative / Redshift deve ser não-negativo.")
    if z == 0:
        return 0.0
    c_km_s = SPEED_OF_LIGHT / 1e3   # km/s
    dh = c_km_s / H0_KM_S_MPC       # Hubble distance in Mpc
    dz = z / n_steps
    total = 0.0
    for i in range(n_steps):
        z0 = i * dz
        z1 = (i + 1) * dz
        total += 0.5 * (1.0 / _E(z0) + 1.0 / _E(z1)) * dz
    return dh * total

def hubble_linear_mpc(z: float) -> float:
    """Model 1 — Linear Hubble:  d = c·z / H₀  [Mpc]"""
    if z < 0:
        raise ValueError("Redshift must be non-negative.")
    return (SPEED_OF_LIGHT / 1e3) * z / H0_KM_S_MPC

def hubble_relativistic_mpc(z: float) -> float:
    """
    Model 2 — Special-relativistic Doppler + Hubble:
    v = c · [(1+z)²-1] / [(1+z)²+1],  d = v / H₀
    """
    if z < 0:
        raise ValueError("Redshift must be non-negative.")
    v_over_c = ((1 + z)**2 - 1) / ((1 + z)**2 + 1)
    v_km_s   = v_over_c * (SPEED_OF_LIGHT / 1e3)
    return v_km_s / H0_KM_S_MPC

def _z_from_comoving_bisection(d_mpc: float, tol: float = 1e-8) -> float:
    """Invert comoving distance to redshift via bisection."""
    if d_mpc <= 0:
        return 0.0
    lo, hi = 0.0, 100.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if comoving_distance_mpc(mid) < d_mpc:
            lo = mid
        else:
            hi = mid
        if (hi - lo) < tol:
            break
    return (lo + hi) / 2

# =============================================================================
#  FORMATTING / FORMATAÇÃO
# =============================================================================

def fmt(value: float) -> str:
    """Format number: scientific if very large or very small, else decimal."""
    if value == 0:
        return "0"
    abs_v = abs(value)
    if abs_v >= 1e4 or abs_v < 1e-2:
        return f"{value:.6e}"
    return f"{value:.6f}"

def separator(char="─", width=65):
    print(char * width)

def header():
    separator("═")
    print("  Conversor de Distâncias Astronômicas")
    print("  Astronomical Distance Converter")
    print("  Edição Olimpíadas / Olympics Edition  |  IOAA · OLAA")
    print("  Programado por Ísis Barbiere  |  v2.0")
    separator("═")

# =============================================================================
#  HISTORY / HISTÓRICO
# =============================================================================

history = []

def log(entry: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    history.append(f"[{timestamp}] {entry}")

def save_history():
    filename = f"historico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("  Histórico de Operações / Operation History\n")
        f.write(f"  Sessão / Session: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 65 + "\n\n")
        for entry in history:
            f.write(entry + "\n")
    print(f"\n  ✔  Histórico salvo em / History saved to: {filename}")

# =============================================================================
#  MENUS / MENUS
# =============================================================================

def print_unit_menu():
    print()
    for key, (name, symbol, _) in UNITS.items():
        print(f"    {key}. {name}  [{symbol}]")
    print()

def menu_reference():
    """Show fixed conversion reference table."""
    separator()
    print("  TABELA DE REFERÊNCIA / REFERENCE TABLE")
    separator()

    refs = [
        ("1 Parsec",              "3.0857 × 10¹⁶ m"),
        ("1 Parsec",              "206 264.806 AU"),
        ("1 Parsec",              "3.2616 ly"),
        ("1 Ano-luz / Light-year","9.4607 × 10¹⁵ m"),
        ("1 Ano-luz / Light-year","63 240 AU"),
        ("1 Ano-luz / Light-year","0.30660 pc"),
        ("1 UA / AU",             "1.4960 × 10¹¹ m"),
        ("1 UA / AU",             "1.5813 × 10⁻⁵ ly"),
        ("1 UA / AU",             "4.8481 × 10⁻⁶ pc"),
        ("1 km",                  "1 000 m"),
        ("1 Segundo-luz / ls",    "2.9979 × 10⁸ m"),
        ("1 Segundo-luz / ls",    "0.002004 AU"),
    ]

    for label, value in refs:
        print(f"    {label:<36} =  {value}")
    separator()

def menu_convert():
    """Unit-to-unit conversion for any pair."""
    separator()
    print("  CONVERSÃO DE UNIDADES / UNIT CONVERSION")
    separator()
    print("  Unidade de ORIGEM / FROM unit:")
    print_unit_menu()

    from_key = input("  Escolha / Choose (1-6): ").strip()
    if from_key not in UNITS:
        print("  ✘  Opção inválida / Invalid option.")
        return

    print("  Unidade de DESTINO / TO unit:")
    print_unit_menu()

    to_key = input("  Escolha / Choose (1-6): ").strip()
    if to_key not in UNITS:
        print("  ✘  Opção inválida / Invalid option.")
        return

    if from_key == to_key:
        print("  ✘  Unidades iguais / Same units — no conversion needed.")
        return

    from_name, from_sym, from_m = UNITS[from_key]
    to_name,   to_sym,   to_m   = UNITS[to_key]

    try:
        value = float(input(f"  Valor em {from_sym} / Value in {from_sym}: "))
    except ValueError:
        print("  ✘  Valor inválido / Invalid value.")
        return

    result = convert(value, from_m, to_m)

    separator()
    print(f"  {fmt(value)} {from_sym}  =  {fmt(result)} {to_sym}")
    separator()

    entry = f"Conversão: {fmt(value)} {from_sym} → {fmt(result)} {to_sym}"
    log(entry)

def menu_modulus():
    """Distance modulus tools."""
    separator()
    print("  MÓDULO DE DISTÂNCIA / DISTANCE MODULUS")
    print("  μ = 5·log₁₀(d / 1 pc) − 5")
    separator()
    print("  1. Distância → Módulo  /  Distance → Modulus")
    print("  2. Módulo → Distância  /  Modulus → Distance")
    print()

    sub = input("  Escolha / Choose (1-2): ").strip()

    try:
        if sub == "1":
            print("  Unidade da distância / Distance unit:")
            print_unit_menu()
            ukey = input("  Escolha / Choose (1-6): ").strip()
            if ukey not in UNITS:
                print("  ✘  Opção inválida.")
                return
            _, sym, u_m = UNITS[ukey]
            value = float(input(f"  Distância em {sym}: "))
            dist_pc = convert(value, u_m, PARSEC)
            mu = distance_to_modulus(dist_pc)
            separator()
            print(f"  d = {fmt(value)} {sym}  =  {fmt(dist_pc)} pc")
            print(f"  μ = {fmt(mu)} mag")
            separator()
            log(f"Módulo de distância: d={fmt(value)} {sym} → μ={fmt(mu)} mag")

        elif sub == "2":
            mu = float(input("  Módulo de distância μ (mag): "))
            dist_pc = modulus_to_distance(mu)
            dist_ly  = convert(dist_pc, PARSEC, LIGHT_YEAR)
            dist_au  = convert(dist_pc, PARSEC, AU)
            separator()
            print(f"  μ = {fmt(mu)} mag")
            print(f"  d = {fmt(dist_pc)} pc")
            print(f"  d = {fmt(dist_ly)} ly")
            print(f"  d = {fmt(dist_au)} AU")
            separator()
            log(f"Módulo de distância: μ={fmt(mu)} mag → d={fmt(dist_pc)} pc")
        else:
            print("  ✘  Opção inválida.")
    except ValueError as e:
        print(f"  ✘  Erro: {e}")

def menu_redshift():
    """Redshift ↔ distance — three cosmological models compared."""
    separator()
    print("  REDSHIFT ↔ DISTÂNCIA / REDSHIFT ↔ DISTANCE")
    separator()
    print("  Modelos disponíveis / Available models:")
    print()
    print("  [1] Hubble linear          d = c·z/H₀               (z << 0.1)")
    print("  [2] Doppler relativístico  v = c·[(1+z)²-1]/[(1+z)²+1], d=v/H₀  (z < ~1)")
    print("  [3] ΛCDM comóvel           d = (c/H₀)·∫dz/E(z)      (qualquer z)")
    print()
    print(f"  Parâmetros / Parameters (Planck 2018):")
    print(f"    H₀ = {H0_KM_S_MPC} km/s/Mpc  |  Ω_m = {OMEGA_M}  |  Ω_Λ = {OMEGA_L}  |  Ω_k = {OMEGA_K}")
    separator()
    print("  1. Redshift z → Distância  /  Redshift z → Distance")
    print("  2. Distância → Redshift z  /  Distance → Redshift z")
    print()

    sub = input("  Escolha / Choose (1-2): ").strip()

    try:
        if sub == "1":
            z = float(input("  Redshift z: "))
            if z < 0:
                raise ValueError("z deve ser não-negativo / z must be non-negative.")

            d1 = hubble_linear_mpc(z)
            d2 = hubble_relativistic_mpc(z)
            d3 = comoving_distance_mpc(z)

            # percentage errors relative to ΛCDM
            err1 = abs(d1 - d3) / d3 * 100 if d3 > 0 else 0
            err2 = abs(d2 - d3) / d3 * 100 if d3 > 0 else 0

            # luminosity and angular diameter distances
            d_lum = d3 * (1 + z)          # d_L = d_C · (1+z)
            d_ang = d3 / (1 + z)          # d_A = d_C / (1+z)

            separator()
            print(f"  z = {fmt(z)}")
            separator()
            print(f"  {'MODELO / MODEL':<38}  {'d [Mpc]':>14}  {'erro/error':>10}")
            separator("─")
            print(f"  {'[1] Hubble linear':<38}  {fmt(d1):>14}  {err1:>9.2f}%")
            print(f"  {'[2] Doppler relativístico / relativistic':<38}  {fmt(d2):>14}  {err2:>9.2f}%")
            print(f"  {'[3] ΛCDM comóvel (referência) / comoving':<38}  {fmt(d3):>14}  {'—':>10}")
            separator()
            print(f"  Distância de luminosidade / Luminosity distance  d_L = {fmt(d_lum)} Mpc")
            print(f"  Distância angular          / Angular diameter     d_A = {fmt(d_ang)} Mpc")
            separator()

            # also show ΛCDM in other units
            d3_pc = d3 * 1e6
            d3_ly = convert(d3_pc, PARSEC, LIGHT_YEAR)
            print(f"  d_C (ΛCDM) em outras unidades / in other units:")
            print(f"    {fmt(d3_pc)} pc")
            print(f"    {fmt(d3_ly)} ly")
            separator()

            if z < 0.05:
                print("  ✔  z << 0.1 — todos os modelos concordam bem / all models agree well.")
            elif z < 0.3:
                print("  ⚠  0.05 < z < 0.3 — modelo [2] supera [1]; prefira [3].")
            else:
                print("  ✘  z ≥ 0.3 — use apenas ΛCDM [3] / use only ΛCDM [3].")
            separator()

            log(f"Redshift z={fmt(z)} → d_linear={fmt(d1)} Mpc | d_relat={fmt(d2)} Mpc | d_ΛCDM={fmt(d3)} Mpc")

        elif sub == "2":
            print()
            print("  Unidade da distância / Distance unit:")
            print_unit_menu()
            print("    7. Megaparsec [Mpc]")
            print()
            ukey = input("  Escolha / Choose (1-7): ").strip()

            if ukey == "7":
                d_mpc = float(input("  Distância em Mpc: "))
            elif ukey in UNITS:
                _, sym, u_m = UNITS[ukey]
                value = float(input(f"  Distância em {sym}: "))
                d_pc  = convert(value, u_m, PARSEC)
                d_mpc = d_pc / 1e6
            else:
                print("  ✘  Opção inválida.")
                return

            # Invert each model
            z_linear = (H0_KM_S_MPC * d_mpc) / (SPEED_OF_LIGHT / 1e3)

            # Relativistic: v = H0·d, then invert doppler
            v_over_c = min((H0_KM_S_MPC * d_mpc) / (SPEED_OF_LIGHT / 1e3), 0.9999)
            z_relat  = math.sqrt((1 + v_over_c) / (1 - v_over_c)) - 1

            z_lcdm   = _z_from_comoving_bisection(d_mpc)

            separator()
            print(f"  d = {fmt(d_mpc)} Mpc")
            separator()
            print(f"  {'MODELO / MODEL':<40}  {'z':>12}")
            separator("─")
            print(f"  {'[1] Hubble linear':<40}  {fmt(z_linear):>12}")
            print(f"  {'[2] Doppler relativístico / relativistic':<40}  {fmt(z_relat):>12}")
            print(f"  {'[3] ΛCDM comóvel (referência) / comoving':<40}  {fmt(z_lcdm):>12}")
            separator()

            log(f"Distância {fmt(d_mpc)} Mpc → z_linear={fmt(z_linear)} | z_relat={fmt(z_relat)} | z_ΛCDM={fmt(z_lcdm)}")
        else:
            print("  ✘  Opção inválida.")
    except ValueError as e:
        print(f"  ✘  Erro: {e}")

def menu_history():
    """Display and optionally save history."""
    separator()
    print("  HISTÓRICO DA SESSÃO / SESSION HISTORY")
    separator()
    if not history:
        print("  Nenhuma operação realizada ainda / No operations yet.")
    else:
        for i, entry in enumerate(history, 1):
            print(f"  {i:>3}. {entry}")
    separator()
    save = input("  Salvar histórico em .txt? / Save history to .txt? (s/y / n): ").strip().lower()
    if save in ("s", "y"):
        save_history()

# =============================================================================
#  MAIN LOOP / LOOP PRINCIPAL
# =============================================================================

def main():
    header()

    MENU = {
        "1": ("Conversão de unidades / Unit conversion",          menu_convert),
        "2": ("Tabela de referência / Reference table",           menu_reference),
        "3": ("Módulo de distância / Distance modulus",           menu_modulus),
        "4": ("Redshift ↔ Distância / Redshift ↔ Distance",      menu_redshift),
        "5": ("Histórico / History",                              menu_history),
        "0": ("Sair / Exit",                                      None),
    }

    while True:
        print()
        separator()
        print("  MENU PRINCIPAL / MAIN MENU")
        separator()
        for key, (label, _) in MENU.items():
            print(f"    {key}. {label}")
        separator()

        choice = input("  Opção / Option: ").strip()

        if choice not in MENU:
            print("  ✘  Opção inválida / Invalid option.")
            continue

        label, action = MENU[choice]

        if choice == "0":
            print()
            separator("═")
            print("  Encerrando. Boas olimpíadas! / Good luck at the olympiads!")
            separator("═")
            if history:
                save = input("  Salvar histórico antes de sair? / Save history before exit? (s/y / n): ").strip().lower()
                if save in ("s", "y"):
                    save_history()
            break

        action()

if __name__ == "__main__":
    main()