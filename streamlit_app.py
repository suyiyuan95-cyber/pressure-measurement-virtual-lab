import streamlit as st
import streamlit.components.v1 as components
import random
import math


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Pressure Measurement Virtual Lab",
    page_icon="💧",
    layout="centered"
)


# ============================================================
# ENGINEERING CONSTANTS
# ============================================================

RHO_HG = 13600.0       # Density of mercury, kg/m^3
G = 9.81               # Gravity, m/s^2

# Calculation tolerance
CALC_TOLERANCE = 0.05  # +/- 5%

# Instrument-reading tolerances
BAROMETER_TOLERANCE = 2.5   # mmHg
GAUGE_TOLERANCE = 2.5       # kPa


# ============================================================
# RANDOM EXPERIMENT VALUES
# ============================================================

def generate_experiment():

    st.session_state.barometer_mm = float(
        random.choice(range(735, 776, 5))
    )

    st.session_state.gauge_kpa = float(
        random.choice(range(20, 81, 5))
    )


def reset_lab():

    keys_to_delete = [
        "barometer_entry",
        "atmospheric_entry",
        "gauge_entry",
        "absolute_entry",
        "student_barometer",
        "student_atmospheric",
        "student_gauge",
        "student_absolute",
    ]

    for key in keys_to_delete:
        st.session_state.pop(key, None)

    generate_experiment()

    st.session_state.stage = 0


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def parse_number(value):

    try:
        return float(value)

    except (TypeError, ValueError):
        return None


def within_five_percent(student_answer, correct_answer):

    allowed_error = abs(correct_answer) * CALC_TOLERANCE

    return (
        abs(student_answer - correct_answer)
        <= allowed_error
    )


# ============================================================
# BAROMETER GRAPHIC
# ============================================================

def barometer_html(value_mm):

    top_value = 780
    bottom_value = 720

    top_y = 30
    bottom_y = 360


    def value_to_y(value):

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


    mercury_y = value_to_y(value_mm)

    mercury_height = bottom_y - mercury_y


    scale_elements = ""


    for value in range(720, 781, 5):

        y = value_to_y(value)

        major = value % 10 == 0


        if major:
            x1 = 75
            stroke_width = 3
        else:
            x1 = 90
            stroke_width = 1.5


        scale_elements += f"""
        <line
            x1="{x1}"
            y1="{y:.1f}"
            x2="120"
            y2="{y:.1f}"
            stroke="#1f2937"
            stroke-width="{stroke_width}"
        />
        """


        if major:

            scale_elements += f"""
            <text
                x="65"
                y="{y + 5:.1f}"
                text-anchor="end"
                font-size="15"
                fill="#111827"
            >
                {value}
            </text>
            """


    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <style>

            body {{
                margin: 0;
                background: white;
                font-family: Arial, Helvetica, sans-serif;
            }}

            .title {{
                text-align: center;
                font-weight: bold;
                font-size: 20px;
                margin-bottom: 5px;
                color: #0f172a;
            }}

            .instruction {{
                text-align: center;
                color: #475569;
                font-size: 14px;
                margin-bottom: 5px;
            }}

        </style>

    </head>


    <body>

        <div class="title">
            Mercury Barometer
        </div>

        <div class="instruction">
            Read the top of the mercury column.
        </div>


        <div style="display:flex; justify-content:center;">

            <svg
                width="260"
                height="400"
                viewBox="0 0 260 400"
            >

                {scale_elements}


                <!-- Glass tube -->

                <rect
                    x="135"
                    y="{top_y}"
                    width="46"
                    height="{bottom_y - top_y}"
                    rx="18"
                    fill="#f8fafc"
                    stroke="#334155"
                    stroke-width="4"
                />


                <!-- Mercury -->

                <rect
                    x="140"
                    y="{mercury_y:.1f}"
                    width="36"
                    height="{mercury_height:.1f}"
                    fill="#64748b"
                />


                <!-- Mercury meniscus -->

                <ellipse
                    cx="158"
                    cy="{mercury_y:.1f}"
                    rx="18"
                    ry="5"
                    fill="#94a3b8"
                />


                <!-- Bottom reservoir -->

                <ellipse
                    cx="158"
                    cy="360"
                    rx="28"
                    ry="15"
                    fill="#64748b"
                    stroke="#334155"
                    stroke-width="3"
                />


                <text
                    x="110"
                    y="392"
                    text-anchor="middle"
                    font-size="16"
                    fill="#111827"
                >
                    mmHg
                </text>

            </svg>

        </div>

    </body>

    </html>
    """

    return html


# ============================================================
# PRESSURE GAUGE GRAPHIC
# ============================================================

def gauge_html(value_kpa):

    center_x = 170
    center_y = 170

    outer_radius = 135

    gauge_elements = ""


    # --------------------------------------------------------
    # Gauge tick marks
    # --------------------------------------------------------

    for value in range(0, 101, 5):

        angle_deg = (
            135
            +
            (value / 100)
            *
            270
        )

        angle = math.radians(angle_deg)


        if value % 20 == 0:
            inner_radius = 112
            stroke_width = 3
        else:
            inner_radius = 120
            stroke_width = 1.5


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


        gauge_elements += f"""
        <line
            x1="{x1:.1f}"
            y1="{y1:.1f}"
            x2="{x2:.1f}"
            y2="{y2:.1f}"
            stroke="#111827"
            stroke-width="{stroke_width}"
        />
        """


        # Major number labels

        if value % 20 == 0:

            label_radius = 93

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


            gauge_elements += f"""
            <text
                x="{tx:.1f}"
                y="{ty + 5:.1f}"
                text-anchor="middle"
                font-size="15"
                font-weight="bold"
                fill="#111827"
            >
                {value}
            </text>
            """


    # --------------------------------------------------------
    # Gauge needle
    # --------------------------------------------------------

    needle_angle_deg = (
        135
        +
        (value_kpa / 100)
        *
        270
    )

    needle_angle = math.radians(
        needle_angle_deg
    )


    needle_radius = 95


    needle_x = (
        center_x
        +
        needle_radius
        *
        math.cos(needle_angle)
    )

    needle_y = (
        center_y
        +
        needle_radius
        *
        math.sin(needle_angle)
    )


    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <style>

            body {{
                margin: 0;
                background: white;
                font-family: Arial, Helvetica, sans-serif;
            }}

            .title {{
                text-align: center;
                font-weight: bold;
                font-size: 20px;
                color: #0f172a;
                margin-bottom: 4px;
            }}

            .instruction {{
                text-align: center;
                color: #475569;
                font-size: 14px;
            }}

        </style>

    </head>


    <body>

        <div class="title">
            Pressure Gauge
        </div>

        <div class="instruction">
            Read the position of the red needle.
        </div>


        <div style="display:flex; justify-content:center;">

            <svg
                width="340"
                height="330"
                viewBox="0 0 340 330"
            >

                <!-- Gauge body -->

                <circle
                    cx="{center_x}"
                    cy="{center_y}"
                    r="145"
                    fill="#f8fafc"
                    stroke="#334155"
                    stroke-width="8"
                />


                {gauge_elements}


                <!-- Needle -->

                <line
                    x1="{center_x}"
                    y1="{center_y}"
                    x2="{needle_x:.1f}"
                    y2="{needle_y:.1f}"
                    stroke="#dc2626"
                    stroke-width="6"
                    stroke-linecap="round"
                />


                <!-- Center hub -->

                <circle
                    cx="{center_x}"
                    cy="{center_y}"
                    r="11"
                    fill="#111827"
                />


                <text
                    x="{center_x}"
                    y="235"
                    text-anchor="middle"
                    font-size="19"
                    font-weight="bold"
                    fill="#334155"
                >
                    kPa
                </text>


                <text
                    x="{center_x}"
                    y="262"
                    text-anchor="middle"
                    font-size="12"
                    fill="#64748b"
                >
                    Gauge Pressure
                </text>

            </svg>

        </div>

    </body>

    </html>
    """

    return html


# ============================================================
# INITIALIZE SESSION
# ============================================================

if "stage" not in st.session_state:

    st.session_state.stage = 0


if "barometer_mm" not in st.session_state:

    generate_experiment()


# ============================================================
# TRUE EXPERIMENT VALUES
# ============================================================

barometer_mm = (
    st.session_state.barometer_mm
)

gauge_kpa = (
    st.session_state.gauge_kpa
)


# Convert mm to m

barometer_m = (
    barometer_mm
    /
    1000
)


# Atmospheric pressure

patm_pa = (
    RHO_HG
    *
    G
    *
    barometer_m
)


patm_kpa = (
    patm_pa
    /
    1000
)


# Absolute pressure

pabs_kpa = (
    patm_kpa
    +
    gauge_kpa
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "💧 Pressure Measurement Virtual Lab"
)

st.write(
    """
    In this experiment, you will determine the
    **absolute pressure** of a pressurized system.

    Complete each laboratory procedure in order.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
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
        f"Stage {st.session_state.stage} of 8"
    )


    st.markdown("---")


    if st.button(
        "🔄 Restart Experiment",
        use_container_width=True
    ):

        reset_lab()

        st.rerun()


# ============================================================
# STAGE 0 — START
# ============================================================

if st.session_state.stage == 0:

    st.header(
        "Experiment Setup"
    )


    st.info(
        """
        You will perform this experiment one step at a time.

        The next procedure will remain locked until the
        current procedure is completed.
        """
    )


    st.subheader(
        "Available Equipment"
    )


    st.write(
        """
        • Mercury barometer  
        • Pressurized vessel  
        • Pressure gauge  
        • Pressure test port  
        • Isolation valve
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


# ============================================================
# SECTION 1 — ATMOSPHERIC PRESSURE
# ============================================================

if st.session_state.stage >= 1:

    st.header(
        "1. Measure Atmospheric Pressure"
    )


# ============================================================
# STAGE 1 — PLACE BAROMETER
# ============================================================

if st.session_state.stage == 1:

    st.write(
        """
        The first measurement required is the
        **local atmospheric pressure**.
        """
    )


    st.warning(
        """
        The barometer is exposed to the surrounding
        atmosphere. It is **not connected to the pressure vessel**.
        """
    )


    st.write(
        """
        Place the mercury barometer at the laboratory
        measurement station.
        """
    )


    if st.button(
        "🧰 Place Barometer at Measurement Station",
        type="primary",
        use_container_width=True
    ):

        st.session_state.stage = 2

        st.rerun()


    st.stop()


# ============================================================
# DISPLAY BAROMETER
# ============================================================

if st.session_state.stage >= 2:

    components.html(
        barometer_html(
            barometer_mm
        ),
        height=450,
        scrolling=False
    )


# ============================================================
# STAGE 2 — READ BAROMETER
# ============================================================

if st.session_state.stage == 2:

    st.subheader(
        "Record Barometer Reading"
    )


    st.write(
        """
        Observe the height of the mercury column.

        Record the value shown by the instrument.
        """
    )


    with st.form(
        "barometer_form"
    ):

        barometer_text = st.text_input(
            "Barometer reading",
            placeholder="Enter your reading",
            key="barometer_entry"
        )


        st.caption(
            "Unit: mmHg"
        )


        submitted = (
            st.form_submit_button(
                "Record Measurement",
                type="primary",
                use_container_width=True
            )
        )


    if submitted:

        answer = parse_number(
            barometer_text
        )


        if answer is None:

            st.error(
                "Please enter a numerical measurement."
            )


        elif (
            abs(
                answer
                -
                barometer_mm
            )
            <=
            BAROMETER_TOLERANCE
        ):

            st.session_state.student_barometer = (
                answer
            )

            st.session_state.stage = 3

            st.rerun()


        else:

            st.error(
                """
                Your measurement does not agree with
                the instrument reading.

                Look carefully at the mercury level
                and scale, then try again.
                """
            )


    st.stop()


# ============================================================
# BAROMETER READING ACCEPTED
# ============================================================

if st.session_state.stage >= 3:

    st.success(
        "✓ Barometer measurement recorded."
    )


    st.write(
        "Recorded barometer reading: "
        f"**{st.session_state.student_barometer:.1f} mmHg**"
    )


# ============================================================
# STAGE 3 — ATMOSPHERIC PRESSURE CALCULATION
# ============================================================

if st.session_state.stage == 3:

    st.subheader(
        "Calculate Atmospheric Pressure"
    )


    st.write(
        """
        Using the barometer measurement you recorded,
        determine the atmospheric pressure.
        """
    )


    with st.expander(
        "Need a formula?"
    ):

        st.latex(
            r"P_{atm}=\rho_{Hg}gh"
        )


        st.write(
            r"""
            Mercury density:
            **13,600 kg/m³**

            Gravitational acceleration:
            **9.81 m/s²**
            """
        )


        st.info(
            "Remember to convert the barometer height from mm to m."
        )


    with st.form(
        "atmospheric_form"
    ):

        atmospheric_text = (
            st.text_input(
                "Atmospheric pressure",
                placeholder="Enter your calculated value",
                key="atmospheric_entry"
            )
        )


        st.caption(
            "Unit: kPa"
        )


        submitted = (
            st.form_submit_button(
                "Check Atmospheric Pressure",
                type="primary",
                use_container_width=True
            )
        )


    if submitted:

        answer = parse_number(
            atmospheric_text
        )


        if answer is None:

            st.error(
                "Please enter a numerical pressure."
            )


        elif within_five_percent(
            answer,
            patm_kpa
        ):

            st.session_state.student_atmospheric = (
                answer
            )

            st.session_state.stage = 4

            st.rerun()


        else:

            percent_error = (
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
                f"""
                The result is outside the allowed ±5% range.

                Current percent error:
                **{percent_error:.1f}%**

                Check your unit conversion and calculation.
                """
            )


    st.stop()


# ============================================================
# ATMOSPHERIC PRESSURE ACCEPTED
# ============================================================

if st.session_state.stage >= 4:

    st.success(
        "✓ Atmospheric pressure calculation accepted."
    )


    st.write(
        "Calculated atmospheric pressure: "
        f"**{st.session_state.student_atmospheric:.2f} kPa**"
    )


    st.header(
        "2. Measure Gauge Pressure"
    )


# ============================================================
# STAGE 4 — CONNECT PRESSURE GAUGE
# ============================================================

if st.session_state.stage == 4:

    st.write(
        """
        You now need to measure the gauge pressure
        inside the pressure vessel.
        """
    )


    st.write(
        """
        Connect the pressure gauge hose to the
        vessel's pressure test port.
        """
    )


    if st.button(
        "🔧 Connect Pressure Gauge to Test Port",
        type="primary",
        use_container_width=True
    ):

        st.session_state.stage = 5

        st.rerun()


    st.stop()


# ============================================================
# STAGE 5 — OPEN VALVE
# ============================================================

if st.session_state.stage == 5:

    st.success(
        "✓ Pressure gauge connected."
    )


    st.warning(
        """
        The test-port isolation valve is still closed.

        The pressure gauge cannot measure the vessel
        pressure until the valve is opened.
        """
    )


    if st.button(
        "🟢 Open Test-Port Valve",
        type="primary",
        use_container_width=True
    ):

        st.session_state.stage = 6

        st.rerun()


    st.stop()


# ============================================================
# DISPLAY GAUGE
# ============================================================

if st.session_state.stage >= 6:

    st.success(
        "✓ Test-port valve is open."
    )


    components.html(
        gauge_html(
            gauge_kpa
        ),
        height=390,
        scrolling=False
    )


# ============================================================
# STAGE 6 — READ GAUGE
# ============================================================

if st.session_state.stage == 6:

    st.subheader(
        "Record Pressure Gauge Reading"
    )


    st.write(
        """
        Observe the gauge needle.

        Record the measured gauge pressure.
        """
    )


    with st.form(
        "gauge_form"
    ):

        gauge_text = st.text_input(
            "Gauge pressure",
            placeholder="Enter your reading",
            key="gauge_entry"
        )


        st.caption(
            "Unit: kPa"
        )


        submitted = (
            st.form_submit_button(
                "Record Gauge Measurement",
                type="primary",
                use_container_width=True
            )
        )


    if submitted:

        answer = parse_number(
            gauge_text
        )


        if answer is None:

            st.error(
                "Please enter a numerical pressure."
            )


        elif (
            abs(
                answer
                -
                gauge_kpa
            )
            <=
            GAUGE_TOLERANCE
        ):

            st.session_state.student_gauge = (
                answer
            )

            st.session_state.stage = 7

            st.rerun()


        else:

            st.error(
                """
                Your recorded value does not match
                the pressure gauge.

                Look carefully at the needle position
                and scale, then try again.
                """
            )


    st.stop()


# ============================================================
# GAUGE READING ACCEPTED
# ============================================================

if st.session_state.stage >= 7:

    st.success(
        "✓ Gauge pressure measurement recorded."
    )


    st.write(
        "Recorded gauge pressure: "
        f"**{st.session_state.student_gauge:.1f} kPa**"
    )


# ============================================================
# STAGE 7 — ABSOLUTE PRESSURE
# ============================================================

if st.session_state.stage == 7:

    st.header(
        "3. Determine Absolute Pressure"
    )


    st.write(
        """
        Use your measured atmospheric pressure
        and measured gauge pressure to determine
        the absolute pressure.
        """
    )


    with st.expander(
        "Need a formula?"
    ):

        st.latex(
            r"P_{abs}=P_{gauge}+P_{atm}"
        )


    with st.form(
        "absolute_form"
    ):

        absolute_text = st.text_input(
            "Absolute pressure",
            placeholder="Enter your calculated value",
            key="absolute_entry"
        )


        st.caption(
            "Unit: kPa"
        )


        submitted = (
            st.form_submit_button(
                "Submit Final Result",
                type="primary",
                use_container_width=True
            )
        )


    if submitted:

        answer = parse_number(
            absolute_text
        )


        if answer is None:

            st.error(
                "Please enter a numerical pressure."
            )


        elif within_five_percent(
            answer,
            pabs_kpa
        ):

            st.session_state.student_absolute = (
                answer
            )

            st.session_state.stage = 8

            st.rerun()


        else:

            percent_error = (
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
                f"""
                Your result is outside the allowed ±5% range.

                Current percent error:
                **{percent_error:.1f}%**

                Recheck the relationship between
                gauge, atmospheric, and absolute pressure.
                """
            )


    st.stop()


# ============================================================
# STAGE 8 — COMPLETE
# ============================================================

if st.session_state.stage == 8:

    st.balloons()


    st.success(
        "🎉 Experiment Complete!"
    )


    st.write(
        """
        You successfully measured atmospheric pressure,
        measured gauge pressure, and determined the
        absolute pressure of the system.
        """
    )


    st.header(
        "Laboratory Results"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Barometer Reading",
            f"{st.session_state.student_barometer:.1f} mmHg"
        )


        st.metric(
            "Atmospheric Pressure",
            f"{st.session_state.student_atmospheric:.2f} kPa"
        )


    with col2:

        st.metric(
            "Gauge Pressure",
            f"{st.session_state.student_gauge:.1f} kPa"
        )


        st.metric(
            "Absolute Pressure",
            f"{st.session_state.student_absolute:.2f} kPa"
        )


    final_percent_error = (
        abs(
            st.session_state.student_absolute
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
        f"{final_percent_error:.2f}%"
    )


    st.info(
        """
        Acceptance requirement:

        Final calculated pressure must be within **±5%**
        of the experiment value.
        """
    )


    with st.expander(
        "Instructor / Reference Values"
    ):

        st.write(
            "Actual barometer reading: "
            f"**{barometer_mm:.1f} mmHg**"
        )


        st.write(
            "Actual atmospheric pressure: "
            f"**{patm_kpa:.2f} kPa**"
        )


        st.write(
            "Actual gauge pressure: "
            f"**{gauge_kpa:.1f} kPa**"
        )


        st.write(
            "Actual absolute pressure: "
            f"**{pabs_kpa:.2f} kPa**"
        )


    if st.button(
        "🔄 Perform Another Experiment",
        type="primary",
        use_container_width=True
    ):

        reset_lab()

        st.session_state.stage = 1

        st.rerun()
