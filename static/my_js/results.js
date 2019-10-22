const table = document.querySelector('#results-table-body');
const orderedTestsNames = Object.keys(JSON.parse(sessionStorage.getItem('orderedTests')));

//  Reset results-badge upon page load
sessionStorage.removeItem('newTests');
resultsBadge.style.display = 'none';


//  Create and populate results table
orderedTestsNames.forEach(test => {
    const data = JSON.parse(sessionStorage.getItem('orderedTests'))[test]
    const row = document.createElement('tr');
    const name = document.createElement('td');
    const value = document.createElement('td');
    const unit = document.createElement('td');
    const referenceRange = document.createElement('td');

    name.textContent = test;
    value.textContent = data[0];
    unit.textContent = data[1];
    if (data[1] == "---") {
        referenceRange.textContent = `${data[2]} - ${data[3]}`;
    }
    else {
        referenceRange.textContent = `${data[2]} - ${data[3]} ${data[1]}`;
    }

    row.appendChild(name);
    row.appendChild(value);
    row.appendChild(unit);
    row.appendChild(referenceRange);
    table.appendChild(row);
})