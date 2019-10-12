//  Initialize materialize modals
const elem = document.querySelector('.modal');
const instance = M.Modal.init(elem, dismissable=true);

// Initialize materialize collapsible
const elems = document.querySelectorAll('.collapsible');
const instances = M.Collapsible.init(elems);