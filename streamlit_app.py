import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# STREAMLIT PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Pressure Measurement Virtual Lab",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Pressure Measurement Virtual Lab")

st.write(
    """
    Perform the pressure measurement experiment by interacting
    with the virtual laboratory equipment.

    **Measure first, record your observations, then calculate.**
    """
)


# ============================================================
# VIRTUAL LAB
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

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #eef2f5;

    color: #1f2937;
}


.lab-app {
    max-width: 1250px;

    margin: auto;

    padding: 5px;
}


/* ============================================================
   PROCEDURE / STATUS
============================================================ */

.procedure-panel {
    background: white;

    border-left:
        7px solid #0284c7;

    border-radius: 10px;

    padding: 18px 20px;

    margin-bottom: 18px;

    box-shadow:
        0 3px 10px
        rgba(0, 0, 0, 0.12);
}


.procedure-title {
    font-weight: bold;

    color: #075985;

    margin-bottom: 6px;
}


#instruction {
    font-size: 16px;
}


/* ============================================================
   LAB ROOM
============================================================ */

.lab-room {
    position: relative;

    height: 730px;

    overflow: hidden;

    border:
        4px solid #475569;

    border-radius: 18px;

    background:
        linear-gradient(
            to bottom,
            #e7edf1 0%,
            #e7edf1 67%,
            #ad8059 67%,
            #895f40 100%
        );

    box-shadow:
        inset 0 0 35px
        rgba(0, 0, 0, 0.13);
}


.lab-room::after {
    content: "";

    position: absolute;

    left: 0;
    right: 0;

    top: 67%;

    height: 10px;

    background: #475569;
}


/* ============================================================
   EQUIPMENT SHELF
============================================================ */

.equipment-shelf {
    position: absolute;

    left: 20px;
    top: 25px;

    width: 270px;
    height: 620px;

    padding: 14px;

    background:
        linear-gradient(
            #d1d5db,
            #9ca3af
        );

    border:
        6px solid #475569;

    border-radius: 12px;

    box-shadow:
        inset 0 0 15px
        rgba(0, 0, 0, 0.25);
}


.shelf-title {
    text-align: center;

    font-size: 18px;

    font-weight: bold;

    margin-bottom: 10px;
}


.shelf-divider {
    height: 5px;

    margin:
        18px -14px;

    background: #64748b;
}


/* ============================================================
   BAROMETER
============================================================ */

.barometer {
    position: relative;

    width: 180px;
    height: 300px;

    margin: auto;

    cursor: grab;

    user-select: none;
}


.barometer:active {
    cursor: grabbing;
}


.baro-body {
    position: absolute;

    left: 5px;
    top: 0;

    width: 170px;
    height: 290px;

    border:
        5px solid #374151;

    border-radius: 16px;

    background:
        linear-gradient(
            90deg,
            #94a3b8,
            #f8fafc 35%,
            #d1d5db 65%,
            #94a3b8
        );

    box-shadow:
        0 6px 12px
        rgba(0, 0, 0, 0.25),

        inset 0 0 12px
        rgba(0, 0, 0, 0.2);
}


.baro-title {
    position: absolute;

    top: 7px;

    width: 100%;

    text-align: center;

    font-size: 11px;

    font-weight: bold;
}


#baroScale {
    position: absolute;

    left: 15px;
    top: 40px;

    width: 75px;
    height: 215px;
}


.scale-mark {
    position: absolute;

    right: 0;

    width: 20px;

    border-top:
        1px solid #111827;
}


.scale-mark.major {
    width: 32px;

    border-top:
        2px solid #111827;
}


.scale-number {
    position: absolute;

    right: 39px;

    transform:
        translateY(-50%);

    font-size: 10px;

    font-weight: bold;
}


.baro-glass {
    position: absolute;

    left: 102px;
    top: 39px;

    width: 32px;
    height: 216px;

    overflow: hidden;

    border:
        3px solid #64748b;

    border-radius:
        15px 15px 5px 5px;

    background:
        linear-gradient(
            90deg,
            rgba(255,255,255,0.85),
            rgba(186,230,253,0.25),
            rgba(255,255,255,0.90)
        );
}


/*
IMPORTANT:

The mercury is invisible at the beginning.
It becomes visible only after the barometer
is placed at the atmospheric station.
*/

#mercury {
    position: absolute;

    bottom: 0;

    width: 100%;

    height: 2%;

    opacity: 0;

    background:
        linear-gradient(
            90deg,
            #334155,
            #d1d5db,
            #475569
        );

    transition:
        height 1.3s ease,
        opacity 0.4s ease;
}


#mercury::before {
    content: "";

    position: absolute;

    left: 0;
    top: -4px;

    width: 100%;
    height: 8px;

    border-radius: 50%;

    background: #94a3b8;
}


.baro-reservoir {
    position: absolute;

    left: 90px;
    top: 245px;

    width: 57px;
    height: 34px;

    border-radius: 50%;

    border:
        3px solid #475569;

    background:
        linear-gradient(
            #cbd5e1,
            #475569
        );
}


/* Cover shown while barometer is inactive */

.instrument-cover {
    position: absolute;

    inset: 0;

    z-index: 10;

    display: flex;

    align-items: center;

    justify-content: center;

    text-align: center;

    padding: 15px;

    border-radius: 12px;

    color: white;

    font-size: 13px;

    font-weight: bold;

    background:
        rgba(15, 23, 42, 0.76);

    pointer-events: none;

    transition:
        opacity 0.4s ease;
}


.instrument-cover.hidden {
    opacity: 0;
}


/* ============================================================
   ATMOSPHERIC MEASUREMENT STATION
============================================================ */

.atmosphere-station {
    position: absolute;

    left: 325px;
    top: 50px;

    width: 305px;
    height: 365px;

    border:
        4px dashed #0284c7;

    border-radius: 18px;

    background:
        rgba(224,242,254,0.70);

    transition: 0.2s;
}


.atmosphere-station.drag-over {
    border-color: #0369a1;

    background:
        rgba(186,230,253,0.95);
}


.atmosphere-station.active {
    border-style: solid;

    border-color: #16a34a;

    background:
        rgba(240,253,244,0.85);
}


.station-heading {
    text-align: center;

    margin-top: 12px;

    color: #075985;

    font-weight: bold;
}


.station-note {
    text-align: center;

    margin-top: 5px;

    color: #475569;

    font-size: 13px;
}


/* ============================================================
   PRESSURE GAUGE
============================================================ */

.gauge {
    position: relative;

    width: 185px;
    height: 235px;

    margin: auto;

    cursor: grab;

    user-select: none;
}


.gauge:active {
    cursor: grabbing;
}


.gauge-face {
    position: absolute;

    left: 8px;
    top: 0;

    width: 170px;
    height: 170px;

    border-radius: 50%;

    border:
        10px solid #475569;

    background:
        radial-gradient(
            circle at 35% 25%,
            #ffffff,
            #f8fafc 58%,
            #d1d5db 100%
        );

    box-shadow:
        0 5px 12px
        rgba(0, 0, 0, 0.28),

        inset 0 0 14px
        rgba(0, 0, 0, 0.16);
}


.gauge-number {
    position: absolute;

    font-size: 10px;

    font-weight: bold;
}


/*
Needle starts at zero.

The needle itself points vertically upward before
rotation.

rotate(-135deg) corresponds to the 0-kPa position.
*/

#needleAssembly {
    position: absolute;

    left: 75px;
    top: 75px;

    width: 0;
    height: 0;

    transform:
        rotate(-135deg);

    transition:
        transform 1.3s
        cubic-bezier(.25,.8,.25,1);
}


.gauge-needle {
    position: absolute;

    left: -2px;
    top: -58px;

    width: 4px;
    height: 58px;

    border-radius: 4px;

    background: #dc2626;
}


.gauge-hub {
    position: absolute;

    left: 67px;
    top: 67px;

    width: 16px;
    height: 16px;

    border-radius: 50%;

    background: #111827;
}


.gauge-unit {
    position: absolute;

    left: 0;
    right: 0;

    top: 105px;

    text-align: center;

    font-size: 11px;

    font-weight: bold;
}


.gauge-stem {
    position: absolute;

    left: 79px;
    top: 170px;

    width: 28px;
    height: 36px;

    border:
        3px solid #6b4219;

    background:
        linear-gradient(
            90deg,
            #8c5a20,
            #e5b864,
            #8c5a20
        );
}


.gauge-fitting {
    position: absolute;

    left: 67px;
    top: 201px;

    width: 52px;
    height: 24px;

    border:
        3px solid #6b4219;

    border-radius: 5px;

    background:
        linear-gradient(
            #b7792d,
            #e5b864,
            #8a551c
        );
}


/* ============================================================
   PRESSURE VESSEL
============================================================ */

.pressure-system {
    position: absolute;

    right: 10px;
    top: 35px;

    width: 555px;
    height: 550px;
}


.pressure-heading {
    text-align: center;

    font-weight: bold;

    color: #334155;
}


.vessel {
    position: absolute;

    left: 85px;
    top: 180px;

    width: 300px;
    height: 190px;

    border:
        6px solid #475569;

    border-radius: 70px;

    background:
        linear-gradient(
            180deg,
            #e5e7eb 0%,
            #aeb8c4 35%,
            #7d8996 62%,
            #cbd5e1 100%
        );

    box-shadow:
        inset 0 13px 22px
        rgba(255,255,255,0.45),

        inset 0 -12px 20px
        rgba(0,0,0,0.18),

        0 8px 14px
        rgba(0,0,0,0.22);
}


.vessel-label {
    position: absolute;

    width: 100%;

    top: 77px;

    text-align: center;

    font-weight: bold;

    color: #334155;
}


.vessel-leg {
    position: absolute;

    bottom: -60px;

    width: 30px;
    height: 65px;

    background: #475569;
}


.vessel-leg.left {
    left: 60px;
}


.vessel-leg.right {
    right: 60px;
}


/* Test port */

.test-port {
    position: absolute;

    right: -34px;
    top: 70px;

    width: 38px;
    height: 48px;

    border:
        3px solid #6b4219;

    background:
        linear-gradient(
            90deg,
            #8a561f,
            #f0c46c,
            #85511d
        );
}


.test-port::after {
    content: "";

    position: absolute;

    right: -20px;
    top: 9px;

    width: 21px;
    height: 24px;

    border-radius:
        0 7px 7px 0;

    background: #111827;
}


/* Gauge drop area */

#portZone {
    position: absolute;

    left: 345px;
    top: 165px;

    width: 190px;
    height: 190px;

    border:
        3px dashed transparent;

    border-radius: 20px;

    transition: 0.2s;
}


#portZone.drag-over {
    border-color: #0284c7;

    background:
        rgba(224,242,254,0.50);
}


/* ============================================================
   CONNECTED GAUGE
============================================================ */

.connected-gauge {
    position: absolute !important;

    left: 355px !important;
    top: 0 !important;

    margin: 0 !important;

    transform:
        scale(0.88);

    cursor: default;
}


/* ============================================================
   HOSE
============================================================ */

#hose {
    display: none;

    position: absolute;

    left: 375px;
    top: 120px;

    width: 90px;
    height: 150px;

    border-right:
        11px solid #1f2937;

    border-bottom:
        11px solid #1f2937;

    border-radius:
        0 0 55px 0;

    z-index: 5;
}


#hose.visible {
    display: block;
}


/* ============================================================
   VALVE
============================================================ */

#valveControl {
    display: none;

    position: absolute;

    left: 415px;
    top: 300px;

    text-align: center;
}


#valveControl.visible {
    display: block;
}


.valve {
    position: relative;

    width: 82px;
    height: 82px;

    margin: auto;

    border:
        7px solid #6b4219;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #efc266,
            #97621f
        );

    cursor: pointer;

    box-shadow:
        0 4px 10px
        rgba(0,0,0,0.25);
}


#valveHandle {
    position: absolute;

    left: 5px;
    top: 29px;

    width: 58px;
    height: 11px;

    border-radius: 7px;

    background: #b91c1c;

    transition:
        transform 0.8s ease;
}


#valveHandle.open {
    transform:
        rotate(90deg);
}


#valveStatus {
    margin-top: 6px;

    font-size: 12px;

    font-weight: bold;
}


/* ============================================================
   STUDENT TASKS
============================================================ */

.tasks {
    margin-top: 20px;
}


.task {
    display: none;

    margin-bottom: 18px;

    padding: 22px;

    background: white;

    border-radius: 12px;

    border-left:
        7px solid #0284c7;

    box-shadow:
        0 3px 10px
        rgba(0,0,0,0.10);
}


.task.active {
    display: block;
}


.task h3 {
    margin-top: 0;

    color: #075985;
}


.input-row {
    display: flex;

    align-items: center;

    flex-wrap: wrap;

    gap: 9px;
}


input {
    width: 190px;

    padding: 11px;

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
        11px 16px;

    border: none;

    border-radius: 7px;

    background: #0284c7;

    color: white;

    cursor: pointer;

    font-size: 15px;
}


button:hover {
    background: #0369a1;
}


.feedback {
    margin-top: 12px;

    padding: 11px;

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
   COMPLETE
============================================================ */

#complete {
    display: none;

    padding: 26px;

    text-align: center;

    border:
        3px solid #16a34a;

    border-radius: 13px;

    background: #f0fdf4;
}


#complete.visible {
    display: block;
}


@media (max-width: 1050px) {

    .lab-room {
        height: 1350px;
    }

}

</style>

</head>


<body>

<div class="lab-app">


<!-- ============================================================
     PROCEDURE
============================================================ -->

<div class="procedure-panel">

    <div class="procedure-title">
        Current Laboratory Procedure
    </div>

    <div id="instruction">
        Step 1 — Drag the mercury barometer from the equipment
        shelf to the atmospheric measurement station.
    </div>

</div>


<!-- ============================================================
     LAB ROOM
============================================================ -->

<div class="lab-room">


<!-- ============================================================
     EQUIPMENT SHELF
============================================================ -->

<div class="equipment-shelf">

<div class="shelf-title">
Equipment Shelf
</div>


<!-- BAROMETER -->

<div
    id="barometer"
    class="barometer"
    draggable="true"
>

<div class="baro-body">

    <div class="baro-title">
        MERCURY BAROMETER
    </div>


    <div id="baroScale">
    </div>


    <div class="baro-glass">

        <div id="mercury">
        </div>

    </div>


    <div class="baro-reservoir">
    </div>


    <div
        id="barometerCover"
        class="instrument-cover"
    >
        Instrument inactive
        <br><br>
        Place at atmospheric measurement station
    </div>

</div>

</div>


<div class="shelf-divider">
</div>


<!-- PRESSURE GAUGE -->

<div
    id="gauge"
    class="gauge"
    draggable="true"
>

<div class="gauge-face">

    <div id="gaugeNumbers">
    </div>


    <!-- Needle always begins at ZERO -->

    <div id="needleAssembly">

        <div class="gauge-needle">
        </div>

    </div>


    <div class="gauge-hub">
    </div>


    <div class="gauge-unit">
        kPa
    </div>

</div>


<div class="gauge-stem">
</div>


<div class="gauge-fitting">
</div>

</div>

</div>


<!-- ============================================================
     ATMOSPHERIC STATION
============================================================ -->

<div
    id="atmosphereStation"
    class="atmosphere-station"
>

<div class="station-heading">
Atmospheric Measurement Station
</div>

<div class="station-note">
Drag the mercury barometer into this area.
</div>

</div>


<!-- ============================================================
     PRESSURE SYSTEM
============================================================ -->

<div class="pressure-system">


<div class="pressure-heading">
Pressure Vessel Test Rig
</div>


<div class="vessel">

    <div class="vessel-label">
        PRESSURE VESSEL
    </div>


    <div class="vessel-leg left">
    </div>


    <div class="vessel-leg right">
    </div>


    <div class="test-port">
    </div>

</div>


<div id="portZone">
</div>


<div id="hose">
</div>


<div id="valveControl">

    <div
        class="valve"
        onclick="openValve()"
    >

        <div id="valveHandle">
        </div>

    </div>


    <div id="valveStatus">
        CLOSED
    </div>

</div>

</div>

</div>


<!-- ============================================================
     STUDENT TASKS
============================================================ -->

<div class="tasks">


<!-- BAROMETER READING -->

<div
    id="barometerTask"
    class="task"
>

<h3>
Step 2 — Record the Barometer Measurement
</h3>

<p>
Read the mercury level directly from the instrument scale.
</p>


<div class="input-row">

<input
    id="barometerInput"
    type="number"
    placeholder="Enter reading"
>

<span>
mmHg
</span>


<button onclick="checkBarometer()">
Record Reading
</button>

</div>


<div id="barometerFeedback">
</div>

</div>


<!-- ATMOSPHERIC PRESSURE -->

<div
    id="atmosphereTask"
    class="task"
>

<h3>
Step 3 — Calculate Atmospheric Pressure
</h3>

<p>
Use the barometer reading that you recorded.
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


<div class="input-row">

<input
    id="atmosphereInput"
    type="number"
    step="0.01"
    placeholder="Enter pressure"
>

<span>
kPa
</span>


<button onclick="checkAtmosphere()">
Check Calculation
</button>

</div>


<div id="atmosphereFeedback">
</div>

</div>


<!-- GAUGE READING -->

<div
    id="gaugeTask"
    class="task"
>

<h3>
Step 6 — Record Gauge Pressure
</h3>

<p>
Read the position of the red pressure-gauge needle.
</p>


<div class="input-row">

<input
    id="gaugeInput"
    type="number"
    placeholder="Enter reading"
>

<span>
kPa
</span>


<button onclick="checkGauge()">
Record Reading
</button>

</div>


<div id="gaugeFeedback">
</div>

</div>


<!-- ABSOLUTE PRESSURE -->

<div
    id="absoluteTask"
    class="task"
>

<h3>
Step 7 — Calculate Absolute Pressure
</h3>


<p>
<strong>
P<sub>abs</sub>
=
P<sub>gauge</sub>
+
P<sub>atm</sub>
</strong>
</p>


<div class="input-row">

<input
    id="absoluteInput"
    type="number"
    step="0.01"
    placeholder="Enter pressure"
>

<span>
kPa
</span>


<button onclick="checkAbsolute()">
Submit Result
</button>

</div>


<div id="absoluteFeedback">
</div>

</div>


<!-- COMPLETE -->

<div id="complete">

<h2>
🎉 Experiment Complete
</h2>


<p>
Your final result is within the required ±5% error.
</p>


<button onclick="location.reload()">
Start New Experiment
</button>

</div>


</div>

</div>


<script>


/* ============================================================
   EXPERIMENT CONSTANTS
============================================================ */

const rhoHg = 13600;

const gravity = 9.81;


/* Random possible barometer readings */

const barometerChoices = [
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


/* Random gauge pressures */

const gaugeChoices = [
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
    barometerChoices[
        Math.floor(
            Math.random()
            *
            barometerChoices.length
        )
    ];


const gaugeValue =
    gaugeChoices[
        Math.floor(
            Math.random()
            *
            gaugeChoices.length
        )
    ];


/* Atmospheric pressure */

const atmosphericPressure =
    rhoHg
    *
    gravity
    *
    (
        barometerValue
        /
        1000
    )
    /
    1000;


/* Absolute pressure */

const absolutePressure =
    atmosphericPressure
    +
    gaugeValue;


/* Student progress */

let atmosphericComplete = false;

let gaugeConnected = false;

let valveOpened = false;


/* ============================================================
   BAROMETER SCALE
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

        const position =
            (
                (value - 720)
                /
                60
            )
            *
            100;


        const mark =
            document.createElement(
                "div"
            );


        mark.className =
            "scale-mark";


        if (
            value % 10 === 0
        ) {

            mark.classList.add(
                "major"
            );

        }


        mark.style.bottom =
            position
            +
            "%";


        scale.appendChild(
            mark
        );


        if (
            value % 10 === 0
        ) {

            const number =
                document.createElement(
                    "div"
                );


            number.className =
                "scale-number";


            number.textContent =
                value;


            number.style.bottom =
                position
                +
                "%";


            scale.appendChild(
                number
            );

        }

    }

}


/* ============================================================
   PRESSURE GAUGE NUMBERS
============================================================ */

function createGaugeNumbers() {

    const parent =
        document.getElementById(
            "gaugeNumbers"
        );


    parent.innerHTML = "";


    const centerX = 75;

    const centerY = 75;

    const radius = 56;


    /*
    Gauge geometry:

    0 kPa   = bottom-left
    50 kPa  = top
    100 kPa = bottom-right
    */


    for (
        let value = 0;
        value <= 100;
        value += 20
    ) {

        const dialAngle =
            135
            +
            (
                value
                /
                100
            )
            *
            270;


        const radians =
            dialAngle
            *
            Math.PI
            /
            180;


        const x =
            centerX
            +
            radius
            *
            Math.cos(
                radians
            );


        const y =
            centerY
            +
            radius
            *
            Math.sin(
                radians
            );


        const label =
            document.createElement(
                "div"
            );


        label.className =
            "gauge-number";


        label.textContent =
            value;


        label.style.left =
            x
            +
            "px";


        label.style.top =
            y
            +
            "px";


        label.style.transform =
            "translate(-50%, -50%)";


        parent.appendChild(
            label
        );

    }

}


/* ============================================================
   RESET GAUGE TO ZERO
============================================================ */

function resetGaugeToZero() {

    /*
    This is the most important correction.

    The gauge stays exactly at ZERO:
    - when experiment begins
    - while sitting on shelf
    - after connecting to the vessel
    - while the valve is CLOSED
    */

    const needle =
        document.getElementById(
            "needleAssembly"
        );


    needle.style.transform =
        "rotate(-135deg)";

}


/* ============================================================
   INITIAL EQUIPMENT STATE
============================================================ */

function initializeEquipment() {

    /* BAROMETER */

    const mercury =
        document.getElementById(
            "mercury"
        );


    mercury.style.opacity =
        "0";


    mercury.style.height =
        "2%";


    /* PRESSURE GAUGE */

    resetGaugeToZero();

}


/* ============================================================
   SET STATUS MESSAGE
============================================================ */

function setInstruction(message) {

    document.getElementById(
        "instruction"
    ).textContent =
        message;

}


/* ============================================================
   BAROMETER DRAG
============================================================ */

const barometer =
    document.getElementById(
        "barometer"
    );


barometer.addEventListener(
    "dragstart",
    event => {

        event.dataTransfer.setData(
            "equipment",
            "barometer"
        );

    }
);


/* ============================================================
   ATMOSPHERE STATION DROP
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
                "equipment"
            );


        if (
            equipment !== "barometer"
        ) {

            alert(
                "Place the mercury barometer at this station."
            );

            return;

        }


        atmosphereStation.appendChild(
            barometer
        );


        barometer.draggable =
            false;


        barometer.style.position =
            "absolute";


        barometer.style.left =
            "60px";


        barometer.style.top =
            "47px";


        barometer.style.margin =
            "0";


        atmosphereStation.classList.add(
            "active"
        );


        /* Remove inactive cover */

        document.getElementById(
            "barometerCover"
        ).classList.add(
            "hidden"
        );


        /*
        Now activate the mercury column.
        */


        const mercuryPercent =
            (
                (
                    barometerValue
                    -
                    720
                )
                /
                60
            )
            *
            100;


        const mercury =
            document.getElementById(
                "mercury"
            );


        mercury.style.opacity =
            "1";


        /*
        Small delay creates the realistic
        settling animation.
        */

        setTimeout(
            () => {

                mercury.style.height =
                    mercuryPercent
                    +
                    "%";

            },
            250
        );


        /*
        Input box appears AFTER reading settles.
        */

        setTimeout(
            () => {

                document.getElementById(
                    "barometerTask"
                ).classList.add(
                    "active"
                );


                setInstruction(
                    "Step 2 — Read the mercury level and record the barometer measurement."
                );

            },
            1500
        );

    }
);


/* ============================================================
   CHECK BAROMETER READING
============================================================ */

function checkBarometer() {

    const raw =
        document.getElementById(
            "barometerInput"
        ).value;


    const answer =
        parseFloat(raw);


    const feedback =
        document.getElementById(
            "barometerFeedback"
        );


    if (
        Number.isNaN(answer)
    ) {

        feedbackMessage(
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

        feedbackMessage(
            feedback,
            "✓ Barometer measurement recorded.",
            true
        );


        document.getElementById(
            "atmosphereTask"
        ).classList.add(
            "active"
        );


        setInstruction(
            "Step 3 — Calculate atmospheric pressure using your measured barometer height."
        );

    }

    else {

        feedbackMessage(
            feedback,
            "Recheck the top of the mercury column and the instrument scale.",
            false
        );

    }

}


/* ============================================================
   CHECK ATMOSPHERIC PRESSURE
============================================================ */

function checkAtmosphere() {

    const raw =
        document.getElementById(
            "atmosphereInput"
        ).value;


    const answer =
        parseFloat(raw);


    const feedback =
        document.getElementById(
            "atmosphereFeedback"
        );


    if (
        Number.isNaN(answer)
    ) {

        feedbackMessage(
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

        atmosphericComplete =
            true;


        feedbackMessage(
            feedback,
            "✓ Atmospheric pressure accepted. Error is within ±5%.",
            true
        );


        setInstruction(
            "Step 4 — Drag the pressure gauge from the equipment shelf to the vessel test port."
        );

    }

    else {

        feedbackMessage(
            feedback,
            "Result is outside ±5%. Check your units and P = ρgh.",
            false
        );

    }

}


/* ============================================================
   PRESSURE GAUGE DRAG
============================================================ */

const gauge =
    document.getElementById(
        "gauge"
    );


gauge.addEventListener(
    "dragstart",
    event => {

        event.dataTransfer.setData(
            "equipment",
            "gauge"
        );

    }
);


/* ============================================================
   PRESSURE GAUGE DROP ON TEST PORT
============================================================ */

const portZone =
    document.getElementById(
        "portZone"
    );


portZone.addEventListener(
    "dragover",
    event => {

        event.preventDefault();


        portZone.classList.add(
            "drag-over"
        );

    }
);


portZone.addEventListener(
    "dragleave",
    () => {

        portZone.classList.remove(
            "drag-over"
        );

    }
);


portZone.addEventListener(
    "drop",
    event => {

        event.preventDefault();


        portZone.classList.remove(
            "drag-over"
        );


        const equipment =
            event.dataTransfer.getData(
                "equipment"
            );


        if (
            equipment !== "gauge"
        ) {

            return;

        }


        if (
            !atmosphericComplete
        ) {

            alert(
                "Complete the atmospheric-pressure measurement first."
            );

            return;

        }


        document.querySelector(
            ".pressure-system"
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
            "visible"
        );


        document.getElementById(
            "valveControl"
        ).classList.add(
            "visible"
        );


        gaugeConnected =
            true;


        /*
        CRITICAL:

        Gauge is now connected,
        but valve is CLOSED.

        Therefore pressure gauge MUST STILL READ ZERO.
        */

        resetGaugeToZero();


        setInstruction(
            "Step 5 — Pressure gauge connected. The valve is CLOSED and the gauge remains at 0 kPa. Open the test-port valve."
        );

    }
);


/* ============================================================
   OPEN VALVE
============================================================ */

function openValve() {

    if (
        !gaugeConnected
        ||
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
        "valveStatus"
    ).textContent =
        "OPEN";


    /*
    Convert actual gauge pressure
    to gauge-needle rotation.

    0 kPa   = -135 degrees
    50 kPa  =   0 degrees
    100 kPa = +135 degrees
    */

    const gaugeRotation =
        -135
        +
        (
            gaugeValue
            /
            100
        )
        *
        270;


    /*
    Gauge stays at zero briefly,
    then pressure reaches instrument.
    */

    setTimeout(
        () => {

            document.getElementById(
                "needleAssembly"
            ).style.transform =
                "rotate("
                +
                gaugeRotation
                +
                "deg)";

        },
        400
    );


    /*
    Input only appears after
    needle finishes moving.
    */

    setTimeout(
        () => {

            document.getElementById(
                "gaugeTask"
            ).classList.add(
                "active"
            );


            setInstruction(
                "Step 6 — The valve is OPEN. Read the pressure gauge and record the measurement."
            );

        },
        1800
    );

}


/* ============================================================
   CHECK GAUGE
============================================================ */

function checkGauge() {

    const raw =
        document.getElementById(
            "gaugeInput"
        ).value;


    const answer =
        parseFloat(raw);


    const feedback =
        document.getElementById(
            "gaugeFeedback"
        );


    if (
        Number.isNaN(answer)
    ) {

        feedbackMessage(
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
            gaugeValue
        )
        <=
        2.5
    ) {

        feedbackMessage(
            feedback,
            "✓ Gauge pressure measurement recorded.",
            true
        );


        document.getElementById(
            "absoluteTask"
        ).classList.add(
            "active"
        );


        setInstruction(
            "Step 7 — Calculate absolute pressure using your atmospheric pressure and gauge pressure measurements."
        );

    }

    else {

        feedbackMessage(
            feedback,
            "Recheck the position of the red pressure-gauge needle.",
            false
        );

    }

}


/* ============================================================
   CHECK ABSOLUTE PRESSURE
============================================================ */

function checkAbsolute() {

    const raw =
        document.getElementById(
            "absoluteInput"
        ).value;


    const answer =
        parseFloat(raw);


    const feedback =
        document.getElementById(
            "absoluteFeedback"
        );


    if (
        Number.isNaN(answer)
    ) {

        feedbackMessage(
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

        feedbackMessage(
            feedback,
            "✓ Absolute pressure accepted.",
            true
        );


        document.getElementById(
            "complete"
        ).classList.add(
            "visible"
        );


        setInstruction(
            "Experiment complete — your final result is within ±5%."
        );

    }

    else {

        feedbackMessage(
            feedback,
            "Result is outside ±5%. Recheck Pabs = Pgauge + Patm.",
            false
        );

    }

}


/* ============================================================
   FEEDBACK
============================================================ */

function feedbackMessage(
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

initializeEquipment();

</script>

</body>

</html>
"""


components.html(
    virtual_lab,
    height=1800,
    scrolling=True
)
