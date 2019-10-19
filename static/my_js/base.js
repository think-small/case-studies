//  Initialize materialize modals
const elem = document.querySelector('.modal');
const modals = M.Modal.init(elem, dismissable=true);

// Initialize materialize collapsible
const elems = document.querySelectorAll('.collapsible');
const collapsibles = M.Collapsible.init(elems);

//  Initialize materialize tabs
const tabElems = document.querySelectorAll('.tabs');
var tabs = M.Tabs.init(tabElems);