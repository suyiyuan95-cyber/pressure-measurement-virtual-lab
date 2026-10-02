import streamlit as st

st.set_page_config(
    page_title="Pressure Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
        max-width: 1550px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

LAB_HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pressure Lab</title>

<style>
:root{
    --ink:#183631;
    --muted:#5b706b;
    --teal:#087f72;
    --mint:#e4f3ed;
    --paper:#f8faf7;
    --line:#dce5de;
    --red:#a24538;
}

*{box-sizing:border-box}

body{
    margin:0;
    background:var(--paper);
    color:var(--ink);
    font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}

button,input{font:inherit}
button{cursor:pointer;border:0}
button:disabled{cursor:not-allowed;opacity:.42}
[hidden]{display:none!important}

button:focus-visible,
input:focus-visible,
summary:focus-visible,
[role=button]:focus-visible{
    outline:3px solid #ce8c35;
    outline-offset:4px;
}

.app{max-width:1500px;margin:auto;padding:27px 28px 22px}
.eyebrow{font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:750;color:var(--teal)}
.top{display:flex;justify-content:space-between;align-items:center;gap:22px}
.top h1{font-size:clamp(29px,3.1vw,42px);font-weight:600;letter-spacing:-1.7px;margin:5px 0}
.top p{margin:3px 0;color:var(--muted);font-size:14px}
.equation{padding:15px 22px;background:#edf2ec;border:1px solid var(--line);border-radius:12px;white-space:nowrap}
.equation small{display:block;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:4px}
.equation strong{font-family:Georgia,serif;font-size:24px;font-weight:normal}
sub{font-size:60%}

.toolbar{display:flex;gap:10px;align-items:center;margin:22px 0 18px}
.chip{font-size:11px;border-radius:30px;background:var(--mint);color:var(--teal);padding:5px 11px;font-weight:700}
.toolbar .meta{color:var(--muted);font-size:12px}
.toolbar .reset{margin-left:auto;background:transparent;color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:6px 12px;font-size:12px}

.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:0 0 20px;padding:0;list-style:none}
.steps li{padding:10px 12px;border-top:2px solid #d8e1da;color:#70817b;font-size:12px;display:flex;align-items:center;gap:9px}
.steps .num{font-size:11px;display:grid;place-items:center;width:23px;height:23px;border-radius:50%;background:#e9eee9}
.steps li.active{border-color:var(--teal);color:var(--ink);font-weight:700}
.steps li.active .num,.steps li.done .num{color:white;background:var(--teal)}
.steps li.done{border-color:#71b6a1;color:var(--teal)}

.workspace{display:grid;grid-template-columns:minmax(0,1fr) 338px;gap:20px;align-items:start}
.bench-card{background:white;border:1px solid var(--line);border-radius:13px;overflow:hidden}
.bench-head{display:flex;align-items:center;justify-content:space-between;padding:15px 20px;border-bottom:1px solid var(--line)}
.bench-head strong{font-size:13px}
.bench-head span{font-size:11px;color:var(--muted)}
.scene-scroll{overflow:auto}

.scene{
    display:block;
    width:100%;
    min-width:690px;
    background:#eaf0eb;
    user-select:none;
    touch-action:none;
}

.scene text{font-family:system-ui,sans-serif}
.scene .lcd-number{font-family:"Courier New",monospace;font-weight:700;letter-spacing:-1px}
.scene [role=button]{cursor:pointer;touch-action:none}
.scene .draggable{cursor:grab;touch-action:none}
.scene .draggable:active{cursor:grabbing}
.scene .dragging{filter:drop-shadow(0 10px 8px #10251f40)}
.drop-target{transition:fill .2s,stroke .2s}
.drop-target.over{fill:#b6e8d6;stroke:#087f72;stroke-width:3}
.scene .hint{font-size:11px;fill:#59736a}
.scene .label{font-size:10px;letter-spacing:1.2px;fill:#5c756b;font-weight:650}
.scene .instrument-label{font-size:8px;letter-spacing:1px;fill:#dae6e2}
.scene .tiny{font-size:8px;fill:#36574b}
.flow{stroke-dasharray:5 16;animation:flow 1s linear infinite}
@keyframes flow{to{stroke-dashoffset:-42}}

.instruction{padding:16px 20px;border-top:1px solid var(--line);display:flex;align-items:flex-start;gap:13px;min-height:87px;background:#f7fbf8}
.instruction .dot{color:white;background:var(--teal);width:24px;height:24px;flex-shrink:0;border-radius:50%;display:grid;place-items:center;font-size:12px;margin-top:2px}
.instruction h2{margin:0 0 3px;font-size:14px}
.instruction p{margin:0;font-size:12px;color:var(--muted)}

.controls{padding:15px 19px 17px}
.controls-title{display:flex;justify-content:space-between;gap:10px;font-size:11px;color:var(--muted);margin-bottom:9px}
.controls-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.control{border:1px solid #cfded5;border-radius:6px;background:white;color:var(--ink);padding:8px 7px;font-size:11px;font-weight:600}
.control:hover:enabled{background:var(--mint);border-color:#9bcab8}
.control.primary{background:var(--teal);border-color:var(--teal);color:white}
.control.primary:hover:enabled{background:#09685f}

.notice{font-size:12px;background:#fff6e5;border:1px solid #ebd9b8;color:#755323;border-radius:7px;padding:10px 12px;margin:0 19px 15px}
.mobile-tip{display:none;font-size:11px;color:var(--muted);padding:7px 15px;background:#fff}

.notebook{background:#fff;border:1px solid var(--line);border-radius:13px;padding:22px;min-width:0}
.book-head{display:flex;justify-content:space-between;align-items:center}
.book-head h2{font-family:Georgia,serif;font-size:23px;font-weight:normal;margin:3px 0}
.book-head span{font-size:10px;color:var(--muted);letter-spacing:1px}
.notebook>.intro{color:var(--muted);font-size:12px;margin:9px 0 21px}
.task{padding:17px 0;border-top:1px solid var(--line)}
.task-title{font-size:13px;margin:0 0 5px;font-weight:700;display:flex;gap:8px;align-items:center}
.task-index{font-size:10px;background:#edf1ed;color:var(--muted);padding:2px 6px;border-radius:4px}
.task p{font-size:12px;color:var(--muted);margin:5px 0 11px}
.lock{font-size:12px;color:#7b8a84;display:block;margin-top:8px}
.task label{display:block;font-size:11px;font-weight:650;margin:11px 0 5px}

.input-row{display:flex;border:1px solid #cbd9cf;border-radius:6px;overflow:hidden;background:#fdfefd}
.input-row input{width:100%;min-width:0;border:0;padding:9px 10px;background:transparent;color:var(--ink);font-size:16px}
.input-row span{font-size:11px;align-self:center;padding:0 10px;color:var(--muted)}
.submit{margin-top:9px;width:100%;padding:9px;background:var(--teal);color:white;border-radius:6px;font-size:12px;font-weight:650}
.submit:hover{background:#09685f}

.formula{border-left:2px solid #a2c8b7;padding:7px 10px!important;background:#f2f7f2;color:#244e3f!important;line-height:1.7}
.feedback{font-size:12px;margin:8px 0 0;color:var(--red)}
.feedback:empty{display:none}
.saved{font-size:13px;background:var(--mint);color:#17604c;padding:9px 11px;border-radius:5px;margin:12px 0 0}

.summary{margin-top:20px;padding:22px 24px;background:#e8f3e9;border:1px solid #bbd7c4;border-radius:12px}
.summary h2{font-family:Georgia,serif;font-size:26px;font-weight:normal;margin:0 0 3px}
.summary>p{font-size:13px;margin:3px 0 16px;color:var(--muted)}
.result-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.result{border-right:1px solid #c2d8c8;padding-right:14px}
.result:last-child{border:0}
.result small{font-size:11px;display:block;color:var(--muted)}
.result strong{font-size:25px;font-weight:550;letter-spacing:-.6px}
.result span{font-size:12px}
.summary-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:18px}
.summary-actions button{padding:9px 14px;border-radius:6px;background:var(--ink);color:white;font-size:12px}
.summary-actions span{font-size:11px;color:var(--muted)}

.below{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:18px}
.note{padding:17px 20px;border:1px solid var(--line);border-radius:10px;background:#f2f5ef}
.note h3{font-size:12px;margin:0 0 6px}
.note p,.note li{font-size:12px;color:var(--muted);margin:0}
.note ul{margin:7px 0 0;padding-left:17px}
.note summary{font-size:12px;font-weight:650;cursor:pointer}
.foot{font-size:11px;color:#72847a;margin:20px 0 0;display:flex;justify-content:space-between;gap:20px}
.foot a{color:var(--muted)}

dialog{max-width:370px;border:1px solid var(--line);border-radius:12px;padding:25px;color:var(--ink)}
dialog::backdrop{background:#122e2770}
dialog h2{margin:0;font-size:20px}
dialog p{font-size:13px;color:var(--muted)}
.dialog-actions{display:flex;gap:10px;justify-content:flex-end}
.dialog-actions button{padding:9px 12px;border-radius:6px;background:#eef3ed}
.dialog-actions .primary{background:var(--teal);color:white}

@media(min-width:1300px){
    .workspace{grid-template-columns:minmax(0,1fr) 350px}
}

@media(max-width:1050px){
    .workspace{grid-template-columns:1fr}
    .notebook{display:grid;grid-template-columns:1fr 1fr;gap:0 24px}
    .book-head,.notebook>.intro{grid-column:1/-1}
    .notebook>.intro{margin-bottom:10px}
    .app{padding:20px}
}

@media(max-width:650px){
    .app{padding:16px 10px}
    .top{display:block}
    .equation{margin-top:15px;padding:10px 15px}
    .equation small{display:inline;margin-right:14px}
    .equation strong{font-size:22px}
    .toolbar{margin-top:15px}
    .toolbar .meta{display:none}
    .steps{gap:5px;margin-bottom:12px}
    .steps li{font-size:10px;padding:7px 2px;gap:5px}
    .steps .num{width:19px;height:19px;flex-shrink:0}
    .notebook{display:block;padding:20px}
    .below{grid-template-columns:1fr;gap:10px}
    .controls-grid{grid-template-columns:repeat(2,1fr)}
    .mobile-tip{display:block}
    .result-grid{gap:9px}
    .result strong{font-size:20px}
    .summary{padding:19px 15px}
    .foot{display:block}
    .bench-head{padding:12px 15px}
    .bench-head span{font-size:10px}
}

@media(prefers-reduced-motion:reduce){
    *{animation:none!important;transition:none!important}
}

@media print{
    .toolbar,.controls,.instruction,.scene-scroll,.steps,.notebook,
    .below,.foot,.bench-head,.summary-actions,.notice{
        display:none!important;
    }
    .workspace{display:none}
    .app{padding:0}
    .summary{break-inside:avoid}
    .top{margin-bottom:20px}
}
</style>
</head>

<body>
<main class="app">

<header class="top">
    <div>
        <div class="eyebrow">Fluid mechanics / Experiment 01</div>
        <h1>Pressure has a reference.</h1>
        <p>
            Measure the atmosphere. Connect the apparatus.
            Find the absolute pressure.
        </p>
    </div>

    <div class="equation">
        <small>The relationship</small>
        <strong>
            P<sub>abs</sub> =
            P<sub>gauge</sub> +
            P<sub>atm</sub>
        </strong>
    </div>
</header>

<div class="toolbar">
    <span class="chip">INTERACTIVE LAB</span>
    <span class="meta">Digital instruments · Simulated measurements</span>
    <button id="resetBtn" class="reset">New experiment ↻</button>
</div>

<ol class="steps" aria-label="Experiment progress">
    <li id="step0" class="active">
        <span class="num">1</span>Measure air
    </li>
    <li id="step1">
        <span class="num">2</span>Convert pressure
    </li>
    <li id="step2">
        <span class="num">3</span>Measure vessel
    </li>
    <li id="step3">
        <span class="num">4</span>Find absolute
    </li>
</ol>

<div class="workspace">

<section class="bench-card" aria-label="Interactive laboratory bench">

    <div class="bench-head">
        <strong>The laboratory bench</strong>
        <span id="benchState">Equipment ready</span>
    </div>

    <div class="mobile-tip">
        Swipe across the bench to see everything.
        All actions also have buttons below.
    </div>

    <div class="scene-scroll">

    <svg id="scene"
         class="scene"
         viewBox="0 0 1040 600"
         aria-labelledby="sceneTitle sceneDesc">

        <title id="sceneTitle">
            Interactive pressure measurement apparatus
        </title>

        <desc id="sceneDesc">
            Drag the barometer from the shelf to the open air station.
            After recording atmospheric pressure, move the digital
            gauge to its stand, zero it, connect the hose, and open
            the valve. Equivalent keyboard accessible controls are
            below the bench.
        </desc>

        <defs>
            <linearGradient id="wall" x2="0" y2="1">
                <stop stop-color="#f1f5ef"/>
                <stop offset="1" stop-color="#dfe9df"/>
            </linearGradient>

            <linearGradient id="steel" x2="0" y2="1">
                <stop stop-color="#d0dad5"/>
                <stop offset=".18" stop-color="#f6f8f3"/>
                <stop offset=".5" stop-color="#b8c8bf"/>
                <stop offset=".79" stop-color="#8ba197"/>
                <stop offset="1" stop-color="#d0dbd2"/>
            </linearGradient>

            <linearGradient id="dark" x2="1" y2="1">
                <stop stop-color="#47635b"/>
                <stop offset=".48" stop-color="#263f37"/>
                <stop offset="1" stop-color="#142e27"/>
            </linearGradient>

            <linearGradient id="brass" x2="0" y2="1">
                <stop stop-color="#b18a4a"/>
                <stop offset=".25" stop-color="#efd294"/>
                <stop offset=".58" stop-color="#c5a260"/>
                <stop offset="1" stop-color="#987540"/>
            </linearGradient>

            <linearGradient id="lcd" x2="0" y2="1">
                <stop stop-color="#b7cc9f"/>
                <stop offset="1" stop-color="#d9e5c7"/>
            </linearGradient>

            <linearGradient id="bench" x2="0" y2="1">
                <stop stop-color="#d2d9c9"/>
                <stop offset="1" stop-color="#b5c3af"/>
            </linearGradient>

            <pattern id="grid"
                     width="40"
                     height="40"
                     patternUnits="userSpaceOnUse">
                <path d="M40 0H0V40"
                      fill="none"
                      stroke="#cbd9ce"
                      stroke-width=".6"/>
            </pattern>

            <filter id="shadow"
                    x="-40%"
                    y="-30%"
                    width="190%"
                    height="185%">
                <feDropShadow
                    dx="0"
                    dy="6"
                    stdDeviation="4"
                    flood-color="#244236"
                    flood-opacity=".17"/>
            </filter>
        </defs>

        <!-- Room and workbench -->

        <rect width="1040" height="600" fill="url(#wall)"/>
        <rect width="1040" height="486" fill="url(#grid)"/>

        <path d="M0 492H1040V600H0Z" fill="url(#bench)"/>
        <path d="M0 492H1040" stroke="#92a790" stroke-width="4"/>
        <path d="M0 568H1040V600H0Z" fill="#8fa88f"/>
        <path d="M0 568H1040" stroke="#e3eadd" stroke-width="3"/>

        <!-- Instrument storage -->

        <rect x="24" y="48"
              width="198" height="502"
              rx="8"
              fill="#c5d2c6"
              stroke="#aebfac"/>

        <rect x="36" y="91"
              width="174" height="250"
              rx="4"
              fill="#bacabd"/>

        <rect x="36" y="368"
              width="174" height="172"
              rx="4"
              fill="#bacabd"/>

        <path d="M25 351H221M25 550H221"
              stroke="#78937e"
              stroke-width="9"/>

        <text x="123" y="75"
              text-anchor="middle"
              class="label">INSTRUMENT STORAGE</text>

        <text x="123" y="363"
              text-anchor="middle"
              font-size="8"
              fill="#3f5c4a">01 / BAROMETER</text>

        <text x="123" y="563"
              text-anchor="middle"
              font-size="8"
              fill="#3f5c4a">02 / PRESSURE GAUGE</text>

        <!-- Atmospheric station -->

        <rect x="262" y="79"
              width="247" height="70"
              rx="5"
              fill="#ffffffb0"
              stroke="#d1ddd0"/>

        <text x="280" y="104"
              class="label">A / AMBIENT AIR</text>

        <text x="280" y="125"
              font-size="12"
              fill="#476658">Open sensor vent to the room</text>

        <rect id="airTarget"
              class="drop-target"
              x="277" y="170"
              width="235" height="313"
              rx="18"
              fill="#e5f0e070"
              stroke="#97b69e"
              stroke-dasharray="7 6"/>

        <g id="airGhost" opacity=".55">
            <rect x="340" y="240"
                  width="107" height="189"
                  rx="17"
                  fill="none"
                  stroke="#92aa96"
                  stroke-dasharray="5 5"/>

            <path d="M377 330h34m-17-17v34"
                  stroke="#92aa96"
                  stroke-width="2"/>

            <text x="394" y="460"
                  text-anchor="middle"
                  class="hint">Place barometer here</text>
        </g>

        <ellipse cx="393" cy="482"
                 rx="88" ry="11"
                 fill="#8da08e"
                 opacity=".3"/>

        <path
            d="M294 209q8-9 16 0t16 0m113 0q8-9 16 0t16 0M302 227q8-9 16 0t16 0m103 0q8-9 16 0t16 0"
            fill="none"
            stroke="#84af9c"
            stroke-width="2"/>

        <!-- Vessel station -->

        <rect x="548" y="46"
              width="447" height="39"
              rx="5"
              fill="#ffffff90"
              stroke="#d1ddd0"/>

        <text x="567" y="70"
              class="label">B / SEALED AIR VESSEL</text>

        <text x="974" y="70"
              text-anchor="end"
              font-size="10"
              fill="#59736a">Gauge reference: room air</text>

        <rect id="gaugeTarget"
              class="drop-target"
              x="721" y="113"
              width="181" height="229"
              rx="20"
              fill="#e5f0e040"
              stroke="#a0b9a4"
              stroke-dasharray="7 6"/>

        <text id="gaugeGhost"
              x="812" y="219"
              text-anchor="middle"
              class="hint">Mount gauge here</text>

        <!-- Gauge stand -->

        <rect x="805" y="311"
              width="12" height="187"
              rx="3"
              fill="url(#steel)"
              stroke="#78968a"/>

        <ellipse cx="811" cy="503"
                 rx="64" ry="9"
                 fill="#546f61"/>

        <ellipse cx="811" cy="498"
                 rx="64" ry="9"
                 fill="#9db09d"/>

        <!-- Pressure vessel -->

        <ellipse cx="708" cy="501"
                 rx="156" ry="12"
                 fill="#698272"
                 opacity=".22"/>

        <path d="M603 456v45h35v-45m144 0v45h35v-45"
              fill="#5c7766"/>

        <path d="M592 503h56m124 0h56"
              stroke="#405e4b"
              stroke-width="5"/>

        <rect x="562" y="333"
              width="302" height="146"
              rx="66"
              fill="url(#steel)"
              stroke="#718e7d"
              stroke-width="2"
              filter="url(#shadow)"/>

        <path d="M618 338q-22 69 0 136m190-136q22 69 0 136"
              stroke="#59796a"
              opacity=".5"
              stroke-width="9"
              fill="none"/>

        <path d="M623 339q-22 69 0 133m180-133q22 69 0 133"
              stroke="#e2eae1"
              opacity=".7"
              stroke-width="2"
              fill="none"/>

        <rect x="651" y="381"
              width="123" height="44"
              rx="4"
              fill="#eaf0e2"
              stroke="#99ab96"/>

        <text x="712" y="398"
              text-anchor="middle"
              font-size="9"
              letter-spacing="1.3"
              fill="#3a5748">COMPRESSED AIR</text>

        <text x="712" y="413"
              text-anchor="middle"
              font-size="8"
              fill="#6b8071">SEALED TRAINING VESSEL</text>

        <!-- Pipe and test port -->

        <path d="M862 359H953V380H862Z"
              fill="url(#brass)"
              stroke="#8c7546"/>

        <rect x="855" y="351"
              width="19" height="37"
              rx="3"
              fill="url(#brass)"
              stroke="#8c7546"/>

        <rect x="934" y="352"
              width="17" height="35"
              rx="3"
              fill="url(#brass)"
              stroke="#8c7546"/>

        <circle id="portTarget"
                class="drop-target"
                cx="961" cy="369"
                r="26"
                fill="transparent"
                stroke="#0e8974"
                stroke-dasharray="4 4"
                opacity=".45"/>

        <text x="939" y="414"
              text-anchor="middle"
              class="hint">Test port</text>

        <!-- Interactive valve -->

        <g id="valve"
           role="button"
           tabindex="0"
           aria-label="Open isolation valve">

            <rect x="866" y="317"
                  width="62" height="79"
                  fill="transparent"/>

            <rect x="888" y="337"
                  width="12" height="29"
                  fill="url(#brass)"
                  stroke="#8c7546"/>

            <g id="valveHandle"
               transform="rotate(90 894 344)">

                <rect x="858" y="338"
                      width="72" height="12"
                      rx="6"
                      fill="#b4664a"
                      stroke="#80412e"/>

                <path d="M864 341h58"
                      stroke="#e2a481"
                      stroke-width="2"/>
            </g>

            <circle cx="894" cy="344"
                    r="5"
                    fill="#bfc8bb"
                    stroke="#697d6c"/>
        </g>

        <text id="valveLabel"
              x="894" y="307"
              text-anchor="middle"
              font-size="10"
              font-weight="700"
              fill="#865037">VALVE CLOSED</text>

        <!-- Hose -->

        <g id="hoseGroup" hidden>
            <path id="hoseShadow"
                  d=""
                  fill="none"
                  stroke="#1a302a33"
                  stroke-width="14"
                  transform="translate(0 3)"/>

            <path id="hosePath"
                  d=""
                  fill="none"
                  stroke="#283c33"
                  stroke-width="11"
                  stroke-linecap="round"/>

            <path id="hoseShine"
                  d=""
                  fill="none"
                  stroke="#6b7d69"
                  stroke-width="2"/>

            <path id="flowPath"
                  class="flow"
                  d=""
                  fill="none"
                  stroke="#aadfbd"
                  stroke-width="3"
                  hidden/>

            <text id="hoseHint"
                  x="584" y="550"
                  class="hint">Drag coupling to the test port ↗</text>
        </g>

        <!-- Digital barometer -->

        <g id="barometer"
           class="draggable"
           role="button"
           tabindex="0"
           aria-label="Place digital barometer in ambient air station"
           transform="translate(65 129)">

            <rect x="0" y="0"
                  width="132" height="210"
                  rx="19"
                  fill="url(#dark)"
                  stroke="#1b352b"
                  stroke-width="2"
                  filter="url(#shadow)"/>

            <rect x="6" y="7"
                  width="120" height="195"
                  rx="15"
                  fill="none"
                  stroke="#6e897b"/>

            <path d="M42 12h48m-48 5h48"
                  stroke="#829b8d"
                  stroke-width="2"/>

            <text x="66" y="38"
                  text-anchor="middle"
                  class="instrument-label">DIGITAL BAROMETER</text>

            <rect x="11" y="50"
                  width="110" height="91"
                  rx="7"
                  fill="#12261e"/>

            <rect x="16" y="55"
                  width="100" height="81"
                  rx="3"
                  fill="url(#lcd)"/>

            <text id="baroMode"
                  x="24" y="70"
                  class="tiny">POWER OFF</text>

            <text id="baroDisplay"
                  x="66" y="104"
                  text-anchor="middle"
                  class="lcd-number"
                  font-size="26"
                  fill="#284030">— — —</text>

            <text x="108" y="121"
                  text-anchor="end"
                  font-size="10"
                  fill="#426044">mmHg</text>

            <circle id="baroLed"
                    cx="25" cy="157"
                    r="3"
                    fill="#839583"/>

            <text id="baroStatus"
                  x="34" y="160"
                  font-size="7"
                  fill="#b5cabb">SENSOR OFF</text>

            <g id="baroPower"
               role="button"
               tabindex="0"
               aria-label="Power on barometer">

                <rect x="45" y="167"
                      width="42" height="30"
                      rx="10"
                      fill="#587867"
                      stroke="#789a81"/>

                <path d="M66 173v8m-4-6a7 7 0 1 0 8 0"
                      fill="none"
                      stroke="#e4efe1"
                      stroke-width="1.7"/>
            </g>

            <circle cx="12" cy="191"
                    r="2"
                    fill="#94a99a"/>

            <circle cx="120" cy="191"
                    r="2"
                    fill="#94a99a"/>
        </g>

        <!-- Digital gauge -->

        <g id="gauge"
           class="draggable"
           role="button"
           tabindex="0"
           aria-label="Mount digital gauge on stand"
           transform="translate(50 372) scale(.89)">

            <rect x="61" y="151"
                  width="25" height="34"
                  fill="url(#brass)"
                  stroke="#8e774a"/>

            <path d="M59 163h30m-30 5h30m-30 5h30"
                  stroke="#8e774a"/>

            <rect x="0" y="0"
                  width="148" height="157"
                  rx="37"
                  fill="url(#steel)"
                  stroke="#668172"
                  stroke-width="2"
                  filter="url(#shadow)"/>

            <rect x="9" y="8"
                  width="130" height="140"
                  rx="30"
                  fill="url(#dark)"
                  stroke="#81988a"/>

            <text x="74" y="32"
                  text-anchor="middle"
                  class="instrument-label">DIGITAL GAUGE</text>

            <rect x="19" y="44"
                  width="110" height="64"
                  rx="4"
                  fill="url(#lcd)"
                  stroke="#172f25"
                  stroke-width="4"/>

            <text id="gaugeMode"
                  x="27" y="58"
                  class="tiny">POWER OFF</text>

            <text id="gaugeDisplay"
                  x="75" y="84"
                  text-anchor="middle"
                  class="lcd-number"
                  font-size="28"
                  fill="#284030">— — —</text>

            <text x="118" y="99"
                  text-anchor="end"
                  font-size="9"
                  fill="#426044">kPa · gauge</text>

            <g id="gaugePower"
               role="button"
               tabindex="0"
               aria-label="Power on gauge">

                <rect x="29" y="117"
                      width="36" height="23"
                      rx="7"
                      fill="#587867"
                      stroke="#789a81"/>

                <text x="47" y="132"
                      text-anchor="middle"
                      font-size="8"
                      fill="#eef6e8">ON</text>
            </g>

            <g id="gaugeZero"
               role="button"
               tabindex="0"
               aria-label="Zero gauge to room air">

                <rect x="80" y="117"
                      width="41" height="23"
                      rx="7"
                      fill="#587867"
                      stroke="#789a81"/>

                <text x="100" y="132"
                      text-anchor="middle"
                      font-size="8"
                      fill="#eef6e8">ZERO</text>
            </g>
        </g>

        <!-- Hose coupling -->

        <g id="coupling"
           class="draggable"
           role="button"
           tabindex="0"
           aria-label="Connect hose coupling to vessel test port"
           transform="translate(634 520)"
           hidden>

            <circle r="28" fill="transparent"/>

            <rect x="-19" y="-9"
                  width="34" height="18"
                  rx="3"
                  fill="url(#brass)"
                  stroke="#8c7546"/>

            <rect x="6" y="-12"
                  width="11" height="24"
                  rx="2"
                  fill="url(#steel)"
                  stroke="#667e6f"/>

            <path d="M-15-9v18m5-18v18m5-18v18"
                  stroke="#8c7546"/>
        </g>

    </svg>
    </div>

    <div class="instruction" role="status" aria-live="polite">
        <span class="dot" id="instructionNumber">1</span>
        <div>
            <h2 id="instructionTitle">
                Place the barometer in room air
            </h2>
            <p id="instructionText">
                Drag the barometer from the top shelf to station A.
                Its display stays off until you power it on.
            </p>
        </div>
    </div>

    <div class="controls">
        <div class="controls-title">
            <strong>Bench controls</strong>
            <span>Use the equipment or these buttons</span>
        </div>

        <div class="controls-grid">
            <button id="placeBaro" class="control primary">
                Place barometer
            </button>
            <button id="powerBaro" class="control" disabled>
                Power barometer
            </button>
            <button id="mountGauge" class="control" disabled>
                Mount gauge
            </button>
            <button id="powerGauge" class="control" disabled>
                Power gauge
            </button>
            <button id="zeroGauge" class="control" disabled>
                Zero to room air
            </button>
            <button id="connectHose" class="control" disabled>
                Connect hose
            </button>
            <button id="toggleValve" class="control" disabled>
                Open valve
            </button>
            <button id="ventLine" class="control" disabled>
                Vent gauge line
            </button>
            <button id="disconnectHose" class="control" disabled>
                Disconnect hose
            </button>
        </div>
    </div>

    <div id="notice"
         class="notice"
         role="status"
         aria-live="polite"
         hidden></div>

</section>

<!-- Student notebook -->

<aside class="notebook" aria-label="Student lab notebook">

    <div class="book-head">
        <h2>Lab notebook</h2>
        <span id="trialTag">TRIAL 01</span>
    </div>

    <p class="intro">
        Read each instrument yourself. Your next calculation
        unlocks after you record the measurement.
    </p>

    <section class="task">
        <h3 class="task-title">
            <span class="task-index">01</span>
            Atmospheric reading
        </h3>

        <span class="lock" id="baroLock">
            Waiting for a stable barometer reading.
        </span>

        <form id="baroForm" hidden>
            <p>Copy the displayed reading to two decimal places.</p>

            <label for="baroInput">Barometer reading</label>

            <div class="input-row">
                <input id="baroInput"
                       type="number"
                       step="0.01"
                       inputmode="decimal"
                       autocomplete="off"
                       required>
                <span>mmHg</span>
            </div>

            <button class="submit">Record reading</button>

            <p id="baroFeedback"
               class="feedback"
               role="alert"></p>
        </form>

        <div id="baroSaved" class="saved" hidden></div>
    </section>

    <section class="task">
        <h3 class="task-title">
            <span class="task-index">02</span>
            Atmospheric pressure
        </h3>

        <span class="lock" id="atmLock">
            Record the barometer reading first.
        </span>

        <form id="atmForm" hidden>
            <p>
                Calculate atmospheric pressure in kPa using
                your barometer reading.
            </p>

            <label for="atmInput">
                Calculated P<sub>atm</sub> · round to 2 decimals
            </label>

            <div class="input-row">
                <input id="atmInput"
                       type="number"
                       step="0.01"
                       inputmode="decimal"
                       autocomplete="off"
                       required>
                <span>kPa</span>
            </div>

            <button class="submit">Check calculation</button>

            <p id="atmFeedback"
               class="feedback"
               role="alert"></p>

            <div id="atmHint"
                 class="notice"
                 style="margin:10px 0 0"
                 hidden>
                Hint: The barometer reads mmHg, but your answer
                must be in kPa. Think about which pressure-unit
                conversion you need.
            </div>
        </form>

        <div id="atmSaved" class="saved" hidden></div>
    </section>

    <section class="task">
        <h3 class="task-title">
            <span class="task-index">03</span>
            Gauge reading
        </h3>

        <span class="lock" id="gaugeLock">
            Complete the atmospheric calculation first.
        </span>

        <form id="gaugeForm" hidden>
            <p>
                With the valve open, wait for STABLE on the gauge.
            </p>

            <label for="gaugeInput">
                Recorded P<sub>gauge</sub> · two decimal places
            </label>

            <div class="input-row">
                <input id="gaugeInput"
                       type="number"
                       step="0.01"
                       inputmode="decimal"
                       autocomplete="off"
                       required>
                <span>kPa</span>
            </div>

            <button class="submit">Record reading</button>

            <p id="gaugeFeedback"
               class="feedback"
               role="alert"></p>
        </form>

        <div id="gaugeSaved" class="saved" hidden></div>
    </section>

    <section class="task">
        <h3 class="task-title">
            <span class="task-index">04</span>
            Absolute pressure
        </h3>

        <span class="lock" id="absLock">
            Record a stable gauge pressure first.
        </span>

        <form id="absForm" hidden>
            <p class="formula">
                P<sub>abs</sub> =
                P<sub>gauge</sub> +
                P<sub>atm</sub><br>
                Use your recorded values in kPa.
            </p>

            <label for="absInput">
                Calculated P<sub>abs</sub> · round to 2 decimals
            </label>

            <div class="input-row">
                <input id="absInput"
                       type="number"
                       step="0.01"
                       inputmode="decimal"
                       autocomplete="off"
                       required>
                <span>kPa</span>
            </div>

            <button class="submit">Complete experiment</button>

            <p id="absFeedback"
               class="feedback"
               role="alert"></p>
        </form>

        <div id="absSaved" class="saved" hidden></div>
    </section>

</aside>
</div>

<section id="summary"
         class="summary"
         hidden
         aria-live="polite">

    <div class="eyebrow">Experiment complete</div>
    <h2>Same pressure. Different reference.</h2>

    <p>
        The gauge measures above room pressure.
        Absolute pressure includes the atmosphere.
    </p>

    <div class="result-grid">
        <div class="result">
            <small>Gauge pressure</small>
            <strong id="resultGauge"></strong>
            <span>kPa</span>
        </div>

        <div class="result">
            <small>Atmospheric pressure</small>
            <strong id="resultAtm"></strong>
            <span>kPa</span>
        </div>

        <div class="result">
            <small>Absolute pressure</small>
            <strong id="resultAbs"></strong>
            <span>kPa</span>
        </div>
    </div>

    <div class="summary-actions">
        <button id="downloadCsv">
            Download lab record (.csv)
        </button>
        <span>
            Finish at the bench: close the valve,
            vent the line, then disconnect.
        </span>
    </div>
</section>

<div class="below">
    <div class="note">
        <h3>Why does the gauge read zero in room air?</h3>
        <p>
            A gauge compares its inlet pressure with atmospheric
            pressure. When both sides are at room pressure, the
            difference is zero. Zero gauge pressure does not mean
            zero absolute pressure.
        </p>
    </div>

    <div class="note">
        <details>
            <summary>How this virtual apparatus behaves</summary>
            <ul>
                <li>
                    The digital barometer reports pressure in mmHg;
                    it has no physical mercury column.
                    Convert the pressure unit to kPa.
                </li>
                <li>
                    The gauge line fills gradually from a sealed
                    vessel. This model assumes the vessel is much
                    larger than the hose, so its pressure stays
                    effectively constant.
                </li>
                <li>
                    Closing the isolation valve traps pressure in
                    the line. Venting the isolated line returns
                    its gauge pressure to zero.
                </li>
                <li>
                    Each new experiment uses new simulated pressures.
                    Download your record before refreshing;
                    this page does not submit grades.
                </li>
            </ul>
        </details>
    </div>
</div>

<footer class="foot">
    <span>PRESSURE LAB / Learn by measuring</span>
    <span>
        Conversion reference:
        <a href="https://www.nist.gov/document/18-appdx-e-19-h133-finalpdf"
           target="_blank"
           rel="noopener noreferrer">
            NIST Handbook 133, Appendix E
        </a>
    </span>
</footer>

</main>

<!-- Reset confirmation -->

<dialog id="resetDialog">
    <h2>Start a new experiment?</h2>
    <p>
        This clears your notebook and generates new pressures.
        Download a completed record first if you want to keep it.
    </p>
    <div class="dialog-actions">
        <button id="cancelReset">Keep working</button>
        <button id="confirmReset" class="primary">Start new</button>
    </div>
</dialog>

<!-- Opens only after the third incorrect atmospheric calculation -->

<dialog id="hintDialog">
    <h2>A small hint</h2>
    <p>
        The barometer reads mmHg, but your answer must be in kPa.
        Think about which pressure-unit conversion you need.
    </p>
    <div class="dialog-actions">
        <button id="closeHint" class="primary">Try again</button>
    </div>
</dialog>

<script>
'use strict';

// ============================================================
// INTERNAL SETTINGS
// These settings are not displayed in the student interface.
// ============================================================

const $ = id => document.getElementById(id);

const MMHG_TO_KPA = 0.1333224;

// Accept answers within ±5% of the corresponding reference.
const ANSWER_TOLERANCE = 0.05;

const HOMES = {
    barometer:{x:65,y:129,k:1},
    gauge:{x:50,y:372,k:.89}
};

const DOCKS = {
    barometer:{x:327,y:267,k:1},
    gauge:{x:737,y:146,k:1}
};

const LOOSE = {x:634,y:520};
const PORT = {x:961,y:369};

let s;
let trial = 0;
let activeDrag = null;
let lastTick = performance.now();

const round2 = value =>
    Math.round((value + Number.EPSILON) * 100) / 100;

const show = (id, visible) => {
    $(id).toggleAttribute('hidden', !visible);
};

const text = (id, value) => {
    if ($(id).textContent !== value) {
        $(id).textContent = value;
    }
};

function log(action) {
    s.events.push({
        at:new Date().toISOString(),
        action
    });
}

function notice(message) {
    text('notice', message);
    show('notice', !!message);
}

function setPosition(id, position) {
    $(id).setAttribute(
        'transform',
        `translate(${position.x} ${position.y}) scale(${position.k ?? 1})`
    );
}

function atStage() {
    return s.absRecorded !== null ? 4 :
           s.gaugeRecorded !== null ? 3 :
           s.atmRecorded !== null ? 2 :
           s.baroRecorded !== null ? 1 : 0;
}

function gaugeStable() {
    return (
        s.connected &&
        s.valveOpen &&
        !s.venting &&
        s.line === s.vesselPressure
    );
}

// Inclusive lower and upper limits.
// A tiny numerical allowance handles floating-point arithmetic.
function withinTolerance(answer, reference) {
    return (
        Number.isFinite(answer) &&
        answer >= 0 &&
        Math.abs(answer - reference) <=
            Math.abs(reference) * ANSWER_TOLERANCE + 1e-9
    );
}

// Calculate from the experiment references.
// This prevents accepted errors from accumulating across stages.
function atmosphericReference() {
    return round2(s.baroPressure * MMHG_TO_KPA);
}

function absoluteReference() {
    return round2(
        s.vesselPressure + atmosphericReference()
    );
}

// ============================================================
// NEW EXPERIMENT
// ============================================================

function reset() {
    if (activeDrag) {
        cancelDrag();
    }

    trial++;

    if ($('hintDialog').open) {
        $('hintDialog').close();
    }

    s = {
        // Generated with two decimal places.
        // Atmospheric reading: 735.00 to 769.99 mmHg.
        baroPressure:
            (Math.floor(Math.random() * 3500) + 73500) / 100,

        // Vessel gauge pressure: 20.00 to 79.99 kPa.
        vesselPressure:
            (Math.floor(Math.random() * 6000) + 2000) / 100,

        baroPlaced:false,
        baroOn:false,
        baroStable:false,
        baroStart:0,

        gaugePlaced:false,
        gaugeOn:false,
        zeroed:false,

        connected:false,
        valveOpen:false,
        venting:false,
        line:0,

        baroRecorded:null,
        atmRecorded:null,
        gaugeRecorded:null,
        absRecorded:null,

        // Resets for every new experiment.
        atmFailures:0,

        started:new Date().toISOString(),
        completed:null,
        events:[]
    };

    for (const kind of ['baro','atm','gauge','abs']) {
        $(kind + 'Form').reset();
        text(kind + 'Feedback', '');
    }

    setPosition('barometer', HOMES.barometer);
    setPosition('gauge', HOMES.gauge);
    setPosition('coupling', LOOSE);

    notice('');

    text(
        'trialTag',
        `TRIAL ${String(trial).padStart(2, '0')}`
    );

    log('Experiment started');
    render();
}

// ============================================================
// BAROMETER
// ============================================================

function placeBarometer() {
    if (s.baroPlaced) return;

    s.baroPlaced = true;

    setPosition('barometer', DOCKS.barometer);

    log('Barometer placed in room air');
    notice('');
    render();
}

function powerBarometer() {
    if (!s.baroPlaced) {
        return notice(
            'Place the barometer at station A before powering it on.'
        );
    }

    if (s.baroOn) return;

    s.baroOn = true;
    s.baroStart = performance.now();

    log('Barometer powered on');
    notice('');
    render();
}

// ============================================================
// GAUGE AND HOSE
// ============================================================

function mountGauge() {
    if (s.atmRecorded === null) {
        return notice(
            'Record the barometer reading and calculate ' +
            'atmospheric pressure before setting up the gauge.'
        );
    }

    if (s.gaugePlaced) return;

    s.gaugePlaced = true;
    setPosition('gauge', DOCKS.gauge);

    log('Gauge mounted on stand');
    notice('');
    render();
}

function powerGauge() {
    if (!s.gaugePlaced) {
        return notice('Mount the gauge on its stand first.');
    }

    if (s.gaugeOn) return;

    s.gaugeOn = true;

    log('Gauge powered on, inlet open to atmosphere');
    notice('');
    render();
}

function zeroGauge() {
    if (!s.gaugeOn) {
        return notice(
            'Mount and power the gauge before zeroing it.'
        );
    }

    if (s.connected || s.line > .001) {
        return notice(
            'Zero the gauge with its inlet disconnected ' +
            'and open to room air.'
        );
    }

    if (s.zeroed) return;

    s.zeroed = true;

    log('Gauge zero checked against room air');
    notice('');
    render();
}

function connectHose() {
    if (!s.zeroed) {
        return notice(
            'Mount the gauge, power it on, and check its ' +
            'zero in room air before connecting.'
        );
    }

    if (s.valveOpen || s.venting) {
        return notice(
            'Close the valve and finish venting ' +
            'before connecting the hose.'
        );
    }

    if (s.connected) return;

    s.connected = true;
    setPosition('coupling', PORT);

    log('Hose coupled with valve closed');
    notice('');
    render();
}

function toggleValve() {
    if (!s.connected) {
        return notice(
            'Connect and latch the hose before ' +
            'opening the isolation valve.'
        );
    }

    if (s.venting) {
        return notice(
            'Let the line finish venting before reopening the valve.'
        );
    }

    s.valveOpen = !s.valveOpen;

    log(
        s.valveOpen
            ? 'Isolation valve opened'
            : 'Isolation valve closed; line pressure trapped'
    );

    notice(
        s.valveOpen
            ? ''
            : 'Valve closed. Any pressure in the hose is trapped; ' +
              'use Vent gauge line to release it.'
    );

    render();
}

function ventLine() {
    if (s.valveOpen) {
        return notice(
            'Close the isolation valve before venting the gauge line.'
        );
    }

    if (!s.connected || s.line === 0 || s.venting) return;

    s.venting = true;

    log('Gauge line vent opened with vessel isolated');

    notice(
        'Venting the isolated gauge line to room air. ' +
        'The vessel stays pressurized.'
    );

    render();
}

function disconnectHose() {
    if (!s.connected) return;

    if (s.valveOpen || s.line > 0 || s.venting) {
        return notice(
            'Close the isolation valve and vent the ' +
            'line to zero before disconnecting.'
        );
    }

    s.connected = false;
    setPosition('coupling', LOOSE);

    log('Hose disconnected at zero gauge pressure');

    notice(
        'Hose disconnected. The vessel valve is closed ' +
        'and the gauge line is at room pressure.'
    );

    render();
}

// ============================================================
// PROCEDURE INSTRUCTIONS
// ============================================================

function instruction() {
    if (s.absRecorded !== null) {
        if (s.valveOpen) {
            return [
                'Measurement complete',
                'Close the valve, vent the gauge line, and ' +
                'disconnect to leave the apparatus ready.'
            ];
        }

        if (s.line > 0) {
            return [
                'Release the trapped line pressure',
                'Use Vent gauge line. Closing the isolation ' +
                'valve does not remove pressure from the hose.'
            ];
        }

        if (s.connected) {
            return [
                'The line is at room pressure',
                'Disconnect the hose. Your completed lab ' +
                'record is ready below.'
            ];
        }

        return [
            'Experiment complete',
            'The vessel is isolated and the gauge is disconnected. ' +
            'Download your record or start a new experiment.'
        ];
    }

    if (s.baroRecorded === null) {
        if (!s.baroPlaced) {
            return [
                'Place the barometer in room air',
                'Drag the barometer from the top shelf to station A. ' +
                'Its display stays off until you power it on.'
            ];
        }

        if (!s.baroOn) {
            return [
                'Power on the barometer',
                'Press the power button on the instrument, ' +
                'or use Power barometer below.'
            ];
        }

        if (!s.baroStable) {
            return [
                'Let the barometer settle',
                'The sensor is sampling room air. Record a reading ' +
                'only when the display says STABLE.'
            ];
        }

        return [
            'Read and record the barometer',
            'Copy the reading from its screen into notebook ' +
            'entry 01, including the decimal.'
        ];
    }

    if (s.atmRecorded === null) {
        return [
            'Convert the atmospheric reading to kPa',
            'Use your barometer reading to calculate atmospheric ' +
            'pressure in kPa. Enter your result to two decimal places.'
        ];
    }

    if (s.gaugeRecorded === null) {
        if (!s.gaugePlaced) {
            return [
                'Mount the digital gauge',
                'Drag it from the lower shelf to the stand above the vessel.'
            ];
        }

        if (!s.gaugeOn) {
            return [
                'Power on the gauge',
                'The inlet is open to the room, so the initial ' +
                'gauge pressure is zero.'
            ];
        }

        if (!s.zeroed) {
            return [
                'Check the atmospheric zero',
                'Press ZERO on the gauge while its inlet ' +
                'is still open to room air.'
            ];
        }

        if (!s.connected) {
            return [
                'Connect the hose with the valve closed',
                'Drag the brass hose coupling to the vessel ' +
                'test port until it snaps into place.'
            ];
        }

        if (s.venting) {
            return [
                'Venting the gauge line',
                'Wait until the isolated gauge line returns to zero.'
            ];
        }

        if (!s.valveOpen) {
            return [
                'Open the isolation valve',
                'Click the red handle. A handle parallel to the pipe ' +
                'means open; across the pipe means closed.'
            ];
        }

        if (!gaugeStable()) {
            return [
                'Watch the pressure equalize',
                'Air enters the gauge line. Wait for the digital ' +
                'reading to stabilize before recording it.'
            ];
        }

        return [
            'Record the stable gauge reading',
            'Read the kPa value on the gauge and enter it ' +
            'in notebook entry 03.'
        ];
    }

    return [
        'Calculate the absolute pressure',
        'Add your recorded gauge and atmospheric pressures ' +
        'in notebook entry 04.'
    ];
}

// ============================================================
// LIVE DISPLAYS — ALWAYS TWO DECIMAL PLACES
// ============================================================

function renderInstruments() {
    text(
        'baroMode',
        !s.baroOn
            ? 'POWER OFF'
            : s.baroStable
                ? 'STABLE'
                : 'SAMPLING'
    );

    let reading = '— — —';

    if (s.baroOn) {
        const elapsed =
            (performance.now() - s.baroStart) / 1000;

        const variation = s.baroStable
            ? 0
            : 1.8 * Math.exp(-elapsed) * Math.sin(elapsed * 8);

        reading = (s.baroPressure + variation).toFixed(2);
    }

    text('baroDisplay', reading);

    text(
        'baroStatus',
        s.baroStable
            ? 'AMBIENT AIR'
            : s.baroOn
                ? 'PLEASE WAIT'
                : 'SENSOR OFF'
    );

    $('baroLed').setAttribute(
        'fill',
        s.baroStable
            ? '#9bd69c'
            : s.baroOn
                ? '#ecc26e'
                : '#839583'
    );

    const mode =
        !s.gaugeOn ? 'POWER OFF' :
        s.venting ? 'VENTING' :
        !s.zeroed ? 'CHECK ZERO' :
        !s.connected ? 'ZERO / AIR' :
        s.valveOpen
            ? (gaugeStable() ? 'STABLE' : 'FILLING')
            : (s.line > 0 ? 'ISOLATED' : 'READY / ZERO');

    text('gaugeMode', mode);

    text(
        'gaugeDisplay',
        s.gaugeOn ? s.line.toFixed(2) : '— — —'
    );

    show('flowPath', s.valveOpen && !gaugeStable());
}

function hosePath(end) {
    const path =
        `M811 331 C811 490 ${end.x + 75} 552 ${end.x} ${end.y}`;

    for (const id of [
        'hoseShadow',
        'hosePath',
        'hoseShine',
        'flowPath'
    ]) {
        $(id).setAttribute('d', path);
    }
}

// ============================================================
// UPDATE INTERFACE
// ============================================================

function render() {
    const stage = atStage();

    for (let i = 0; i < 4; i++) {
        $('step' + i).className =
            i < stage ? 'done' :
            i === stage ? 'active' : '';

        if (i === stage) {
            $('step' + i).setAttribute('aria-current', 'step');
        } else {
            $('step' + i).removeAttribute('aria-current');
        }
    }

    const instructions = instruction();

    text('instructionTitle', instructions[0]);
    text('instructionText', instructions[1]);

    text(
        'instructionNumber',
        stage === 4 ? '✓' : String(stage + 1)
    );

    const benchState =
        s.venting ? 'Venting line' :
        s.valveOpen
            ? (gaugeStable() ? 'Pressure stable' : 'Line pressurizing')
            : s.connected
                ? (s.line > 0 ? 'Line isolated' : 'Hose connected')
                : s.gaugePlaced
                    ? 'Gauge station ready'
                    : s.baroOn
                        ? (
                            s.baroStable
                                ? 'Ambient reading stable'
                                : 'Sampling ambient air'
                        )
                        : 'Equipment ready';

    text('benchState', benchState);

    show('airGhost', !s.baroPlaced);
    show('gaugeGhost', !s.gaugePlaced);
    show('hoseGroup', s.gaugePlaced);
    show('coupling', s.gaugePlaced);
    show('hoseHint', s.gaugePlaced && !s.connected);

    $('airTarget').setAttribute(
        'stroke-dasharray',
        s.baroPlaced ? 'none' : '7 6'
    );

    $('gaugeTarget').setAttribute(
        'stroke-dasharray',
        s.gaugePlaced ? 'none' : '7 6'
    );

    $('portTarget').setAttribute(
        'opacity',
        s.zeroed && !s.connected ? '1' : '.25'
    );

    $('valveHandle').setAttribute(
        'transform',
        `rotate(${s.valveOpen ? 0 : 90} 894 344)`
    );

    text(
        'valveLabel',
        s.valveOpen ? 'VALVE OPEN' : 'VALVE CLOSED'
    );

    $('valve').setAttribute(
        'aria-label',
        s.valveOpen
            ? 'Close isolation valve'
            : 'Open isolation valve'
    );

    if (!activeDrag || activeDrag.id !== 'coupling') {
        hosePath(s.connected ? PORT : LOOSE);
    }

    const allowed = {
        placeBaro:
            !s.baroPlaced,

        powerBaro:
            s.baroPlaced && !s.baroOn,

        mountGauge:
            s.atmRecorded !== null && !s.gaugePlaced,

        powerGauge:
            s.gaugePlaced && !s.gaugeOn,

        zeroGauge:
            s.gaugeOn && !s.zeroed && !s.connected,

        connectHose:
            s.zeroed &&
            !s.connected &&
            !s.valveOpen &&
            !s.venting,

        toggleValve:
            s.connected && !s.venting,

        ventLine:
            s.connected &&
            !s.valveOpen &&
            s.line > 0 &&
            !s.venting,

        disconnectHose:
            s.connected &&
            !s.valveOpen &&
            s.line === 0 &&
            !s.venting
    };

    for (const [id, enabled] of Object.entries(allowed)) {
        $(id).disabled = !enabled;

        $(id).classList.toggle(
            'primary',
            enabled && !['ventLine', 'disconnectHose'].includes(id)
        );
    }

    text(
        'toggleValve',
        s.valveOpen ? 'Close valve' : 'Open valve'
    );

    // The hint remains available after the third failed attempt.
    show(
        'atmHint',
        s.atmFailures >= 3 && s.atmRecorded === null
    );

    const visible = {
        baro:
            s.baroStable && s.baroRecorded === null,

        atm:
            s.baroRecorded !== null && s.atmRecorded === null,

        gauge:
            s.atmRecorded !== null && s.gaugeRecorded === null,

        abs:
            s.gaugeRecorded !== null && s.absRecorded === null
    };

    const recordKeys = {
        baro:'baroRecorded',
        atm:'atmRecorded',
        gauge:'gaugeRecorded',
        abs:'absRecorded'
    };

    for (const [key, isVisible] of Object.entries(visible)) {
        const recorded = s[recordKeys[key]] !== null;

        show(key + 'Form', isVisible);
        show(key + 'Lock', !isVisible && !recorded);
        show(key + 'Saved', recorded);
    }

    const ready = gaugeStable();

    $('gaugeInput').disabled = !ready;
    $('gaugeForm').querySelector('button').disabled = !ready;

    if (s.baroRecorded !== null) {
        text(
            'baroSaved',
            `✓ ${s.baroRecorded.toFixed(2)} mmHg recorded`
        );
    }

    if (s.atmRecorded !== null) {
        text(
            'atmSaved',
            `✓ ${s.atmRecorded.toFixed(2)} kPa calculated`
        );
    }

    if (s.gaugeRecorded !== null) {
        text(
            'gaugeSaved',
            `✓ ${s.gaugeRecorded.toFixed(2)} kPa recorded`
        );
    }

    if (s.absRecorded !== null) {
        text(
            'absSaved',
            `✓ ${s.absRecorded.toFixed(2)} kPa absolute`
        );
    }

    show('summary', s.absRecorded !== null);

    if (s.absRecorded !== null) {
        text('resultGauge', s.gaugeRecorded.toFixed(2));
        text('resultAtm', s.atmRecorded.toFixed(2));
        text('resultAbs', s.absRecorded.toFixed(2));
    }

    renderInstruments();
}

// ============================================================
// STUDENT ANSWERS
// ============================================================

function readNumber(id, feedbackId) {
    const raw = $(id).value.trim();
    const value = Number(raw);

    if (raw === '' || !Number.isFinite(value)) {
        text(feedbackId, 'Enter a numerical value first.');
        return null;
    }

    return value;
}

function feedback(id, message) {
    text(id, message);
}

// Barometer recording
$('baroForm').addEventListener('submit', event => {
    event.preventDefault();

    if (!s.baroStable || s.baroRecorded !== null) return;

    const answer = readNumber('baroInput', 'baroFeedback');

    if (answer === null) return;

    if (!withinTolerance(answer, s.baroPressure)) {
        return feedback(
            'baroFeedback',
            'Recheck the barometer display and try again.'
        );
    }

    s.baroRecorded = round2(answer);

    log('Barometer reading recorded');
    notice('');
    render();

    $('atmInput').focus({preventScroll:true});
});

// Atmospheric calculation
$('atmForm').addEventListener('submit', event => {
    event.preventDefault();

    if (s.baroRecorded === null || s.atmRecorded !== null) return;

    const answer = readNumber('atmInput', 'atmFeedback');

    if (answer === null) return;

    const correct = atmosphericReference();

    if (!withinTolerance(answer, correct)) {
        s.atmFailures++;

        feedback(
            'atmFeedback',
            'That answer is not accepted. ' +
            'Check your calculation and try again.'
        );

        show('atmHint', s.atmFailures >= 3);

        // Pop up once, immediately after the third incorrect answer.
        if (s.atmFailures === 3) {
            $('hintDialog').showModal();
        }

        return;
    }

    s.atmRecorded = round2(answer);

    log('Atmospheric pressure calculation accepted');
    notice('');
    render();
});

// Gauge recording
$('gaugeForm').addEventListener('submit', event => {
    event.preventDefault();

    if (!gaugeStable() || s.gaugeRecorded !== null) return;

    const answer = readNumber('gaugeInput', 'gaugeFeedback');

    if (answer === null) return;

    if (!withinTolerance(answer, s.vesselPressure)) {
        return feedback(
            'gaugeFeedback',
            'Recheck the stable gauge display and try again.'
        );
    }

    s.gaugeRecorded = round2(answer);

    log('Stable gauge pressure recorded with valve open');
    notice('');
    render();

    $('absInput').focus({preventScroll:true});
});

// Absolute-pressure calculation
$('absForm').addEventListener('submit', event => {
    event.preventDefault();

    if (s.gaugeRecorded === null || s.absRecorded !== null) return;

    const answer = readNumber('absInput', 'absFeedback');

    if (answer === null) return;

    const correct = absoluteReference();

    if (!withinTolerance(answer, correct)) {
        return feedback(
            'absFeedback',
            'Check your calculation using both pressures in kPa, ' +
            'then try again.'
        );
    }

    s.absRecorded = round2(answer);
    s.completed = new Date().toISOString();

    log('Absolute pressure calculation accepted');
    notice('');
    render();
});

// ============================================================
// BUTTON CONTROLS
// ============================================================

const actions = {
    placeBaro:placeBarometer,
    powerBaro:powerBarometer,
    mountGauge,
    powerGauge,
    zeroGauge,
    connectHose,
    toggleValve,
    ventLine,
    disconnectHose
};

for (const [id, action] of Object.entries(actions)) {
    $(id).addEventListener('click', action);
}

function bindSvgButton(id, action) {
    $(id).addEventListener('pointerdown', event => {
        event.stopPropagation();
    });

    $(id).addEventListener('click', event => {
        event.stopPropagation();
        action();
    });

    $(id).addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            event.stopPropagation();
            action();
        }
    });
}

bindSvgButton('baroPower', powerBarometer);
bindSvgButton('gaugePower', powerGauge);
bindSvgButton('gaugeZero', zeroGauge);
bindSvgButton('valve', toggleValve);

// ============================================================
// DRAG AND DROP
// ============================================================

function point(event) {
    const p = $('scene').createSVGPoint();

    p.x = event.clientX;
    p.y = event.clientY;

    return p.matrixTransform(
        $('scene').getScreenCTM().inverse()
    );
}

function inRect(p, x, y, width, height) {
    return (
        p.x >= x &&
        p.x <= x + width &&
        p.y >= y &&
        p.y <= y + height
    );
}

function validDrop(id, p) {
    if (id === 'barometer') {
        return inRect(p, 277, 170, 235, 313);
    }

    if (id === 'gauge') {
        return inRect(p, 710, 105, 203, 243);
    }

    return Math.hypot(
        p.x - PORT.x,
        p.y - PORT.y
    ) < 52;
}

function home(id) {
    if (id === 'barometer') {
        return s.baroPlaced ? DOCKS.barometer : HOMES.barometer;
    }

    if (id === 'gauge') {
        return s.gaugePlaced ? DOCKS.gauge : HOMES.gauge;
    }

    return s.connected ? PORT : LOOSE;
}

function target(id) {
    return id === 'barometer'
        ? 'airTarget'
        : id === 'gauge'
            ? 'gaugeTarget'
            : 'portTarget';
}

function cancelDrag() {
    if (!activeDrag) return;

    const {id, pointerId} = activeDrag;

    if ($(id).hasPointerCapture(pointerId)) {
        $(id).releasePointerCapture(pointerId);
    }

    $(id).classList.remove('dragging');
    $(target(id)).classList.remove('over');

    setPosition(id, home(id));

    activeDrag = null;
    render();
}

function setupDrag(id, action) {
    const element = $(id);

    element.addEventListener('keydown', event => {
        if (event.target !== element) return;

        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            action();
        }
    });

    element.addEventListener('pointerdown', event => {
        if (event.button !== 0 || activeDrag) return;

        if (
            (id === 'barometer' && s.baroPlaced) ||
            (id === 'gauge' && s.gaugePlaced) ||
            (id === 'coupling' && s.connected)
        ) {
            return;
        }

        event.preventDefault();

        activeDrag = {
            id,
            pointerId:event.pointerId,
            start:point(event),
            origin:home(id),
            moved:false
        };

        element.setPointerCapture(event.pointerId);
        element.classList.add('dragging');

        notice('');
    });

    element.addEventListener('pointermove', event => {
        if (
            !activeDrag ||
            activeDrag.id !== id ||
            activeDrag.pointerId !== event.pointerId
        ) {
            return;
        }

        const p = point(event);
        const drag = activeDrag;

        const dx = p.x - drag.start.x;
        const dy = p.y - drag.start.y;

        if (Math.hypot(dx, dy) > 6) {
            drag.moved = true;
        }

        const position = {
            x:drag.origin.x + dx,
            y:drag.origin.y + dy,
            k:drag.origin.k
        };

        setPosition(id, position);

        if (id === 'coupling') {
            hosePath(position);
        }

        $(target(id)).classList.toggle(
            'over',
            validDrop(id, p)
        );
    });

    element.addEventListener('pointerup', event => {
        if (
            !activeDrag ||
            activeDrag.id !== id ||
            activeDrag.pointerId !== event.pointerId
        ) {
            return;
        }

        const drag = activeDrag;
        const p = point(event);

        activeDrag = null;

        element.releasePointerCapture(event.pointerId);
        element.classList.remove('dragging');
        $(target(id)).classList.remove('over');

        setPosition(id, home(id));

        if (!drag.moved || validDrop(id, p)) {
            action();
        } else {
            notice(
                id === 'barometer'
                    ? 'Place the barometer inside station A.'
                    : id === 'gauge'
                        ? 'Place the gauge in the stand above the vessel.'
                        : 'Bring the coupling to the brass test port ' +
                          'on the right side of the valve.'
            );
        }

        render();
    });

    element.addEventListener('pointercancel', () => {
        if (activeDrag?.id === id) {
            cancelDrag();
        }
    });

    element.addEventListener('lostpointercapture', () => {
        if (activeDrag?.id === id) {
            cancelDrag();
        }
    });
}

setupDrag('barometer', placeBarometer);
setupDrag('gauge', mountGauge);
setupDrag('coupling', connectHose);

// ============================================================
// TOUCH PANNING
// ============================================================

let benchPan = null;

$('scene').addEventListener('pointerdown', event => {
    if (
        event.pointerType === 'mouse' ||
        event.target.closest('.draggable,[role="button"]')
    ) {
        return;
    }

    const scroll = document.querySelector('.scene-scroll');

    benchPan = {
        id:event.pointerId,
        x:event.clientX,
        y:event.clientY,
        left:scroll.scrollLeft,
        top:window.scrollY
    };

    $('scene').setPointerCapture(event.pointerId);
});

$('scene').addEventListener('pointermove', event => {
    if (!benchPan || benchPan.id !== event.pointerId) return;

    document.querySelector('.scene-scroll').scrollLeft =
        benchPan.left + benchPan.x - event.clientX;

    window.scrollTo(
        window.scrollX,
        benchPan.top + benchPan.y - event.clientY
    );
});

for (const eventName of [
    'pointerup',
    'pointercancel',
    'lostpointercapture'
]) {
    $('scene').addEventListener(eventName, event => {
        if (benchPan?.id === event.pointerId) {
            benchPan = null;
        }
    });
}

document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && activeDrag) {
        cancelDrag();
    }
});

window.addEventListener('blur', () => {
    if (activeDrag) {
        cancelDrag();
    }
});

// ============================================================
// HINT AND RESET DIALOGS
// ============================================================

$('closeHint').addEventListener('click', () => {
    $('hintDialog').close();
    $('atmInput').focus({preventScroll:true});
});

$('resetBtn').addEventListener('click', () => {
    $('resetDialog').showModal();
});

$('cancelReset').addEventListener('click', () => {
    $('resetDialog').close();
});

$('confirmReset').addEventListener('click', () => {
    $('resetDialog').close();
    reset();
});

// ============================================================
// DOWNLOAD STUDENT RECORD
// ============================================================

$('downloadCsv').addEventListener('click', () => {
    if (s.absRecorded === null) return;

    const rows = [
        ['Pressure Lab', 'Experiment record'],
        ['Trial', trial],
        ['Started (UTC)', s.started],
        ['Completed (UTC)', s.completed],
        [],
        ['Quantity', 'Student value', 'Unit'],
        ['Barometer reading', s.baroRecorded.toFixed(2), 'mmHg'],
        ['Atmospheric pressure', s.atmRecorded.toFixed(2), 'kPa'],
        ['Gauge pressure', s.gaugeRecorded.toFixed(2), 'kPa'],
        ['Absolute pressure', s.absRecorded.toFixed(2), 'kPa'],
        [],
        ['Method', 'P_abs = P_gauge + P_atm'],
        ['Data type', 'Simulated instructional measurements'],
        [],
        ['Time (UTC)', 'Procedure event'],
        ...s.events.map(event => [
            event.at,
            event.action
        ])
    ];

    const csv = rows.map(row =>
        row.map(value =>
            '"' + String(value).replaceAll('"', '""') + '"'
        ).join(',')
    ).join('\r\n');

    const url = URL.createObjectURL(
        new Blob(
            ['\ufeff' + csv],
            {type:'text/csv;charset=utf-8;'}
        )
    );

    const link = document.createElement('a');

    link.href = url;
    link.download = `pressure-lab-trial-${trial}.csv`;

    document.body.appendChild(link);
    link.click();
    link.remove();

    setTimeout(() => URL.revokeObjectURL(url), 1000);
});

// ============================================================
// RUN THE SIMULATION
// ============================================================

reset();

setInterval(() => {
    const now = performance.now();

    const dt = Math.min(
        (now - lastTick) / 1000,
        .25
    );

    lastTick = now;

    let changed = false;
    const wasStable = gaugeStable();

    // Barometer becomes stable after sampling.
    if (
        s.baroOn &&
        !s.baroStable &&
        now - s.baroStart >= 2300
    ) {
        s.baroStable = true;

        log('Barometer reading stable');
        changed = true;
    }

    // Open valve: gradually pressurize the gauge line.
    if (s.valveOpen && s.connected) {
        s.line +=
            (s.vesselPressure - s.line) *
            (1 - Math.exp(-dt / .55));

        if (s.vesselPressure - s.line < .03) {
            s.line = s.vesselPressure;
        }

    // Closed valve with vent open: depressurize the line.
    } else if (s.venting) {
        s.line *= Math.exp(-dt / .4);

        if (s.line < .03) {
            s.line = 0;
            s.venting = false;

            log('Gauge line vented to atmosphere');

            notice(
                'Gauge line at zero. You may disconnect the hose ' +
                'or reopen the valve for another reading.'
            );

            changed = true;
        }
    }

    // Closing the valve without venting traps pressure in the line.
    if (wasStable !== gaugeStable()) {
        changed = true;

        if (gaugeStable()) {
            log('Gauge pressure stable');
        }
    }

    if (changed) {
        render();
    } else {
        renderInstruments();
    }

}, 100);

</script>
</body>
</html>
"""

if hasattr(st, "iframe"):
    st.iframe(
        LAB_HTML,
        height="content",
        tab_index=0,
    )
else:
    import streamlit.components.v1 as components

    components.html(
        LAB_HTML,
        height=1350,
        scrolling=True,
        tab_index=0,
    )
