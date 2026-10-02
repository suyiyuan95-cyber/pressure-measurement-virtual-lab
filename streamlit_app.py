import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Pressure Measurement Virtual Lab",
    page_icon="💧",
    layout="wide"
)


st.title("💧 Pressure Measurement Virtual Lab")

st.write(
    """
    Perform the experiment by interacting with the
    virtual laboratory equipment.

    **Do not calculate anything until you have taken
    the required measurement.**
    """
)


virtual_lab = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

/* ============================================================
   GENERAL PAGE
============================================================ */

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #edf2f5;
    color: #1f2937;
}


#labApp {
    max-width: 1250px;
    margin: auto;
}


/* ============================================================
   PROCEDURE PANEL
============================================================ */

.procedure {
    background: white;

    border-left: 7px solid #0284c7;

    padding: 18px;

    margin-bottom: 18px;

    border-radius: 10px;

    box-shadow:
        0 3px 10px rgba(0,0,0,0.12);
}


.procedure strong {
    color: #075985;
}


/* ============================================================
   LAB ROOM
============================================================ */

.lab-room {

    position: relative;

    height: 720px;

    overflow: hidden;

    border: 4px solid #475569;

    border-radius: 18px;

    background:
        linear-gradient(
            to bottom,
            #e8eef2 0%,
            #e8eef2 68%,
            #a87850 68%,
            #8d603e 100%
        );

    box-shadow:
        inset 0 0 35px rgba(0,0,0,.13);
}


/* lab bench edge */

.lab-room::after {

    content: "";

    position: absolute;

    left: 0;
    right: 0;

    top: 68%;

    height: 10px;

    background: #4b5563;
}


/* ============================================================
   EQUIPMENT CABINET
============================================================ */

.shelf {

    position: absolute;

    left: 22px;
    top: 28px;

    width: 270px;
    height: 610px;

    padding: 15px;

    background:
        linear-gradient(
            #d1d5db,
            #9ca3af
        );

    border: 6px solid #475569;

    border-radius: 12px;

    box-shadow:
        inset 0 0 15px rgba(0,0,0,.25);
}


.shelf-title {

    text-align: center;

    font-weight: bold;

    font-size: 18px;

    margin-bottom: 15px;
}


.shelf-divider {

    height: 5px;

    background: #64748b;

    margin: 20px -15px;
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


/* metal backing */

.baro-body {

    position: absolute;

    left: 5px;
    top: 0;

    width: 170px;
    height: 290px;

    border-radius: 16px;

    border: 5px solid #374151;

    background:
        linear-gradient(
            90deg,
            #94a3b8,
            #f8fafc 35%,
            #d1d5db 65%,
            #94a3b8
        );

    box-shadow:
        0 6px 12px rgba(0,0,0,.25),
        inset 0 0 12px rgba(0,0,0,.2);
}


.baro-title {

    position: absolute;

    top: 7px;

    width: 100%;

    text-align: center;

    font-size: 11px;

    font-weight: bold;
}


/* measuring scale */

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

    border-top: 1px solid #111827;
}


.scale-mark.major {

    width: 32px;

    border-top: 2px solid #111827;
}


.scale-number {

    position: absolute;

    right: 39px;

    transform: translateY(-50%);

    font-size: 10px;

    font-weight: bold;
}


/* glass tube */

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
            rgba(255,255,255,.85),
            rgba(186,230,253,.25),
            rgba(255,255,255,.9)
        );
}


/* mercury column */

#mercury {

    position: absolute;

    bottom: 0;

    width: 100%;

    height: 4%;

    opacity: 0;

    background:

        linear-gradient(
            90deg,
            #334155,
            #cbd5e1,
            #475569
        );

    transition:
        height 1.4s ease,
        opacity .5s ease;
}


/* mercury meniscus */

#mercury::before {

    content: "";

    position: absolute;

    top: -4px;

    left: 0;

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

    border: 3px solid #475569;

    background:
        linear-gradient(
            #cbd5e1,
            #475569
        );
}


/* inactive equipment cover */

.instrument-cover {

    position: absolute;

    inset: 0;

    z-index: 10;

    display: flex;

    align-items: center;

    justify-content: center;

    text-align: center;

    padding: 10px;

    font-weight: bold;

    color: white;

    border-radius: 15px;

    background:
        rgba(15,23,42,.76);

    pointer-events: none;

    transition: opacity .5s;
}


.instrument-cover.hidden {

    opacity: 0;
}


/* ============================================================
   ATMOSPHERIC STATION
============================================================ */

.atmosphere-station {

    position: absolute;

    left: 335px;
    top: 55px;

    width: 300px;
    height: 360px;

    border:

        4px dashed #0284c7;

    border-radius: 18px;

    background:
        rgba(224,242,254,.7);

    transition: .2s;
}


.atmosphere-station.dragging-over {

    background:
        rgba(186,230,253,.95);

    border-color: #0369a1;
}


.atmosphere-station.active {

    border-style: solid;

    border-color: #16a34a;

    background:
        rgba(240,253,244,.85);
}


.station-heading {

    text-align: center;

    color: #075985;

    font-weight: bold;

    margin-top: 12px;
}


.station-note {

    text-align: center;

    font-size: 13px;

    color: #475569;
}


/* ============================================================
   PRESSURE GAUGE
============================================================ */

.gauge {

    position: relative;

    width: 185px;
    height: 240px;

    margin: auto;

    cursor: grab;

    user-select: none;
}


.gauge-face {

    position: absolute;

    left: 8px;
    top: 0;

    width: 170px;
    height: 170px;

    border-radius: 50%;

    border: 10px solid #475569;

    background:
        radial-gradient(
            circle at 35% 25%,
            white,
            #f8fafc 55%,
            #d1d5db 100%
        );

    box-shadow:
        0 5px 12px rgba(0,0,0,.28),
        inset 0 0 14px rgba(0,0,0,.16);
}


.gauge-number {

    position: absolute;

    font-size: 10px;

    font-weight: bold;
}


/* gauge needle */

#needleAssembly {

    position: absolute;

    left: 75px;
    top: 75px;

    width: 0;
    height: 0;

    transform: rotate(-135deg);

    transition:

        transform 1.2s cubic-bezier(.25,.8,.25,1);
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

    border: 3px solid #6b4219;

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

    border: 3px solid #6b4219;

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

    right: 15px;
    top: 40px;

    width: 545px;
    height: 530px;
}


.pressure-heading {

    text-align: center;

    font-weight: bold;

    color: #334155;
}


.vessel {

    position: absolute;

    left: 80px;
    top: 175px;

    width: 300px;
    height: 190px;

    border-radius: 70px;

    border: 6px solid #475569;

    background:
        linear-gradient(
            180deg,
            #e5e7eb 0%,
            #aeb8c4 35%,
            #7d8996 62%,
            #cbd5e1 100%
        );

    box-shadow:
        inset 0 13px 22px rgba(255,255,255,.45),
        inset 0 -12px 20px rgba(0,0,0,.18),
        0 8px 14px rgba(0,0,0,.22);
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


/* test port */

.test-port {

    position: absolute;

    right: -34px;
    top: 70px;

    width: 38px;
    height: 48px;

    border: 3px solid #6b4219;

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


#portZone {

    position: absolute;

    left: 340px;
    top: 170px;

    width: 180px;
    height: 180px;

    border-radius: 20px;

    border:

        3px dashed transparent;
}


#portZone.dragging-over {

    border-color: #0284c7;

    background:
        rgba(224,242,254,.45);
}


/* ============================================================
   CONNECTED GAUGE
============================================================ */

.connected-gauge {

    position: absolute !important;

    left: 345px !important;
    top: 5px !important;

    margin: 0 !important;

    transform: scale(.88);

    cursor: default;
}


/* ============================================================
   FLEXIBLE HOSE
============================================================ */

#hose {

    display: none;

    position: absolute;

    left: 367px;
    top: 125px;

    width: 90px;
    height: 145px;

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

    left: 407px;
    top: 292px;

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

    border-radius: 50%;

    border: 7px solid #6b4219;

    background:
        radial-gradient(
            circle,
            #efc266,
            #97621f
        );

    cursor: pointer;

    box-shadow:
        0 4px 10px rgba(0,0,0,.25);
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
        transform .8s ease;
}


#valveHandle.open {

    transform: rotate(90deg);
}


#valveStatus {

    margin-top: 6px;

    font-size: 12px;

    font-weight: bold;
}


/* ============================================================
   TASK CARDS
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
        0 3px 10px rgba(0,0,0,.1);
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

</style>

</head>


<body>

<div id="labApp">


<!-- PROCEDURE -->

<div class="procedure">

<strong>
Current procedure:
</strong>

<span id="instruction">

Drag the mercury barometer from the equipment shelf
to the atmospheric measurement station.

</span>

</div>



<!-- LAB ROOM -->

<div class="lab-room">


<!-- EQUIPMENT SHELF -->

<div class="shelf">

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

Instrument not positioned
for measurement

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



<!-- ATMOSPHERIC STATION -->

<div
    id="atmosphereStation"
    class="atmosphere-station"
>

<div class="station-heading">

Atmospheric Measurement Station

</div>


<div class="station-note">

Place the mercury barometer inside this area.

</div>

</div>



<!-- PRESSURE SYSTEM -->

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
Record Barometer Measurement
</h3>

<p>

Read the mercury level directly from the instrument.

</p>


<div class="input-row">

<input
    id="barometerInput"
    type="number"
    placeholder="Enter measurement"
>

<span>
mmHg
</span>


<button onclick="checkBarometer()">

Record

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
Calculate Atmospheric Pressure
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

ρ<sub>Hg</sub>
=
13,600 kg/m³

<br>

g
=
9.81 m/s²

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

Check

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
Record Gauge Pressure
</h3>

<p>

Read the position of the red needle.

</p>


<div class="input-row">

<input
    id="gaugeInput"
    type="number"
    placeholder="Enter measurement"
>

<span>
kPa
</span>


<button onclick="checkGauge()">

Record

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
Calculate Absolute Pressure
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



<div id="complete">

<h2>
🎉 Experiment Complete
</h2>

<p>

Your calculated absolute pressure is within
the required ±5%.

</p>


<button onclick="location.reload()">

Start New Experiment

</button>

</div>


</div>

</div>



<script>

/* ============================================================
   RANDOM EXPERIMENT
============================================================ */

const rhoHg =
    13600;


const gravity =
    9.81;


const barometerChoices =
[
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


const gaugeChoices =
[
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


const absolutePressure =
    atmosphericPressure
    +
    gaugeValue;



let atmosphericComplete =
    false;


let gaugeConnected =
    false;


let valveOpened =
    false;


/* ============================================================
   BUILD BAROMETER SCALE
============================================================ */

function createBarometerScale() {

    const scale =
        document.getElementById(
            "baroScale"
        );


    for (
        let v = 720;
        v <= 780;
        v += 5
    ) {

        const position =
            (
                (v - 720)
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
            v % 10 === 0
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
            v % 10 === 0
        ) {

            const label =
                document.createElement(
                    "div"
                );


            label.className =
                "scale-number";


            label.textContent =
                v;


            label.style.bottom =
                position
                +
                "%";


            scale.appendChild(
                label
            );

        }

    }

}


/* ============================================================
   BUILD GAUGE
============================================================ */

function createGaugeNumbers() {

    const parent =
        document.getElementById(
            "gaugeNumbers"
        );


    const center =
        75;


    const radius =
        56;


    for (
        let value = 0;
        value <= 100;
        value += 20
    ) {

        const degrees =
            -135
            +
            (
                value
                /
                100
            )
            *
            270;


        const radians =
            degrees
            *
            Math.PI
            /
            180;


        const x =
            center
            +
            radius
            *
            Math.cos(
                radians
            );


        const y =
            center
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
   INITIAL INSTRUMENT STATE
============================================================ */

function initializeEquipment() {

    /*
    IMPORTANT:
    The actual barometer reading is NOT visible
    when the experiment begins.
    */

    document.getElementById(
        "mercury"
    ).style.opacity =
        "0";


    document.getElementById(
        "mercury"
    ).style.height =
        "4%";


    /*
    Gauge stays at 0 kPa initially.
    */

    document.getElementById(
        "needleAssembly"
    ).style.transform =
        "rotate(-135deg)";

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
   ATMOSPHERIC DROP
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
            "dragging-over"
        );

    }
);


atmosphereStation.addEventListener(
    "dragleave",
    () => {

        atmosphereStation.classList.remove(
            "dragging-over"
        );

    }
);


atmosphereStation.addEventListener(
    "drop",
    event => {

        event.preventDefault();


        atmosphereStation.classList.remove(
            "dragging-over"
        );


        const equipment =
            event.dataTransfer.getData(
                "equipment"
            );


        if (
            equipment
            !==
            "barometer"
        ) {

            alert(
                "This station requires the mercury barometer."
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
            "45px";


        barometer.style.margin =
            "0";


        atmosphereStation.classList.add(
            "active"
        );


        /*
        REMOVE INACTIVE COVER
        */

        document.getElementById(
            "barometerCover"
        ).classList.add(
            "hidden"
        );


        /*
        NOW activate the mercury reading.
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
        Small delay produces settling animation.
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
        ONLY NOW show student reading box.
        */

        setTimeout(
            () => {

                document.getElementById(
                    "barometerTask"
                ).classList.add(
                    "active"
                );


                setInstruction(
                    "Read the mercury level and record the barometer measurement."
                );

            },
            1300
        );

    }
);


/* ============================================================
   CHECK BAROMETER
============================================================ */

function checkBarometer() {

    const answer =
        Number(
            document.getElementById(
                "barometerInput"
            ).value
        );


    const feedback =
        document.getElementById(
            "barometerFeedback"
        );


    if (
        !Number.isFinite(answer)
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
            "Calculate atmospheric pressure from the measurement."
        );

    }

    else {

        feedbackMessage(
            feedback,
            "Check the mercury level and scale again.",
            false
        );

    }

}


/* ============================================================
   ATMOSPHERIC PRESSURE
============================================================ */

function checkAtmosphere() {

    const answer =
        Number(
            document.getElementById(
                "atmosphereInput"
            ).value
        );


    const feedback =
        document.getElementById(
            "atmosphereFeedback"
        );


    if (
        !Number.isFinite(answer)
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
        error <= .05
    ) {

        atmosphericComplete =
            true;


        feedbackMessage(
            feedback,
            "✓ Atmospheric pressure accepted. Error is within ±5%.",
            true
        );


        setInstruction(
            "Drag the pressure gauge to the pressure vessel test port."
        );

    }

    else {

        feedbackMessage(
            feedback,
            "Result is outside ±5%. Check P = ρgh and your units.",
            false
        );

    }

}


/* ============================================================
   GAUGE DRAG
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
   GAUGE TEST-PORT DROP
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
            "dragging-over"
        );

    }
);


portZone.addEventListener(
    "dragleave",
    () => {

        portZone.classList.remove(
            "dragging-over"
        );

    }
);


portZone.addEventListener(
    "drop",
    event => {

        event.preventDefault();


        portZone.classList.remove(
            "dragging-over"
        );


        const equipment =
            event.dataTransfer.getData(
                "equipment"
            );


        if (
            equipment
            !==
            "gauge"
        ) {

            return;

        }


        if (
            !atmosphericComplete
        ) {

            alert(
                "Complete the atmospheric pressure measurement first."
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
        Gauge needle remains at ZERO.
        */

        document.getElementById(
            "needleAssembly"
        ).style.transform =
            "rotate(-135deg)";


        setInstruction(
            "Pressure gauge connected. Open the test-port valve."
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
    Gauge finally receives pressure.
    */

    const gaugeAngle =
        -135
        +
        (
            gaugeValue
            /
            100
        )
        *
        270;


    setTimeout(
        () => {

            document.getElementById(
                "needleAssembly"
            ).style.transform =
                "rotate("
                +
                gaugeAngle
                +
                "deg)";

        },
        400
    );


    /*
    Student input appears only AFTER
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
                "Read the pressure gauge and record the measurement."
            );

        },
        1600
    );

}


/* ============================================================
   CHECK GAUGE
============================================================ */

function checkGauge() {

    const answer =
        Number(
            document.getElementById(
                "gaugeInput"
            ).value
        );


    const feedback =
        document.getElementById(
            "gaugeFeedback"
        );


    if (
        !Number.isFinite(answer)
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
            "✓ Gauge pressure recorded.",
            true
        );


        document.getElementById(
            "absoluteTask"
        ).classList.add(
            "active"
        );


        setInstruction(
            "Calculate absolute pressure from the two measurements."
        );

    }

    else {

        feedbackMessage(
            feedback,
            "Check the pressure gauge needle again.",
            false
        );

    }

}


/* ============================================================
   CHECK ABSOLUTE PRESSURE
============================================================ */

function checkAbsolute() {

    const answer =
        Number(
            document.getElementById(
                "absoluteInput"
            ).value
        );


    const feedback =
        document.getElementById(
            "absoluteFeedback"
        );


    if (
        !Number.isFinite(answer)
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
        error <= .05
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
            "Experiment complete."
        );

    }

    else {

        feedbackMessage(
            feedback,
            "Outside ±5%. Check Pabs = Pgauge + Patm.",
            false
        );

    }

}


/* ============================================================
   HELPERS
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


function setInstruction(
    message
) {

    document.getElementById(
        "instruction"
    ).textContent =
        message;

}


/* ============================================================
   INITIALIZE
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
    height=1750,
    scrolling=True
)
