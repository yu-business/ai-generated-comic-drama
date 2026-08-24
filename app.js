const storageKey = "ai-comic-drama-workbench";

const defaultState = {
  project: {
    title: "逆光重生",
    genre: "都市情感",
    platform: "抖音短剧",
    hook: "女主在订婚夜发现背叛，意外获得重启人生的机会，用冷静和智慧夺回主动权。"
  },
  characters: [
    {
      name: "林晚",
      role: "女主",
      description: "外表温柔，内心清醒，擅长隐藏情绪。"
    },
    {
      name: "顾承安",
      role: "男主",
      description: "克制冷峻的投资人，观察力极强。"
    }
  ],
  scenes: [
    {
      title: "订婚宴前夜",
      visual: "华丽酒店宴会厅，水晶灯落在香槟塔上，林晚站在人群边缘听见未婚夫的秘密通话。",
      dialogue: "林晚：原来这场婚约，从一开始就是骗局。",
      shot: "近景",
      mood: "紧张",
      duration: 5
    },
    {
      title: "重启瞬间",
      visual: "雨夜街口，车灯刺破水雾，林晚回头看见手机日期回到三个月前。",
      dialogue: "旁白：这一次，她不会再把命运交给任何人。",
      shot: "特写",
      mood: "惊讶",
      duration: 6
    }
  ],
  selectedScene: 0
};

let state = loadState();

const sections = document.querySelectorAll(".section");
const navItems = document.querySelectorAll(".nav-item");
const projectForm = document.querySelector("#projectForm");
const sceneForm = document.querySelector("#sceneForm");
const sceneList = document.querySelector("#sceneList");
const characterList = document.querySelector("#characterList");
const timelinePreview = document.querySelector("#timelinePreview");

function loadState() {
  const saved = localStorage.getItem(storageKey);
  if (!saved) return structuredClone(defaultState);

  try {
    return { ...structuredClone(defaultState), ...JSON.parse(saved) };
  } catch {
    return structuredClone(defaultState);
  }
}

function saveState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function setSection(id) {
  sections.forEach((section) => section.classList.toggle("active", section.id === id));
  navItems.forEach((item) => item.classList.toggle("active", item.dataset.section === id));
}

function renderProject() {
  projectForm.title.value = state.project.title;
  projectForm.genre.value = state.project.genre;
  projectForm.platform.value = state.project.platform;
  projectForm.hook.value = state.project.hook;
}

function renderStats() {
  document.querySelector("#sceneCount").textContent = state.scenes.length;
  document.querySelector("#characterCount").textContent = state.characters.length;
  document.querySelector("#promptCount").textContent = state.scenes.length * 2;

  timelinePreview.innerHTML = state.scenes
    .map((scene, index) => `<div class="timeline-item">S${String(index + 1).padStart(2, "0")} · ${escapeHtml(scene.title)} · ${scene.duration}s</div>`)
    .join("");
}

function renderCharacters() {
  characterList.innerHTML = state.characters
    .map(
      (character, index) => `
        <article class="character-card">
          <label>姓名<input data-character="${index}" data-field="name" value="${escapeAttr(character.name)}"></label>
          <label>身份<input data-character="${index}" data-field="role" value="${escapeAttr(character.role)}"></label>
          <label>人物描述<textarea rows="4" data-character="${index}" data-field="description">${escapeHtml(character.description)}</textarea></label>
        </article>
      `
    )
    .join("");
}

function renderScenes() {
  sceneList.innerHTML = state.scenes
    .map(
      (scene, index) => `
        <button class="scene-card ${index === state.selectedScene ? "active" : ""}" data-scene="${index}">
          <strong>S${String(index + 1).padStart(2, "0")} · ${escapeHtml(scene.title)}</strong>
          <span>${escapeHtml(scene.shot)} / ${escapeHtml(scene.mood)} / ${scene.duration}s</span>
        </button>
      `
    )
    .join("");

  const scene = state.scenes[state.selectedScene];
  document.querySelector("#currentSceneLabel").textContent = `Scene ${String(state.selectedScene + 1).padStart(2, "0")}`;
  sceneForm.title.value = scene.title;
  sceneForm.visual.value = scene.visual;
  sceneForm.dialogue.value = scene.dialogue;
  sceneForm.shot.value = scene.shot;
  sceneForm.mood.value = scene.mood;
  sceneForm.duration.value = scene.duration;
  document.querySelector("#durationValue").textContent = `${scene.duration} 秒`;
}

function renderPrompts() {
  const scene = state.scenes[state.selectedScene];
  const cast = state.characters.map((character) => `${character.name}（${character.role}：${character.description}）`).join("；");

  document.querySelector("#imagePrompt").textContent = [
    `作品：${state.project.title}`,
    `类型：${state.project.genre}`,
    `角色：${cast}`,
    `画面：${scene.visual}`,
    `镜头：${scene.shot}`,
    `情绪：${scene.mood}`,
    "风格：高质量国漫短剧分镜，电影级灯光，清晰人物表情，竖屏构图，细节丰富。"
  ].join("\n");

  document.querySelector("#videoPrompt").textContent = [
    `时长：${scene.duration} 秒`,
    `平台：${state.project.platform}`,
    `场景：${scene.title}`,
    `动作与氛围：${scene.visual}`,
    `台词：${scene.dialogue}`,
    `运镜：${scene.shot}，轻微推镜，节奏紧凑，情绪从克制到爆发。`
  ].join("\n");
}

function renderAll() {
  renderProject();
  renderStats();
  renderCharacters();
  renderScenes();
  renderPrompts();
}

function updateSelectedScene(field, value) {
  state.scenes[state.selectedScene][field] = field === "duration" ? Number(value) : value;
  saveState();
  renderStats();
  renderScenes();
  renderPrompts();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("'", "&#39;");
}

navItems.forEach((item) => {
  item.addEventListener("click", () => setSection(item.dataset.section));
});

projectForm.addEventListener("input", (event) => {
  state.project[event.target.name] = event.target.value;
  saveState();
  renderPrompts();
});

sceneForm.addEventListener("input", (event) => {
  updateSelectedScene(event.target.name, event.target.value);
});

sceneList.addEventListener("click", (event) => {
  const card = event.target.closest("[data-scene]");
  if (!card) return;
  state.selectedScene = Number(card.dataset.scene);
  saveState();
  renderScenes();
  renderPrompts();
});

characterList.addEventListener("input", (event) => {
  const index = Number(event.target.dataset.character);
  const field = event.target.dataset.field;
  state.characters[index][field] = event.target.value;
  saveState();
  renderStats();
  renderPrompts();
});

document.querySelector("#addSceneBtn").addEventListener("click", () => {
  state.scenes.push({
    title: `新分镜 ${state.scenes.length + 1}`,
    visual: "描述这个镜头里的人物、环境、动作和关键道具。",
    dialogue: "输入台词或旁白。",
    shot: "中景",
    mood: "紧张",
    duration: 5
  });
  state.selectedScene = state.scenes.length - 1;
  saveState();
  setSection("storyboard");
  renderAll();
});

document.querySelector("#duplicateSceneBtn").addEventListener("click", () => {
  const scene = structuredClone(state.scenes[state.selectedScene]);
  scene.title = `${scene.title} 副本`;
  state.scenes.splice(state.selectedScene + 1, 0, scene);
  state.selectedScene += 1;
  saveState();
  renderAll();
});

document.querySelector("#addCharacterBtn").addEventListener("click", () => {
  state.characters.push({
    name: "新角色",
    role: "身份",
    description: "补充外貌、性格、动机和关系。"
  });
  saveState();
  renderAll();
});

document.querySelector("#copyPromptBtn").addEventListener("click", async () => {
  const promptText = `${document.querySelector("#imagePrompt").textContent}\n\n${document.querySelector("#videoPrompt").textContent}`;
  await navigator.clipboard.writeText(promptText);
});

document.querySelector("#exportBtn").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(state, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "ai-comic-drama-project.json";
  link.click();
  URL.revokeObjectURL(url);
});

renderAll();
