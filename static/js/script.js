window.addEventListener("load", () => {
  setTimeout(() => {
    document.getElementById("loader").style.opacity = "0";
    document.getElementById("loader").style.pointerEvents = "none";
  }, 700);
});

const menuBtn = document.getElementById("menuBtn");
const navLinks = document.getElementById("navLinks");
const navItems = document.querySelectorAll(".nav-links a");

if (menuBtn && navLinks) {
    menuBtn.addEventListener("click", () => {
        navLinks.classList.toggle("show");
        menuBtn.innerHTML = navLinks.classList.contains("show")
            ? '<i class="fa-solid fa-xmark"></i>'
            : '<i class="fa-solid fa-bars"></i>';
    });
}

function toggleDropdown() {
  document.getElementById("userDropdown").classList.toggle("show");
}

window.onclick = function (event) {
  if (!event.target.closest(".user-dropdown")) {
    let dropdown = document.getElementById("userDropdown");
    if (dropdown.classList.contains("show")) {
      dropdown.classList.remove("show");
    }
  }
};
navItems.forEach((item) => {
  item.addEventListener("click", () => {
    navLinks.classList.remove("show");
    menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
  });
});

window.addEventListener("scroll", () => {
  const sections = document.querySelectorAll("section[id]");
  const scrollY = window.pageYOffset;

  sections.forEach((section) => {
    const sectionHeight = section.offsetHeight;
    const sectionTop = section.offsetTop - 130;
    const sectionId = section.getAttribute("id");
    const activeLink = document.querySelector(
      `.nav-links a[href="#${sectionId}"]`,
    );

    if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
      navItems.forEach((link) => link.classList.remove("active"));
      if (activeLink) activeLink.classList.add("active");
    }
  });
});


// ================= On Screen Chatbot Assistant =================
const chatbotToggle = document.getElementById("chatbotToggle");
const chatbotBox = document.getElementById("chatbotBox");
const chatbotClose = document.getElementById("chatbotClose");
const chatbotForm = document.getElementById("chatbotForm");
const chatbotInput = document.getElementById("chatbotInput");
const chatbotMessages = document.getElementById("chatbotMessages");
const quickButtons = document.querySelectorAll(".chatbot-quick-actions button");

const botAnswers = [
  {
    keywords: ["appointment", "appoint", "doctor", "booking", "book"],
    answer:
      "To book a doctor appointment: 1) Click the Doctor's Appointment menu or Book Appointment button. 2) Go to the Appointment Booking section. 3) Click the Book Appointment button. 4) Fill your name, mobile, problem and message in the contact/booking form.",
    linkText: "Go to Appointment",
    link: appointmentURL,
  },
  {
    keywords: ["diet", "nutrition", "planner", "food", "workout"],
    answer:
      "To open AI Diet Planner: go to the Services area and choose AI Diet Planner / Smart Nutrition. Add your dietary preference, fitness goal, lifestyle, restrictions, health condition and query. Then click Get Recommendation.",
    linkText: "Diet Planner",
    link: diet_plannerURL,
  },
  {
    keywords: ["disease", "deasis", "know", "symptom", "detect", "image"],
    answer:
      "For Know Your Disease using AI/ML: open the Services section, choose Know Your Disease, then enter symptoms or upload an image if your AI model page supports it. The system can guide about possible disease information, but final confirmation should always be from a doctor.",
    linkText: "Know Your Disease",
    link: "#services",
  },
  {
    keywords: ["first", "aid", "emergency", "cut", "snake", "heart", "blood"],
    answer:
      "For First Aid Guide: click First Aid from the navbar or hero button. Select the emergency type and follow the step-by-step instructions. For serious cases, call emergency medical help immediately.",
    linkText: "First Aid Guide",
    link: frist_aidURL,
  },
  {
    keywords: ["awareness", "aware", "tips", "health", "lifestyle"],
    answer:
      "For Health Awareness: open the Awareness section to read health tips, lifestyle guidance, campaigns, regular checkup advice, sleep, food and mental wellbeing tips.",
    linkText: "Health Awareness",
    link: health_awarenessURL,
  },
  {
    keywords: ["contact", "support", "message", "help", "phone", "email"],
    answer:
      "For support: go to Contact Us, enter your name, email, mobile number and message. Then click Send Message.",
    linkText: "Contact Us",
    link: "#contact",
  },
];

function toggleChatbot(show) {
  chatbotBox.classList.toggle("active", show);
  if (show) chatbotInput.focus();
}

function addMessage(text, type = "bot", linkText = "", link = "") {
  const msg = document.createElement("div");
  msg.className = `${type}-message message`;
  msg.innerHTML = text;

  if (linkText && link) {
    const btn = document.createElement("a");
    btn.href = link;
    btn.className = "chatbot-link";
    btn.textContent = linkText;
    btn.addEventListener("click", () => {
      if (link.startsWith("#")) toggleChatbot(false);
    });
    msg.appendChild(document.createElement("br"));
    msg.appendChild(btn);
  }

  chatbotMessages.appendChild(msg);
  chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

function getBotReply(question) {
  const q = question.toLowerCase();
  return (
    botAnswers.find((item) => item.keywords.some((word) => q.includes(word))) || {
      answer:
        "I can guide you about: Book Appointment, AI Diet Planner, Know Your Disease using AI/ML, First Aid, Awareness, Login and Contact Support. Please type one of these topics.",
      linkText: "View Services",
      link: "#services",
    }
  );
}

function sendChatMessage(question) {
  const cleanQuestion = question.trim();
  if (!cleanQuestion) return;

  addMessage(cleanQuestion, "user");

  setTimeout(() => {
    const reply = getBotReply(cleanQuestion);
    addMessage(reply.answer, "bot", reply.linkText, reply.link);
  }, 350);
}

if (chatbotToggle && chatbotBox) {
  chatbotToggle.addEventListener("click", () => {
    toggleChatbot(!chatbotBox.classList.contains("active"));
  });

  chatbotClose.addEventListener("click", () => toggleChatbot(false));

  chatbotForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendChatMessage(chatbotInput.value);
    chatbotInput.value = "";
  });

  quickButtons.forEach((btn) => {
    btn.addEventListener("click", () => sendChatMessage(btn.dataset.question));
  });

  setTimeout(() => {
    if (!chatbotBox.classList.contains("active")) {
      addMessage("Need help? Click the chat icon and I will show where each feature is.");
    }
  }, 1800);
}
