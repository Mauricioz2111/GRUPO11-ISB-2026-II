"""
Preparación de datos de pestañeo (EOG, BITalino/OpenSignals) para Edge Impulse.

Entradas (no se modifican):
    datos/pestaneo/pestaneo1.txt          señal principal
    datos/pestaneo/pestaneo1eventos.txt   marcas de los pestañeos

Salidas:
    datos_edge_impulse/{training,testing}/{pestaneo1,reposo}/*.csv
    resultados/pestaneo1_senal_completa.png
    resultados/pestaneo1_segmentos.png
    resultados/pestaneo1_control_calidad.csv
"""
import json
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------- Rutas (relativas a Software/) ----------------
BASE = Path(__file__).resolve().parent.parent
ARCHIVO_SENAL = BASE / "datos" / "pestaneo" / "pestaneo1.txt"
ARCHIVO_EVENTOS = BASE / "datos" / "pestaneo" / "pestaneo1eventos.txt"
CARPETA_EI = BASE / "datos_edge_impulse"
CARPETA_RES = BASE / "resultados"

# ---------------- Parámetros ----------------
CANAL = "A1"
SEG_ANTES = 0.75          # s antes del inicio del evento
SEG_DESPUES = 1.25        # s después -> ventana de 2 s
MS_BASE = 300             # ms iniciales para la mediana de línea base
MARGEN_REPOSO = 0.5       # s mínimos entre un reposo y cualquier ventana de pestañeo
N_TEST = 1                # eventos completos que van a Testing
SEMILLA = 11              # división reproducible (grupo 11)
MARGEN_ADC = 0.01         # "cerca del límite" = 1 % de la escala completa


# ---------------- Lectura ----------------
def leer_cabecera(ruta):
    with ruta.open("r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if linea.startswith("# {"):
                return next(iter(json.loads(linea[2:]).values()))
            if linea.strip() == "# EndOfHeader":
                break
    raise ValueError("No se encontró la cabecera de OpenSignals.")


def leer_eventos(ruta):
    filas = []
    with ruta.open("r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            c = linea.split("\t")
            if len(c) >= 5:
                filas.append((float(c[3]), float(c[4])))
    return filas


def limites_adc(cab, canal):
    """Bits del canal según 'resolution' (alineado con 'column')."""
    i = cab["column"].index(canal)
    bits = cab["resolution"][i]
    return 0, 2 ** bits - 1, bits


# ---------------- Segmentación ----------------
def ventana(t_ini, fs, n_total):
    """Devuelve (i0, i1) de una ventana de 2 s que empieza en t_ini."""
    i0 = int(round(t_ini * fs))
    i1 = i0 + int(round((SEG_ANTES + SEG_DESPUES) * fs))
    if i0 < 0 or i1 > n_total:
        return None
    return i0, i1


def elegir_reposos(ventanas_pest, duracion, fs, n_necesarios):
    """Un reposo centrado en cada hueco libre entre ventanas de pestañeo
    (selección determinista, sin mirar la amplitud de la señal)."""
    largo = SEG_ANTES + SEG_DESPUES
    bordes = [0.0]
    for a, b in ventanas_pest:
        bordes += [a, b]
    bordes.append(duracion)
    huecos = [(bordes[k], bordes[k + 1]) for k in range(0, len(bordes), 2)]
    reposos = []
    for a, b in huecos:
        libre_a, libre_b = a + MARGEN_REPOSO, b - MARGEN_REPOSO
        if libre_b - libre_a >= largo:
            centro = (libre_a + libre_b) / 2
            reposos.append(round(centro - largo / 2, 3))
    return reposos[:n_necesarios] if len(reposos) >= n_necesarios else reposos


# ---------------- Control de calidad ----------------
def estadisticas(raw, lo, hi, fs):
    rango = hi - lo
    cerca_lo = lo + MARGEN_ADC * rango
    cerca_hi = hi - MARGEN_ADC * rango
    max_run = max(
        (len(g) for g in np.split(raw, np.flatnonzero(np.diff(raw)) + 1)),
        default=0,
    )
    return {
        "minimo": raw.min(), "maximo": raw.max(),
        "media": raw.mean(), "mediana": float(np.median(raw)),
        "desv_std": raw.std(), "rango": raw.max() - raw.min(),
        "n_muestras": len(raw), "n_nan": int(np.isnan(raw).sum()),
        "muestras_en_limite_inf": int(np.sum(raw <= lo)),
        "pct_cerca_inferior": 100 * np.mean(raw <= cerca_lo),
        "pct_cerca_superior": 100 * np.mean(raw >= cerca_hi),
        "racha_constante_max_ms": int(max_run * 1000 / fs),
        "segmento_constante": bool(np.ptp(raw) == 0),
    }


def observacion(est, base_saturada):
    obs = []
    if est["pct_cerca_inferior"] > 1 or est["pct_cerca_superior"] > 1:
        obs.append("posible clipping/saturacion")
    if est["racha_constante_max_ms"] >= 50:
        obs.append(f"racha constante de {est['racha_constante_max_ms']} ms")
    if base_saturada:
        obs.append("linea base (primeros 300 ms) saturada: correccion poco confiable")
    if est["segmento_constante"]:
        obs.append("segmento constante")
    return "; ".join(obs) if obs else "sin observaciones"


def main():
    # ---------- Señal ----------
    cab = leer_cabecera(ARCHIVO_SENAL)
    fs = float(cab["sampling rate"])
    cols = cab["column"]
    assert CANAL in cols, f"No existe el canal {CANAL}"
    datos = np.loadtxt(ARCHIVO_SENAL, comments="#")
    senal = datos[:, cols.index(CANAL)]
    n_total = len(senal)
    duracion = n_total / fs
    lo, hi, bits = limites_adc(cab, CANAL)

    # ---------- Eventos ----------
    crudos = leer_eventos(ARCHIVO_EVENTOS)
    inicios = sorted({round(s, 3) for s, _ in crudos})
    advertencias = []

    # ---------- Pestañeos ----------
    pest = []
    for t in inicios:
        v = ventana(t - SEG_ANTES, fs, n_total)
        if v is None:
            advertencias.append(f"Evento en {t:.2f} s: la ventana sale del registro, se omite.")
            continue
        pest.append({"t_evento": t, "i0": v[0], "i1": v[1]})

    # ---------- Reposos ----------
    vent_t = [(p["i0"] / fs, p["i1"] / fs) for p in pest]
    t_rep = elegir_reposos(vent_t, duracion, fs, len(pest))
    reposos = []
    for t0 in t_rep:
        v = ventana(t0, fs, n_total)
        reposos.append({"t_evento": np.nan, "i0": v[0], "i1": v[1]})
    n = min(len(pest), len(reposos))
    if len(pest) != len(reposos):
        advertencias.append(f"Cantidades distintas: {len(pest)} pestaneo1 / {len(reposos)} reposos; se equilibra a {n}.")
    pest, reposos = pest[:n], reposos[:n]

    # No superposición reposo vs pestañeo
    for r in reposos:
        for p in pest:
            assert r["i1"] + MARGEN_REPOSO * fs <= p["i0"] or r["i0"] >= p["i1"] + MARGEN_REPOSO * fs, \
                "Reposo demasiado cerca de un pestañeo"

    # ---------- División Training / Testing (por evento completo) ----------
    rng = random.Random(SEMILLA)
    idx = list(range(n))
    idx_test_p = set(rng.sample(idx, N_TEST))
    idx_test_r = set(rng.sample(idx, N_TEST))
    for k, p in enumerate(pest):
        p["conjunto"] = "testing" if k in idx_test_p else "training"
    for k, r in enumerate(reposos):
        r["conjunto"] = "testing" if k in idx_test_r else "training"

    # Numeración 001..00N en orden temporal
    for lista, etiqueta in ((pest, "pestaneo1"), (reposos, "reposo")):
        for k, s in enumerate(lista, start=1):
            s["etiqueta"] = etiqueta
            s["archivo"] = f"{etiqueta}_{k:03d}.csv"

    # ---------- Guardado y QC ----------
    for sub in ("training", "testing"):
        for et in ("pestaneo1", "reposo"):
            (CARPETA_EI / sub / et).mkdir(parents=True, exist_ok=True)
    CARPETA_RES.mkdir(parents=True, exist_ok=True)

    n_base = int(round(MS_BASE * fs / 1000))
    filas_qc = []
    for s in pest + reposos:
        raw = senal[s["i0"]:s["i1"]]
        est = estadisticas(raw, lo, hi, fs)           # QC sobre la señal sin corregir
        base = float(np.median(raw[:n_base]))
        base_sat = (base <= lo + MARGEN_ADC * (hi - lo)) or (base >= hi - MARGEN_ADC * (hi - lo))
        corr = raw - base
        s["raw"], s["corr"], s["linea_base"] = raw, corr, base
        ts = np.arange(len(corr)) * int(round(1000 / fs))
        ruta = CARPETA_EI / s["conjunto"] / s["etiqueta"] / s["archivo"]
        pd.DataFrame({"timestamp": ts, "eog_a1": np.round(corr, 1)}).to_csv(ruta, index=False)
        s["ruta"] = ruta
        filas_qc.append({
            "archivo": s["archivo"], "etiqueta": s["etiqueta"],
            "tiempo_inicial_s": s["i0"] / fs, "tiempo_final_s": s["i1"] / fs,
            "tiempo_evento_s": s["t_evento"], "conjunto": s["conjunto"],
            "linea_base_raw": base, **est,
            "observaciones": observacion(est, base_sat),
        })
    qc = pd.DataFrame(filas_qc).round(3)
    qc.to_csv(CARPETA_RES / "pestaneo1_control_calidad.csv", index=False)

    # ---------- Figuras ----------
    t = np.arange(n_total) / fs
    fig, ax = plt.subplots(figsize=(14, 4.5))
    ax.plot(t, senal, lw=0.5, color="navy")
    for k, p in enumerate(pest):
        ax.axvspan(p["i0"] / fs, p["i1"] / fs, color="red", alpha=0.12,
                   label="ventana pestañeo" if k == 0 else None)
        ax.axvline(p["t_evento"], color="red", ls="--", lw=0.8,
                   label="evento" if k == 0 else None)
    for k, r in enumerate(reposos):
        ax.axvspan(r["i0"] / fs, r["i1"] / fs, color="green", alpha=0.12,
                   label="ventana reposo" if k == 0 else None)
    ax.axhline(lo, color="k", lw=0.6, ls=":"); ax.axhline(hi, color="k", lw=0.6, ls=":")
    ax.set(xlabel="Tiempo (s)", ylabel=f"{CANAL} (ADC, {bits} bits)",
           title="pestaneo1: señal completa con eventos")
    ax.legend(loc="upper right"); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(CARPETA_RES / "pestaneo1_senal_completa.png", dpi=150); plt.close(fig)

    tr = np.arange(2000) / fs - SEG_ANTES
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.5), sharey=True)
    for s in pest:
        ax[0].plot(tr, s["corr"], lw=0.7, label=f'{s["archivo"]} ({s["conjunto"][:5]})')
    for s in reposos:
        ax[1].plot(tr, s["corr"], lw=0.7, label=f'{s["archivo"]} ({s["conjunto"][:5]})')
    for lista, color, nom in ((pest, "red", "pestaneo1"), (reposos, "green", "reposo")):
        M = np.array([s["corr"] for s in lista])
        ax[2].plot(tr, M.mean(0), color=color, label=f"{nom}: media")
        ax[2].fill_between(tr, M.mean(0) - M.std(0), M.mean(0) + M.std(0), color=color, alpha=0.15)
    ax[0].axvline(0, color="k", ls="--", lw=0.8)
    for a_, tit in zip(ax, ("Pestañeos superpuestos", "Reposos superpuestos", "Comparación (media ± std)")):
        a_.set_title(tit); a_.set_xlabel("Tiempo respecto al inicio del evento (s)"); a_.grid(alpha=0.25)
        a_.legend(fontsize=7)
    ax[0].set_ylabel("A1 con línea base corregida")
    fig.tight_layout(); fig.savefig(CARPETA_RES / "pestaneo1_segmentos.png", dpi=150); plt.close(fig)

    # ---------- Validación local ----------
    ok = True
    todos = []
    for s in pest + reposos:
        d = pd.read_csv(s["ruta"])
        chk = (list(d.columns) == ["timestamp", "eog_a1"] and len(d) == 2000
               and d["timestamp"].iloc[0] == 0
               and (np.diff(d["timestamp"]) == 1000 / fs).all()
               and not d.isna().any().any())
        if not chk:
            ok = False; advertencias.append(f"Formato inválido: {s['archivo']}")
        todos.append((s["etiqueta"], s["i0"], s["i1"], s["conjunto"]))
    sets = {c: [(a, b) for _, a, b, cc in todos if cc == c] for c in ("training", "testing")}
    solapes = any(a1 < b2 and a2 < b1 for a1, b1 in sets["training"] for a2, b2 in sets["testing"])
    dup_idx = len({(a, b) for _, a, b, _ in todos}) != len(todos)
    contenido = [tuple(np.round(s["corr"], 1)) for s in pest + reposos]
    dup_cont = len(set(contenido)) != len(contenido)
    centrado = all(abs((p["i0"] / fs + SEG_ANTES) - p["t_evento"]) < 1e-9 for p in pest)

    # ---------- Terminal ----------
    print("=" * 56)
    print(f"Frecuencia: {fs:.0f} Hz | Canal: {CANAL} (columna {cols.index(CANAL)}), ADC {bits} bits [{lo}, {hi}]")
    print(f"Duración: {duracion:.2f} s ({n_total} muestras) | Columnas: {cols}")
    print(f"Eventos totales (filas): {len(crudos)} | únicos: {len(inicios)} -> {inicios}")
    print(f"Segmentos válidos: {len(pest)} pestaneo1 + {len(reposos)} reposo")
    for c in ("training", "testing"):
        for et in ("pestaneo1", "reposo"):
            arch = sorted(s["archivo"] for s in pest + reposos if s["conjunto"] == c and s["etiqueta"] == et)
            print(f"  {c}/{et}: {arch}")
    print("Reposos (inicio s):", [round(r["i0"] / fs, 2) for r in reposos])
    print(f"Validación: formato CSV={'OK' if ok else 'FALLA'} | solape train/test={'SI' if solapes else 'no'} | "
          f"ventanas duplicadas={'SI' if dup_idx else 'no'} | contenido duplicado={'SI' if dup_cont else 'no'} | "
          f"pestañeos centrados={'OK' if centrado else 'FALLA'}")
    afect = qc[qc["observaciones"] != "sin observaciones"]
    if len(afect):
        advertencias.append(f"{len(afect)}/{len(qc)} segmentos con observaciones de calidad (ver control_calidad.csv)")
    print("Advertencias:" + ("" if advertencias else " ninguna"))
    for a in advertencias:
        print("  -", a)
    print(qc[["archivo", "conjunto", "pct_cerca_inferior", "pct_cerca_superior", "linea_base_raw", "observaciones"]]
          .to_string(index=False))


if __name__ == "__main__":
    main()
