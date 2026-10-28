/**
 * Google Apps Script for AI Portfolio Management System
 * 
 * Instructions:
 * 1. Open Google Sheets -> Extensions -> Apps Script
 * 2. Replace Code.gs with this code.
 * 3. Select 'initialAuth' in the function dropdown and click 'Run' to authorize.
 * 4. Click 'Deploy' -> 'New deployment' -> Select type: 'Web app'
 * 5. Set 'Execute as': 'Me', 'Who has access': 'Anyone'
 * 6. Click 'Deploy' and copy the Web App URL into the Portfolio app!
 * 
 * NOTE: If you see "Error 401: invalid_client", open Google Sheets in an
 * Incognito window with ONLY your primary Google account signed in.
 */

// Run this once in the editor to grant authorization without 401 errors
function initialAuth() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  Logger.log("Authorized successfully for spreadsheet: " + ss.getName());
  return "Authorized!";
}

function doPost(e) {
  try {
    var raw = e.postData.contents;
    var payload = JSON.parse(raw);
    var data = payload.data || payload;
    
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    // 1. Profile
    if (data.profile) {
      var p = data.profile;
      var profSheet = getOrCreateSheet(ss, "Profile");
      profSheet.clear();
      var profHeaders = ["Field", "Value"];
      var profRows = [
        ["Name", p.name || ""],
        ["Title", p.title || ""],
        ["Email", p.email || ""],
        ["Phone", p.phone || ""],
        ["Location", p.location || ""],
        ["LinkedIn", p.linkedin || ""],
        ["GitHub", p.github || ""],
        ["Portfolio URL", p.portfolio_url || ""],
        ["Professional Summary", p.summary || ""],
        ["Last Updated", new Date().toISOString()]
      ];
      writeTable(profSheet, profHeaders, profRows);
    }
    
    // 2. Education
    if (data.education) {
      var eduSheet = getOrCreateSheet(ss, "Education");
      eduSheet.clear();
      var eduHeaders = ["ID", "Institution", "Degree", "Field of Study", "Start Year", "End Year", "Score", "Highlights"];
      var eduRows = data.education.map(function(item) {
        return [item.id, item.institution, item.degree, item.field_of_study, item.start_year, item.end_year, item.score || "", item.highlights || ""];
      });
      writeTable(eduSheet, eduHeaders, eduRows);
    }
    
    // 3. Skills
    if (data.skills) {
      var skillsSheet = getOrCreateSheet(ss, "Skills");
      skillsSheet.clear();
      var skillsHeaders = ["ID", "Skill Name", "Category", "Proficiency", "Highlighted"];
      var skillsRows = data.skills.map(function(item) {
        return [item.id, item.name, item.category, item.proficiency, item.is_highlighted ? "Yes" : "No"];
      });
      writeTable(skillsSheet, skillsHeaders, skillsRows);
    }
    
    // 4. Experience
    if (data.experiences) {
      var expSheet = getOrCreateSheet(ss, "Experience");
      expSheet.clear();
      var expHeaders = ["ID", "Company", "Role", "Location", "Start Date", "End Date", "Current", "Description", "Technologies"];
      var expRows = data.experiences.map(function(item) {
        return [item.id, item.company, item.role, item.location || "", item.start_date, item.end_date, item.is_current ? "Yes" : "No", item.description, item.technologies || ""];
      });
      writeTable(expSheet, expHeaders, expRows);
    }
    
    // 5. Projects
    if (data.projects) {
      var projSheet = getOrCreateSheet(ss, "Projects");
      projSheet.clear();
      var projHeaders = ["ID", "Title", "Subtitle / Role", "Tech Stack", "Description", "Architecture Highlights", "Repo Link", "Demo Link", "Featured"];
      var projRows = data.projects.map(function(item) {
        return [item.id, item.title, item.subtitle_role, item.tech_stack, item.description, item.architecture_highlights || "", item.repo_link || "", item.demo_link || "", item.is_featured ? "Yes" : "No"];
      });
      writeTable(projSheet, projHeaders, projRows);
    }
    
    // 6. Certifications
    if (data.certifications) {
      var certSheet = getOrCreateSheet(ss, "Certifications");
      certSheet.clear();
      var certHeaders = ["ID", "Name", "Issuing Org", "Issue Date", "Credential ID", "Credential URL"];
      var certRows = data.certifications.map(function(item) {
        return [item.id, item.name, item.issuing_org, item.issue_date, item.credential_id || "", item.credential_url || ""];
      });
      writeTable(certSheet, certHeaders, certRows);
    }
    
    // 7. Achievements
    if (data.achievements) {
      var achSheet = getOrCreateSheet(ss, "Achievements");
      achSheet.clear();
      var achHeaders = ["ID", "Title", "Issuer", "Date", "Description", "Category"];
      var achRows = data.achievements.map(function(item) {
        return [item.id, item.title, item.issuer, item.date || "", item.description, item.category || ""];
      });
      writeTable(achSheet, achHeaders, achRows);
    }
    
    // 8. Publications
    if (data.publications) {
      var pubSheet = getOrCreateSheet(ss, "Publications");
      pubSheet.clear();
      var pubHeaders = ["ID", "Title", "Type", "Publisher", "Publication Date", "URL", "Abstract"];
      var pubRows = data.publications.map(function(item) {
        return [item.id, item.title, item.venue_type, item.publisher, item.publication_date || "", item.url || "", item.abstract];
      });
      writeTable(pubSheet, pubHeaders, pubRows);
    }
    
    // 9. Languages
    if (data.languages) {
      var langSheet = getOrCreateSheet(ss, "Languages");
      langSheet.clear();
      var langHeaders = ["ID", "Language", "Proficiency"];
      var langRows = data.languages.map(function(item) {
        return [item.id, item.language, item.proficiency];
      });
      writeTable(langSheet, langHeaders, langRows);
    }
    
    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: "Portfolio data successfully synced to all sheets",
      synced_at: new Date().toISOString()
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: "active",
    name: "AI Portfolio Management Google Sheets Bridge",
    instructions: "Send a POST request with portfolio JSON to synchronize sheets."
  })).setMimeType(ContentService.MimeType.JSON);
}

function getOrCreateSheet(ss, sheetName) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }
  return sheet;
}

function writeTable(sheet, headers, rows) {
  var allData = [headers];
  if (rows && rows.length > 0) {
    allData = allData.concat(rows);
  }
  
  var range = sheet.getRange(1, 1, allData.length, headers.length);
  range.setValues(allData);
  
  // Style headers
  var headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground("#1E293B"); // Slate 800
  headerRange.setFontColor("#FFFFFF");
  headerRange.setFontWeight("bold");
  headerRange.setHorizontalAlignment("center");
  
  sheet.setFrozenRows(1);
  for (var i = 1; i <= headers.length; i++) {
    sheet.autoResizeColumn(i);
  }
}

