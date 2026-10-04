/* Explainer web toolkit · inlined by `explainer sync`. Edit explainer_kit/web/explainer.js, not a page copy.
 *
 * Explainer.model          values from model.yaml (the page's <script id="explainer-model"> block)
 * Explainer.tracker(v)     one shared value; .get() .set(v) .on(fn)
 * Explainer.slider(el, t, opts)   range input bound to a tracker; presets set the value exactly
 * Explainer.bars(el, opts) bar chart that keeps each bar's identity; returns update(values)
 * Explainer.predict(el, opts)     predict-first gate: hides [data-after=id] until the reader commits
 * Explainer.video(el, opts)       video that stops at predict pauses from the render's timeline.json
 * Explainer.store                 per-reader storage that never throws (private windows, blocked storage)
 */
const Explainer = (() => {
  const store = {
    get(key, fallback = null) {
      try { const v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); } catch { return fallback; }
    },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* storage unavailable */ } },
  };

  const model = (() => {
    try { return JSON.parse(document.getElementById("explainer-model")?.textContent || "{}"); } catch { return {}; }
  })();

  function tracker(initial) {
    let value = initial;
    const subs = new Set();
    return {
      get: () => value,
      set(v) { if (v === value) return; value = v; subs.forEach((fn) => fn(value)); },
      on(fn) { subs.add(fn); fn(value); return () => subs.delete(fn); },
    };
  }

  // Escape text that comes from the reader (typed predictions). Author strings may contain markup like <sub>.
  const esc = (x) => String(x).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  function el(tag, attrs = {}, html = "") {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
    if (html) node.innerHTML = html;
    return node;
  }

  /* Slider. With `log`, the input moves in log10 space. Presets set the tracker to the exact preset value,
   * not to the nearest slider step (a 0.005 step would turn 0.5 into 0.501). */
  function slider(root, t, { id, label, min, max, log = false, step, presets = [], format = (x) => x.toFixed(2),
                              thermal = false, scale } = {}) {
    id = id || `ex-slider-${Math.random().toString(36).slice(2, 8)}`;
    const toInput = (v) => (log ? Math.log10(v) : v);
    const fromInput = (x) => (log ? 10 ** x : x);
    root.classList.add("ex-control");
    root.innerHTML = `<div class="ex-control-head"><label for="${id}">${label}</label>
      <span class="ex-value" aria-live="polite"></span></div>
      <input type="range" id="${id}" ${thermal ? 'class="ex-thermal"' : ""} min="${toInput(min)}" max="${toInput(max)}"
        step="${step ?? (toInput(max) - toInput(min)) / 400}">
      ${scale ? `<div class="ex-scale" aria-hidden="true">${scale.map((s) => `<span>${s}</span>`).join("")}</div>` : ""}
      ${presets.length ? `<div class="ex-presets" role="group" aria-label="${label} presets">${presets
        .map((p) => `<button type="button" data-v="${p.value ?? p}">${p.label ?? format(p.value ?? p)}</button>`).join("")}</div>` : ""}`;
    const input = root.querySelector("input");
    const out = root.querySelector(".ex-value");
    input.addEventListener("input", () => t.set(fromInput(parseFloat(input.value))));
    root.querySelectorAll(".ex-presets button").forEach((b) => b.addEventListener("click", () => t.set(parseFloat(b.dataset.v))));
    t.on((v) => {
      if (Number.isFinite(v)) input.value = toInput(Math.min(Math.max(v, min), max));
      out.textContent = format(v);
      input.setAttribute("aria-valuetext", format(v));
      root.querySelectorAll(".ex-presets button").forEach((b) =>
        b.setAttribute("aria-pressed", String(Math.abs(parseFloat(b.dataset.v) - v) < 1e-12)));
    });
    return input;
  }

  /* Bars. `labels` is fixed; update(values) changes heights so each bar stays the same object. */
  function bars(root, { labels, sublabels = [], colors = [], max = 1, format = (x) => x.toFixed(3), tip } = {}) {
    root.innerHTML = "";
    const chart = el("div", { class: "ex-bars", role: "img", "aria-label": `Bar chart: ${labels.join(", ")}` });
    chart.style.setProperty("--n", labels.length);
    const names = el("div", { class: "ex-bar-labels" });
    names.style.setProperty("--n", labels.length);
    const tipEl = el("div", { class: "ex-tip" });
    tipEl.hidden = true;
    let current = labels.map(() => 0);
    const cols = labels.map((name, i) => {
      const col = el("div", { class: "ex-bar-col", tabindex: "0" }, `<span class="ex-bar-val num"></span><div class="ex-bar"></div>`);
      if (colors[i]) col.querySelector(".ex-bar").style.setProperty("--c", colors[i]);
      const show = () => {
        tipEl.textContent = tip ? tip(i, current[i]) : `${name} · ${format(current[i])}`;
        tipEl.style.left = `${col.offsetLeft + col.offsetWidth / 2}px`;
        tipEl.style.top = `${col.offsetTop + col.offsetHeight * (1 - Math.min(current[i] / max, 1)) - 28}px`;
        tipEl.hidden = false;
      };
      ["mouseenter", "focus"].forEach((e) => col.addEventListener(e, show));
      ["mouseleave", "blur"].forEach((e) => col.addEventListener(e, () => (tipEl.hidden = true)));
      chart.appendChild(col);
      names.appendChild(el("span", {}, `${name}${sublabels[i] ? `<small>${sublabels[i]}</small>` : ""}`));
      return col;
    });
    chart.appendChild(tipEl);
    root.append(chart, names);
    return function update(values) {
      current = values;
      cols.forEach((col, i) => {
        col.querySelector(".ex-bar").style.height = `${Math.max((values[i] / max) * 100, 0.4)}%`;
        col.querySelector(".ex-bar-val").textContent = format(values[i]);
      });
    };
  }

  /* Predict-first gate. The reader commits a prediction before the answer appears.
   * Elements with data-after="<id>" stay hidden until then. The prediction is kept per reader. */
  function predict(root, { id, question, type = "number", choices = [], unit = "", answer, judge, explain = "" }) {
    const key = `explainer:${location.pathname}:predict:${id}`;
    root.classList.add("ex-predict");
    root.innerHTML = `<span class="ex-predict-head">Predict first</span><p>${question}</p>
      <form>${type === "choice"
        ? choices.map((c, i) => `<label class="ex-choice"><input type="radio" name="${id}" value="${i}" required> ${c}</label>`).join("")
        : `<input type="${type === "number" ? "number" : "text"}" step="any" name="${id}" aria-label="Your prediction" required> ${unit}`}
        <button type="submit" class="ex-primary">Commit prediction</button></form>
      <div class="ex-result" aria-live="polite" hidden></div>`;
    const form = root.querySelector("form");
    const result = root.querySelector(".ex-result");
    const gated = () => document.querySelectorAll(`[data-after="${id}"]`);
    gated().forEach((g) => { g.classList.add("ex-gated"); g.hidden = true; });

    function reveal(guess) {
      const shown = type === "choice" ? choices[guess] : `${esc(guess)} ${unit}`.trim();
      const correct = answer === undefined ? null : judge ? judge(guess) : type === "choice" ? guess === answer : null;
      const verdict = correct === null ? "" : correct ? '<span class="ex-good">matches</span>' : '<span class="ex-bad">does not match</span>';
      const answerText = answer === undefined ? "" : type === "choice" ? choices[answer] : `${answer} ${unit}`.trim();
      result.innerHTML = `Your prediction: <strong>${shown}</strong>${answerText ? ` · Result: <strong>${answerText}</strong> ${verdict}` : ""}${explain ? `<br>${explain}` : ""}`;
      result.hidden = false;
      form.querySelectorAll("input, button").forEach((x) => (x.disabled = true));
      gated().forEach((g) => (g.hidden = false));
      root.dispatchEvent(new CustomEvent("predicted", { detail: { guess } }));
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = new FormData(form).get(id);
      const guess = type === "choice" ? Number(data) : type === "number" ? Number(data) : String(data);
      store.set(key, guess);
      reveal(guess);
    });
    const saved = store.get(key);
    if (saved !== null) reveal(saved);
    return { reveal };
  }

  /* Video with predict pauses. `timeline` is the render's timeline.json (object or URL). At each predict
   * event the video pauses and asks for a prediction; the reader continues after committing one. */
  async function video(root, { src, poster, captions, timeline }) {
    root.classList.add("ex-video");
    root.innerHTML = `<video controls preload="metadata" playsinline ${poster ? `poster="${poster}"` : ""}>
        <source src="${src}" type="video/mp4">${captions ? `<track kind="captions" src="${captions}" srclang="en" label="English">` : ""}
      </video><div class="ex-overlay" hidden><div></div></div><div class="ex-chapters"></div>`;
    const v = root.querySelector("video");
    const overlay = root.querySelector(".ex-overlay");
    let events = [];
    try {
      const data = typeof timeline === "string" ? await (await fetch(timeline)).json() : timeline;
      events = (data?.events || []).filter((e) => e.kind === "predict");
    } catch { /* no timeline: plain video */ }
    const done = new Set();
    const chapters = root.querySelector(".ex-chapters");
    events.forEach((e, i) => {
      const b = el("button", { type: "button" }, `Predict ${i + 1} · ${Math.floor(e.t / 60)}:${String(Math.floor(e.t % 60)).padStart(2, "0")}`);
      b.addEventListener("click", () => { v.currentTime = Math.max(e.t - 0.5, 0); v.play(); });
      chapters.appendChild(b);
    });
    v.addEventListener("timeupdate", () => {
      const e = events.find((e, i) => !done.has(i) && v.currentTime >= e.t + 1.2 && v.currentTime < e.t + 6);
      if (!e) return;
      const i = events.indexOf(e);
      done.add(i);
      v.pause();
      const box = overlay.firstElementChild;
      predict(box, { id: `video-${i}`, question: e.question, type: "text" });
      box.addEventListener("predicted", () => {
        const go = el("button", { type: "button", class: "ex-primary" }, "Continue the video");
        go.addEventListener("click", () => { overlay.hidden = true; v.play(); });
        box.appendChild(go);
        go.focus();
      }, { once: true });
      overlay.hidden = false;
    });
    return v;
  }

  return { model, store, tracker, slider, bars, predict, video };
})();
