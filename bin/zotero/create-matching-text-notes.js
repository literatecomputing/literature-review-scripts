// This is a script for Zotero that creates notes for selected items with the surrounding text of the terms 'reflexivity', 'positionality', and 'subjectivity'.
// TO use it, select the items you want to process in Zotero, then run the script from the Zotero console (/Tools/Developer/Run JavaScript).

// Get first selected item
var selectedItems = ZoteroPane.getSelectedItems();
const skipExisting = false;

function getSurroundingLines(fulltext, term) {
  // Split the fulltext by actual newline characters
  const lines = fulltext.split('\n');

  // Convert term to lowercase for case-insensitive search
  const termLower = term.toLowerCase().replace(/ty$/, "t");

  const surroundingLinesArray = [];
  
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].toLowerCase().includes(termLower)) {
      const start = Math.max(0, i - 5);
      const end = Math.min(lines.length, i + 11);
      const surroundingLines = lines.slice(start, end).join('\n');
      surroundingLinesArray.push(surroundingLines);
    }
  }

  return surroundingLinesArray.map(surroundingLines => {
    return surroundingLines.replace(new RegExp(`(${termLower}[a-z]*)`, 'gi'), ' -----> $1 <----- ');
  }).join('\n\n===================================================\n\n');
}

async function insertNoteForTerm(item, term) {
  // get all notes for item
  const noteIDs = item.getNotes();
  var note = null;
  // use exsting note if it exists
  for (let id of noteIDs) {
    note = Zotero.Items.get(id);
    if (note.note.split('\n')[0].includes(`${term} search`)) {
      if (skipExisting) {
        return;
      }
      break;
    }
  }
  var fulltext = [];
  if (item.isRegularItem()) { // not an attachment already
    let attachmentIDs = item.getAttachments();
    for (let id of attachmentIDs) {
        let attachment = Zotero.Items.get(id);
        if (attachment.attachmentContentType == 'application/pdf'
                || attachment.attachmentContentType == 'text/html') {
            fulltext.push(await attachment.attachmentText);
        }
    }
  }
  const searchLines = getSurroundingLines(fulltext.join("\n"), term);

  if (!searchLines) {
    // Term not found in fulltext
    return null;
  }

  if (!note) {
    note = new Zotero.Item('note');
  }
  note.setNote(`${term} search\n\n ${searchLines}`);
  note.parentItemID = item.id;
  await item.saveTx();
  await note.saveTx();

  return note;
}

processedItems = [];
for (let item of selectedItems) {
  insertNoteForTerm(item, 'reflexivity');
  insertNoteForTerm(item, 'positionality');
  insertNoteForTerm(item, 'subjectivity');
  // insertNoteForTerm(item, 'subjectivity-banana-pants');
  // check if a note has been added
  const noteIDs = item.getNotes();
  // add tag if no notes were added
  if (noteIDs.length === 0) {
    item.addTag('missing-all-terms');
  }

  processedItems.push(item);
}

return processedItems;


