import streamlit as st
import random
import math


# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="Pressure Measurement Virtual Lab",
    page_icon="💧",
    layout="centered",
)


# ==========================================================
# ENGINEERING CONSTANTS
# ==========================================================

RHO_HG = 13600.0       # Density of mercury, kg/m^3
G = 9.81               # Gravity, m/s^2

CALC_TOL = 0.05        # ±5% for calculated answers

# Instrument reading tolerance:
# half of one 5-unit scale division
BARO_READ_TOL = 2.5    # mmHg
GAUGE_READ_TOL = 2.5   # kPa


# ==========================================================
# CREATE A NEW RANDOM EXPERIMENT
# ==========================================================

def generate_values():

    st.session_state.barometer_mm = float(
        random.choice(
            range(735, 776, 5)
        )
    )

    st.session_state.gauge_kpa = float(
        random.choice(
            range(20, 81, 5)
        )
    )


def reset_lab():

    keys_to_clear = [
        "baro_entry",
        "patm_entry",
        "gauge_entry",
        "pabs_entry",
        "student_baro",
        "student_patm",
        "student_gauge",
        "student_pabs",
    ]

    for key in keys_to_clear:
        st.session_state.pop(
            key,
            None
        )

    generate_values()

    st.session_state.stage = 0


# ==========================================================
# CHECK ±5%
# ==========================================================

def within_percent(
    answer,
    correct,
    tolerance=CALC_TOL
):

    return (
        abs(answer - correct)
        <=
        abs(correct) * tolerance
    )


def parse_number(text):

    try:
        return float(text)

    except (
        TypeError,
        ValueError
    ):

        return None


# ==========================================================
# DRAW BAROMETER
# ==========================================================

def barometer_svg(value_mm):

    top_value = 780
    bottom_value = 720

    top_y = 25
    bottom_y = 350


    def y_for(value):

        return (
            bottom_y
            -
            (
                (value - bottom_value)
                /
                (top_value - bottom_value)
            )
            *
            (bottom_y - top_y)
        )


    mercury_y = y_for(
        value_mm
    )

    mercury_height = (
        bottom_y
        -
        mercury_y
    )


    marks = []


    for value in range(
        720,
        781,
        5
    ):

        y = y_for(value)

        major = (
            value % 10 == 0
        )


        x1 = (
            75
            if major
            else 88
        )


        width = (
            3
            if major
            else 1.5
        )


        marks.append(
            f"""
            <line
                x1="{x1}"
                y1="{y:.1f}"
                x2="115"
                y2="{y:.1f}"
                stroke="#334155"
                stroke-width="{width}"
            />
            """
        )


        if major:

            marks.append(
                f"""
                <text
                    x="65"
                    y="{y + 5:.1f}"
                    text-anchor="end"
                    font-size="15"
                    fill="#0f172a"
                >
                    {value}
                </text>
                """
            )


    return f"""

    <div
        style="
        display:flex;
        justify-content:center;
        "
    >

    <svg
        width="250"
        height="390"
        viewBox="0 0 250 390"
    >

        <text
            x="125"
            y="18"
            text-anchor="middle"
            font-size="18"
            font-weight="700"
        >
            Mercury Barometer
        </text>


        {''.join(marks)}


        <rect
            x="125"
            y="{top_y}"
            width="42"
            height="{bottom_y - top_y}"
            rx="18"
            fill="white"
            stroke="#334155"
            stroke-width="4"
        />


        <rect
            x="130"
            y="{mercury_y:.1f}"
            width="32"
            height="{mercury_height:.1f}"
            fill="#64748b"
        />


        <ellipse
            cx="146"
            cy="{mercury_y:.1f}"
            rx="16"
            ry="5"
            fill="#94a3b8"
        />


        <text
            x="125"
            y="380"
            text-anchor="middle"
            font-size="15"
        >
            Scale: mmHg
        </text>

    </svg>

    </div>

    """


# ==========================================================
# DRAW PRESSURE GAUGE
# ==========================================================

def gauge_svg(value_kpa):

    center_x = 160
    center_y = 160

    radius = 125

    marks = []


    for value in range(
        0,
        101,
        5
    ):

        angle = math.radians(
            135
            +
            (
                value
                /
                100
            )
            *
            270
        )


        outer_radius = 118


        inner_radius = (
            103
            if value % 20 == 0
            else 110
        )


        x1 = (
            center_x
            +
            outer_radius
            *
            math.cos(angle)
        )


        y1 = (
            center_y
            +
            outer_radius
            *
            math.sin(angle)
        )


        x2 = (
            center_x
            +
            inner_radius
            *
            math.cos(angle)
        )


        y2 = (
            center_y
            +
            inner_radius
            *
            math.sin(angle)
        )


        marks.append(
            f"""
            <line
                x1="{x1:.1f}"
                y1="{y1:.1f}"
                x2="{x2:.1f}"
                y2="{y2:.1f}"
                stroke="#111827"
                stroke-width="{
                    3
                    if value % 20 == 0
                    else 1.5
                }"
            />
            """
        )


        if value % 20 == 0:

            label_radius = 88


            tx = (
                center_x
                +
                label_radius
                *
                math.cos(angle)
            )


            ty = (
                center_y
                +
                label_radius
                *
                math.sin(angle)
            )


            marks.append(
                f"""
                <text
                    x="{tx:.1f}"
                    y="{ty + 5:.1f}"
                    text-anchor="middle"
                    font-size="14"
                    font-weight="700"
                >
                    {value}
                </text>
                """
            )


    needle_angle = math.radians(
        135
        +
        (
            value_kpa
            /
            100
        )
        *
        270
    )


    needle_radius = 90


    needle_x = (
        center_x
        +
        needle_radius
        *
        math.cos(
            needle_angle
        )
    )


    needle_y = (
        center_y
        +
        needle_radius
        *
        math.sin(
            needle_angle
        )
    )


    return f"""

    <div
        style="
        display:flex;
        justify-content:center;
        "
    >

    <svg
        width="330"
        height="330"
        viewBox="0 0 320 320"
    >

        <circle
            cx="{center_x}"
            cy="{center_y}"
            r="{radius}"
            fill="white"
            stroke="#334155"
            stroke-width="7"
        />


        {''.join(marks)}


        <line
            x1="{center_x}"
            y1="{center_y}"
            x2="{needle_x:.1f}"
            y2="{needle_y:.1f}"
            stroke="#dc2626"
            stroke-width="5"
            stroke-linecap="round"
        />


        <circle
            cx="{center_x}"
            cy="{center_y}"
            r="9"
            fill="#111827"
        />


        <text
            x="{center_x}"
            y="225"
            text-anchor="middle"
            font-size="18"
            font-weight="700"
        >
            kPa
        </text>

    </svg>

    </div>

    """


# ==========================================================
# INITIALIZE SESSION
# ==========================================================

if "stage" not in st.session_state:

    st.session_state.stage = 0


if (
    "barometer_mm"
    not in st.session_state
    or
    "gauge_kpa"
    not in st.session_state
):

    generate_values()


# ==========================================================
# TRUE VALUES
# ==========================================================

barometer_mm = (
    st.session_state.barometer_mm
)

gauge_kpa = (
    st.session_state.gauge_kpa
)


patm_kpa = (
    RHO_HG
    *
    G
    *
    (
        barometer_mm
        /
        1000
    )
    /
    1000
)


pabs_kpa = (
    patm_kpa
    +
    gauge_kpa
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "💧 Pressure Measurement Virtual Lab"
)

st.caption(
    "Determine absolute pressure using "
    "a barometer and a pressure gauge."
)


# ==========================================================
# PROGRESS
# ==========================================================

with st.sidebar:

    st.subheader(
        "Lab Progress"
    )


    progress = min(
        st.session_state.stage
        /
        8,
        1.0
    )


    st.progress(
        progress
    )


    st.write(
        f"Stage "
        f"{st.session_state.stage} "
        f"of 8"
    )


    if st.button(
        "Start a new experiment",
        use_container_width=True
    ):

        reset_lab()

        st.rerun()


# ==========================================================
# STAGE 0 — START
# ==========================================================

if st.session_state.stage == 0:

    st.info(
        "Complete the experiment one action "
        "at a time. The next step stays "
        "locked until the current step is complete."
    )


    st.markdown(
        """
        **Equipment**

        - Mercury barometer
        - Pressure vessel
        - Pressure gauge
        - Test-port valve
        """
    )


    if st.button(
        "▶ Start Experiment",
        type="primary",
        use_container_width=True
    ):

        st.session_state.stage = 1

        st.rerun()


    st.stop()


# ==========================================================
# PART 1 — BAROMETER
# ==========================================================

if st.session_state.stage >= 1:

    st.header(
        "1. Measure Atmospheric Pressure"
    )


# ==========================================================
# STAGE 1 — PLACE BAROMETER
# ==========================================================

if st.session_state.stage == 1:

    st.write(
        "Place the mercury barometer "
        "at the laboratory station."
    )


    st.caption(
        "The barometer measures the surrounding "
        "atmospheric pressure. It is not connected "
        "to the pressure vessel."
    )


    if st.button(
        "🧰 Place Barometer at Lab Station",
        type="primary"
    ):

        st.session_state.stage = 2

        st.rerun()


    st.stop()


# ==========================================================
# SHOW BAROMETER
# ==========================================================

if st.session_state.stage >= 2:

    st.markdown(
        barometer_svg(
            barometer_mm
        ),
        unsafe_allow_html=True
    )


# ==========================================================
# STAGE 2 — READ BAROMETER
# ==========================================================

if st.session_state.stage == 2:

    st.write(
        "Read the mercury level from the scale."
    )


    with st.form(
        "barometer_form"
    ):

        barometer_text = st.text_input(
            "Record your barometer reading (mmHg)",
            key="baro_entry"
        )


        submitted = (
            st.form_submit_button(
                "Record Barometer Reading",
                type="primary"
            )
        )


    if submitted:

        answer = parse_number(
            barometer_text
        )


        if answer is None:

            st.error(
                "Enter a numerical reading."
            )


        elif (
            abs(
                answer
                -
                barometer_mm
            )
            <=
            BARO_READ_TOL
        ):

            st.session_state.student_baro = (
                answer
            )

            st.session_state.stage = 3

            st.rerun()


        else:

            st.error(
                "That reading is outside the "
                "instrument-reading tolerance. "
                "Look at the scale again."
            )


    st.stop()


# ==========================================================
# BAROMETER COMPLETE
# ==========================================================

if st.session_state.stage >= 3:

    st.success(
        "Barometer reading recorded: "
        f"{st.session_state.student_baro:.1f} mmHg"
    )


# ==========================================================
# STAGE 3 — CALCULATE ATM PRESSURE
# ==========================================================

if st.session_state.stage == 3:

    st.subheader(
        "Calculate Atmospheric Pressure"
    )


    st.write(
        "Using your measured barometer reading, "
        "calculate atmospheric pressure."
    )


    with st.expander(
        "Need a formula hint?"
    ):

        st.latex(
            r"P_{atm}=\rho_{Hg}gh"
        )

        st.write(
            "ρHg = 13,600 kg/m³"
        )

        st.write(
            "g = 9.81 m/s²"
        )

        st.write(
            "Remember to convert mm to m."
        )


    with st.form(
        "atmosphere_form"
    ):

        atmosphere_text = (
            st.text_input(
                "Atmospheric pressure (kPa)",
                key="patm_entry"
            )
        )


        submitted = (
            st.form_submit_button(
                "Check Atmospheric Pressure",
                type="primary"
            )
        )


    if submitted:

        answer = parse_number(
            atmosphere_text
        )


        if answer is None:

            st.error(
                "Enter a numerical pressure."
            )


        elif within_percent(
            answer,
            patm_kpa
        ):

            st.session_state.student_patm = (
                answer
            )

            st.session_state.stage = 4

            st.rerun()


        else:

            error_percent = (
                abs(
                    answer
                    -
                    patm_kpa
                )
                /
                patm_kpa
                *
                100
            )


            st.error(
                "Not within ±5%. "
                f"Your current error is "
                f"approximately "
                f"{error_percent:.1f}%."
            )


    st.stop()


# ==========================================================
# PART 2 — PRESSURE GAUGE
# ==========================================================

if st.session_state.stage >= 4:

    st.success(
        "Atmospheric pressure accepted: "
        f"{st.session_state.student_patm:.2f} kPa"
    )


    st.header(
        "2. Measure Gauge Pressure"
    )


# ==========================================================
# STAGE 4 — CONNECT GAUGE
# ==========================================================

if st.session_state.stage == 4:

    st.write(
        "Connect the pressure gauge hose "
        "to the pressure vessel test port."
    )


    if st.button(
        "🔧 Connect Pressure Gauge",
        type="primary"
    ):

        st.session_state.stage = 5

        st.rerun()


    st.stop()


# ==========================================================
# STAGE 5 — OPEN VALVE
# ==========================================================

if st.session_state.stage == 5:

    st.write(
        "The pressure gauge is connected, "
        "but the test port is isolated."
    )


    st.write(
        "Open the test-port valve so the gauge "
        "is exposed to the vessel pressure."
    )


    if st.button(
        "🟢 Open Test-Port Valve",
        type="primary"
    ):

        st.session_state.stage = 6

        st.rerun()


    st.stop()


# ==========================================================
# SHOW PRESSURE GAUGE
# ==========================================================

if st.session_state.stage >= 6:

    st.markdown(
        gauge_svg(
            gauge_kpa
        ),
        unsafe_allow_html=True
    )


# ==========================================================
# STAGE 6 — READ GAUGE
# ==========================================================

if st.session_state.stage == 6:

    st.write(
        "Read the pressure gauge and "
        "record the gauge pressure."
    )


    with st.form(
        "gauge_form"
    ):

        gauge_text = st.text_input(
            "Gauge pressure reading (kPa)",
            key="gauge_entry"
        )


        submitted = (
            st.form_submit_button(
                "Record Gauge Reading",
                type="primary"
            )
        )


    if submitted:

        answer = parse_number(
            gauge_text
        )


        if answer is None:

            st.error(
                "Enter a numerical reading."
            )


        elif (
            abs(
                answer
                -
                gauge_kpa
            )
            <=
            GAUGE_READ_TOL
        ):

            st.session_state.student_gauge = (
                answer
            )

            st.session_state.stage = 7

            st.rerun()


        else:

            st.error(
                "That reading is outside the "
                "instrument-reading tolerance. "
                "Check the gauge needle again."
            )


    st.stop()


# ==========================================================
# STAGE 7 — ABSOLUTE PRESSURE
# ==========================================================

if st.session_state.stage >= 7:

    st.success(
        "Gauge pressure recorded: "
        f"{st.session_state.student_gauge:.1f} kPa"
    )


if st.session_state.stage == 7:

    st.header(
        "3. Determine Absolute Pressure"
    )


    st.write(
        "Use the atmospheric pressure "
        "and gauge pressure you measured."
    )


    with st.expander(
        "Need a formula hint?"
    ):

        st.latex(
            r"P_{abs}=P_{gauge}+P_{atm}"
        )


    with st.form(
        "absolute_form"
    ):

        absolute_text = st.text_input(
            "Absolute pressure (kPa)",
            key="pabs_entry"
        )


        submitted = (
            st.form_submit_button(
                "Check Final Result",
                type="primary"
            )
        )


    if submitted:

        answer = parse_number(
            absolute_text
        )


        if answer is None:

            st.error(
                "Enter a numerical pressure."
            )


        elif within_percent(
            answer,
            pabs_kpa
        ):

            st.session_state.student_pabs = (
                answer
            )

            st.session_state.stage = 8

            st.rerun()


        else:

            error_percent = (
                abs(
                    answer
                    -
                    pabs_kpa
                )
                /
                pabs_kpa
                *
                100
            )


            st.error(
                "Your result is not within ±5%. "
                f"Current error ≈ "
                f"{error_percent:.1f}%."
            )


    st.stop()


# ==========================================================
# STAGE 8 — COMPLETE
# ==========================================================

if st.session_state.stage == 8:

    st.balloons()


    st.success(
        "Experiment complete! "
        "Your final absolute pressure "
        "is within ±5%."
    )


    st.subheader(
        "Lab Record"
    )


    st.write(
        "Barometer reading: "
        f"**{st.session_state.student_baro:.1f} mmHg**"
    )


    st.write(
        "Atmospheric pressure: "
        f"**{st.session_state.student_patm:.2f} kPa**"
    )


    st.write(
        "Gauge pressure: "
        f"**{st.session_state.student_gauge:.1f} kPa**"
    )


    st.write(
        "Absolute pressure: "
        f"**{st.session_state.student_pabs:.2f} kPa**"
    )


    final_error = (
        abs(
            st.session_state.student_pabs
            -
            pabs_kpa
        )
        /
        pabs_kpa
        *
        100
    )


    st.metric(
        "Final Percent Error",
        f"{final_error:.2f}%"
    )


    with st.expander(
        "Instructor / Reference Values"
    ):

        st.write(
            "Actual barometer value: "
            f"{barometer_mm:.1f} mmHg"
        )

        st.write(
            "Actual atmospheric pressure: "
            f"{patm_kpa:.2f} kPa"
        )

        st.write(
            "Actual gauge pressure: "
            f"{gauge_kpa:.1f} kPa"
        )

        st.write(
            "Actual absolute pressure: "
            f"{pabs_kpa:.2f} kPa"
        )


    if st.button(
        "🔄 Run Another Experiment",
        type="primary",
        use_container_width=True
    ):

        reset_lab()

        st.session_state.stage = 1

        st.rerun()
