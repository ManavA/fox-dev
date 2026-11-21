# Logic prototype

One self-contained HTML file that lets anyone drive a state model by clicking buttons. Use it when the question is about business logic, state transitions or data shape: things that read fine on paper and only feel wrong once pushed through real cases.

1. **State the question** in one visible paragraph at the top of the page, so the answer can be checked against it later.
2. **Isolate the logic** in one `<script>` block written as a small pure module that could be lifted into the real code: a reducer `(state, action) => state`, an explicit state machine (when "which actions are legal now" is part of the question), pure functions over a plain type, or a class that owns its state. No DOM inside it; the page calls in, nothing calls out.
3. **Build the page** with plain HTML/CSS/JS, inline, no build, opens by double-click. Labels use domain language, not code names. Top to bottom:
   - title and the question;
   - the full current state as labelled fields, re-rendered after every click, with what just changed called out;
   - free-play buttons, one per action;
   - guided scenarios, one per tab: a short description and the ordered buttons to press. Cover the happy path, a tricky edge case, and an attempt at something that should be illegal.
4. **Hand it over.** The useful moments are "wait, that should not be possible": bugs in the idea.
5. **Capture.** Lift the validated module into the real code, put the verdict in the spec, and keep the HTML shell on a throwaway branch.

Avoid: a framework or bundler, persistence, logic tangled into click handlers, scenarios that only show the happy path.
