(function () {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("lesson") || "03";
  const lesson = window.COURSE_DECKS && window.COURSE_DECKS[id];
  const root = document.getElementById("deck");

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
  const list = (items, className = "") => `<ul class="${className}">${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
  const cards = (items) => `<div class="grid-three">${items.map((item) => `<div class="card"><strong>${escapeHtml(item[0])}</strong>${escapeHtml(item[1])}</div>`).join("")}</div>`;
  const section = (eyebrow, title, body) => `<section><p class="eyebrow">${escapeHtml(eyebrow)}</p><h2>${escapeHtml(title)}</h2>${body}</section>`;

  if (!lesson) {
    root.innerHTML = section("课程课件", "没有找到这节课", `<p class="lead">请从课件目录重新选择。课程编号：${escapeHtml(id)}</p>`);
  } else {
    document.title = `${lesson.title}｜CTF 网络安全实战基础`;
    root.innerHTML = [
      `<section><p class="eyebrow">CTF 网络安全实战基础 · ${escapeHtml(lesson.week)}</p><h1>${escapeHtml(lesson.title)}</h1><p class="lead">${escapeHtml(lesson.hook)}</p><p class="meta">${escapeHtml(lesson.track)} · 95 分钟 · Signal / Trace</p></section>`,
      section("今天能带走什么", "三个目标", cards(lesson.goals.map((goal, index) => [`0${index + 1}`, goal]))),
      section("先抓住主线", lesson.focusTitle, `<div class="panel">${escapeHtml(lesson.focus)}</div>`),
      section("概念地图", "四个关键点", cards(lesson.concepts)),
      section("课堂主线", "把猜想变成证据", list(lesson.activity, "step-list")),
      section("检查点", lesson.checkTitle, `<p class="lead">${escapeHtml(lesson.check)}</p>`),
      section("可选探索", "感兴趣再继续", `<div class="panel"><span class="warm">Optional</span><p>${escapeHtml(lesson.optional)}</p></div>`),
      section("安全加餐", lesson.snackTitle, `<p class="lead">${escapeHtml(lesson.snack)}</p>`),
      section("课后轻任务", lesson.taskTitle, `<p>${escapeHtml(lesson.task)}</p><p class="meta">不要求连续打卡；可以提交卡点记录。</p>`),
      `<section><p class="eyebrow">本节收束</p><h2>${escapeHtml(lesson.takeaway)}</h2><p class="lead">${escapeHtml(lesson.next)}</p></section>`
    ].join("");
  }

  Reveal.initialize({ hash: true, slideNumber: "c/t", transition: "fade", transitionSpeed: "fast" });
}());
