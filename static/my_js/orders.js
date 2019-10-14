console.log(caseTestResults);
console.log(normalResults);

//  Initialize materialize autocomplete
//  Add panel names to test names passed to autocomplete instance
const testNames = {};
normalResults.forEach(test => testNames[displayTestName(test.testName)] = null);
makeArrayOfPanels().forEach(panel => testNames[displayTestName(panel.testName)] = null);
const autocompleteInput = document.querySelector('.autocomplete');
const instance = M.Autocomplete.init(autocompleteInput, {data: testNames, minLength: 2, limit: 5});

//  Declare/Init variables
const input = document.querySelector('#order-input');
const submitButton = document.querySelector('#order-submit');
let orderedTests;
if (Object.keys(sessionStorage).includes('orderedTests')) {
    orderedTests = JSON.parse(sessionStorage['orderedTests']);
}
else {
    orderedTests = {};
    sessionStorage.setItem('orderedTests', JSON.stringify(orderedTests));
}
const BMP = ['sodium', 'potassium', 'chloride', 'glucose', 'creatinine', 'co2', 'calcium', 'bun'];
const CMP = [...BMP, 'albumin', 'total_bilirubin', 'total_protein', 'alt', 'ast', 'alkaline_phosphatase'];
const HFT = ['total_protein', 'albumin', 'total_bilirubin', 'direct_bilirubin', 'alt', 'ast', 'alkaline_phosphatase'];
const lipidPanel = ['total_cholesterol', 'hdl', 'triglycerides'];
const ironPanel = ['iron', 'transferrin', 'ferritin'];
const renalPanel = [...BMP, 'albumin', 'phosphorus'];

//  Submit button event listener
submitButton.addEventListener("click", event => {
    let inputValue = input.value;

    if (checkForDuplicates(sessionStorage.getItem('orderedTests'), inputValue)) {
        clearInput();
        M.toast({html: "Duplicate order"});
    }
    else {
        findOrder(inputValue);
    }
    clearInput();
});

//  Pressing enter key trigger submit button event
input.addEventListener("keyup", event => {
    if (event.keyCode == 13) {
        submitButton.click();
    }
})

//  Helper functions
function calcAnionGap(sodium, chloride, co2) {
    return sodium - chloride - co2;
}

function calcVLDL(triglycerides) {
    return triglycerides / 5;
}

function calcLDL(total_cholesterol, hdl, vldl) {
    return total_cholesterol - hdl - vldl;
}

function checkForDuplicates(collection, element) {
    modifiedCollection = Object.keys(JSON.parse(collection)).map(testName => standardTestName(testName));
    return modifiedCollection.includes(standardTestName(element));
}

function findOrder(inputValue) {
    //  Check if user's order exists in caseTestResults
    let isInCaseTestResults = caseTestResults.some(test => test.testName.toLowerCase() == standardTestName(inputValue));
    let isInNormalTestResults = normalResults.some(test => test.testName.toLowerCase() == standardTestName(inputValue));
    
    if (isInCaseTestResults) {
        caseTestResults
            .filter(result => result.testName.toLowerCase() == standardTestName(inputValue))
            .forEach(result => {
                const val = getRandomNumber(result.lowerBound, result.upperBound, result.valueType, result.precision);
                orderedTests[result.testName] = val;
                sessionStorage.setItem('orderedTests', JSON.stringify(orderedTests));
            });
    }
    else if (isInNormalTestResults) {
        //  If not found, check normalTestResults
        normalResults
            .filter(result => result.testName.toLowerCase() == standardTestName(inputValue))
            .forEach(result => {
                const val = getRandomNumber(result.lowerBound, result.upperBound, result.valueType, result.precision);
                orderedTests[result.testName] = val;
                sessionStorage.setItem('orderedTests', JSON.stringify(orderedTests));
            });
    }
    else if (!isInCaseTestResults && !isInNormalTestResults) {
        clearInput();
        M.toast({html: 'Test Not Available'});            
    }
}

function makeArrayOfPanels() {
    return [{"testName": "BMP"}, {"testName": "CMP"}, {"testName": "HFT"}, {"testName": "lipid_panel"}, {"testName": "renal_panel"}, {"testName": "iron_panel"}]
}

function standardTestName(str) {
    return str.toLowerCase().replace(/ /g, "_");
}

function displayTestName(str) {
    return str.replace(/_/g, " ");
}

function getRandomNumber(min, max, type, precision = 0) {
    switch (type) {
        case 'integer':
            return getRandomInteger(min, max);
        case 'float':
            return getRandomFloat(min, max, precision);
    }
}

function getRandomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function getRandomFloat(min, max, precision) {
    return parseFloat((Math.random() * (max - min) + min).toFixed(precision));
}

function clearInput() {
    input.value = "";
}