/**
 * AI-Powered Portfolio Management & Dynamic Resume Generator
 * Single Page Application Logic
 */

let currentPortfolio = null;
let currentJDAnalysis = null;
let selectedCategory = "profile";
let editingEntryId = null; // null = Add, number = Edit

// Initialize App
document.addEventListener("DOMContentLoaded", async () => {
    setupTabNavigation();
    setupEventListeners();
    await loadConfigStatus();
    await loadPortfolioData();
    await loadSampleJDs();
});

// Toast notification helper
function showToast(message, type = "info") {
    const container = document.getElementById("toastContainer");
    if (!container) return;
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// Tab navigation handler
function setupTabNavigation() {
    const navButtons = document.querySelectorAll(".nav-tab-btn");
    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.getAttribute("data-tab");
            switchTab(targetTab);
        });
    });

    const subTabButtons = document.querySelectorAll(".sub-tab-btn");
    subTabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            subTabButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            selectedCategory = btn.getAttribute("data-subtab");
            renderDatabaseTable();
        });
    });
}

function switchTab(tabId) {
    document.querySelectorAll(".nav-tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

    const activeBtn = document.querySelector(`.nav-tab-btn[data-tab="${tabId}"]`);
    const activePane = document.getElementById(`tab-${tabId}`);

    if (activeBtn) activeBtn.classList.add("active");
    if (activePane) activePane.classList.add("active");

    if (tabId === "portfolio") {
        renderShowcase();
    } else if (tabId === "database") {
        renderDatabaseTable();
    } else if (tabId === "sheets") {
        renderSheetsHub();
    } else if (tabId === "resume-preview") {
        updateLiveResumePreview();
    }
}

// Fetch Full Portfolio Data
async function loadPortfolioData() {
    try {
        const res = await fetch("/api/portfolio");
        if (!res.ok) throw new Error("Failed to load portfolio");
        currentPortfolio = await res.json();
        renderShowcase();
        renderDatabaseTable();
        populateResumeSelectors();
    } catch (e) {
        showToast("Error loading portfolio: " + e.message, "error");
    }
}

// Config status
async function loadConfigStatus() {
    try {
        const res = await fetch("/api/config/status");
        const status = await res.json();
        const geminiStatus = document.getElementById("geminiStatusBadge");
        if (geminiStatus) {
            if (status.gemini_configured) {
                geminiStatus.className = "badge-status";
                geminiStatus.innerHTML = `<span class="dot"></span> Gemini API Live`;
            } else {
                geminiStatus.className = "badge-status inactive";
                geminiStatus.innerHTML = `<span class="dot"></span> Gemini (Rule Engine)`;
            }
        }
    } catch (e) {
        console.error(e);
    }
}

// Render Showcase Tab (Daksh / Marcus inspired)
function renderShowcase() {
    if (!currentPortfolio || !currentPortfolio.profile) return;
    const p = currentPortfolio.profile;

    document.getElementById("showcaseName").innerText = p.name || "Raj Bharat Rasal";
    document.getElementById("showcaseTitle").innerText = p.title || "Backend Systems Architect";
    document.getElementById("showcaseSummary").innerText = p.summary || "";
    
    const emailEl = document.getElementById("showcaseEmail");
    if (emailEl) {
        emailEl.innerText = p.email || "";
        emailEl.href = `mailto:${p.email || ""}`;
    }

    const phoneEl = document.getElementById("showcasePhone");
    if (phoneEl) phoneEl.innerText = p.phone || "";

    const locEl = document.getElementById("showcaseLocation");
    if (locEl) locEl.innerText = p.location || "";

    const liEl = document.getElementById("showcaseLinkedIn");
    if (liEl) liEl.href = p.linkedin || "#";

    const ghEl = document.getElementById("showcaseGithub");
    if (ghEl) ghEl.href = p.github || "#";

    // Stats
    document.getElementById("statProjectsCount").innerText = (currentPortfolio.projects || []).length;
    document.getElementById("statSkillsCount").innerText = (currentPortfolio.skills || []).length;
    document.getElementById("statWhitepapersCount").innerText = (currentPortfolio.publications || []).length;

    // Featured Projects
    const projContainer = document.getElementById("showcaseProjectsGrid");
    if (projContainer) {
        projContainer.innerHTML = "";
        (currentPortfolio.projects || []).forEach(proj => {
            const card = document.createElement("div");
            card.className = "project-card";
            const techTags = (proj.tech_stack || "").split(",").map(t => `<span class="tech-tag">${t.trim()}</span>`).join("");
            
            card.innerHTML = `
                <div>
                    <div class="project-badge-row">
                        <span class="tag-badge">${proj.is_featured ? "Featured System" : "Project"}</span>
                        <span style="font-size:0.75rem; color:var(--text-muted);">${proj.start_date || ""} - ${proj.end_date || "Present"}</span>
                    </div>
                    <h3 class="project-title">${proj.title}</h3>
                    <div class="project-role">${proj.subtitle_role}</div>
                    <p class="project-desc">${(proj.description || "").replace(/\n/g, "<br>")}</p>
                    ${proj.architecture_highlights ? `
                        <div class="project-arch-box">
                            <strong>Architecture:</strong> ${proj.architecture_highlights}
                        </div>
                    ` : ""}
                    <div class="project-tech-tags">${techTags}</div>
                </div>
                <div class="project-links">
                    ${proj.repo_link ? `<a href="${proj.repo_link}" target="_blank" class="project-link-btn">Code Repository →</a>` : ""}
                    ${proj.demo_link ? `<a href="${proj.demo_link}" target="_blank" class="project-link-btn">Live Architecture →</a>` : ""}
                </div>
            `;
            projContainer.appendChild(card);
        });
    }

    // Whitepapers
    const pubContainer = document.getElementById("showcasePubsGrid");
    if (pubContainer) {
        pubContainer.innerHTML = "";
        (currentPortfolio.publications || []).forEach(pub => {
            const item = document.createElement("div");
            item.className = "project-card";
            item.innerHTML = `
                <div>
                    <div class="project-badge-row">
                        <span class="tag-badge" style="background:rgba(6, 182, 212, 0.15); color:#67e8f9; border-color:rgba(6, 182, 212, 0.3);">${pub.venue_type}</span>
                        <span style="font-size:0.75rem; color:var(--text-muted);">${pub.publication_date || ""}</span>
                    </div>
                    <h3 class="project-title" style="font-size:1.05rem;">${pub.title}</h3>
                    <div class="project-role">${pub.publisher}</div>
                    <p class="project-desc">${pub.abstract}</p>
                </div>
                ${pub.url ? `<div class="project-links"><a href="${pub.url}" target="_blank" class="project-link-btn">Read Whitepaper →</a></div>` : ""}
            `;
            pubContainer.appendChild(item);
        });
    }

    // Skills Matrix
    const skillsContainer = document.getElementById("showcaseSkillsMatrix");
    if (skillsContainer) {
        skillsContainer.innerHTML = "";
        const grouped = {};
        (currentPortfolio.skills || []).forEach(s => {
            if (!grouped[s.category]) grouped[s.category] = [];
            grouped[s.category].push(s);
        });

        for (const [cat, sList] of Object.entries(grouped)) {
            const groupEl = document.createElement("div");
            groupEl.className = "skills-category-group";
            const pills = sList.map(s => `
                <span class="skill-pill ${s.is_highlighted ? 'highlight' : ''}">
                    <span class="skill-prof-dot"></span>
                    ${s.name}
                </span>
            `).join("");
            groupEl.innerHTML = `
                <div class="skills-cat-title">${cat}</div>
                <div class="skills-pills-wrap">${pills}</div>
            `;
            skillsContainer.appendChild(groupEl);
        }
    }
}

// Render Database CRUD Table
function renderDatabaseTable() {
    if (!currentPortfolio) return;
    const tableHeader = document.getElementById("crudTableHeader");
    const tableBody = document.getElementById("crudTableBody");
    const titleEl = document.getElementById("crudCategoryTitle");

    titleEl.innerText = selectedCategory.charAt(0).toUpperCase() + selectedCategory.slice(1);

    if (selectedCategory === "profile") {
        const p = currentPortfolio.profile || {};
        tableHeader.innerHTML = `<tr><th>Field</th><th>Value</th><th>Action</th></tr>`;
        tableBody.innerHTML = `
            <tr><td><strong>Name</strong></td><td>${p.name || ""}</td><td rowspan="8"><button class="btn btn-primary btn-sm" onclick="openEditProfileModal()">✏️ Edit Profile</button></td></tr>
            <tr><td><strong>Title</strong></td><td>${p.title || ""}</td></tr>
            <tr><td><strong>Email</strong></td><td>${p.email || ""}</td></tr>
            <tr><td><strong>Phone</strong></td><td>${p.phone || ""}</td></tr>
            <tr><td><strong>Location</strong></td><td>${p.location || ""}</td></tr>
            <tr><td><strong>LinkedIn</strong></td><td>${p.linkedin || ""}</td></tr>
            <tr><td><strong>GitHub</strong></td><td>${p.github || ""}</td></tr>
            <tr><td><strong>Summary</strong></td><td>${p.summary || ""}</td></tr>
        `;
        return;
    }

    const items = currentPortfolio[selectedCategory] || [];

    if (selectedCategory === "skills") {
        tableHeader.innerHTML = `<tr><th>ID</th><th>Name</th><th>Category</th><th>Proficiency</th><th>Highlighted</th><th>Actions</th></tr>`;
        tableBody.innerHTML = items.map(s => `
            <tr>
                <td>${s.id}</td>
                <td><strong>${s.name}</strong></td>
                <td><span class="tag-badge">${s.category}</span></td>
                <td>${s.proficiency}</td>
                <td>${s.is_highlighted ? "Yes" : "No"}</td>
                <td>
                    <button class="btn btn-outline btn-sm" onclick="openEditEntryModal('skills', ${s.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteEntry('skills', ${s.id})">Delete</button>
                </td>
            </tr>
        `).join("");
    } else if (selectedCategory === "projects") {
        tableHeader.innerHTML = `<tr><th>ID</th><th>Title</th><th>Role</th><th>Tech Stack</th><th>Featured</th><th>Actions</th></tr>`;
        tableBody.innerHTML = items.map(p => `
            <tr>
                <td>${p.id}</td>
                <td><strong>${p.title}</strong></td>
                <td>${p.subtitle_role}</td>
                <td>${p.tech_stack}</td>
                <td>${p.is_featured ? "Yes" : "No"}</td>
                <td>
                    <button class="btn btn-outline btn-sm" onclick="openEditEntryModal('projects', ${p.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteEntry('projects', ${p.id})">Delete</button>
                </td>
            </tr>
        `).join("");
    } else if (selectedCategory === "education") {
        tableHeader.innerHTML = `<tr><th>ID</th><th>Institution</th><th>Degree</th><th>Field</th><th>Years</th><th>Actions</th></tr>`;
        tableBody.innerHTML = items.map(e => `
            <tr>
                <td>${e.id}</td>
                <td><strong>${e.institution}</strong></td>
                <td>${e.degree}</td>
                <td>${e.field_of_study}</td>
                <td>${e.start_year} - ${e.end_year}</td>
                <td>
                    <button class="btn btn-outline btn-sm" onclick="openEditEntryModal('education', ${e.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteEntry('education', ${e.id})">Delete</button>
                </td>
            </tr>
        `).join("");
    } else if (selectedCategory === "experiences") {
        tableHeader.innerHTML = `<tr><th>ID</th><th>Company</th><th>Role</th><th>Duration</th><th>Technologies</th><th>Actions</th></tr>`;
        tableBody.innerHTML = items.map(ex => `
            <tr>
                <td>${ex.id}</td>
                <td><strong>${ex.company}</strong></td>
                <td>${ex.role}</td>
                <td>${ex.start_date} - ${ex.end_date}</td>
                <td>${ex.technologies || ""}</td>
                <td>
                    <button class="btn btn-outline btn-sm" onclick="openEditEntryModal('experiences', ${ex.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteEntry('experiences', ${ex.id})">Delete</button>
                </td>
            </tr>
        `).join("");
    } else if (selectedCategory === "certifications") {
        tableHeader.innerHTML = `<tr><th>ID</th><th>Name</th><th>Issuing Org</th><th>Date</th><th>Credential ID</th><th>Actions</th></tr>`;
        tableBody.innerHTML = items.map(c => `
            <tr>
                <td>${c.id}</td>
                <td><strong>${c.name}</strong></td>
                <td>${c.issuing_org}</td>
                <td>${c.issue_date}</td>
                <td>${c.credential_id || ""}</td>
                <td>
                    <button class="btn btn-outline btn-sm" onclick="openEditEntryModal('certifications', ${c.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteEntry('certifications', ${c.id})">Delete</button>
                </td>
            </tr>
        `).join("");
    } else if (selectedCategory === "achievements") {
        tableHeader.innerHTML = `<tr><th>ID</th><th>Title</th><th>Issuer</th><th>Date</th><th>Category</th><th>Actions</th></tr>`;
        tableBody.innerHTML = items.map(a => `
            <tr>
                <td>${a.id}</td>
                <td><strong>${a.title}</strong></td>
                <td>${a.issuer}</td>
                <td>${a.date || ""}</td>
                <td>${a.category || ""}</td>
                <td>
                    <button class="btn btn-outline btn-sm" onclick="openEditEntryModal('achievements', ${a.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteEntry('achievements', ${a.id})">Delete</button>
                </td>
            </tr>
        `).join("");
    } else if (selectedCategory === "publications") {
        tableHeader.innerHTML = `<tr><th>ID</th><th>Title</th><th>Type</th><th>Publisher</th><th>Date</th><th>Actions</th></tr>`;
        tableBody.innerHTML = items.map(pub => `
            <tr>
                <td>${pub.id}</td>
                <td><strong>${pub.title}</strong></td>
                <td>${pub.venue_type}</td>
                <td>${pub.publisher}</td>
                <td>${pub.publication_date || ""}</td>
                <td>
                    <button class="btn btn-outline btn-sm" onclick="openEditEntryModal('publications', ${pub.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteEntry('publications', ${pub.id})">Delete</button>
                </td>
            </tr>
        `).join("");
    } else if (selectedCategory === "languages") {
        tableHeader.innerHTML = `<tr><th>ID</th><th>Language</th><th>Proficiency</th><th>Actions</th></tr>`;
        tableBody.innerHTML = items.map(l => `
            <tr>
                <td>${l.id}</td>
                <td><strong>${l.language}</strong></td>
                <td>${l.proficiency}</td>
                <td>
                    <button class="btn btn-outline btn-sm" onclick="openEditEntryModal('languages', ${l.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteEntry('languages', ${l.id})">Delete</button>
                </td>
            </tr>
        `).join("");
    }
}

// Aliases for inline backward compatibility
function openEditSkillModal(id) { openEditEntryModal('skills', id); }
function openEditProjectModal(id) { openEditEntryModal('projects', id); }

// Edit Profile Modal
function openEditProfileModal() {
    if (!currentPortfolio || !currentPortfolio.profile) return;
    const p = currentPortfolio.profile;
    document.getElementById("editProfName").value = p.name || "";
    document.getElementById("editProfTitle").value = p.title || "";
    document.getElementById("editProfEmail").value = p.email || "";
    document.getElementById("editProfPhone").value = p.phone || "";
    document.getElementById("editProfLocation").value = p.location || "";
    document.getElementById("editProfLinkedIn").value = p.linkedin || "";
    document.getElementById("editProfGithub").value = p.github || "";
    document.getElementById("editProfPortfolioUrl").value = p.portfolio_url || "";
    document.getElementById("editProfSummary").value = p.summary || "";
    document.getElementById("editProfileModal").classList.add("active");
}

function closeEditProfileModal() {
    document.getElementById("editProfileModal").classList.remove("active");
}

async function saveProfileChanges() {
    const payload = {
        name: document.getElementById("editProfName").value.trim(),
        title: document.getElementById("editProfTitle").value.trim(),
        email: document.getElementById("editProfEmail").value.trim(),
        phone: document.getElementById("editProfPhone").value.trim(),
        location: document.getElementById("editProfLocation").value.trim(),
        linkedin: document.getElementById("editProfLinkedIn").value.trim(),
        github: document.getElementById("editProfGithub").value.trim(),
        portfolio_url: document.getElementById("editProfPortfolioUrl").value.trim(),
        summary: document.getElementById("editProfSummary").value.trim()
    };

    if (!payload.name || !payload.email) {
        showToast("Name and Email are required", "error");
        return;
    }

    try {
        const res = await fetch("/api/profile", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error("Failed to update profile");
        showToast("Profile updated successfully!", "success");
        closeEditProfileModal();
        await loadPortfolioData();
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Dynamic Entry Modal for ALL 8 Categories
function openAddEntryModal() {
    if (selectedCategory === "profile") {
        openEditProfileModal();
        return;
    }
    editingEntryId = null;
    setupDynamicModalFields(selectedCategory, null);
    document.getElementById("dynamicEntryModalTitle").innerText = `Add New ${selectedCategory.slice(0, -1).toUpperCase()}`;
    document.getElementById("dynamicEntrySubmitBtn").innerText = "Create Entry";
    document.getElementById("dynamicEntryModal").classList.add("active");
}

function openEditEntryModal(cat, id) {
    editingEntryId = id;
    const items = currentPortfolio[cat] || [];
    const item = items.find(x => x.id === id);
    if (!item) return;

    setupDynamicModalFields(cat, item);
    document.getElementById("dynamicEntryModalTitle").innerText = `Edit ${cat.toUpperCase()} #${id}`;
    document.getElementById("dynamicEntrySubmitBtn").innerText = "Save Changes";
    document.getElementById("dynamicEntryModal").classList.add("active");
}

function closeDynamicEntryModal() {
    document.getElementById("dynamicEntryModal").classList.remove("active");
    editingEntryId = null;
}

function setupDynamicModalFields(cat, item = {}) {
    const container = document.getElementById("dynamicFieldsContainer");
    container.innerHTML = "";

    if (cat === "skills") {
        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Skill Name:</label>
                <input id="dyn_skill_name" type="text" class="form-control" value="${item?.name || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Category:</label>
                <select id="dyn_skill_cat" class="form-control">
                    <option value="Languages" ${item?.category === 'Languages' ? 'selected' : ''}>Languages</option>
                    <option value="Distributed Systems & Architecture" ${item?.category === 'Distributed Systems & Architecture' ? 'selected' : ''}>Distributed Systems & Architecture</option>
                    <option value="AI & Machine Learning" ${item?.category === 'AI & Machine Learning' ? 'selected' : ''}>AI & Machine Learning</option>
                    <option value="Backend & Cloud" ${item?.category === 'Backend & Cloud' ? 'selected' : ''}>Backend & Cloud</option>
                    <option value="Security & Systems" ${item?.category === 'Security & Systems' ? 'selected' : ''}>Security & Systems</option>
                    <option value="Soft Skills" ${item?.category === 'Soft Skills' ? 'selected' : ''}>Soft Skills</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Proficiency:</label>
                <select id="dyn_skill_prof" class="form-control">
                    <option value="Expert" ${item?.proficiency === 'Expert' ? 'selected' : ''}>Expert</option>
                    <option value="Advanced" ${item?.proficiency === 'Advanced' ? 'selected' : ''}>Advanced</option>
                    <option value="Intermediate" ${item?.proficiency === 'Intermediate' ? 'selected' : ''}>Intermediate</option>
                </select>
            </div>
            <div class="form-group" style="display:flex; align-items:center; gap:0.5rem;">
                <input id="dyn_skill_highlight" type="checkbox" ${item?.is_highlighted ? 'checked' : ''}>
                <label for="dyn_skill_highlight" class="form-label" style="margin-bottom:0;">Highlight on Resume / Showcase</label>
            </div>
        `;
    } else if (cat === "projects") {
        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Project Title:</label>
                <input id="dyn_proj_title" type="text" class="form-control" value="${item?.title || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Subtitle / Candidate Role:</label>
                <input id="dyn_proj_role" type="text" class="form-control" value="${item?.subtitle_role || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Tech Stack:</label>
                <input id="dyn_proj_stack" type="text" class="form-control" value="${item?.tech_stack || ''}" required>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div class="form-group">
                    <label class="form-label">Start Date:</label>
                    <input id="dyn_proj_start" type="text" class="form-control" value="${item?.start_date || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">End Date:</label>
                    <input id="dyn_proj_end" type="text" class="form-control" value="${item?.end_date || ''}">
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Description (bullet points separated by newlines):</label>
                <textarea id="dyn_proj_desc" class="form-control" style="min-height:90px;" required>${item?.description || ''}</textarea>
            </div>
            <div class="form-group">
                <label class="form-label">Key Architecture Highlights:</label>
                <textarea id="dyn_proj_arch" class="form-control">${item?.architecture_highlights || ''}</textarea>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div class="form-group">
                    <label class="form-label">Repo URL:</label>
                    <input id="dyn_proj_repo" type="text" class="form-control" value="${item?.repo_link || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Demo URL:</label>
                    <input id="dyn_proj_demo" type="text" class="form-control" value="${item?.demo_link || ''}">
                </div>
            </div>
            <div class="form-group" style="display:flex; align-items:center; gap:0.5rem;">
                <input id="dyn_proj_featured" type="checkbox" ${item?.is_featured !== false ? 'checked' : ''}>
                <label for="dyn_proj_featured" class="form-label" style="margin-bottom:0;">Featured Project</label>
            </div>
        `;
    } else if (cat === "education") {
        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Institution:</label>
                <input id="dyn_edu_inst" type="text" class="form-control" value="${item?.institution || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Degree:</label>
                <input id="dyn_edu_deg" type="text" class="form-control" value="${item?.degree || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Field of Study:</label>
                <input id="dyn_edu_field" type="text" class="form-control" value="${item?.field_of_study || ''}" required>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div class="form-group">
                    <label class="form-label">Start Year:</label>
                    <input id="dyn_edu_start" type="text" class="form-control" value="${item?.start_year || ''}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">End Year:</label>
                    <input id="dyn_edu_end" type="text" class="form-control" value="${item?.end_year || ''}" required>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Score / Grade / Status:</label>
                <input id="dyn_edu_score" type="text" class="form-control" value="${item?.score || ''}">
            </div>
            <div class="form-group">
                <label class="form-label">Academic Highlights:</label>
                <textarea id="dyn_edu_highlights" class="form-control">${item?.highlights || ''}</textarea>
            </div>
        `;
    } else if (cat === "experiences") {
        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Company / Practice Organization:</label>
                <input id="dyn_exp_comp" type="text" class="form-control" value="${item?.company || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Role Title:</label>
                <input id="dyn_exp_role" type="text" class="form-control" value="${item?.role || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Location:</label>
                <input id="dyn_exp_loc" type="text" class="form-control" value="${item?.location || ''}">
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div class="form-group">
                    <label class="form-label">Start Date:</label>
                    <input id="dyn_exp_start" type="text" class="form-control" value="${item?.start_date || ''}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">End Date:</label>
                    <input id="dyn_exp_end" type="text" class="form-control" value="${item?.end_date || ''}" required>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Description / Bullet Points:</label>
                <textarea id="dyn_exp_desc" class="form-control" style="min-height:90px;" required>${item?.description || ''}</textarea>
            </div>
            <div class="form-group">
                <label class="form-label">Technologies / Concepts Applied:</label>
                <input id="dyn_exp_tech" type="text" class="form-control" value="${item?.technologies || ''}">
            </div>
            <div class="form-group" style="display:flex; align-items:center; gap:0.5rem;">
                <input id="dyn_exp_curr" type="checkbox" ${item?.is_current ? 'checked' : ''}>
                <label for="dyn_exp_curr" class="form-label" style="margin-bottom:0;">Current Position</label>
            </div>
        `;
    } else if (cat === "certifications") {
        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Certification Name:</label>
                <input id="dyn_cert_name" type="text" class="form-control" value="${item?.name || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Issuing Organization:</label>
                <input id="dyn_cert_org" type="text" class="form-control" value="${item?.issuing_org || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Issue Date:</label>
                <input id="dyn_cert_date" type="text" class="form-control" value="${item?.issue_date || ''}" required>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div class="form-group">
                    <label class="form-label">Credential ID:</label>
                    <input id="dyn_cert_id" type="text" class="form-control" value="${item?.credential_id || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Verification URL:</label>
                    <input id="dyn_cert_url" type="text" class="form-control" value="${item?.credential_url || ''}">
                </div>
            </div>
        `;
    } else if (cat === "achievements") {
        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Achievement Title:</label>
                <input id="dyn_ach_title" type="text" class="form-control" value="${item?.title || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Issuer / Competition Body:</label>
                <input id="dyn_ach_issuer" type="text" class="form-control" value="${item?.issuer || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Date:</label>
                <input id="dyn_ach_date" type="text" class="form-control" value="${item?.date || ''}">
            </div>
            <div class="form-group">
                <label class="form-label">Category:</label>
                <input id="dyn_ach_cat" type="text" class="form-control" value="${item?.category || 'Competition'}">
            </div>
            <div class="form-group">
                <label class="form-label">Description:</label>
                <textarea id="dyn_ach_desc" class="form-control" required>${item?.description || ''}</textarea>
            </div>
        `;
    } else if (cat === "publications") {
        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Whitepaper / Publication Title:</label>
                <input id="dyn_pub_title" type="text" class="form-control" value="${item?.title || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Venue / Type:</label>
                <input id="dyn_pub_type" type="text" class="form-control" value="${item?.venue_type || 'Architecture Whitepaper'}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Publisher / Affiliation:</label>
                <input id="dyn_pub_pub" type="text" class="form-control" value="${item?.publisher || ''}" required>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div class="form-group">
                    <label class="form-label">Publication Date:</label>
                    <input id="dyn_pub_date" type="text" class="form-control" value="${item?.publication_date || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">URL / Repository:</label>
                    <input id="dyn_pub_url" type="text" class="form-control" value="${item?.url || ''}">
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Abstract / Architecture Overview:</label>
                <textarea id="dyn_pub_abs" class="form-control" style="min-height:90px;" required>${item?.abstract || ''}</textarea>
            </div>
        `;
    } else if (cat === "languages") {
        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Language:</label>
                <input id="dyn_lang_name" type="text" class="form-control" value="${item?.language || ''}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Proficiency:</label>
                <input id="dyn_lang_prof" type="text" class="form-control" value="${item?.proficiency || 'Professional Working Proficiency'}" required>
            </div>
        `;
    }
}

// Submit Add or Edit Entry
async function submitDynamicEntry() {
    const cat = selectedCategory;
    let payload = {};

    if (cat === "skills") {
        payload = {
            name: document.getElementById("dyn_skill_name").value.trim(),
            category: document.getElementById("dyn_skill_cat").value,
            proficiency: document.getElementById("dyn_skill_prof").value,
            is_highlighted: document.getElementById("dyn_skill_highlight").checked
        };
    } else if (cat === "projects") {
        payload = {
            title: document.getElementById("dyn_proj_title").value.trim(),
            subtitle_role: document.getElementById("dyn_proj_role").value.trim(),
            tech_stack: document.getElementById("dyn_proj_stack").value.trim(),
            start_date: document.getElementById("dyn_proj_start").value.trim(),
            end_date: document.getElementById("dyn_proj_end").value.trim(),
            description: document.getElementById("dyn_proj_desc").value.trim(),
            architecture_highlights: document.getElementById("dyn_proj_arch").value.trim(),
            repo_link: document.getElementById("dyn_proj_repo").value.trim(),
            demo_link: document.getElementById("dyn_proj_demo").value.trim(),
            is_featured: document.getElementById("dyn_proj_featured").checked
        };
    } else if (cat === "education") {
        payload = {
            institution: document.getElementById("dyn_edu_inst").value.trim(),
            degree: document.getElementById("dyn_edu_deg").value.trim(),
            field_of_study: document.getElementById("dyn_edu_field").value.trim(),
            start_year: document.getElementById("dyn_edu_start").value.trim(),
            end_year: document.getElementById("dyn_edu_end").value.trim(),
            score: document.getElementById("dyn_edu_score").value.trim(),
            highlights: document.getElementById("dyn_edu_highlights").value.trim()
        };
    } else if (cat === "experiences") {
        payload = {
            company: document.getElementById("dyn_exp_comp").value.trim(),
            role: document.getElementById("dyn_exp_role").value.trim(),
            location: document.getElementById("dyn_exp_loc").value.trim(),
            start_date: document.getElementById("dyn_exp_start").value.trim(),
            end_date: document.getElementById("dyn_exp_end").value.trim(),
            description: document.getElementById("dyn_exp_desc").value.trim(),
            technologies: document.getElementById("dyn_exp_tech").value.trim(),
            is_current: document.getElementById("dyn_exp_curr").checked
        };
    } else if (cat === "certifications") {
        payload = {
            name: document.getElementById("dyn_cert_name").value.trim(),
            issuing_org: document.getElementById("dyn_cert_org").value.trim(),
            issue_date: document.getElementById("dyn_cert_date").value.trim(),
            credential_id: document.getElementById("dyn_cert_id").value.trim(),
            credential_url: document.getElementById("dyn_cert_url").value.trim()
        };
    } else if (cat === "achievements") {
        payload = {
            title: document.getElementById("dyn_ach_title").value.trim(),
            issuer: document.getElementById("dyn_ach_issuer").value.trim(),
            date: document.getElementById("dyn_ach_date").value.trim(),
            category: document.getElementById("dyn_ach_cat").value.trim(),
            description: document.getElementById("dyn_ach_desc").value.trim()
        };
    } else if (cat === "publications") {
        payload = {
            title: document.getElementById("dyn_pub_title").value.trim(),
            venue_type: document.getElementById("dyn_pub_type").value.trim(),
            publisher: document.getElementById("dyn_pub_pub").value.trim(),
            publication_date: document.getElementById("dyn_pub_date").value.trim(),
            url: document.getElementById("dyn_pub_url").value.trim(),
            abstract: document.getElementById("dyn_pub_abs").value.trim()
        };
    } else if (cat === "languages") {
        payload = {
            language: document.getElementById("dyn_lang_name").value.trim(),
            proficiency: document.getElementById("dyn_lang_prof").value.trim()
        };
    }

    try {
        const isEdit = (editingEntryId !== null);
        const url = isEdit ? `/api/${cat}/${editingEntryId}` : `/api/${cat}`;
        const method = isEdit ? "PUT" : "POST";

        const res = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail ? JSON.stringify(err.detail) : "Operation failed");
        }

        showToast(isEdit ? "Entry updated successfully!" : "Entry created successfully!", "success");
        closeDynamicEntryModal();
        await loadPortfolioData();
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Delete Entry
async function deleteEntry(category, id) {
    if (!confirm(`Are you sure you want to delete this ${category} entry?`)) return;
    try {
        const res = await fetch(`/api/${category}/${id}`, { method: "DELETE" });
        if (!res.ok) throw new Error("Delete failed");
        showToast("Entry deleted successfully", "success");
        await loadPortfolioData();
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Google Sheets Hub
function renderSheetsHub() {
    if (!currentPortfolio) return;
    const summaryEl = document.getElementById("sheetsTabSummary");
    if (!summaryEl) return;
    summaryEl.innerHTML = `
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:1rem; margin-top:1rem;">
            <div class="stat-box"><div class="stat-num">1</div><div class="stat-label">Profile Record</div></div>
            <div class="stat-box"><div class="stat-num">${(currentPortfolio.skills || []).length}</div><div class="stat-label">Skills Categorized</div></div>
            <div class="stat-box"><div class="stat-num">${(currentPortfolio.projects || []).length}</div><div class="stat-label">Systems & Projects</div></div>
            <div class="stat-box"><div class="stat-num">${(currentPortfolio.experiences || []).length}</div><div class="stat-label">Experience Rows</div></div>
            <div class="stat-box"><div class="stat-num">${(currentPortfolio.education || []).length}</div><div class="stat-label">Education Records</div></div>
            <div class="stat-box"><div class="stat-num">${(currentPortfolio.publications || []).length}</div><div class="stat-label">Whitepapers</div></div>
        </div>
    `;
    switchSpreadsheetSheet('Profile');
}

// Interactive Google Sheets Spreadsheet Viewer
function switchSpreadsheetSheet(sheetName, el) {
    if (el) {
        el.parentElement.querySelectorAll(".sub-tab-btn").forEach(b => b.classList.remove("active"));
        el.classList.add("active");
    }
    if (!currentPortfolio) return;
    const thead = document.getElementById("spreadsheetPreviewHead");
    const tbody = document.getElementById("spreadsheetPreviewBody");
    if (!thead || !tbody) return;

    let headers = [];
    let rows = [];

    if (sheetName === "Profile") {
        headers = ["Row", "A (Field)", "B (Value)"];
        const p = currentPortfolio.profile || {};
        const fields = [
            ["Name", p.name || ""], ["Title", p.title || ""], ["Email", p.email || ""],
            ["Phone", p.phone || ""], ["Location", p.location || ""], ["LinkedIn", p.linkedin || ""],
            ["GitHub", p.github || ""], ["Portfolio URL", p.portfolio_url || ""], ["Professional Summary", p.summary || ""]
        ];
        rows = fields.map((f, i) => [i + 2, f[0], f[1]]);
    } else if (sheetName === "Education") {
        headers = ["Row", "A (Institution)", "B (Degree)", "C (Field)", "D (Start)", "E (End)", "F (Score)"];
        rows = (currentPortfolio.education || []).map((e, i) => [i + 2, e.institution, e.degree, e.field_of_study, e.start_year, e.end_year, e.score || ""]);
    } else if (sheetName === "Skills") {
        headers = ["Row", "A (Skill Name)", "B (Category)", "C (Proficiency)", "D (Highlighted)"];
        rows = (currentPortfolio.skills || []).map((s, i) => [i + 2, s.name, s.category, s.proficiency, s.is_highlighted ? "Yes" : "No"]);
    } else if (sheetName === "Experience") {
        headers = ["Row", "A (Company)", "B (Role)", "C (Start)", "D (End)", "E (Description)"];
        rows = (currentPortfolio.experiences || []).map((ex, i) => [i + 2, ex.company, ex.role, ex.start_date, ex.end_date, ex.description.slice(0, 70) + "..."]);
    } else if (sheetName === "Projects") {
        headers = ["Row", "A (Title)", "B (Role)", "C (Tech Stack)", "D (Featured)", "E (Architecture Highlights)"];
        rows = (currentPortfolio.projects || []).map((p, i) => [i + 2, p.title, p.subtitle_role, p.tech_stack, p.is_featured ? "Yes" : "No", (p.architecture_highlights || "").slice(0, 60) + "..."]);
    } else if (sheetName === "Certifications") {
        headers = ["Row", "A (Name)", "B (Issuing Org)", "C (Date)", "D (Credential ID)"];
        rows = (currentPortfolio.certifications || []).map((c, i) => [i + 2, c.name, c.issuing_org, c.issue_date, c.credential_id || ""]);
    } else if (sheetName === "Achievements") {
        headers = ["Row", "A (Title)", "B (Issuer)", "C (Date)", "D (Category)"];
        rows = (currentPortfolio.achievements || []).map((a, i) => [i + 2, a.title, a.issuer, a.date || "", a.category || ""]);
    } else if (sheetName === "Publications") {
        headers = ["Row", "A (Title)", "B (Venue Type)", "C (Publisher)", "D (Date)"];
        rows = (currentPortfolio.publications || []).map((pb, i) => [i + 2, pb.title, pb.venue_type, pb.publisher, pb.publication_date || ""]);
    } else if (sheetName === "Languages") {
        headers = ["Row", "A (Language)", "B (Proficiency)"];
        rows = (currentPortfolio.languages || []).map((l, i) => [i + 2, l.language, l.proficiency]);
    }

    thead.innerHTML = `<tr>${headers.map((h, i) => `<th style="${i === 0 ? 'width:50px; text-align:center; color:#64748b;' : 'color:var(--accent-emerald); font-weight:700;'}">${h}</th>`).join("")}</tr>`;
    tbody.innerHTML = rows.map(r => `
        <tr>
            ${r.map((cell, ci) => ci === 0 ? `<td style="text-align:center; color:#64748b; font-weight:600;">${cell}</td>` : `<td>${cell}</td>`).join("")}
        </tr>
    `).join("");
}

// Database Schema Inspector
async function toggleDatabaseInspector() {
    const container = document.getElementById("dbInspectorContainer");
    if (!container) return;
    if (container.style.display === "block") {
        container.style.display = "none";
        return;
    }
    container.style.display = "block";
    const grid = document.getElementById("dbInspectorGrid");
    grid.innerHTML = `<div style="color:var(--text-muted); font-size:0.8rem;">Loading SQLite schema...</div>`;
    try {
        const res = await fetch("/api/database/inspect");
        const data = await res.json();
        grid.innerHTML = data.tables.map(t => `
            <div style="background:rgba(15,23,42,0.8); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:0.85rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
                    <strong style="color:var(--accent-cyan); font-family:var(--font-mono); font-size:0.85rem;">${t.table_name}</strong>
                    <span class="tag-badge" style="font-size:0.65rem;">${t.row_count} rows</span>
                </div>
                <div style="font-size:0.72rem; color:var(--text-muted); font-family:var(--font-mono); max-height:85px; overflow-y:auto; line-height:1.4;">
                    ${t.columns.map(c => `<div>• ${c.name} <span style="color:#64748b;">(${c.type})</span></div>`).join("")}
                </div>
            </div>
        `).join("");
    } catch (e) {
        grid.innerHTML = `<div style="color:var(--accent-rose); font-size:0.8rem;">Error loading schema: ${e.message}</div>`;
    }
}

// Sample JDs loader
async function loadSampleJDs() {
    try {
        const res = await fetch("/api/sample-jds");
        const jds = await res.json();
        const select = document.getElementById("sampleJdSelect");
        if (!select) return;
        select.innerHTML = `<option value="">-- Choose a pre-loaded Sample Job Description --</option>`;
        jds.forEach(jd => {
            const opt = document.createElement("option");
            opt.value = jd.id;
            opt.innerText = `${jd.title} (${jd.company})`;
            opt.dataset.desc = jd.description;
            opt.dataset.title = jd.title;
            select.appendChild(opt);
        });

        select.addEventListener("change", (e) => {
            const selectedOpt = select.options[select.selectedIndex];
            if (selectedOpt && selectedOpt.dataset.desc) {
                document.getElementById("jdInput").value = selectedOpt.dataset.desc;
                document.getElementById("targetTitleInput").value = selectedOpt.dataset.title;
            }
        });
    } catch (e) {
        console.error(e);
    }
}

// AI JD Analysis
async function analyzeJobDescription() {
    const jd = document.getElementById("jdInput").value.trim();
    const title = document.getElementById("targetTitleInput").value.trim();

    if (!jd) {
        showToast("Please enter or select a Job Description first", "error");
        return;
    }

    const btn = document.getElementById("analyzeJdBtn");
    const originalText = btn.innerHTML;
    btn.innerHTML = `<span class="dot" style="animation:pulse 1s infinite"></span> Analyzing with Gemini AI...`;
    btn.disabled = true;

    try {
        const res = await fetch("/api/ai/analyze-jd", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job_description: jd, target_title: title })
        });
        if (!res.ok) throw new Error("JD Analysis failed");
        currentJDAnalysis = await res.json();
        renderJDAnalysisResults(currentJDAnalysis);
        showToast("Job Description successfully analyzed!", "success");
    } catch (e) {
        showToast(e.message, "error");
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function renderJDAnalysisResults(data) {
    document.getElementById("analysisResultsCard").style.display = "block";
    document.getElementById("matchScoreNum").innerText = `${data.match_score}%`;
    document.getElementById("detectedRoleTitle").innerText = data.role_title;
    document.getElementById("detectedCompany").innerText = data.company_name;

    // Matched skills
    const matchedWrap = document.getElementById("matchedSkillsWrap");
    matchedWrap.innerHTML = data.matched_skills.map(s => `<span class="tag-badge" style="background:rgba(16,185,129,0.15); color:#6ee7b7; border-color:rgba(16,185,129,0.3);">✓ ${s}</span>`).join(" ");

    // Missing skills
    const missingWrap = document.getElementById("missingSkillsWrap");
    missingWrap.innerHTML = data.missing_skills.map(s => `<span class="tag-badge" style="background:rgba(244,63,94,0.15); color:#fda4af; border-color:rgba(244,63,94,0.3);">+ ${s}</span>`).join(" ");

    // Domain keywords
    const keywordsWrap = document.getElementById("domainKeywordsWrap");
    keywordsWrap.innerHTML = data.domain_keywords.map(k => `<span class="tech-tag">${k}</span>`).join(" ");

    // Recommendations
    const recsList = document.getElementById("recommendationsList");
    recsList.innerHTML = data.recommendations.map(r => `<li>${r}</li>`).join("");

    // Set tailored summary
    document.getElementById("tailoredSummaryInput").value = data.suggested_summary;

    // Automatically check suggested items
    if (data.suggested_project_ids && data.suggested_project_ids.length > 0) {
        document.querySelectorAll("input[name='sel_project']").forEach(cb => {
            cb.checked = data.suggested_project_ids.includes(parseInt(cb.value));
        });
    }

    if (data.suggested_skill_ids && data.suggested_skill_ids.length > 0) {
        document.querySelectorAll("input[name='sel_skill']").forEach(cb => {
            cb.checked = data.suggested_skill_ids.includes(parseInt(cb.value));
        });
    }

    updateLiveResumePreview();
}

// Populate resume item selection lists
function populateResumeSelectors() {
    if (!currentPortfolio) return;

    // Projects Checklist
    const projList = document.getElementById("projectSelectionList");
    if (projList) {
        projList.innerHTML = (currentPortfolio.projects || []).map(p => `
            <label class="selection-item">
                <input type="checkbox" name="sel_project" value="${p.id}" ${p.is_featured ? 'checked' : ''} onchange="updateLiveResumePreview()">
                <div class="selection-info">
                    <div class="selection-title">${p.title}</div>
                    <div class="selection-desc">${p.subtitle_role} • ${p.tech_stack}</div>
                </div>
            </label>
        `).join("");
    }

    // Skills Checklist
    const skillList = document.getElementById("skillSelectionList");
    if (skillList) {
        skillList.innerHTML = (currentPortfolio.skills || []).map(s => `
            <label class="selection-item" style="padding:0.4rem 0.65rem;">
                <input type="checkbox" name="sel_skill" value="${s.id}" ${s.is_highlighted ? 'checked' : ''} onchange="updateLiveResumePreview()">
                <div class="selection-info">
                    <div class="selection-title" style="font-size:0.8rem;">${s.name}</div>
                    <div class="selection-desc" style="font-size:0.7rem;">${s.category}</div>
                </div>
            </label>
        `).join("");
    }

    // Experience Checklist
    const expList = document.getElementById("expSelectionList");
    if (expList) {
        expList.innerHTML = (currentPortfolio.experiences || []).map(e => `
            <label class="selection-item">
                <input type="checkbox" name="sel_exp" value="${e.id}" checked onchange="updateLiveResumePreview()">
                <div class="selection-info">
                    <div class="selection-title">${e.company} — ${e.role}</div>
                    <div class="selection-desc">${e.start_date} - ${e.end_date}</div>
                </div>
            </label>
        `).join("");
    }

    // Publications Checklist
    const pubList = document.getElementById("pubSelectionList");
    if (pubList) {
        pubList.innerHTML = (currentPortfolio.publications || []).map(pb => `
            <label class="selection-item">
                <input type="checkbox" name="sel_pub" value="${pb.id}" checked onchange="updateLiveResumePreview()">
                <div class="selection-info">
                    <div class="selection-title">${pb.title}</div>
                    <div class="selection-desc">${pb.venue_type} • ${pb.publication_date || ""}</div>
                </div>
            </label>
        `).join("");
    }
}

// Live Resume Preview
async function updateLiveResumePreview() {
    if (!currentPortfolio || !currentPortfolio.profile) return;

    const payload = getResumePayload();
    try {
        const res = await fetch("/api/resume/preview", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error("Failed to render preview");
        const data = await res.json();
        renderResumeHTML(data);
    } catch (e) {
        console.error("Preview error:", e);
    }
}

function getResumePayload() {
    const targetTitle = (document.getElementById("targetTitleInput")?.value || "").trim() || currentPortfolio?.profile?.title || "Systems Architect";
    const jd = (document.getElementById("jdInput")?.value || "").trim();
    const customSummary = (document.getElementById("tailoredSummaryInput")?.value || "").trim();

    const selectedProjects = Array.from(document.querySelectorAll("input[name='sel_project']:checked")).map(cb => parseInt(cb.value));
    const selectedSkills = Array.from(document.querySelectorAll("input[name='sel_skill']:checked")).map(cb => parseInt(cb.value));
    const selectedExp = Array.from(document.querySelectorAll("input[name='sel_exp']:checked")).map(cb => parseInt(cb.value));
    const selectedPubs = Array.from(document.querySelectorAll("input[name='sel_pub']:checked")).map(cb => parseInt(cb.value));

    return {
        target_title: targetTitle,
        job_description: jd,
        custom_summary: customSummary,
        selected_project_ids: selectedProjects,
        selected_skill_ids: selectedSkills,
        selected_experience_ids: selectedExp,
        selected_publication_ids: selectedPubs,
        selected_certification_ids: (currentPortfolio?.certifications || []).map(c => c.id),
        selected_achievement_ids: (currentPortfolio?.achievements || []).map(a => a.id)
    };
}

function renderResumeHTML(data) {
    const container = document.getElementById("liveResumeDocument");
    if (!container) return;
    const p = data.profile || {};

    let html = `
        <div style="text-align:left;">
            <h1>${(p.name || "Raj Bharat Rasal").toUpperCase()}</h1>
            <div class="preview-target-title">${data.target_title || ""}</div>
            <div class="preview-contact">
                ${[p.location, p.phone, p.email, p.linkedin?.replace('https://',''), p.github?.replace('https://','')].filter(Boolean).join("  |  ")}
            </div>
            <hr class="preview-divider" style="margin-bottom:0.75rem;">
        </div>
    `;

    // Professional Summary
    if (data.custom_summary) {
        html += `
            <div class="preview-section-title">PROFESSIONAL SUMMARY</div>
            <p class="preview-body-text">${data.custom_summary}</p>
        `;
    }

    // Skills
    if (data.skills && data.skills.length > 0) {
        html += `<div class="preview-section-title">TECHNICAL & ARCHITECTURAL SKILLS</div>`;
        const grouped = {};
        data.skills.forEach(s => {
            if (!grouped[s.category]) grouped[s.category] = [];
            grouped[s.category].push(s.name);
        });
        for (const [cat, names] of Object.entries(grouped)) {
            html += `<p class="preview-body-text"><strong>${cat}:</strong> ${names.join(", ")}</p>`;
        }
    }

    // Projects
    if (data.projects && data.projects.length > 0) {
        html += `<div class="preview-section-title">FEATURED SYSTEMS & PROJECTS</div>`;
        data.projects.forEach(proj => {
            const bullets = (proj.description || "").split("\n").filter(Boolean);
            html += `
                <div style="margin-bottom:0.6rem;">
                    <div class="preview-item-row">
                        <span>${proj.title} — ${proj.subtitle_role}</span>
                        <span style="font-size:0.78rem; font-weight:normal; color:#64748b;">${proj.start_date || ""} - ${proj.end_date || "Present"}</span>
                    </div>
                    <div class="preview-item-sub">Tech Stack: ${proj.tech_stack}</div>
                    <ul>
                        ${bullets.map(b => `<li class="preview-bullet">${b.replace(/^[•\-\*]\s*/, '')}</li>`).join("")}
                        ${proj.architecture_highlights ? `<li class="preview-bullet"><strong>Architecture:</strong> ${proj.architecture_highlights}</li>` : ""}
                    </ul>
                </div>
            `;
        });
    }

    // Experience
    if (data.experiences && data.experiences.length > 0) {
        html += `<div class="preview-section-title">EXPERIENCE & LEADERSHIP</div>`;
        data.experiences.forEach(exp => {
            const bullets = (exp.description || "").split("\n").filter(Boolean);
            html += `
                <div style="margin-bottom:0.6rem;">
                    <div class="preview-item-row">
                        <span>${exp.company} — ${exp.role}</span>
                        <span style="font-size:0.78rem; font-weight:normal; color:#64748b;">${exp.start_date} - ${exp.end_date}</span>
                    </div>
                    <ul>
                        ${bullets.map(b => `<li class="preview-bullet">${b.replace(/^[•\-\*]\s*/, '')}</li>`).join("")}
                    </ul>
                </div>
            `;
        });
    }

    // Publications
    if (data.publications && data.publications.length > 0) {
        html += `<div class="preview-section-title">SYSTEM DESIGN SPECIFICATIONS & WHITEPAPERS</div>`;
        data.publications.forEach(pub => {
            html += `
                <div style="margin-bottom:0.45rem;">
                    <div class="preview-item-row">
                        <span>${pub.title} (${pub.venue_type})</span>
                        <span style="font-size:0.78rem; font-weight:normal; color:#64748b;">${pub.publication_date || ""}</span>
                    </div>
                    <p class="preview-body-text" style="margin-top:0.15rem;">${pub.abstract}</p>
                </div>
            `;
        });
    }

    // Education
    if (data.education && data.education.length > 0) {
        html += `<div class="preview-section-title">EDUCATION</div>`;
        data.education.forEach(edu => {
            html += `
                <div style="margin-bottom:0.45rem;">
                    <div class="preview-item-row">
                        <span>${edu.institution} — ${edu.degree}</span>
                        <span style="font-size:0.78rem; font-weight:normal; color:#64748b;">${edu.start_year} - ${edu.end_year}</span>
                    </div>
                    <div class="preview-item-sub">Field: ${edu.field_of_study} ${edu.score ? ' | Score: ' + edu.score : ''}</div>
                    ${edu.highlights ? `<p class="preview-body-text">${edu.highlights}</p>` : ''}
                </div>
            `;
        });
    }

    // Achievements
    if (data.achievements && data.achievements.length > 0) {
        html += `<div class="preview-section-title">ACHIEVEMENTS & SECURITY RESEARCH</div>`;
        html += `<ul>${data.achievements.map(a => `<li class="preview-bullet"><strong>${a.title}:</strong> ${a.description}</li>`).join("")}</ul>`;
    }

    // Certifications
    if (data.certifications && data.certifications.length > 0) {
        html += `<div class="preview-section-title">CERTIFICATIONS & ACCREDITATIONS</div>`;
        html += `<ul>${data.certifications.map(c => `<li class="preview-bullet"><strong>${c.name}</strong> — ${c.issuing_org} (${c.issue_date})</li>`).join("")}</ul>`;
    }

    container.innerHTML = html;
}

// Download PDF
async function downloadPDFResume() {
    const payload = getResumePayload();
    showToast("Generating high-resolution ATS PDF...", "info");
    try {
        const res = await fetch("/api/resume/export-pdf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error("PDF generation failed");
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `Resume_${payload.target_title.replace(/\s+/g, '_')}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        showToast("PDF Resume downloaded successfully!", "success");
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Download DOCX
async function downloadDOCXResume() {
    const payload = getResumePayload();
    showToast("Generating ATS-compliant Word Document (.docx)...", "info");
    try {
        const res = await fetch("/api/resume/export-docx", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error("DOCX generation failed");
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `Resume_${payload.target_title.replace(/\s+/g, '_')}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        showToast("DOCX Resume downloaded successfully!", "success");
    } catch (e) {
        showToast(e.message, "error");
    }
}

// AI Unstructured Parser
async function parseUnstructuredText() {
    const text = document.getElementById("unstructuredTextInput").value.trim();
    if (!text) {
        showToast("Please enter unstructured text or paste a resume.", "error");
        return;
    }
    const btn = document.getElementById("parseTextBtn");
    btn.innerHTML = `<span class="dot" style="animation:pulse 1s infinite"></span> Extracting with Gemini...`;
    btn.disabled = true;

    try {
        const res = await fetch("/api/ai/parse-unstructured", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ raw_text: text })
        });
        if (!res.ok) throw new Error("Parsing failed");
        const parsed = await res.json();
        document.getElementById("parsedOutputContainer").style.display = "block";
        document.getElementById("parsedJsonPreview").innerText = JSON.stringify(parsed, null, 2);
        showToast("Information successfully structured by Gemini!", "success");
    } catch (e) {
        showToast(e.message, "error");
    } finally {
        btn.innerHTML = `Extract Structured Fields with Gemini`;
        btn.disabled = false;
    }
}

async function importParsedTextToDB() {
    const text = document.getElementById("unstructuredTextInput").value.trim();
    if (!text) return;
    try {
        const res = await fetch("/api/ai/import-unstructured", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ raw_text: text })
        });
        if (!res.ok) throw new Error("Import failed");
        showToast("Extracted entities imported to database!", "success");
        await loadPortfolioData();
        switchTab("database");
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Google Sheets Sync
async function syncGoogleSheets() {
    const webhookUrl = document.getElementById("sheetsWebhookUrlInput").value.trim();
    if (!webhookUrl) {
        showToast("Please enter your Google Apps Script Webhook URL", "error");
        return;
    }
    const btn = document.getElementById("syncSheetsBtn");
    btn.innerHTML = `<span class="dot" style="animation:pulse 1s infinite"></span> Syncing to Google Sheets...`;
    btn.disabled = true;

    try {
        const res = await fetch("/api/sheets/sync-webhook", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ webhook_url: webhookUrl })
        });
        const result = await res.json();
        if (!res.ok) throw new Error(result.detail || "Sync failed");
        showToast("Successfully synchronized database with Google Sheets!", "success");
    } catch (e) {
        showToast(e.message, "error");
    } finally {
        btn.innerHTML = `Push Database to Live Google Sheet`;
        btn.disabled = false;
    }
}

// Reset Database
async function resetDatabase() {
    if (!confirm("Reset database to Raj Bharat Rasal's verified records?")) return;
    try {
        const res = await fetch("/api/portfolio/reset", { method: "POST" });
        if (!res.ok) throw new Error("Reset failed");
        showToast("Database reset to verified portfolio records", "success");
        await loadPortfolioData();
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Settings Modal
function openSettingsModal() {
    document.getElementById("settingsModal").classList.add("active");
}

function closeSettingsModal() {
    document.getElementById("settingsModal").classList.remove("active");
}

async function saveSettings() {
    const geminiKey = document.getElementById("settingsGeminiKey").value.trim();
    const webhookUrl = document.getElementById("settingsWebhookUrl").value.trim();

    try {
        const res = await fetch("/api/config/keys", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ gemini_api_key: geminiKey, sheets_webhook_url: webhookUrl })
        });
        if (!res.ok) throw new Error("Failed to save settings");
        showToast("Settings updated successfully", "success");
        closeSettingsModal();
        await loadConfigStatus();
    } catch (e) {
        showToast(e.message, "error");
    }
}

function setupEventListeners() {
    document.getElementById("analyzeJdBtn")?.addEventListener("click", analyzeJobDescription);
    document.getElementById("parseTextBtn")?.addEventListener("click", parseUnstructuredText);
    document.getElementById("importParsedBtn")?.addEventListener("click", importParsedTextToDB);
    document.getElementById("syncSheetsBtn")?.addEventListener("click", syncGoogleSheets);
    document.getElementById("downloadPdfBtn")?.addEventListener("click", downloadPDFResume);
    document.getElementById("downloadDocxBtn")?.addEventListener("click", downloadDOCXResume);
    document.getElementById("printResumeBtn")?.addEventListener("click", () => window.print());
    document.getElementById("resetDbBtn")?.addEventListener("click", resetDatabase);
}
