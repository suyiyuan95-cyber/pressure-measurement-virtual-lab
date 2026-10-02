import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# STREAMLIT PAGE
# ============================================================

st.set_page_config(
    page_title="Pressure Measurement Virtual Lab",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Pressure Measurement Virtual Lab")

st.write(
    """
    Complete the experiment by interacting with the virtual laboratory.

    **Drag, connect, measure, record, and calculate — just like a physical lab.**
    """
)


# ============================================================
# DIGITAL VIRTUAL LAB
# ============================================================

virtual_lab = r"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<style>

/* ============================================================
   GENERAL
============================================================ */

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background:
        linear-gradient(
            180deg,
            #dfe7ec 0%,
            #eef3f6 45%,
            #d9e1e6 100%
        );
    color: #1f2937;
}

.lab-wrapper {
    max-width: 1250px;
    margin: auto;
    padding: 20px;
}


/* ============================================================
   TOP STATUS PANEL
============================================================ */

.status-panel {
    background: #ffffff;
    border-left: 7px solid #0284c7;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.12);
}

.status-title {
    font-weight: bold;
    color: #075985;
    margin-bottom: 6px;
}

#statusText {
    font-size: 16px;
}


/* ============================================================
   LAB ROOM
============================================================ */

.lab-room {
    position: relative;

    min-height: 740px;

    background:
        linear-gradient(
            to bottom,
            #edf4f7 0%,
            #edf4f7 66%,
            #a98260 66%,
            #8b694e 100%
        );

    border: 3px solid #64748b;
    border-radius: 18px;

    overflow: hidden;

    box-shadow:
        inset 0 0 30px rgba(0,0,0,0.12),
        0 4px 18px rgba(0,0,0,0.15);
}


/* Wall horizontal line */

.lab-room::before {
    content: "";

    position: absolute;

    left: 0;
    right: 0;

    top: 66%;

    height: 6px;

    background: #475569;
}


/* ============================================================
   EQUIPMENT SHELF
============================================================ */

.equipment-shelf {
    position: absolute;

    left: 25px;
    top: 35px;

    width: 290px;
    min-height: 570px;

    background:
        linear-gradient(
            180deg,
            #d1d5db,
            #b8bec6
        );

    border: 6px solid #475569;

    border-radius: 12px;

    box-shadow:
        inset 0 0 15px rgba(0,0,0,0.25);

    padding: 15px;
}

.equipment-shelf h3 {
    text-align: center;
    margin-top: 4px;
    color: #1e293b;
}

.shelf-line {
    border-top: 5px solid #64748b;
    margin: 22px -15px;
}


/* ============================================================
   DRAGGABLE INSTRUMENTS
============================================================ */

.instrument {
    position: relative;

    margin: 12px auto;

    cursor: grab;

    user-select: none;

    transition:
        transform 0.18s,
        filter 0.18s;

    touch-action: none;
}

.instrument:hover {
    transform: scale(1.025);
    filter: drop-shadow(
        0 5px 6px rgba(0,0,0,0.22)
    );
}

.instrument:active {
    cursor: grabbing;
}


/* ============================================================
   DIGITAL BAROMETER
============================================================ */

.barometer-unit {
    width: 185px;
    height: 310px;
}

.baro-frame {
    position: absolute;

    width: 165px;
    height: 290px;

    left: 10px;
    top: 5px;

    border: 5px solid #374151;
    border-radius: 18px;

    background:
        linear-gradient(
            90deg,
            #cbd5e1,
            #f8fafc 35%,
            #d1d5db 70%,
            #94a3b8
        );

    box-shadow:
        inset 0 0 8px rgba(0,0,0,0.22),
        0 4px 8px rgba(0,0,0,0.25);
}


/* Barometer title */

.baro-name {
    position: absolute;

    width: 100%;
    top: 9px;

    text-align: center;

    font-size: 12px;
    font-weight: bold;

    color: #1f2937;
}


/* Scale area */

.baro-scale {
    position: absolute;

    left: 16px;
    top: 36px;

    width: 70px;
    height: 220px;
}


/* Glass tube */

.glass-tube {
    position: absolute;

    left: 97px;
    top: 35px;

    width: 34px;
    height: 220px;

    background:
        linear-gradient(
            90deg,
            rgba(255,255,255,0.7),
            rgba(219,234,254,0.32),
            rgba(255,255,255,0.75)
        );

    border: 3px solid #64748b;

    border-radius:
        16px 16px 5px 5px;

    overflow: hidden;
}


/* Mercury */

.mercury {
    position: absolute;

    bottom: 0;

    width: 100%;

    height: 40%;

    background:
        linear-gradient(
            90deg,
            #475569 0%,
            #d1d5db 40%,
            #64748b 70%,
            #334155 100%
        );

    transition: height 1.1s ease;
}


/* meniscus */

.mercury::before {
    content: "";

    position: absolute;

    left: 1px;
    top: -4px;

    width: calc(100% - 2px);
    height: 8px;

    background: #94a3b8;

    border-radius: 50%;
}


/* reservoir */

.baro-reservoir {
    position: absolute;

    left: 86px;
    top: 247px;

    width: 58px;
    height: 35px;

    border-radius: 50%;

    border: 3px solid #475569;

    background:
        linear-gradient(
            #cbd5e1 0%,
            #64748b 45%,
            #334155 100%
        );
}


/* ============================================================
   BAROMETER SCALE
============================================================ */

.baro-mark {
    position: absolute;

    right: 0;

    width: 22px;

    border-top: 1px solid #1f2937;
}

.baro-mark.major {
    width: 33px;

    border-top:
        2px solid #111827;
}

.baro-label {
    position: absolute;

    right: 39px;

    transform:
        translateY(-50%);

    font-size: 10px;
    font-weight: bold;

    color: #111827;
}


/* ============================================================
   DIGITAL PRESSURE GAUGE
============================================================ */

.gauge-unit {
    width: 190px;
    height: 245px;

    margin-top: 10px;
}

.gauge-case {
    position: absolute;

    left: 10px;
    top: 5px;

    width: 170px;
    height: 170px;

    border-radius: 50%;

    border: 10px solid #475569;

    background:
        radial-gradient(
            circle at 35% 30%,
            #ffffff,
            #f1f5f9 55%,
            #d1d5db 100%
        );

    box-shadow:
        inset 0 0 14px rgba(0,0,0,0.20),
        0 5px 10px rgba(0,0,0,0.25);
}

.gauge-glass {
    position: absolute;

    left: 7px;
    top: 7px;

    width: 136px;
    height: 136px;

    border-radius: 50%;

    border:
        2px solid rgba(255,255,255,0.75);

    pointer-events: none;
}


/* Gauge numbers */

.gauge-number {
    position: absolute;

    font-size: 10px;
    font-weight: bold;

    color: #111827;
}


/* Needle */

.needle-holder {
    position: absolute;

    left: 75px;
    top: 75px;

    width: 0;
    height: 0;

    transform: rotate(-135deg);

    transition:
        transform 1.2s cubic-bezier(.2,.8,.2,1);
}

.gauge-needle {
    position: absolute;

    width: 4px;
    height: 56px;

    left: -2px;
    top: -56px;

    background: #dc2626;

    border-radius:
        4px 4px 0 0;
}

.gauge-hub {
    position: absolute;

    left: 67px;
    top: 67px;

    width: 16px;
    height: 16px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #64748b,
            #111827
        );
}

.gauge-kpa {
    position: absolute;

    left: 0;
    right: 0;
    top: 105px;

    text-align: center;

    font-size: 11px;
    font-weight: bold;
}


/* Gauge bottom connector */

.gauge-connector {
    position: absolute;

    left: 79px;
    top: 170px;

    width: 30px;
    height: 37px;

    background:
        linear-gradient(
            90deg,
            #9a6c2f,
            #e3b45e,
            #8c5a20
        );

    border:
        3px solid #6b4219;
}

.gauge-fitting {
    position: absolute;

    left: 68px;
    top: 202px;

    width: 52px;
    height: 25px;

    border-radius: 6px;

    background:
        linear-gradient(
            #b7792d,
            #e2ad58,
            #85531d
        );

    border:
        3px solid #6b4219;
}


/* ============================================================
   ATMOSPHERIC MEASUREMENT STATION
============================================================ */

.atmosphere-station {
    position: absolute;

    left: 365px;
    top: 45px;

    width: 310px;
    height: 350px;

    border:
        4px dashed #0284c7;

    border-radius: 18px;

    background:
        rgba(224,242,254,0.67);

    transition:
        background 0.25s,
        border-color 0.25s;
}

.atmosphere-station.drag-over {
    background:
        rgba(186,230,253,0.92);

    border-color: #0369a1;
}

.atmosphere-station.active {
    border-style: solid;

    border-color: #16a34a;

    background:
        rgba(240,253,244,0.82);
}

.station-title {
    text-align: center;

    margin-top: 12px;

    font-weight: bold;

    color: #075985;
}

.station-subtitle {
    text-align: center;

    font-size: 13px;

    color: #475569;
}


/* ============================================================
   PRESSURE VESSEL
============================================================ */

.pressure-area {
    position: absolute;

    right: 25px;
    top: 45px;

    width: 470px;
    height: 510px;
}

.pressure-area h3 {
    text-align: center;

    margin-top: 5px;

    color: #334155;
}

.vessel {
    position: absolute;

    left: 85px;
    top: 130px;

    width: 280px;
    height: 190px;

    border:
        6px solid #475569;

    border-radius: 70px;

    background:
        linear-gradient(
            180deg,
            #e2e8f0 0%,
            #aeb8c4 35%,
            #8794a3 60%,
            #cbd5e1 100%
        );

    box-shadow:
        inset 0 10px 18px rgba(255,255,255,0.42),
        inset 0 -10px 20px rgba(0,0,0,0.20),
        0 8px 14px rgba(0,0,0,0.25);
}

.vessel-band {
    position: absolute;

    top: 0;

    width: 15px;
    height: 100%;

    background: #64748b;
}

.vessel-band.left {
    left: 55px;
}

.vessel-band.right {
    right: 55px;
}

.vessel-label {
    position: absolute;

    left: 0;
    right: 0;

    top: 76px;

    text-align: center;

    font-weight: bold;

    color: #334155;
}


/* legs */

.vessel-leg {
    position: absolute;

    width: 28px;
    height: 65px;

    background: #475569;

    bottom: -58px;
}

.vessel-leg.one {
    left: 55px;
}

.vessel-leg.two {
    right: 55px;
}


/* ============================================================
   TEST PORT
============================================================ */

.test-port {
    position: absolute;

    right: -30px;
    top: 73px;

    width: 35px;
    height: 44px;

    background:
        linear-gradient(
            90deg,
            #9a6c2f,
            #f3c56d,
            #8a571e
        );

    border:
        3px solid #6b4219;

    border-radius: 5px;
}

.test-port::after {
    content: "";

    position: absolute;

    right: -18px;
    top: 8px;

    width: 20px;
    height: 23px;

    background: #111827;

    border-radius:
        0 8px 8px 0;
}


/* Drop zone around port */

.port-drop-zone {
    position: absolute;

    right: -115px;
    top: 20px;

    width: 150px;
    height: 160px;

    border:
        3px dashed transparent;

    border-radius: 20px;

    transition: 0.2s;
}

.port-drop-zone.drag-over {
    border-color: #0284c7;

    background:
        rgba(224,242,254,0.55);
}


/* ============================================================
   HOSE
============================================================ */

.hose {
    position: absolute;

    display: none;

    left: 310px;
    top: 60px;

    width: 115px;
    height: 130px;

    border-right:
        11px solid #222;

    border-top:
        11px solid #222;

    border-radius:
        0 55px 0 0;

    z-index: 3;
}

.hose.connected {
    display: block;
}


/* ============================================================
   CONNECTED GAUGE POSITION
============================================================ */

.connected-gauge {
    position: absolute !important;

    left: 275px !important;
    top: -50px !important;

    margin: 0 !important;

    transform: scale(0.88);
}


/* ============================================================
   VALVE
============================================================ */

.valve-group {
    position: absolute;

    left: 362px;
    top: 228px;

    text-align: center;

    display: none;
}

.valve-group.visible {
    display: block;
}

.valve-body {
    position: relative;

    width: 82px;
    height: 82px;

    margin: auto;

    border-radius: 50%;

    border: 7px solid #6b4219;

    background:
        radial-gradient(
            circle,
            #dba74e,
            #95601f
        );

    cursor: pointer;

    box-shadow:
        0 5px 10px rgba(0,0,0,0.25);
}

.valve-handle {
    position: absolute;

    left: 5px;
    top: 30px;

    width: 60px;
    height: 11px;

    border-radius: 8px;

    background: #b91c1c;

    transform: rotate(0deg);

    transition:
        transform 0.8s ease;
}

.valve-handle.open {
    transform: rotate(90deg);
}

.valve-label {
    margin-top: 5px;

    font-size: 12px;
    font-weight: bold;
}


/* ============================================================
   TASK PANELS
============================================================ */

.tasks-area {
    margin-top: 24px;
}

.task-card {
    display: none;

    background: white;

    padding: 22px;

    margin-bottom: 18px;

    border-radius: 12px;

    border-left:
        7px solid #0284c7;

    box-shadow:
        0 3px 11px rgba(0,0,0,0.11);
}

.task-card.active {
    display: block;
}

.task-card h3 {
    margin-top: 0;

    color: #075985;
}

.measurement-row {
    display: flex;

    align-items: center;

    gap: 10px;

    flex-wrap: wrap;
}

input {
    width: 190px;

    padding: 12px;

    font-size: 16px;

    border:
        2px solid #cbd5e1;

    border-radius: 7px;
}

input:focus {
    outline: none;

    border-color: #0284c7;
}

button {
    padding:
        11px 17px;

    border: none;

    border-radius: 7px;

    background: #0284c7;

    color: white;

    font-size: 15px;

    cursor: pointer;
}

button:hover {
    background: #0369a1;
}

.feedback {
    margin-top: 12px;

    padding: 10px 12px;

    border-radius: 6px;
}

.correct {
    background: #dcfce7;

    color: #166534;

    border-left:
        5px solid #16a34a;
}

.incorrect {
    background: #fee2e2;

    color: #991b1b;

    border-left:
        5px solid #dc2626;
}


/* ============================================================
   COMPLETE PANEL
============================================================ */

.complete-panel {
    display: none;

    background: #f0fdf4;

    border:
        3px solid #16a34a;

    border-radius: 14px;

    padding: 28px;

    margin-top: 25px;

    text-align: center;

    box-shadow:
        0 3px 12px rgba(0,0,0,0.10);
}

.complete-panel.visible {
    display: block;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 1000px) {

    .lab-room {
        min-height: 1250px;
    }

    .equipment-shelf {
        left: 50%;
        transform: translateX(-50%);

        width: 300px;
    }

    .atmosphere-station {
        left: 50%;
        transform: translateX(-50%);

        top: 635px;
    }

    .pressure-area {
        left: 50%;
        transform: translateX(-50%);

        top: 980px;
    }
}

</style>

</head>


<body>

<div class="lab-wrapper">


<!-- ============================================================
     STATUS
============================================================= -->

<div class="status-panel">

    <div class="status-title">
        Laboratory Procedure
    </div>

    <div id="statusText">
        Step 1 — Drag the mercury barometer from the equipment shelf
        to the atmospheric measurement station.
    </div>

</div>


<!-- ============================================================
     LAB ROOM
============================================================= -->

<div
    id="labRoom"
    class="lab-room"
>


<!-- ============================================================
     EQUIPMENT SHELF
============================================================= -->

<div class="equipment-shelf">

<h3>
Equipment Shelf
</h3>


<!-- BAROMETER -->

<div
    id="barometerInstrument"
    class="instrument barometer-unit"
    draggable="true"
    data-equipment="barometer"
>

    <div class="baro-frame">

        <div class="baro-name">
            MERCURY BAROMETER
        </div>


        <div
            id="baroScale"
            class="baro-scale"
        >
        </div>


        <div class="glass-tube">

            <div
                id="mercuryColumn"
                class="mercury"
            >
            </div>

        </div>


        <div class="baro-reservoir">
        </div>

    </div>

</div>


<div class="shelf-line">
</div>


<!-- GAUGE -->

<div
    id="gaugeInstrument"
    class="instrument gauge-unit"
    draggable="true"
    data-equipment="gauge"
>

    <div class="gauge-case">

        <div
            id="gaugeNumbers"
        >
        </div>


        <div
            id="needleHolder"
            class="needle-holder"
        >

            <div class="gauge-needle">
            </div>

        </div>


        <div class="gauge-hub">
        </div>


        <div class="gauge-kpa">
            kPa
        </div>


        <div class="gauge-glass">
        </div>

    </div>


    <div class="gauge-connector">
    </div>


    <div class="gauge-fitting">
    </div>

</div>

</div>


<!-- ============================================================
     ATMOSPHERIC MEASUREMENT STATION
============================================================= -->

<div
    id="atmosphereStation"
    class="atmosphere-station"
    data-zone="atmosphere"
>

    <div class="station-title">
        Atmospheric Measurement Station
    </div>

    <div class="station-subtitle">
        Place the barometer here
    </div>

</div>


<!-- ============================================================
     PRESSURE SYSTEM
============================================================= -->

<div
    class="pressure-area"
>

<h3>
Pressurized System
</h3>


<div class="vessel">

    <div class="vessel-band left">
    </div>

    <div class="vessel-band right">
    </div>


    <div class="vessel-label">
        PRESSURE VESSEL
    </div>


    <div class="vessel-leg one">
    </div>

    <div class="vessel-leg two">
    </div>


    <div class="test-port">
    </div>


    <div
        id="portDropZone"
        class="port-drop-zone"
        data-zone="port"
    >
    </div>

</div>


<!-- HOSE -->

<div
    id="hose"
    class="hose"
>
</div>


<!-- VALVE -->

<div
    id="valveGroup"
    class="valve-group"
>

    <div
        id="valveBody"
        class="valve-body"
        onclick="turnValve()"
    >

        <div
            id="valveHandle"
            class="valve-handle"
        >
        </div>

    </div>


    <div
        id="valveLabel"
        class="valve-label"
    >
        CLOSED
    </div>

</div>

</div>

</div>


<!-- ============================================================
     STUDENT TASKS
============================================================= -->

<div class="tasks-area">


<!-- TASK 1 -->

<div
    id="barometerTask"
    class="task-card"
>

<h3>
Step 2 — Record the Barometer Reading
</h3>

<p>
Read the top of the mercury column from the barometer scale.
</p>


<div class="measurement-row">

<input
    id="barometerInput"
    type="number"
    placeholder="Enter reading"
>

<span>
mmHg
</span>

<button
    onclick="checkBarometer()"
>
Record Reading
</button>

</div>


<div
    id="barometerFeedback"
>
</div>

</div>


<!-- TASK 2 -->

<div
    id="atmosphereTask"
    class="task-card"
>

<h3>
Step 3 — Calculate Atmospheric Pressure
</h3>

<p>
Use your measured barometer reading.
</p>

<p>
<strong>
P<sub>atm</sub>
=
ρ<sub>Hg</sub>gh
</strong>
</p>

<p>
ρ<sub>Hg</sub> = 13,600 kg/m³
<br>
g = 9.81 m/s²
</p>


<div class="measurement-row">

<input
    id="atmosphericInput"
    type="number"
    step="0.01"
    placeholder="Enter result"
>

<span>
kPa
</span>

<button
    onclick="checkAtmospheric()"
>
Check Calculation
</button>

</div>


<div
    id="atmosphericFeedback"
>
</div>

</div>


<!-- TASK 3 -->

<div
    id="gaugeTask"
    class="task-card"
>

<h3>
Step 6 — Record Gauge Pressure
</h3>

<p>
Read the red needle after the valve has been opened.
</p>


<div class="measurement-row">

<input
    id="gaugeInput"
    type="number"
    placeholder="Enter reading"
>

<span>
kPa
</span>

<button
    onclick="checkGauge()"
>
Record Reading
</button>

</div>


<div
    id="gaugeFeedback"
>
</div>

</div>


<!-- TASK 4 -->

<div
    id="absoluteTask"
    class="task-card"
>

<h3>
Step 7 — Calculate Absolute Pressure
</h3>

<p>
Use:
</p>

<p>
<strong>
P<sub>abs</sub>
=
P<sub>gauge</sub>
+
P<sub>atm</sub>
</strong>
</p>


<div class="measurement-row">

<input
    id="absoluteInput"
    type="number"
    step="0.01"
    placeholder="Enter result"
>

<span>
kPa
</span>

<button
    onclick="checkAbsolute()"
>
Submit Result
</button>

</div>


<div
    id="absoluteFeedback"
>
</div>

</div>


<!-- COMPLETE -->

<div
    id="completePanel"
    class="complete-panel"
>

<h2>
🎉 Experiment Complete
</h2>

<p>
Your calculated absolute pressure is within the required ±5%.
</p>

<button
    onclick="location.reload()"
>
Run New Experiment
</button>

</div>


</div>

</div>


<script>

/* ============================================================
   ENGINEERING VALUES
============================================================ */

const RHO_HG = 13600;
const G = 9.81;

const barometerValues = [
    735,
    740,
    745,
    750,
    755,
    760,
    765,
    770,
    775
];

const gaugeValues = [
    20,
    25,
    30,
    35,
    40,
    45,
    50,
    55,
    60,
    65,
    70,
    75,
    80
];


const barometerValue =
    barometerValues[
        Math.floor(
            Math.random()
            *
            barometerValues.length
        )
    ];


const gaugeValue =
    gaugeValues[
        Math.floor(
            Math.random()
            *
            gaugeValues.length
        )
    ];


const atmosphericPressure =
    RHO_HG
    *
    G
    *
    (
        barometerValue
        /
        1000
    )
    /
    1000;


const absolutePressure =
    atmosphericPressure
    +
    gaugeValue;


/* ============================================================
   STUDENT PROGRESS
============================================================ */

let atmosphericAccepted = false;
let gaugeConnected = false;
let valveOpened = false;


/* ============================================================
   CREATE BAROMETER SCALE
============================================================ */

function createBarometerScale() {

    const scale =
        document.getElementById(
            "baroScale"
        );


    for (
        let value = 720;
        value <= 780;
        value += 5
    ) {

        const percentage =
            (
                (value - 720)
                /
                60
            )
            *
            100;


        const line =
            document.createElement(
                "div"
            );


        line.className =
            "baro-mark";


        if (
            value % 10 === 0
        ) {

            line.classList.add(
                "major"
            );

        }


        line.style.bottom =
            percentage
            +
            "%";


        scale.appendChild(
            line
        );


        if (
            value % 10 === 0
        ) {

            const label =
                document.createElement(
                    "div"
                );


            label.className =
                "baro-label";


            label.style.bottom =
                percentage
                +
                "%";


            label.textContent =
                value;


            scale.appendChild(
                label
            );

        }

    }


    const mercuryPercentage =
        (
            (barometerValue - 720)
            /
            60
        )
        *
        100;


    document.getElementById(
        "mercuryColumn"
    ).style.height =
        mercuryPercentage
        +
        "%";

}


/* ============================================================
   CREATE GAUGE NUMBERS
============================================================ */

function createGaugeNumbers() {

    const parent =
        document.getElementById(
            "gaugeNumbers"
        );


    const cx = 75;
    const cy = 75;

    const radius = 56;


    for (
        let value = 0;
        value <= 100;
        value += 20
    ) {

        const angleDeg =
            -135
            +
            (
                value
                /
                100
            )
            *
            270;


        const angle =
            angleDeg
            *
            Math.PI
            /
            180;


        const x =
            cx
            +
            radius
            *
            Math.cos(angle);


        const y =
            cy
            +
            radius
            *
            Math.sin(angle);


        const number =
            document.createElement(
                "div"
            );


        number.className =
            "gauge-number";


        number.textContent =
            value;


        number.style.left =
            x
            +
            "px";


        number.style.top =
            y
            +
            "px";


        number.style.transform =
            "translate(-50%,-50%)";


        parent.appendChild(
            number
        );

    }

}


/* ============================================================
   STATUS
============================================================ */

function setStatus(message) {

    document.getElementById(
        "statusText"
    ).textContent =
        message;

}


/* ============================================================
   DRAG START
============================================================ */

document.querySelectorAll(
    ".instrument"
).forEach(
    element => {

        element.addEventListener(
            "dragstart",
            event => {

                event.dataTransfer.setData(
                    "text/plain",
                    element.dataset.equipment
                );

            }
        );

    }
);


/* ============================================================
   ATMOSPHERE DROP
============================================================ */

const atmosphereStation =
    document.getElementById(
        "atmosphereStation"
    );


atmosphereStation.addEventListener(
    "dragover",
    event => {

        event.preventDefault();

        atmosphereStation.classList.add(
            "drag-over"
        );

    }
);


atmosphereStation.addEventListener(
    "dragleave",
    () => {

        atmosphereStation.classList.remove(
            "drag-over"
        );

    }
);


atmosphereStation.addEventListener(
    "drop",
    event => {

        event.preventDefault();


        atmosphereStation.classList.remove(
            "drag-over"
        );


        const equipment =
            event.dataTransfer.getData(
                "text/plain"
            );


        if (
            equipment
            !==
            "barometer"
        ) {

            alert(
                "Use the mercury barometer at this station."
            );

            return;

        }


        const barometer =
            document.getElementById(
                "barometerInstrument"
            );


        atmosphereStation.appendChild(
            barometer
        );


        barometer.style.position =
            "absolute";

        barometer.style.left =
            "62px";

        barometer.style.top =
            "45px";

        barometer.style.margin =
            "0";

        barometer.draggable =
            false;


        atmosphereStation.classList.add(
            "active"
        );


        document.getElementById(
            "barometerTask"
        ).classList.add(
            "active"
        );


        setStatus(
            "Step 2 — Read the mercury barometer and record the measurement."
        );

    }
);


/* ============================================================
   CHECK BAROMETER
============================================================ */

function checkBarometer() {

    const answer =
        parseFloat(
            document.getElementById(
                "barometerInput"
            ).value
        );


    const feedback =
        document.getElementById(
            "barometerFeedback"
        );


    if (
        Number.isNaN(answer)
    ) {

        showFeedback(
            feedback,
            "Enter a numerical measurement.",
            false
        );

        return;

    }


    if (
        Math.abs(
            answer
            -
            barometerValue
        )
        <=
        2.5
    ) {

        showFeedback(
            feedback,
            "✓ Barometer measurement recorded.",
            true
        );


        document.getElementById(
            "atmosphereTask"
        ).classList.add(
            "active"
        );


        setStatus(
            "Step 3 — Calculate atmospheric pressure using the measured barometer height."
        );

    }

    else {

        showFeedback(
            feedback,
            "Recheck the top of the mercury column and the scale.",
            false
        );

    }

}


/* ============================================================
   CHECK ATMOSPHERIC PRESSURE
============================================================ */

function checkAtmospheric() {

    const answer =
        parseFloat(
            document.getElementById(
                "atmosphericInput"
            ).value
        );


    const feedback =
        document.getElementById(
            "atmosphericFeedback"
        );


    if (
        Number.isNaN(answer)
    ) {

        showFeedback(
            feedback,
            "Enter a numerical pressure.",
            false
        );

        return;

    }


    const error =
        Math.abs(
            answer
            -
            atmosphericPressure
        )
        /
        atmosphericPressure;


    if (
        error <= 0.05
    ) {

        atmosphericAccepted =
            true;


        showFeedback(
            feedback,
            "✓ Atmospheric pressure accepted. Your result is within ±5%.",
            true
        );


        setStatus(
            "Step 4 — Drag the pressure gauge from the equipment shelf to the vessel test port."
        );

    }

    else {

        showFeedback(
            feedback,
            "Result is outside ±5%. Check your unit conversion and P = ρgh.",
            false
        );

    }

}


/* ============================================================
   GAUGE DROP
============================================================ */

const portDropZone =
    document.getElementById(
        "portDropZone"
    );


portDropZone.addEventListener(
    "dragover",
    event => {

        event.preventDefault();

        portDropZone.classList.add(
            "drag-over"
        );

    }
);


portDropZone.addEventListener(
    "dragleave",
    () => {

        portDropZone.classList.remove(
            "drag-over"
        );

    }
);


portDropZone.addEventListener(
    "drop",
    event => {

        event.preventDefault();


        portDropZone.classList.remove(
            "drag-over"
        );


        const equipment =
            event.dataTransfer.getData(
                "text/plain"
            );


        if (
            equipment
            !==
            "gauge"
        ) {

            alert(
                "Connect the pressure gauge to the vessel test port."
            );

            return;

        }


        if (
            !atmosphericAccepted
        ) {

            alert(
                "Complete the atmospheric pressure measurement first."
            );

            return;

        }


        const gauge =
            document.getElementById(
                "gaugeInstrument"
            );


        document.querySelector(
            ".pressure-area"
        ).appendChild(
            gauge
        );


        gauge.classList.add(
            "connected-gauge"
        );


        gauge.draggable =
            false;


        document.getElementById(
            "hose"
        ).classList.add(
            "connected"
        );


        document.getElementById(
            "valveGroup"
        ).classList.add(
            "visible"
        );


        gaugeConnected =
            true;


        setStatus(
            "Step 5 — Gauge connected. Turn the red valve handle to OPEN."
        );

    }
);


/* ============================================================
   TURN VALVE
============================================================ */

function turnValve() {

    if (
        !gaugeConnected
    ) {
        return;
    }


    if (
        valveOpened
    ) {
        return;
    }


    valveOpened =
        true;


    document.getElementById(
        "valveHandle"
    ).classList.add(
        "open"
    );


    document.getElementById(
        "valveLabel"
    ).textContent =
        "OPEN";


    const needleAngle =
        -135
        +
        (
            gaugeValue
            /
            100
        )
        *
        270;


    document.getElementById(
        "needleHolder"
    ).style.transform =
        "rotate("
        +
        needleAngle
        +
        "deg)";


    document.getElementById(
        "gaugeTask"
    ).classList.add(
        "active"
    );


    setStatus(
        "Step 6 — Valve open. Read the pressure gauge and record the measurement."
    );

}


/* ============================================================
   CHECK GAUGE
============================================================ */

function checkGauge() {

    const answer =
        parseFloat(
            document.getElementById(
                "gaugeInput"
            ).value
        );


    const feedback =
        document.getElementById(
            "gaugeFeedback"
        );


    if (
        Number.isNaN(answer)
    ) {

        showFeedback(
            feedback,
            "Enter a numerical pressure.",
            false
        );

        return;

    }


    if (
        Math.abs(
            answer
            -
            gaugeValue
        )
        <=
        2.5
    ) {

        showFeedback(
            feedback,
            "✓ Gauge pressure recorded.",
            true
        );


        document.getElementById(
            "absoluteTask"
        ).classList.add(
            "active"
        );


        setStatus(
            "Step 7 — Calculate absolute pressure using your measured atmospheric and gauge pressures."
        );

    }

    else {

        showFeedback(
            feedback,
            "Recheck the position of the red gauge needle.",
            false
        );

    }

}


/* ============================================================
   CHECK ABSOLUTE PRESSURE
============================================================ */

function checkAbsolute() {

    const answer =
        parseFloat(
            document.getElementById(
                "absoluteInput"
            ).value
        );


    const feedback =
        document.getElementById(
            "absoluteFeedback"
        );


    if (
        Number.isNaN(answer)
    ) {

        showFeedback(
            feedback,
            "Enter a numerical pressure.",
            false
        );

        return;

    }


    const error =
        Math.abs(
            answer
            -
            absolutePressure
        )
        /
        absolutePressure;


    if (
        error <= 0.05
    ) {

        showFeedback(
            feedback,
            "✓ Absolute pressure accepted.",
            true
        );


        document.getElementById(
            "completePanel"
        ).classList.add(
            "visible"
        );


        setStatus(
            "Experiment complete — final result is within ±5%."
        );

    }

    else {

        showFeedback(
            feedback,
            "Result is outside ±5%. Recheck Pabs = Pgauge + Patm.",
            false
        );

    }

}


/* ============================================================
   FEEDBACK
============================================================ */

function showFeedback(
    element,
    message,
    correct
) {

    element.className =
        correct
        ?
        "feedback correct"
        :
        "feedback incorrect";


    element.textContent =
        message;

}


/* ============================================================
   START
============================================================ */

createBarometerScale();

createGaugeNumbers();

</script>

</body>

</html>
"""


components.html(
    virtual_lab,
    height=1700,
    scrolling=True
)
