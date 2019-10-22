//  Initialize materialize modals
const elem = document.querySelector('.modal');
const modals = M.Modal.init(elem, dismissable=true);

// Initialize materialize collapsible
const elems = document.querySelectorAll('.collapsible');
const collapsibles = M.Collapsible.init(elems);

//  Initialize materialize tabs
const tabElems = document.querySelectorAll('.tabs');
var tabs = M.Tabs.init(tabElems);

//  Update transcripts badge
const transcriptsBadge = document.querySelector('.transcripts-badge');
if (sessionStorage.getItem('newTranscripts') == null || sessionStorage.getItem('newTests').length == 0) {
    transcriptsBadge.style.display = 'none';
}
else {
    transcriptsBadge.style.display = 'flex';
    transcriptsBadge.innerText = JSON.parse(sessionStorage.getItem('newTranscripts')).length;
}

//  Update results badge
const resultsBadge = document.querySelector('.results-badge');
if (sessionStorage.getItem('newTests') == null || sessionStorage.getItem('newTests').length == 0) {
    resultsBadge.style.display = 'none';
}
else {
    resultsBadge.style.display = 'flex';
    resultsBadge.innerText = JSON.parse(sessionStorage.getItem('newTests')).length;
}