// A slider with a play/pause button that steps through `values`, for use with view().
// Dragging the slider scrubs; pressing play advances one step every `delay` ms and
// starts over from the beginning if it's already at the end.
import {html} from "npm:htl";

export function scrubber(values, {initial = values.length - 1, delay = 500, format = (v) => v, label = ""} = {}) {
  const form = html`<form class="scrubber">
    <button name="b" type="button" class="play-button" aria-label="Play"></button>
    <label>
      <input name="i" type="range" min="0" max=${values.length - 1} value=${initial} step="1" />
      <output name="o"></output>
    </label>
    ${label ? html`<span class="scrubber-label">${label}</span>` : ""}
  </form>`;
  let timer = null;

  function show() {
    const i = form.i.valueAsNumber;
    form.value = values[i];
    form.o.value = format(values[i], i, values);
  }
  function stop() {
    clearInterval(timer);
    timer = null;
    form.b.classList.remove("playing");
    form.b.setAttribute("aria-label", "Play");
  }
  function step() {
    // Stop quietly if the page re-rendered this cell and the old form was removed.
    if (!form.isConnected) return stop();
    if (form.i.valueAsNumber >= values.length - 1) return stop();
    form.i.valueAsNumber += 1;
    show();
    form.dispatchEvent(new Event("input", {bubbles: true}));
  }
  function start() {
    if (form.i.valueAsNumber >= values.length - 1) {
      form.i.valueAsNumber = 0;
      show();
      form.dispatchEvent(new Event("input", {bubbles: true}));
    }
    timer = setInterval(step, delay);
    form.b.classList.add("playing");
    form.b.setAttribute("aria-label", "Pause");
  }

  form.b.onclick = () => (timer ? stop() : start());
  form.i.oninput = (e) => {
    e.stopPropagation(); // re-dispatched from the form with the new value
    show();
    form.dispatchEvent(new Event("input", {bubbles: true}));
  };
  form.onsubmit = (e) => e.preventDefault();
  show();
  return form;
}
