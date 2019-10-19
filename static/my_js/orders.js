//  Initialize materialize autocomplete
//  Add panel names to test names passed to autocomplete instance
const testNames = {};
normalResults.forEach(test => testNames[displayTestName(test.testName)] = null);
makeArrayOfPanels(true).forEach(panel => testNames[displayTestName(panel.testName)] = null);
const autocompleteInput = document.querySelector('.autocomplete');
const instance = M.Autocomplete.init(autocompleteInput, {data: testNames, minLength: 2, limit: 5});

//  Declare/Init variables
const input = document.querySelector('#order-input');
const submitButton = document.querySelector('#order-submit');

//  If previous orders exist, populate <div id =#ordered-tests> on orders.html page
//  Also populate orderedTests object
let orderedTests;
if (Object.keys(sessionStorage).includes('orderedTests')) {
    orderedTests = JSON.parse(sessionStorage['orderedTests']);
    displayOrders();
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
        displayOrders();
    }
    clearInput();
});

//  Pressing enter key trigger submit button event
input.addEventListener("keyup", event => {
    if (event.keyCode == 13) {
        submitButton.click();
    }
})

//  ********** HELPER FUNCTIONS **********
function calcAnionGap(sodium, chloride, co2) {
    return [Math.round(sodium - chloride - co2), "---", 12, 16];
}

function calcLDL(total_cholesterol, hdl, vldl) {
    return [Math.round(total_cholesterol - hdl - vldl), "mg/dL", 80, 200];
}

function checkForDuplicates(collection, element) {
    /**
        Checks to see if user is ordering a duplicate test. Needs to handle test panel orders.
        @param { String[] }  collection - array of strings representing tests already ordered
        @param {string} element - user's new order
        @returns {boolean} - True if element is found in collection, otherwise false
    */
    modifiedCollection = Object.keys(JSON.parse(collection)).map(testName => standardTestName(testName));
    switch (standardTestName(element)) {
        case "bmp":
            return modifiedCollection.some(element => BMP.includes(element));
        case "cmp":
            return modifiedCollection.some(element => CMP.includes(element));
        case "hft":
            return modifiedCollection.some(element => HFT.includes(element));
        case "lipid_panel":
            return modifiedCollection.some(element => lipidPanel.includes(element));
        case "renal_panel":
            return modifiedCollection.some(element => renalPanel.includes(element));
        case "iron_panel":
            return modifiedCollection.some(element => ironPanel.includes(element));
    }
    return modifiedCollection.includes(standardTestName(element));
}

function findOrder(inputValue) {
    /**
        Take user input and check if it is:
            -A panel order. If so, iterate through the appropriate panel, and order each test
             according to whether it is in caseTestResults or normalResults.
            -In caseTestResults. If so, push the key-value pair of inputValue: [value, units, lowerBound, upperBound]
             into sessionStorage['orderedTests']
            -In normalResults. If so, push the key value pair of inputValue: [value, units, lowerBound, upperBound]
             into sessionStorage['orderedTests']
        @param {string} inputValue - name of test being ordered by user

    */
    let isInCaseTestResults = caseTestResults.some(test => test.testName.toLowerCase() == standardTestName(inputValue));
    let isInNormalTestResults = normalResults.some(test => test.testName.toLowerCase() == standardTestName(inputValue));
    let isAPanelOrder = makeArrayOfPanels(true).some(panel => panel.testName.toLowerCase() == standardTestName(inputValue));
    
    if (isAPanelOrder) {
        switch(standardTestName(inputValue)) {
            case "bmp":
                return orderPanelTests(BMP);
            case "cmp":
                return orderPanelTests(CMP);
            case "hft":
                return orderPanelTests(HFT);
            case "renal_panel":
                return orderPanelTests(renalPanel);
            case "lipid_panel":
                return orderPanelTests(lipidPanel);
            case "iron_panel":
                return orderPanelTests(ironPanel);
        }
    }
    else if (isInCaseTestResults) {
        retrieveResults(standardTestName(inputValue), caseTestResults);
    }
    else if (isInNormalTestResults) {
        retrieveResults(standardTestName(inputValue), normalResults);
    }
    else if (!isInCaseTestResults && !isInNormalTestResults) {
        clearInput();
        M.toast({html: 'Test Not Available'});            
    }
}

function orderPanelTests(panel) {
    /**
        Iterate through panel, and if test is in caseTestResults, generate result from its params.
        Otherwise, check if test in normalResults and generate result from its params. Push result
        to sessionStorage['orderedTests'].
        Incorporate computed results depending upon the panel ordered. If BMP, CMP, or renalPanel 
        are ordered, then push [anion_gap, "---", 12, 16].  If lipidPanel, then push 
        [lipid_panel, "mg/dL", 80, 200].

        @param { String[] } panel - names of tests in a given panel
    */
    panel.forEach(test => {
        if (testNamesToArray(caseTestResults).includes(standardTestName(test))) {
            retrieveResults(test, caseTestResults);
        }
        else if (testNamesToArray(normalResults).includes(standardTestName(test))) {            
            retrieveResults(test, normalResults);
        }
    });
    
    const data = JSON.parse(sessionStorage.getItem('orderedTests'));
    const value = 0;
    if (panel == BMP || panel == CMP || panel == renalPanel) {        
        orderedTests['anion_gap'] = calcAnionGap(data['sodium'][value], data['chloride'][value], data['co2'][value]);
        sessionStorage.setItem('orderedTests', JSON.stringify(orderedTests));
    }
    else if (panel == lipidPanel) {
        const calculatedLDL = calcLDL(data['total_cholesterol'][value], data['hdl'][value], data['triglycerides'][value]/5);
        orderedTests['calculated_ldl'] = calculatedLDL;
        sessionStorage.setItem('orderedTests', JSON.stringify(orderedTests));
    }
}

function retrieveResults(test, arrayOfResults) {
    /**
        Given a test_name look for corresponding test in arrayOfResults, generate a random_number
        within the params of the test, and push data to sessionStorage as test_name: random_number
        @param {string} test - name of test to be found
        @param { Object[] } arrayOfResults - expecting either caseTestResults or normalResults
    */
    arrayOfResults
        .filter(result => result.testName.toLowerCase() == standardTestName(test))
        .forEach(foundTest => {
            const val = getRandomNumber(foundTest.lowerBound, foundTest.upperBound, foundTest.valueType, foundTest.precision);
            if (arrayOfResults == normalResults) {
                orderedTests[standardTestName(test)] = [val, foundTest.units, foundTest.lowerBound, foundTest.upperBound];
            }
            else if (arrayOfResults == caseTestResults) {
                normalResults
                    .filter(t => t.testName.toLowerCase() == standardTestName(foundTest.testName))
                    .forEach(ft => {
                        orderedTests[standardTestName(test)] = [val, foundTest.units, ft.lowerBound, ft.upperBound]
                    })
            }
            sessionStorage.setItem('orderedTests', JSON.stringify(orderedTests));
        })
}

function makeArrayOfPanels(arrOfObj) {
    /**
        Returns either an array of test panel names or an array of objects with testName: panelName
        key-value pairs.
        @param {boolean} arrOfObj - flag to indicate whether function should return array of objects or array of strings
        @return { (Object[] | String[]) } if arrofObj is True, return an array of objects, otherwise return array of strings
    */
    if (arrOfObj) {
        return [{"testName": "BMP"}, {"testName": "CMP"}, {"testName": "HFT"}, {"testName": "lipid_panel"}, {"testName": "renal_panel"}, {"testName": "iron_panel"}]
    }
    else {
        return ["BMP", "CMP", "HFT", "lipid_panel", "renal_panel", "iron_panel"];
    }
}

function displayOrders() {
    /**
        Populates <div id = 'ordered-tests'> with chips representing the names of 
        ordered tests. Needs to be run with every page refresh.
    */
    htmlDiv = document.querySelector('#ordered-tests');
    htmlDiv.innerText = "";
    Object.keys(JSON.parse(sessionStorage.getItem('orderedTests')))
        .forEach(test => {
            chip = document.createElement('div');
            chip.className = 'chip';
            chip.innerText = test;
            htmlDiv.appendChild(chip);
        })    
}

function testNamesToArray(arrayOfObj) {
    return arrayOfObj.map(test => test.testName.toLowerCase());
}

function standardTestName(str) {
    return str.toLowerCase().replace(/ /g, "_");
}

function displayTestName(str) {
    return str
            .replace(/_/g, " ")
            .split(" ")
            .map(word => word[0].toUpperCase() + word.substr(1))
            .join(" ");
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