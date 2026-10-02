import streamlit as st
import streamlit.components.v1 as components


# ==========================================================
# STREAMLIT PAGE
# ==========================================================

st.set_page_config(
    page_title="Pressure Measurement Virtual Lab",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Pressure Measurement Virtual Lab")

st.write(
    """
    Complete the experiment by interacting with the virtual
    laboratory equipment.

    **Drag the instruments to the correct locations and record
    your measurements.**
    """
)


# ==========================================================
# VIRTUAL LAB GAME
# ==========================================================

virtual_lab = r"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #eef4f8;
    color: #1f2937;
}


/* ======================================================
   MAIN LAB
====================================================== */

.lab {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}

.panel {
    background: white;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.10);
}

h2 {
    color: #075985;
}


/* ======================================================
   STATUS
====================================================== */

.status {
    background: #e0f2fe;
    border-left: 6px solid #0284c7;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 7px;
}


/* ======================================================
   LAB BENCH
====================================================== */

.lab-area {
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 20px;
}


/* ======================================================
   EQUIPMENT TRAY
====================================================== */

.tray {
    background: #f8fafc;
    border: 2px solid #cbd5e1;
    border-radius: 12px;
    padding: 15px;
}

.tray h3 {
    text-align: center;
}


.instrument {
    background: white;
    border: 3px solid #64748b;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
    text-align: center;

    cursor: grab;

    user-select: none;

    transition: 0.2s;
}

.instrument:hover {
    transform: scale(1.03);
    border-color: #0284c7;
}

.instrument:active {
    cursor: grabbing;
}


.instrument-icon {
    font-size: 55px;
}


/* ======================================================
   EXPERIMENT AREA
====================================================== */

.experiment-area {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}


/* ======================================================
   DROP ZONES
====================================================== */

.drop-zone {
    min-height: 280px;

    border: 3px dashed #94a3b8;

    border-radius: 15px;

    background: #f8fafc;

    display: flex;
    flex-direction: column;

    justify-content: center;
    align-items: center;

    padding: 20px;

    text-align: center;

    transition: 0.2s;
}


.drop-zone.drag-over {
    border-color: #0284c7;
    background: #e0f2fe;
}


.drop-zone.success {
    border-style: solid;
    border-color: #16a34a;
    background: #f0fdf4;
}


.zone-icon {
    font-size: 60px;
}


/* ======================================================
   BAROMETER
====================================================== */

.barometer-container {
    display: none;
    margin-top: 10px;
}


.barometer {
    position: relative;

    width: 180px;
    height: 330px;

    margin: auto;
}


.baro-scale {
    position: absolute;

    left: 0;
    top: 10px;

    width: 80px;
    height: 300px;
}


.baro-tube {
    position: absolute;

    left: 100px;
    top: 10px;

    width: 45px;
    height: 300px;

    border: 4px solid #334155;

    border-radius:
        18px 18px 6px 6px;

    overflow: hidden;

    background: white;
}


.mercury {
    position: absolute;

    bottom: 0;

    width: 100%;

    background:
        linear-gradient(
            to right,
            #475569,
            #cbd5e1,
            #475569
        );

    transition: height 0.8s;
}


.scale-line {
    position: absolute;

    right: 0;

    width: 28px;

    border-top: 1px solid #334155;
}


.scale-line.major {
    width: 40px;
    border-top: 2px solid #111827;
}


.scale-label {
    position: absolute;

    right: 47px;

    transform:
        translateY(-50%);

    font-size: 13px;
}


/* ======================================================
   PRESSURE VESSEL
====================================================== */

.vessel {
    width: 250px;
    height: 180px;

    background:
        linear-gradient(
            #cbd5e1,
            #94a3b8
        );

    border: 5px solid #475569;

    border-radius: 50px;

    position: relative;

    margin: 25px auto;
}


.vessel-label {
    position: absolute;

    width: 100%;

    top: 70px;

    text-align: center;

    font-weight: bold;
}


.test-port {
    position: absolute;

    width: 30px;
    height: 30px;

    background: #111827;

    border-radius: 50%;

    right: -18px;
    top: 70px;
}


.test-port-label {
    position: absolute;

    right: -95px;
    top: 68px;

    font-size: 13px;
}


/* ======================================================
   GAUGE
====================================================== */

.gauge-container {
    display: none;

    margin-top: 20px;
}


.gauge {
    position: relative;

    width: 260px;
    height: 260px;

    border: 8px solid #334155;

    border-radius: 50%;

    background: white;

    margin: auto;
}


.gauge-tick {
    position: absolute;

    width: 2px;
    height: 14px;

    background: #111827;

    left: 50%;
    top: 12px;

    transform-origin:
        1px 118px;
}


.gauge-number {
    position: absolute;

    font-size: 13px;
    font-weight: bold;
}


.needle-wrapper {
    position: absolute;

    left: 50%;
    top: 50%;

    width: 0;
    height: 0;

    transform: rotate(-120deg);

    transition:
        transform 1s ease;
}


.needle {
    position: absolute;

    width: 5px;
    height: 90px;

    left: -2px;
    top: -90px;

    background: #dc2626;

    border-radius: 5px;
}


.gauge-center {
    position: absolute;

    left: 50%;
    top: 50%;

    width: 18px;
    height: 18px;

    transform:
        translate(
            -50%,
            -50%
        );

    border-radius: 50%;

    background: #111827;
}


.gauge-unit {
    position: absolute;

    left: 50%;
    top: 68%;

    transform:
        translateX(-50%);

    font-weight: bold;
}


/* ======================================================
   INPUT / CALCULATIONS
====================================================== */

.task {
    display: none;

    background: white;

    border-left:
        6px solid #0284c7;

    padding: 20px;

    margin-top: 20px;

    border-radius: 8px;
}


.task.active {
    display: block;
}


.input-row {
    display: flex;

    align-items: center;

    gap: 8px;

    margin-top: 10px;
}


input {
    width: 180px;

    padding: 10px;

    border:
        2px solid #cbd5e1;

    border-radius: 7px;

    font-size: 16px;
}


button {
    padding:
        11px 18px;

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


button.secondary {
    background: #475569;
}


.feedback {
    margin-top: 12px;

    padding: 10px;

    border-radius: 6px;
}


.correct {
    background: #dcfce7;
    color: #166534;
}


.incorrect {
    background: #fee2e2;
    color: #991b1b;
}


/* ======================================================
   VALVE
====================================================== */

.valve-area {
    display: none;

    text-align: center;

    margin-top: 15px;
}


.valve-button {
    background: #16a34a;
}


.valve-button:hover {
    background: #15803d;
}


/* ======================================================
   COMPLETE
====================================================== */

.complete {
    display: none;

    background: #dcfce7;

    border:
        3px solid #16a34a;

    border-radius: 12px;

    padding: 25px;

    text-align: center;

    margin-top: 25px;
}


@media (
    max-width: 850px
) {

    .lab-area {
        grid-template-columns: 1fr;
    }

    .experiment-area {
        grid-template-columns: 1fr;
    }

}

</style>

</head>


<body>


<div class="lab">


<!-- =====================================================
     STATUS
===================================================== -->

<div
    class="status"
    id="status"
>
    Step 1:
    Drag the barometer from the equipment tray
    to the Atmospheric Measurement Station.
</div>



<!-- =====================================================
     LAB AREA
===================================================== -->

<div class="lab-area">


<!-- EQUIPMENT TRAY -->

<div class="tray">

<h3>
🧰 Equipment Tray
</h3>


<div
    id="barometerInstrument"
    class="instrument"
    draggable="true"
    ondragstart="dragStart(event)"
    data-equipment="barometer"
>

    <div class="instrument-icon">
        🌡️
    </div>

    <strong>
        Mercury Barometer
    </strong>

    <p>
        Drag to measurement station
    </p>

</div>



<div
    id="gaugeInstrument"
    class="instrument"
    draggable="true"
    ondragstart="dragStart(event)"
    data-equipment="gauge"
>

    <div class="instrument-icon">
        🧭
    </div>

    <strong>
        Pressure Gauge
    </strong>

    <p>
        Use after atmospheric
        pressure is determined
    </p>

</div>


</div>



<!-- EXPERIMENT AREA -->

<div class="experiment-area">


<!-- ATMOSPHERE STATION -->

<div
    id="atmosphereZone"
    class="drop-zone"
    ondragover="allowDrop(event)"
    ondragleave="leaveDrop(event)"
    ondrop="dropEquipment(event)"
    data-zone="atmosphere"
>

    <div class="zone-icon">
        🌤️
    </div>

    <h3>
        Atmospheric Measurement Station
    </h3>

    <p>
        Place the barometer here
        to measure atmospheric pressure.
    </p>


    <div
        id="barometerDisplay"
        class="barometer-container"
    >

        <div class="barometer">

            <div
                id="baroScale"
                class="baro-scale"
            >
            </div>


            <div class="baro-tube">

                <div
                    id="mercury"
                    class="mercury"
                >
                </div>

            </div>

        </div>

        <strong>
            Mercury Barometer
        </strong>

    </div>

</div>



<!-- PRESSURE VESSEL -->

<div
    id="vesselZone"
    class="drop-zone"
    ondragover="allowDrop(event)"
    ondragleave="leaveDrop(event)"
    ondrop="dropEquipment(event)"
    data-zone="vessel"
>

    <h3>
        Pressurized Vessel
    </h3>


    <div class="vessel">

        <div class="vessel-label">
            PRESSURE VESSEL
        </div>


        <div class="test-port"></div>


        <div class="test-port-label">
            Test Port
        </div>

    </div>


    <p>
        Connect the pressure gauge
        to the test port.
    </p>


    <div
        id="valveArea"
        class="valve-area"
    >

        <button
            class="valve-button"
            onclick="openValve()"
        >
            🟢 Open Test-Port Valve
        </button>

    </div>


    <div
        id="gaugeDisplay"
        class="gauge-container"
    >

        <div class="gauge">

            <div
                id="gaugeScale"
            >
            </div>


            <div
                id="needleWrapper"
                class="needle-wrapper"
            >

                <div class="needle">
                </div>

            </div>


            <div class="gauge-center">
            </div>


            <div class="gauge-unit">
                kPa
            </div>

        </div>

    </div>

</div>


</div>

</div>



<!-- =====================================================
     TASK 1
     RECORD BAROMETER
===================================================== -->

<div
    id="barometerTask"
    class="task"
>

<h2>
Step 2 — Record Barometer Reading
</h2>

<p>
Read the mercury level from the instrument.
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


<div
    id="barometerFeedback"
>
</div>

</div>



<!-- =====================================================
     TASK 2
     ATMOSPHERIC PRESSURE
===================================================== -->

<div
    id="atmosphericTask"
    class="task"
>

<h2>
Step 3 — Calculate Atmospheric Pressure
</h2>

<p>
Use your recorded barometer measurement.
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
    id="atmosphericInput"
    type="number"
    step="0.01"
    placeholder="Enter pressure"
>

<span>
kPa
</span>

<button onclick="checkAtmospheric()">
Check Calculation
</button>

</div>


<div
    id="atmosphericFeedback"
>
</div>

</div>



<!-- =====================================================
     TASK 3
     GAUGE READING
===================================================== -->

<div
    id="gaugeTask"
    class="task"
>

<h2>
Step 6 — Record Pressure Gauge Reading
</h2>

<p>
Read the red needle on the pressure gauge.
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


<div
    id="gaugeFeedback"
>
</div>

</div>



<!-- =====================================================
     TASK 4
     ABSOLUTE PRESSURE
===================================================== -->

<div
    id="absoluteTask"
    class="task"
>

<h2>
Step 7 — Calculate Absolute Pressure
</h2>


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
Submit Final Result
</button>

</div>


<div
    id="absoluteFeedback"
>
</div>

</div>



<!-- =====================================================
     COMPLETE
===================================================== -->

<div
    id="complete"
    class="complete"
>

<h2>
🎉 Experiment Complete!
</h2>

<p>
Your final absolute pressure is within
the required ±5% error.
</p>

<button onclick="location.reload()">
🔄 Start New Experiment
</button>

</div>


</div>



<script>


// ==========================================================
// EXPERIMENT VALUES
// ==========================================================

const rhoHg = 13600;

const gravity = 9.81;


// Random barometer
const possibleBarometer =
[
735,740,745,750,755,
760,765,770,775
];


const possibleGauge =
[
20,25,30,35,40,45,
50,55,60,65,70,75,80
];


const barometerValue =
possibleBarometer[
Math.floor(
Math.random()
*
possibleBarometer.length
)
];


const gaugeValue =
possibleGauge[
Math.floor(
Math.random()
*
possibleGauge.length
)
];


const atmosphericPressure =
rhoHg
*
gravity
*
(barometerValue / 1000)
/
1000;


const absolutePressure =
atmosphericPressure
+
gaugeValue;



// ==========================================================
// STUDENT DATA
// ==========================================================

let studentBarometer = null;

let studentAtmospheric = null;

let studentGauge = null;

let valveOpened = false;



// ==========================================================
// CREATE BAROMETER SCALE
// ==========================================================

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

        const percent =
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
        "scale-line";


        if (
            value % 10 === 0
        ) {

            line.classList.add(
                "major"
            );

        }


        line.style.bottom =
        percent + "%";


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
            "scale-label";


            label.style.bottom =
            percent + "%";


            label.textContent =
            value;


            scale.appendChild(
                label
            );

        }

    }


    const mercuryPercent =
    (
        (barometerValue - 720)
        /
        60
    )
    *
    100;


    document.getElementById(
        "mercury"
    ).style.height =
    mercuryPercent + "%";

}



// ==========================================================
// CREATE GAUGE SCALE
// ==========================================================

function createGaugeScale() {

    const scale =
    document.getElementById(
        "gaugeScale"
    );


    const center = 130;

    const radius = 105;


    for (
        let value = 0;
        value <= 100;
        value += 20
    ) {

        const angle =
        -120
        +
        (value / 100)
        *
        240;


        const radians =
        angle
        *
        Math.PI
        /
        180;


        const x =
        center
        +
        radius
        *
        Math.sin(
            radians
        );


        const y =
        center
        -
        radius
        *
        Math.cos(
            radians
        );


        const number =
        document.createElement(
            "div"
        );


        number.className =
        "gauge-number";


        number.textContent =
        value;


        number.style.left =
        x + "px";


        number.style.top =
        y + "px";


        number.style.transform =
        "translate(-50%, -50%)";


        scale.appendChild(
            number
        );

    }

}



// ==========================================================
// DRAG
// ==========================================================

function dragStart(event) {

    const equipment =
    event.currentTarget.dataset.equipment;


    event.dataTransfer.setData(
        "equipment",
        equipment
    );

}



// ==========================================================
// ALLOW DROP
// ==========================================================

function allowDrop(event) {

    event.preventDefault();


    event.currentTarget.classList.add(
        "drag-over"
    );

}



// ==========================================================
// LEAVE DROP
// ==========================================================

function leaveDrop(event) {

    event.currentTarget.classList.remove(
        "drag-over"
    );

}



// ==========================================================
// DROP EQUIPMENT
// ==========================================================

function dropEquipment(event) {

    event.preventDefault();


    event.currentTarget.classList.remove(
        "drag-over"
    );


    const equipment =
    event.dataTransfer.getData(
        "equipment"
    );


    const zone =
    event.currentTarget.dataset.zone;



    // BAROMETER

    if (
        equipment === "barometer"
        &&
        zone === "atmosphere"
    ) {

        event.currentTarget.classList.add(
            "success"
        );


        document.getElementById(
            "barometerDisplay"
        ).style.display =
        "block";


        document.getElementById(
            "barometerInstrument"
        ).style.display =
        "none";


        document.getElementById(
            "barometerTask"
        ).classList.add(
            "active"
        );


        setStatus(
            "Step 2: Read the mercury barometer and record the measurement."
        );


        return;

    }



    // GAUGE

    if (
        equipment === "gauge"
        &&
        zone === "vessel"
    ) {

        if (
            studentAtmospheric === null
        ) {

            alert(
                "Determine atmospheric pressure before connecting the pressure gauge."
            );

            return;

        }


        event.currentTarget.classList.add(
            "success"
        );


        document.getElementById(
            "gaugeInstrument"
        ).style.display =
        "none";


        document.getElementById(
            "valveArea"
        ).style.display =
        "block";


        setStatus(
            "Step 5: Pressure gauge connected. Open the test-port valve."
        );


        return;

    }



    alert(
        "That instrument does not belong in this location."
    );

}



// ==========================================================
// BAROMETER CHECK
// ==========================================================

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
        isNaN(answer)
    ) {

        showFeedback(
            feedback,
            "Enter a numerical reading.",
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

        studentBarometer =
        answer;


        showFeedback(
            feedback,
            "✓ Measurement recorded.",
            true
        );


        document.getElementById(
            "atmosphericTask"
        ).classList.add(
            "active"
        );


        setStatus(
            "Step 3: Calculate atmospheric pressure using your barometer reading."
        );

    }

    else {

        showFeedback(
            feedback,
            "Recheck the mercury level and scale.",
            false
        );

    }

}



// ==========================================================
// ATMOSPHERIC PRESSURE
// ==========================================================

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
        isNaN(answer)
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

        studentAtmospheric =
        answer;


        showFeedback(
            feedback,
            "✓ Atmospheric pressure accepted. Result is within ±5%.",
            true
        );


        setStatus(
            "Step 4: Drag the pressure gauge from the equipment tray to the vessel test port."
        );

    }

    else {

        showFeedback(
            feedback,
            "Result is outside ±5%. Recheck the calculation.",
            false
        );

    }

}



// ==========================================================
// OPEN VALVE
// ==========================================================

function openValve() {

    valveOpened =
    true;


    document.getElementById(
        "valveArea"
    ).style.display =
    "none";


    document.getElementById(
        "gaugeDisplay"
    ).style.display =
    "block";


    const needleAngle =
    -120
    +
    (
        gaugeValue
        /
        100
    )
    *
    240;


    document.getElementById(
        "needleWrapper"
    ).style.transform =
    `rotate(${needleAngle}deg)`;


    document.getElementById(
        "gaugeTask"
    ).classList.add(
        "active"
    );


    setStatus(
        "Step 6: Valve open. Read the pressure gauge and record the measurement."
    );

}



// ==========================================================
// GAUGE READING
// ==========================================================

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
        isNaN(answer)
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

        studentGauge =
        answer;


        showFeedback(
            feedback,
            "✓ Gauge pressure measurement recorded.",
            true
        );


        document.getElementById(
            "absoluteTask"
        ).classList.add(
            "active"
        );


        setStatus(
            "Step 7: Calculate the absolute pressure."
        );

    }

    else {

        showFeedback(
            feedback,
            "Recheck the pressure gauge needle.",
            false
        );

    }

}



// ==========================================================
// ABSOLUTE PRESSURE
// ==========================================================

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
        isNaN(answer)
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
            "complete"
        ).style.display =
        "block";


        setStatus(
            "Experiment complete!"
        );

    }

    else {

        showFeedback(
            feedback,
            "Result is outside ±5%. Recheck Pgauge + Patm.",
            false
        );

    }

}



// ==========================================================
// FEEDBACK
// ==========================================================

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



// ==========================================================
// STATUS
// ==========================================================

function setStatus(message) {

    document.getElementById(
        "status"
    ).textContent =
    message;

}



// ==========================================================
// START
// ==========================================================

createBarometerScale();

createGaugeScale();

</script>


</body>

</html>
"""


components.html(
    virtual_lab,
    height=1500,
    scrolling=True
)
